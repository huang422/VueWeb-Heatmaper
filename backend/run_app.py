"""
PyInstaller Entry Point
解決相對導入問題的入口點
"""

import sys
from pathlib import Path

# 將 backend 目錄加入 Python 路徑
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# 導入並執行主程序
if __name__ == "__main__":
    from src.main import *

    # 執行 main.py 的主程序
    import uvicorn
    import threading

    # 判斷是否為打包模式
    is_packaged = getattr(sys, 'frozen', False)

    # Find available port
    port = find_available_port()
    if port is None:
        logger.error("No available ports found in range 8000-8010")
        port = API_CONFIG['port']

    host = API_CONFIG['host']
    url = f"http://{host}:{port}"

    # 自動開啟瀏覽器（打包模式）
    if is_packaged:
        logger.info("Running as packaged executable")
        logger.info(f"Server will start at {url}")

        # 在背景執行緒中開啟瀏覽器
        browser_thread = threading.Thread(target=open_browser, args=(url,), daemon=True)
        browser_thread.start()

        # 打包模式：直接使用 app 實例
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level=API_CONFIG['log_level']
        )
    else:
        # 開發模式
        logger.info(f"Running in development mode at {url}")
        uvicorn.run(
            "src.main:app",
            host=host,
            port=port,
            reload=API_CONFIG['reload'],
            log_level=API_CONFIG['log_level']
        )
