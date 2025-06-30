# 📸 ImageSEOMetaReWrite

![Status](https://img.shields.io/badge/status-not%20maintained-lightgrey)
![Python Version](https://img.shields.io/badge/python-3.8%2B-green)
![License](https://img.shields.io/badge/license-MIT-blue)

> 批量向 JPEG / PNG / TIFF / WebP 图片写入 SEO 元数据（作者、版权、标题、描述、关键词等），支持中文无乱码，多线程并行。  
> 由 AI 辅助生成，当前不维护，仅供参考和使用。

## 功能特点

- 支持 JPEG / PNG / TIFF / WebP 图片格式
- 批量处理，支持多线程加速
- 写入作者、版权、标题、描述、关键词等 SEO 元数据
- 中文支持良好，避免乱码（XP* UTF-16LE & PNG iTXt）
- 支持通过命令行参数或 JSON 配置文件输入
- 支持递归扫描目录
- 支持输出到指定目录或覆盖原文件

## 安装依赖

确保你已安装 Python 3.8 或更高版本，然后安装所需依赖：

```bash
pip install -r requirements.txt
```

## 快速开始

方法一：使用 JSON 配置文件（推荐）

1.创建配置文件（例如 config.json）：

```json
{
  "inputs": ["test_images/"],
  "recursive": true,
  "author": "测试用户",
  "copyright_": "©2025 Test",
  "title": "测试标题",
  "desc": "这是一张用于测试的图片",
  "keywords": ["测试", "样例", "演示"],
  "outdir": "test_output",
  "overwrite": false,
  "workers": 2
}
```

2.执行命令：

```bash
python batch_seo_meta.py --config config.json
```

方法二：使用命令行参数直接运行

```bash
python batch_seo_meta.py test_images \
  --recursive \
  --author "测试用户" \
  --copyright "©2025 Test" \
  --title "测试标题" \
  --description "这是一张用于测试的图片" \
  --keywords "测试,样例,演示" \
  --outdir test_output \
  --workers 2
```

## 📁 示例运行目录结构

```arduino
.
├── batch_seo_meta.py
├── config.json
├── photos/
│   ├── image1.jpg
│   ├── image2.png
│   └── ...
└── dist/  ← 输出文件将保存至此
```

## ⚙️ 参数说明

| 参数名           | 类型     | 是否必填 | 说明 |
|------------------|----------|----------|------|
| `inputs`         | 路径列表 | ✅       | 要处理的图片文件或文件夹路径（支持多个） |
| `--recursive` 或 `-r` | 选项     | ❌       | 是否递归扫描子文件夹 |
| `--author`       | 字符串   | ✅       | 作者（写入 EXIF XPAuthor 或 PNG Author） |
| `--copyright`    | 字符串   | ✅       | 版权信息（写入 PNG Copyright） |
| `--title`        | 字符串   | ✅       | 标题（写入 EXIF XPTitle 或 PNG Title） |
| `--description`  | 字符串   | ✅       | 描述内容（写入 EXIF XPComment 或 PNG Description） |
| `--keywords`     | 字符串   | ✅       | 关键词，用英文逗号 `,` 分隔，如 `"城市,夜景,剪影"` |
| `--outdir`       | 路径     | ❌       | 输出目录，默认保存在每张图片所在目录的 `output/` 子目录中 |
| `--overwrite`    | 选项     | ❌       | 是否覆盖原图（默认否，如启用将替换原文件） |
| `--workers`      | 整数     | ❌       | 多线程数量，默认等于 CPU 核心数 |
| `--config`       | 文件路径 | ❌       | 从 JSON 配置文件中加载参数（命令行参数优先） |

## 项目说明

本项目由 AI 辅助生成，未经长期维护和持续更新，仅供学习和参考。

使用时请务必备份重要图片数据，避免因程序错误导致文件丢失或损坏。

## 许可证

本项目采用 MIT 许可证，欢迎自由使用和修改，但不提供任何保证。

详见 [LICENSE](./LICENSE) 文件。
