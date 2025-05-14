# PO-Translator GUI
> DeepL-powered PO-file translator with a bilingual Tkinter interface  

---

## ✨ Features
| Feature | Description |
|---------|-------------|
| **DeepL integration** | Translate any `.po` file through the DeepL API |
| **Language detection** | Strings already in another language are **copied instead of translated** |
| **Runtime cache** | Skips duplicate strings to save your quota |
| **Progress bar & bilingual GUI** | Live progress indicator, Chinese / English UI |
| **One-click launcher** | `run.bat` creates a virtual env and installs deps (≈ 10 s on first run) |

---

## 🚀 Quick Start

### Requirements
* Windows **or** macOS / Linux  
* Python 3.9 + (added to `PATH`)  
* Internet connection (first run & DeepL requests)

#### Windows

```bash
git clone https://github.com/Kaiyue-Han/po-translator.git
cd po-translator
run.bat                          # double-click works too
```


First launch creates a virtual environment and downloads dependencies.
**Do not close** the black CMD window while the app is running.

#### macOS / Linux
```bash
git clone https://github.com/Kaiyue-Han/po-translator.git
cd po-translator
python -m pip install -r requirements.txt   # one-time install
python po_translator.py              # launch GUI
```
## 🔑 DeepL API Key
1. Sign up at https://www.deepl.com/ and grab your key.
2. Free tier ≈ 500 k characters / month.
3. Paste the key into the GUI (masked input).

## ⚠️ Tips
1. Although the script never edits your original file directly, **always back up the source file** before you start translating.
2. **Test with a small sample first** to avoid wasting quota.
3. DeepL does NOT support Simplified ⇄ Traditional Chinese yet.
4. Strings shorter than 5 characters are always sent to DeepL (detection is unreliable).
5. Any string not in the selected source language is copied unchanged.

## 🐞 Issues & Feedback
- File bugs or feature requests via Issues.
- Discussions & PRs are welcome!

## 📄 License
Released under the MIT License – see LICENSE for details.

