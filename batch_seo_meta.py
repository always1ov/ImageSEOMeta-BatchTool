# -*- coding: utf-8 -*-
"""
batch_seo_meta.py
~~~~~~~~~~~~~~~~~
批量向 JPEG / PNG / TIFF 等图片写入 SEO 元数据（丢弃旧信息）：
  • 作者 / 版权 / 标题 / 描述 / 关键词
  • 中文零乱码（XP* UTF‑16LE & PNG iTXt）
  • 多线程并行
兼容 Python 3.8+
支持通过 --config 参数加载 JSON 配置文件
"""

from typing import List, Optional, Dict, Tuple
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import logging
import os
import sys
import json
import multiprocessing

from PIL import Image, PngImagePlugin, UnidentifiedImageError
import piexif

# ---------- 日志 ---------- #
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s"
)
log = logging.getLogger("batch_seo_meta")

# ---------- EXIF 常量 ---------- #
XP_TITLE    = 0x9C9B
XP_COMMENT  = 0x9C9C
XP_AUTHOR   = 0x9C9D
XP_KEYWORDS = 0x9C9E
_UTF16_LIMIT = 65534

def _xp(text: str) -> bytes:
    if not text:
        return b""
    data = f"{text}\x00".encode("utf-16le")
    if len(data) > _UTF16_LIMIT:
        log.warning("字段过长已截断：%s…", text[:20])
        data = data[:_UTF16_LIMIT]
    return data

def _add_itxt_or_text(info: PngImagePlugin.PngInfo, key: str, val: str):
    if hasattr(info, "add_itxt"):
        info.add_itxt(key, val, lang="zh")
    else:
        info.add_text(key, val)
        log.warning("旧版 Pillow 不支持 iTXt，字段 '%s' 可能乱码。", key)

# ---------- 单图处理 ---------- #
def write_one(
    src: Path,
    *,
    author: str,
    copyright_: str,
    title: str,
    desc: str,
    keywords: List[str],
    outdir: Optional[Path] = None,
    overwrite: bool = False
) -> Tuple[Path, bool, str]:
    if not src.exists():
        return src, False, "文件不存在"

    try:
        with Image.open(src) as im:
            fmt = im.format.upper()
            target_dir = Path(outdir) if outdir else src.parent / "output"
            target_dir.mkdir(parents=True, exist_ok=True)
            dst = target_dir / src.name

            if fmt in ("JPEG", "TIFF"):
                exif_dict = {"0th": {}, "Exif": {}, "1st": {}, "thumbnail": None}
                exif_dict["0th"].update({
                    XP_TITLE:    _xp(title),
                    XP_COMMENT:  _xp(desc),
                    XP_AUTHOR:   _xp(author),
                    XP_KEYWORDS: _xp(";".join(keywords)),
                })
                im.save(dst, format=fmt, exif=piexif.dump(exif_dict))

            elif fmt == "PNG":
                meta = PngImagePlugin.PngInfo()
                _add_itxt_or_text(meta, "Title", title)
                _add_itxt_or_text(meta, "Description", desc)
                _add_itxt_or_text(meta, "Author", author)
                _add_itxt_or_text(meta, "Copyright", copyright_)
                _add_itxt_or_text(meta, "Keywords", ", ".join(keywords))
                im.save(dst, pnginfo=meta)

            else:
                im.save(dst, format=fmt)

    except UnidentifiedImageError:
        return src, False, "无法识别为图像"
    except Exception as e:
        return src, False, f"处理错误: {e}"

    if overwrite:
        try:
            os.replace(dst, src)
            dst = src
        except Exception as e:
            return src, False, f"覆盖失败: {e}"

    return dst, True, ""

# ---------- 扫描输入 ---------- #
def gather_images(paths: List[str], recursive: bool) -> List[Path]:
    exts = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"}
    imgs: List[Path] = []
    for p in paths:
        path = Path(p)
        if path.is_file():
            if path.suffix.lower() in exts:
                imgs.append(path)
        elif path.is_dir():
            pattern = "**/*" if recursive else "*"
            imgs.extend(
                f for f in path.glob(pattern)
                if f.suffix.lower() in exts and f.is_file()
            )
        else:
            log.warning("忽略无效路径: %s", p)
    return imgs

# ---------- 批量 ---------- #
def process_bulk(
    files: List[Path],
    *,
    author: str,
    copyright_: str,
    title: str,
    desc: str,
    keywords: List[str],
    outdir: Optional[Path],
    overwrite: bool,
    workers: int
):
    total = len(files)
    if total == 0:
        log.error("未找到需要处理的图片")
        return
    log.info("共 %d 张图片，使用 %d 个线程…", total, workers)
    ok = err = 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futs = {
            pool.submit(
                write_one, f,
                author=author,
                copyright_=copyright_,
                title=title,
                desc=desc,
                keywords=keywords,
                outdir=outdir,
                overwrite=overwrite
            ): f for f in files
        }
        for fut in as_completed(futs):
            src = futs[fut]
            dst, success, msg = fut.result()
            if success:
                ok += 1
                log.debug("✅ %s → %s", src.name, dst)
            else:
                err += 1
                log.error("❌ %s (%s)", src, msg)
    log.info("完成：成功 %d / 失败 %d", ok, err)

# ---------- CLI ---------- #
def cli():
    parser = argparse.ArgumentParser(
        description="批量写入 SEO 元数据 (JPEG / PNG / TIFF / WebP)"
    )
    parser.add_argument("--config", help="从 JSON 配置文件加载参数")

    parser.add_argument("inputs", nargs="*", help="待处理的文件或文件夹")
    parser.add_argument("--author", help="作者")
    parser.add_argument("--copyright", dest="copyright_", help="版权")
    parser.add_argument("--title", help="标题")
    parser.add_argument("--description", dest="desc", help="描述")
    parser.add_argument("--keywords", help="关键词，用逗号分隔")
    parser.add_argument("-r", "--recursive", action="store_true", help="递归扫描文件夹")
    parser.add_argument("--outdir", help="输出目录")
    parser.add_argument("--overwrite", action="store_true", help="覆盖原图")
    parser.add_argument("--workers", type=int, default=multiprocessing.cpu_count(), help="线程数")

    args, _ = parser.parse_known_args()

    # 如果指定配置文件，就加载配置
    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            config = json.load(f)
        parser.set_defaults(**config)

    args = parser.parse_args()

    # 检查必要参数
    required = ["author", "copyright_", "title", "desc", "keywords"]
    missing = [f for f in required if not getattr(args, f)]
    if missing:
        parser.error("缺少必要参数：" + ", ".join(missing))

    # 处理关键词
    if isinstance(args.keywords, str):
        keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
    else:
        keywords = args.keywords

    # 输入文件
    images = gather_images(args.inputs, args.recursive)

    process_bulk(
        images,
        author=args.author,
        copyright_=args.copyright_,
        title=args.title,
        desc=args.desc,
        keywords=keywords,
        outdir=Path(args.outdir) if args.outdir else None,
        overwrite=args.overwrite,
        workers=max(1, args.workers)
    )

if __name__ == "__main__":
    cli()
