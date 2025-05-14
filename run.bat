@echo off
:: run.bat — 双击即可运行/自动配置
setlocal

:: 1. 选择 Python 解释器 (优先用 py -3)
where py >nul 2>&1 && (set PY=py -3) || (set PY=python)

:: 2. 创建虚拟环境（若尚未存在）
if not exist ".venv\Scripts\python.exe" (
    echo [Setup] Creating virtual environment...
    %PY% -m venv .venv
)

:: 3. 激活虚拟环境
call ".venv\Scripts\activate.bat"

:: 4. 安装 / 更新依赖（只首轮会装）
echo [Setup] Installing required packages if missing...
python -m pip install --upgrade --quiet pip
python -m pip install --quiet polib deepl langdetect

:: 5. 运行 GUI
echo [Run] Launching PO Translator GUI...
python po_translator.py %*

endlocal