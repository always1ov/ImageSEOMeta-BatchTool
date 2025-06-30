# 📸 Batch SEO Meta Writer

![Status](https://img.shields.io/badge/status-not%20maintained-lightgrey)
![Python Version](https://img.shields.io/badge/python-3.8%2B-green)
![License](https://img.shields.io/badge/license-MIT-blue)

> 批量给 JPEG/PNG/TIFF/WebP 图片添加 SEO 元数据（作者、标题、关键词等），支持中文无乱码。由 AI 辅助生成，当前不维护。


## 🛠 依赖安装

在使用前，请先安装依赖库：

```bash
pip install pillow piexif
```

## 🚀 快速开始

将本项目下载并解压后，打开终端（命令行），进入项目目录，执行：

```bash
python batch_seo_meta.py ./photos \
  --recursive \
  --author "测试作者" \
  --copyright "©2025 测试版权" \
  --title "测试标题" \
  --description "测试描述" \
  --keywords "测试,示例,关键字"
```

## ⚙️ 主要参数说明

| 参数           | 说明                     |
|----------------|--------------------------|
| `--author`     | 作者                     |
| `--copyright`  | 版权信息                 |
| `--title`      | 标题                     |
| `--description`| 描述                     |
| `--keywords`   | 关键词，逗号分隔         |
| `--recursive`  | 是否递归处理子目录       |
| `--outdir`     | 指定统一输出目录（可选） |
| `--overwrite`  | 是否覆盖原文件（谨慎用） |

## 📄 配置文件使用方法（可选）

1. 创建一个 `config.json` 文件，内容示例：

```json
{
  "inputs": ["./images"],
  "recursive": true,
  "author": "测试作者",
  "copyright": "©2025 测试版权",
  "title": "测试标题",
  "description": "测试描述",
  "keywords": "测试,示例,关键字",
  "outdir": "output",
  "overwrite": false,
  "workers": 4
}
```

2. 执行脚本时指定配置文件：

```bash
python batch_seo_meta.py --config config.json
```

## ℹ️ 注意事项

- 默认不会修改原图，避免数据丢失。  
- 覆盖原图请务必备份！  
- 支持的图片格式：`.jpg`, `.jpeg`, `.png`, `.tif`, `.tiff`, `.webp`  
- 支持中文字段，无乱码。  

## 📌 项目说明

本项目由 [OpenAI ChatGPT](https://openai.com/chatgpt) 辅助生成，作者整理发布，**目前不维护**，请自行使用或修改.
