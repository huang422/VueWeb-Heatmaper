"""
PyInstaller Build Script - All-in-One Executable
打包前端 + 後端 + Python 執行環境 = 單一 exe
客戶完全不需要安裝任何東西
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# 專案路徑
BACKEND_DIR = Path(__file__).parent
PROJECT_ROOT = BACKEND_DIR.parent
DATA_DIR = PROJECT_ROOT / 'data'
FRONTEND_DIR = PROJECT_ROOT / 'frontend'
DIST_DIR = BACKEND_DIR / 'dist'
BUILD_DIR = BACKEND_DIR / 'build'

def check_prerequisites():
    """檢查前置條件"""
    print("🔍 檢查前置條件...")

    # 檢查 PyInstaller
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller 未安裝")
        print("   請執行: pip install pyinstaller")
        return False

    # 檢查資料檔案
    data_file = DATA_DIR / 'data.csv'
    if not data_file.exists():
        print(f"❌ 資料檔案不存在: {data_file}")
        return False
    print(f"✓ 資料檔案: {data_file}")

    # 檢查前端已建置
    frontend_dist = FRONTEND_DIR / 'dist'
    if not frontend_dist.exists() or not (frontend_dist / 'index.html').exists():
        print(f"❌ 前端未建置")
        print(f"   請執行: cd {FRONTEND_DIR} && npm run build")
        return False
    print(f"✓ 前端已建置: {frontend_dist}")

    return True

def clean_build_dirs():
    """清理舊的建置檔案"""
    print("\n🧹 清理舊檔案...")
    for dir_path in [DIST_DIR, BUILD_DIR]:
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"  清除: {dir_path}")

    # 清理舊的 spec 檔案
    for spec_file in BACKEND_DIR.glob('*.spec'):
        spec_file.unlink()
        print(f"  清除: {spec_file}")

def build_exe():
    """執行 PyInstaller 打包"""
    print("\n🔨 開始打包...")
    print("=" * 60)

    # 使用絕對路徑
    data_csv = str((DATA_DIR / 'data.csv').absolute())
    frontend_dist = str((FRONTEND_DIR / 'dist').absolute())
    run_app_py = str((BACKEND_DIR / 'run_app.py').absolute())
    src_dir = str((BACKEND_DIR / 'src').absolute())

    # PyInstaller 參數
    args = [
        'pyinstaller',
        '--name=StoreHeatmap',
        '--onefile',
        '--console',
        '--clean',
        '--noconfirm',

        # 加入資料和前端
        f'--add-data={data_csv}{os.pathsep}data',
        f'--add-data={frontend_dist}{os.pathsep}frontend/dist',

        # 加入整個 src 目錄作為資料
        f'--add-data={src_dir}{os.pathsep}src',

        # Hidden imports
        '--hidden-import=uvicorn.logging',
        '--hidden-import=uvicorn.loops',
        '--hidden-import=uvicorn.loops.auto',
        '--hidden-import=uvicorn.protocols',
        '--hidden-import=uvicorn.protocols.http',
        '--hidden-import=uvicorn.protocols.http.auto',
        '--hidden-import=uvicorn.protocols.websockets',
        '--hidden-import=uvicorn.protocols.websockets.auto',
        '--hidden-import=uvicorn.lifespan',
        '--hidden-import=uvicorn.lifespan.on',

        # 排除不需要的模組
        '--exclude-module=tkinter',
        '--exclude-module=matplotlib',
        '--exclude-module=IPython',
        '--exclude-module=jupyter',
        '--exclude-module=pytest',

        # 優化
        '--noupx',
        '--optimize=2',

        # 入口點（使用 run_app.py）
        run_app_py
    ]

    # 執行 PyInstaller
    try:
        print(f"執行指令: {' '.join(args[:5])}...")
        result = subprocess.run(args, cwd=BACKEND_DIR, check=True)
        print("\n✅ 打包成功!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 打包失敗: {e}")
        return False

def show_summary():
    """顯示摘要"""
    exe_file = DIST_DIR / 'StoreHeatmap.exe'

    print("\n" + "=" * 60)
    print("🎉 打包完成!")
    print("=" * 60)

    if exe_file.exists():
        size_mb = exe_file.stat().st_size / (1024 * 1024)
        print(f"\n📦 輸出檔案: {exe_file}")
        print(f"📊 檔案大小: {size_mb:.1f} MB")

    print("\n✅ 包含內容:")
    print("  ✓ Python 執行環境")
    print("  ✓ 後端 API (FastAPI + Uvicorn)")
    print("  ✓ 前端 UI (Vue 3 + OpenLayers)")
    print("  ✓ 資料檔案 (data.csv)")
    print("  ✓ 所有依賴套件")

    print("\n🚀 使用方式:")
    print("  1. 將 StoreHeatmap.exe 複製到任何 Windows 電腦")
    print("  2. 雙擊執行")
    print("  3. 瀏覽器會自動開啟 http://localhost:8000")
    print("  4. 完全不需要安裝 Python 或任何依賴!")

    print("\n💡 優點:")
    print("  ✓ 單一檔案，易於分發")
    print("  ✓ 客戶無需安裝任何東西")
    print("  ✓ 雙擊即用")
    print("  ✓ 離線可用")

    print("\n⚠️ 注意:")
    print("  - 必須在 Windows 電腦上執行此腳本")
    print("  - Linux/Mac 無法編譯 Windows exe")
    print("  - 首次啟動可能需要幾秒鐘")

    print("=" * 60)

def main():
    """主程序"""
    print("=" * 60)
    print("Store Heatmap - 完整打包工具")
    print("前端 + 後端 + Python = 單一 exe")
    print("=" * 60)

    # 檢查是否在 Windows
    if os.name != 'nt':
        print("\n⚠️  警告: 當前系統不是 Windows")
        print("PyInstaller 無法跨平台編譯")
        print("請在 Windows 電腦上執行此腳本")
        print("\n建議:")
        print("1. 將整個專案複製到 Windows 電腦")
        print("2. 安裝依賴: pip install -r requirements.txt")
        print("3. 安裝 PyInstaller: pip install pyinstaller")
        print("4. 執行: python build_exe.py")
        sys.exit(1)

    # 檢查前置條件
    if not check_prerequisites():
        print("\n❌ 前置條件檢查失敗")
        sys.exit(1)

    # 清理舊檔案
    clean_build_dirs()

    # 執行打包
    if not build_exe():
        print("\n❌ 打包失敗")
        sys.exit(1)

    # 顯示摘要
    show_summary()

if __name__ == '__main__':
    main()
