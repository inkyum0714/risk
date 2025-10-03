# Copilot Instructions for the `risk` Project

## Overview
This project is a Python-based web application for risk and weather data lookup, using Flask for the backend and HTML templates for the frontend. It integrates with external APIs (Korean government, KMA) and uses Selenium for data scraping and automated testing.

## Key Components
- `riskmap.py`, `WeatherMap.py`, `exchange_rate_map.py`: Flask apps exposing `/main` and other endpoints, rendering `templates/main.html`.
- `Symbol.py`: Contains country and symbol mapping data (e.g., `country_code_data_two`, `country_code_data_five_number`).
- `templates/main.html`: Main UI, expects variables like `values` and `risks` from Flask routes.
- `temp.py`, `test.py`: Use Selenium for scraping and/or automated browser-based tests.

## Data Flow
- User submits forms in `main.html` → Flask route (`/main`, `/rate`, `/Weather`) → Data lookup/API call → Render template with results.
- Country codes and station numbers are mapped using data from `Symbol.py`.
- External API keys are hardcoded in Python files (e.g., `api_key` in `riskmap.py`, `WeatherMap.py`).

## Developer Workflows
- **Run Flask app:**
  ```bash
  python riskmap.py
  # or
  python WeatherMap.py
  ```
- **Selenium scripts:**
  - Run `temp.py` or `test.py` for scraping or browser automation.
- **Templates:**
  - Edit `templates/main.html` for UI changes. Flask routes must pass required variables (`values`, `risks`).
- **Dependencies:**
  - Requires `Flask`, `requests`, `selenium` (install via `pip`).

## Project Conventions
- API keys are stored directly in source (not secure for production).
- All Flask apps use `main.html` for rendering results.
- Data mapping logic (country codes, symbols) is centralized in `Symbol.py`.
- Form field names in HTML must match those expected in Flask routes (e.g., `stn`, `riskmap`).

## Examples
- To add a new country code, update the relevant dictionary in `Symbol.py`.
- To add a new data lookup, create a new Flask route and update `main.html` to include a form for it.

## External Integrations
- Korean government travel alarm API (see `riskmap.py`).
- KMA weather API (see `WeatherMap.py`).
- Selenium WebDriver for scraping/testing (see `temp.py`, `test.py`).

---
If any section is unclear or missing, please provide feedback for further refinement.
