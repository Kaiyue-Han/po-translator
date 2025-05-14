#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
po_translator_gui.py
DeepL 批量翻译 .po 文件 – 带 Tkinter GUI、langdetect 语言检测、运行时缓存
"""

import threading
import polib
import deepl
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from langdetect import detect, DetectorFactory, LangDetectException

DetectorFactory.seed = 0  # 让 langdetect 结果可重复

# ─────────────────────────────────────────────────────────
# DeepL 支持的语言代码（2025-05-14）
# ─────────────────────────────────────────────────────────
SRC_LANGS = [
    "AR","BG","CS","DA","DE","EL","EN","ES","ET","FI","FR","HU","ID","IT","JA",
    "KO","LT","LV","NB","NL","PL","PT","RO","RU","SK","SL","SV","TR","UK","ZH"
]

TGT_LANGS = [
    "AR","BG","CS","DA","DE","EL",
    "EN","EN-GB","EN-US",
    "ES","ET","FI","FR","HE","HU","ID","IT","JA","KO",
    "LT","LV","NB","NL","PL",
    "PT","PT-BR","PT-PT",
    "RO","RU","SK","SL","SV","TR","UK",
    "ZH","ZH-HANS","ZH-HANT"
]
# ─────────────────────────────────────────────────────────

# ──────── 工具函数 ────────
def _norm(code: str) -> str:
    return (code or "").lower().split("-", 1)[0]

def need_translate(text: str, src_lang: str, min_len: int = 5) -> bool:
    """
    判断是否需要翻译：
    - 文本过短 → 直接翻译
    - langdetect 识别结果 与 源语言前缀一致 → 需要翻译
    - 否则认为已是目标语言 → 不翻译
    """
    if len(text) < min_len:
        return True
    try:
        detected = _norm(detect(text))
        return detected == _norm(src_lang)
    except LangDetectException:
        return True  # 无法识别时保险起见翻译

def translate_po(
    in_path: Path,
    out_path: Path,
    src_lang: str,
    tgt_lang: str,
    api_key: str,
    translate_all: bool,
    progress_cb=None,
):
    """翻译主函数（支持进度回调与运行时缓存）"""
    translator = deepl.Translator(api_key)
    po = polib.pofile(in_path)

    tgt_prefix = _norm(tgt_lang)
    cache: dict[tuple[str, str], str] = {}

    # ① 预热缓存：已有译文放入
    for e in po:
        if e.msgstr.strip():
            cache[(e.msgid, tgt_prefix)] = e.msgstr.strip()

    total = len(po)
    done = 0

    for entry in po:
        original = entry.msgid.strip()
        if not original:
            done += 1
            if progress_cb:
                progress_cb(done, total)
            continue

        # 跳过已翻译行（除非选了“全部重新翻译”）
        if not translate_all and entry.msgstr.strip():
            done += 1
            if progress_cb:
                progress_cb(done, total)
            continue

        key = (original, tgt_prefix)
        if key in cache:                          # 命中缓存
            entry.msgstr = cache[key]
        else:
            if need_translate(original, src_lang):
                try:
                    result = translator.translate_text(
                        original,
                        source_lang=src_lang.upper(),
                        target_lang=tgt_lang.upper()
                    )
                    entry.msgstr = result.text
                except Exception as e:
                    print("Translate error:", e)
                    entry.msgstr = ""             # 留空，方便下次重试
            else:
                # 原文已是目标语言 → 直接复制
                entry.msgstr = original

            cache[key] = entry.msgstr             # 写入缓存

        done += 1
        if progress_cb:
            progress_cb(done, total)

    po.save(out_path)

# ──────── Tkinter GUI ────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PO Translator (DeepL)")
        self.geometry("550x440")
        self.resizable(False, False)

        # 文件路径变量
        self.in_path_var  = tk.StringVar()
        self.out_dir_var  = tk.StringVar()
        self.out_name_var = tk.StringVar(value="output.po")

        # 语言 & 选项
        self.src_var       = tk.StringVar(value="ZH")
        self.tgt_var       = tk.StringVar(value="EN-US")
        self.key_var       = tk.StringVar()
        self.translate_all = tk.BooleanVar(value=False)

        # 进度
        self.progress_val = tk.DoubleVar(value=0.0)
        self.progress_lbl = tk.StringVar(value="等待开始 / Waiting to start")

        self._build_ui()

    def _build_ui(self):
        pady = dict(pady=4)

        # 输入文件
        ttk.Label(self, text="源文件 / Source file:").pack(anchor="w", **pady)
        frm_in = ttk.Frame(self); frm_in.pack(fill="x", **pady)
        ttk.Entry(frm_in, textvariable=self.in_path_var, width=52)\
            .pack(side="left", fill="x", expand=True)
        ttk.Button(frm_in, text="浏览 / Browse", command=self._choose_in)\
            .pack(side="left", padx=4)

        # 输出目录
        ttk.Label(self, text="输出目录 / Output folder:").pack(anchor="w", **pady)
        frm_out = ttk.Frame(self); frm_out.pack(fill="x", **pady)
        ttk.Entry(frm_out, textvariable=self.out_dir_var, width=52)\
            .pack(side="left", fill="x", expand=True)
        ttk.Button(frm_out, text="浏览 / Browse", command=self._choose_out_dir)\
            .pack(side="left", padx=4)

        # 输出文件名
        ttk.Label(self, text="输出文件名 / Output filename:").pack(anchor="w", **pady)
        ttk.Entry(self, textvariable=self.out_name_var, width=34)\
            .pack(anchor="w", **pady)

        # 语言选择
        frm_lang = ttk.Frame(self); frm_lang.pack(fill="x", **pady)
        ttk.Label(frm_lang, text="源语言 / Source:").pack(side="left")
        ttk.Combobox(frm_lang, textvariable=self.src_var,
                     values=SRC_LANGS, width=10, state="readonly")\
            .pack(side="left", padx=4)
        ttk.Label(frm_lang, text="目标语言 / Target:").pack(side="left")
        ttk.Combobox(frm_lang, textvariable=self.tgt_var,
                     values=TGT_LANGS, width=12, state="readonly")\
            .pack(side="left", padx=4)

        # 选项复选框
        ttk.Checkbutton(self,
            text="全部重新翻译 / Translate all (otherwise only empty msgstr)",
            variable=self.translate_all)\
            .pack(anchor="w", **pady)

        # DeepL Key
        ttk.Label(self, text="DeepL API Key:").pack(anchor="w", **pady)
        ttk.Entry(self, textvariable=self.key_var, show="*", width=50)\
            .pack(anchor="w", **pady)

        # 进度条
        ttk.Progressbar(self, variable=self.progress_val, maximum=100)\
            .pack(fill="x", padx=4, pady=6)
        ttk.Label(self, textvariable=self.progress_lbl).pack(anchor="center")

        # 开始按钮
        ttk.Button(self, text="开始翻译 / Start", command=self._start_translate)\
            .pack(pady=8)

    # 文件&目录选择
    def _choose_in(self):
        path = filedialog.askopenfilename(
            title="选择源 .po 文件 / Select source .po",
            filetypes=[("PO files", "*.po"), ("All files", "*.*")]
        )
        if path:
            self.in_path_var.set(path)
            if not self.out_dir_var.get():
                self.out_dir_var.set(str(Path(path).parent))

    def _choose_out_dir(self):
        path = filedialog.askdirectory(title="选择输出目录 / Select output folder")
        if path:
            self.out_dir_var.set(path)

    # 启动翻译线程
    def _start_translate(self):
        in_path  = Path(self.in_path_var.get())
        out_dir  = Path(self.out_dir_var.get())
        out_name = self.out_name_var.get().strip() or "output.po"
        api_key  = self.key_var.get().strip()

        if not in_path.exists():
            messagebox.showerror("错误 / Error", "请选择有效源文件\nSelect a valid source file")
            return
        if not out_dir.exists():
            messagebox.showerror("错误 / Error", "输出目录不存在\nOutput folder not found")
            return
        if not api_key:
            messagebox.showerror("错误 / Error", "请输入 DeepL API Key")
            return

        out_path = out_dir / out_name

        # 禁用按钮
        for child in self.winfo_children():
            if isinstance(child, ttk.Button):
                child.state(["disabled"])

        self.progress_val.set(0.0)
        self.progress_lbl.set("I' m working. DON'T TOUCH ME")

        threading.Thread(
            target=self._translate_thread,
            args=(
                in_path,
                out_path,
                self.src_var.get(),
                self.tgt_var.get(),
                api_key,
                self.translate_all.get()
            ),
            daemon=True
        ).start()

    # 后台线程
    def _translate_thread(self, in_path, out_path, src, tgt, key, trans_all):
        def _cb(done, total):
            pct = done / total * 100
            self.progress_val.set(pct)
            self.progress_lbl.set(f"{done}/{total}  ({pct:.2f}%)")

        try:
            translate_po(in_path, out_path, src, tgt, key, trans_all, _cb)
            self.progress_lbl.set(f"完成! 已保存 / Done! Saved to: {out_path}")
        except Exception as e:
            self.progress_lbl.set(f"出错 / Error: {e}")
            messagebox.showerror("翻译出错 / Translation failed", str(e))
        finally:
            for child in self.winfo_children():
                if isinstance(child, ttk.Button):
                    child.state(["!disabled"])

# ──────── 入口 ────────
if __name__ == "__main__":
    App().mainloop()