"""
FastAPI Application Entry Point
Main application with CORS middleware and route registration.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from .utils.config import API_CONFIG, CORS_CONFIG, get_data_path
from .services.data_loader import initialize_cache
from .api.routes import data, demographics

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Store Heatmap Visualization API",
    description="REST API for interactive geographic heatmap visualization of user distribution data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_CONFIG['allow_origins'],
    allow_credentials=CORS_CONFIG['allow_credentials'],
    allow_methods=CORS_CONFIG['allow_methods'],
    allow_headers=CORS_CONFIG['allow_headers'],
)


@app.on_event("startup")
async def startup_event():
    """Initialize data cache on application startup."""
    try:
        data_path = get_data_path()
        logger.info(f"Initializing data cache from {data_path}")
        initialize_cache(str(data_path))
        logger.info("Application startup complete")
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise


@app.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns:
        Status and timestamp
    """
    from datetime import datetime
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


# Register API routes
app.include_router(data.router, prefix="/api", tags=["data"])
app.include_router(demographics.router, prefix="/api", tags=["demographics"])


# Serve frontend static files (for packaged executable)
# In development, Vite dev server handles frontend
try:
    frontend_dist = Path(__file__).parent.parent.parent / "frontend" / "dist"
    if frontend_dist.exists():
        app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")

        @app.get("/")
        async def serve_frontend():
            """Serve frontend index.html"""
            return FileResponse(str(frontend_dist / "index.html"))
except Exception as e:
    logger.warning(f"Frontend static files not available: {e}")


def find_available_port(start_port=8000, end_port=8010):
    """
    Find an available port in the specified range.

    Args:
        start_port: Starting port number
        end_port: Ending port number

    Returns:
        Available port number or None if none found
    """
    import socket

    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    return None


def open_browser(url, delay=2.0):
    """
    Open browser after a delay to ensure server is ready.

    Args:
        url: URL to open
        delay: Delay in seconds before opening browser
    """
    import time
    import webbrowser

    time.sleep(delay)
    try:
        logger.info(f"Opening browser at {url}")
        webbrowser.open(url)
    except Exception as e:
        logger.warning(f"Failed to open browser: {e}")


if __name__ == "__main__":
    import uvicorn
    import sys
    import threading

    # Determine if running as packaged executable
    is_packaged = getattr(sys, 'frozen', False)

    # Find available port
    port = find_available_port()
    if port is None:
        logger.error("No available ports found in range 8000-8010")
        port = API_CONFIG['port']

    host = API_CONFIG['host']
    url = f"http://{host}:{port}"

    # Auto-launch browser for packaged executable
    if is_packaged:
        logger.info("Running as packaged executable")
        logger.info(f"Server will start at {url}")

        # Start browser in background thread
        browser_thread = threading.Thread(target=open_browser, args=(url,), daemon=True)
        browser_thread.start()

        # Run server without reload in packaged mode
        uvicorn.run(
            app,  # Use app instance directly (not string) when packaged
            host=host,
            port=port,
            log_level=API_CONFIG['log_level']
        )
    else:
        # Development mode
        logger.info(f"Running in development mode at {url}")
        uvicorn.run(
            "src.main:app",
            host=host,
            port=port,
            reload=API_CONFIG['reload'],
            log_level=API_CONFIG['log_level']
        )
