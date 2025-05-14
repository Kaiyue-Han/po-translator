# PO-Translator GUI  
> DeepL-powered PO file translator with a bilingual Tkinter interface  
> 基于 DeepL API 的 .po 文件批量翻译工具（中英双语界面）

---

## ✨ Features / 功能亮点
| EN | 中文 |
|----|------|
| Translate any `.po` file via DeepL API | 通过 DeepL 接口自动翻译 `.po` 文件 |
| Auto-detect source language – strings already in another language will be **copied instead of translated** | 自动检测源语言，若文本本身不是源语言，则**直接复制**不再翻译 |
| Runtime cache to avoid paying twice for identical strings | 运行时缓存，避免相同文本重复计费 |
| Progress bar & bilingual GUI (中文 / English) | 带进度条的中英双语界面 |
| One-click `run.bat` – auto-creates venv & installs deps | 双击 `run.bat` 一键运行（首次约 10 秒自动安装依赖） |

---

## 🚀 Quick Start / 快速开始

> **Prerequisite**  
> - Windows & Python 3.9+ (added to PATH)  
> - Internet connection (for first-time dependency install & DeepL API)

```bash
# 1. Clone the repo / 克隆仓库
git clone https://github.com/Kaiyue-Han/po-translator.git
cd po-translator

# 2. Windows: just double-click run.bat / 双击 run.bat 即可
#    ▸ First run ≈ 10 s for installing packages
#    ▸ KEEP the black CMD window open while the app is running

#    macOS / Linux
python -m pip install -r requirements.txt   # install deps once
python po_translator_gui_bi.py              # launch GUI
