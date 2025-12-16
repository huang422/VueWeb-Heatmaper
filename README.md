# Data Visualization HeatMap

An interactive web application that visualizes geographic distribution of user data through heatmaps on a Taiwan map. The system displays time-based heatmap visualizations with automatic hourly cycling, filtering by month and duration metrics, and demographic breakdowns.

## Features

-  **Interactive Heatmap**: Visualize user density across Taiwan with grid-based heatmap
-  **Time-Based Analysis**: Auto-cycling through 24 hours to reveal temporal patterns
-  **Month Filtering**: Filter data across 4 months (Dec 2024, Feb 2025, May 2025, Aug 2025)
- ⏱ **Duration Metrics**: Analyze by total users, <10min, 10-30min, >30min stay duration
-  **Demographics**: Gender and age distribution charts with Chinese labels
-  **Manual Controls**: Timeline slider, play/pause, reset functionality
-  **Responsive Design**: Works from 320px mobile to 4K desktop

## Technology Stack

### Backend
- **FastAPI** (Python 3.9+) - Web framework
- **Pandas** - Data processing
- **NumPy** & **Numba** - Coordinate conversion (TWD97 TM2)
- **Uvicorn** - ASGI server

### Frontend
- **Vue.js 3** (Composition API) - UI framework
- **OpenLayers 9** - Mapping library
- **Apache ECharts 5** - Charting library
- **Proj4** - Coordinate projection
- **Vite** - Build tool

## Quick Start

### Prerequisites
- Python 3.9+ (conda environment "fapi" recommended)
- Node.js 16.x or higher
- Git

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd store_heatmap
   ```

2. **Backend Setup**
   ```bash
   conda create -n fapi python=3.9 -y
   conda activate fapi
   cd backend
   pip install -r requirements.txt
   python -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
   ```

3. **Frontend Setup** (in new terminal)
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the application**
   - Frontend: http://localhost:5173
   - API Documentation: http://127.0.0.1:8000/docs

## Project Structure

```
store_heatmap/
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── main.py         # Application entry point
│   │   ├── api/            # API routes and models
│   │   ├── services/       # Business logic
│   │   ├── models/         # Data models
│   │   └── utils/          # Configuration
│   └── tests/              # Backend tests
├── frontend/                # Vue.js frontend
│   ├── src/
│   │   ├── components/     # Vue components
│   │   ├── views/          # Page views
│   │   ├── composables/    # Composition API logic
│   │   └── services/       # API client
│   └── public/             # Static assets
├── data/
│   └── data.csv            # Source data
├── docs/                    # Documentation
└── specs/                   # Feature specifications
```

## Data Format

The system processes CSV data with the following structure:
- **Grid Coordinates**: gx, gy (TWD97 TM2 system)
- **Time**: month (YYYYMM), hour (0-23)
- **Metrics**: avg_total_users, avg_users_under_10min, avg_users_10_30min, avg_users_over_30min
- **Demographics**: sex_1 (male %), sex_2 (female %), age_1 through age_9 (age group %)

## Building Windows Executable

```bash
# 1. Build frontend
cd frontend
npm run build

# 2. Build executable
cd ../backend
python build_exe.py
```

Output: `backend/dist/StoreHeatmap.exe` (40-60MB)

## API Endpoints

- `GET /api/heatmap` - Location data for map visualization
- `GET /api/demographics` - Gender and age statistics
- `GET /api/metadata` - Available months, hours, metrics
- `GET /health` - Server health check

See [API Documentation](http://127.0.0.1:8000/docs) when server is running.

## Performance

- API response time: <500ms
- Visualization rendering: <1s
- Coordinate conversion: ~260,000 conversions/second
- Memory usage: ~5MB data cache

## Documentation

- [User Guide](docs/user-guide.md) - How to use the application
- [Data Format](docs/data-format.md) - CSV schema documentation
- [Build Instructions](docs/build-instructions.md) - Development and packaging
- [Quickstart Guide](specs/001-heatmap-visualization/quickstart.md) - Developer onboarding

## License

[Add license information]

## Contributors

[Add contributor information]
