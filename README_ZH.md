# PO-Translator GUI
> 基于 DeepL API 的 `.po` 文件批量翻译工具（中英双语界面）

---

## ✨ 功能亮点
| 功能 | 说明 |
|------|------|
| **DeepL 接口** | 通过 DeepL API 一键翻译任何 `.po` 文件 |
| **自动语言检测** | 若字符串本身并非「源语言」，则**直接复制**，不浪费额度 |
| **运行时缓存** | 同一次运行内，相同文本只翻译一次，节省配额 |
| **进度条 + 中英界面** | 实时显示翻译进度，界面支持中/英切换 |
| **一键启动** | `run.bat` 首次运行≈10 秒，自动创建虚拟环境并安装依赖 |

---

## 🚀 快速开始

### 环境要求
* Windows（推荐使用 `run.bat`）或 macOS / Linux  
* Python 3.9 及以上（已加入 `PATH`）  
* 首次运行及调用 DeepL API 需联网

#### Windows

```bash
git clone https://github.com/Kaiyue-Han/po-translator.git
cd po-translator
run.bat                    # 直接双击亦可
```
**首次运行**会自动创建虚拟环境并下载安装依赖。
程序运行期间**请勿关闭**最先弹出的黑色 CMD 窗口。

#### macOS / Linux
```bash
git clone https://github.com/Kaiyue-Han/po-translator.git
cd po-translator
python -m pip install -r requirements.txt   # 第一次安装依赖
python po_translator_gui_bi.py              # 启动界面
```

## 🔑 DeepL API Key
1. 访问 https://www.deepl.com 注册账号并获取 Key
2. 免费额度约 50 万字符 / 月
3. 在界面中粘贴 Key

## ⚠️ 使用建议
1. 虽然不会直接修改源文件，但还是请**翻译前请备份源文件**
2. 先用**少量文本试跑**，确认效果，避免浪费额度
3. DeepL 暂不支持简体 ⇄ 繁体中文互译
4. 字符串长度 < 5 会直接调用 DeepL（检测不准）
5. 若句子本身不是「源语言」，程序会 原样复制，不占额度

## 🐞 反馈与 Bug
- 请在 Issues 提交问题或功能需求
- 欢迎 PR 与讨论！

## 📄 许可证
本项目基于 MIT License 开源，详见 LICENSE。
