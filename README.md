# PRE_Project

## Overview
A platform for automated competitive and internal pattern analysis, from company name input to strategic dashboards.

## Setup
1. Create and activate the virtual environment:
   ```
   python -m venv venv
   .\venv\Scripts\Activate
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Main Directories
- `config/` - Configuration files
- `mcp_infrastructure/` - Server/client logic
- `agents/` - Modular agents for scraping, pattern detection, etc.
- `data/` - All collected/generated data
- `competitor_discovery/` - Competitor identification logic
- `synthetic_data_generators/` - Internal data generation
- `pattern_recognition/` - Pattern analysis modules
- `dashboards/` - Dashboard logic
- `api/` - API endpoints
- `frontend/` - Frontend code
- `utils/` - Utility scripts
- `tests/` - Tests
- `logs/` - Log files 