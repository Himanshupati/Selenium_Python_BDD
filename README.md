# Selenium_Python_BDD

## Overview

This repository is a Python Selenium BDD automation framework built with `pytest` and `pytest-bdd`. It uses a page object pattern plus shared test utilities to run browser-based scenarios. The current example covers login functionality for the `saucedemo.com` site.

## Repository Structure

- `conftest.py` - pytest fixtures, hooks, browser setup, and reporting integration.
- `pytest.ini` - default pytest options.
- `requirements.txt` - required Python packages.
- `config/`
  - `config.properties` - local credentials and service keys (Sauce Labs, database, etc.).
  - `siteconfig.json` - environment/site URL mapping.
  - `testconfig.json` - framework runtime settings such as browser and wait time.
- `pages/`
  - `BasePage.py` - shared locator helpers, common actions, and browser utilities.
  - `loginpage.py` - login page locators and page-specific helpers.
- `tests/`
  - `features/` - BDD feature files.
  - `step_definitions/` - pytest-bdd step implementations.
- `utils/`
  - `browser_manager.py` - browser factory for Chrome, Firefox, and Sauce Labs remote sessions.
  - `config_loader.py` - config file loader utilities.
- `reports/` - generated HTML test reports.

## Prerequisites

- Python 3.11+ (project is tested on Python 3.13)
- Chrome / Firefox browser installed for local execution
- ChromeDriver / GeckoDriver available on PATH or managed by webdriver-manager
- Internet access for Sauce Labs execution if used

## Setup

1. Create and activate a Python virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Configure test settings

- `config/testconfig.json`
  - `browser` can be `chrome`, `firefox`, `chrome_headless`, `sauce_desktop`, or other supported Sauce Labs values.
  - `wait_time` controls default explicit wait seconds.
  - `save_logs` toggles logging behavior.

- `config/siteconfig.json`
  - Defines environments such as `prod`, `test`, `qa` and site entries with URL values.

- `config/config.properties`
  - Store Sauce Labs credentials under `[SAUCELABS_CRED]`.

Example `config/testconfig.json`:

```json
{
  "browser": "chrome",
  "wait_time": 30,
  "save_logs": "false"
}
```

Example `config/siteconfig.json`:

```json
{
  "prod": [
    {
      "site": "sauce",
      "url": "https://www.saucedemo.com/",
      "searchers": "sauce",
      "socialnum": 0
    }
  ]
}
```

## How the Framework Works

- `conftest.py` loads configuration and defines fixtures:
  - `site`, `env`, `rversion`, `url`, and `browser`.
  - Browser selection is driven by `config/testconfig.json`.
  - `BrowserManager` launches local or Sauce Labs browsers.
  - `EventFiringWebDriver` wraps the browser to handle events and optional Cloudflare detection.

- `pages/BasePage.py` provides shared functions:
  - `get_locator_type_and_value()` resolves locator tuples from page locators.
  - `enter_text()`, `get_element_text()`, `force_click()`, `scroll_into_view()`, and more.

- `pages/loginpage.py` defines locators for the login page and exposes methods such as:
  - `get_element()`
  - `get_elements()`
  - `get_loginpage_element_locator_type_and_value()`

- `tests/features/login.feature` describes BDD scenarios.
- `tests/step_definitions/test_loginpage.py` maps Gherkin steps to Selenium actions.

## Run Tests

Run a single scenario tag with pytest and generate an HTML report:

```powershell
pytest -m "valid_login" -v -q -s --capture sys --html=.\Reports\sauce.html --self-contained-html --site=sauce --env=prod --disable-warnings
```

If you need to execute against Sauce Labs, set `browser` to a Sauce Labs flavor in `config/testconfig.json`, for example `sauce_desktop`, and ensure credentials are configured in `config/config.properties`.

### Example local run

```powershell
pytest -v -q --site=sauce --env=prod
```

## Available Test Tags

- `@login_signin`
- `@valid_login`

These tags are defined in the feature file and can be used with `pytest -m`.

## Report Location

- HTML reports are written to `reports/`.
- The example command writes to `reports/sauce.html`.

## Notes

- The framework uses `pytest-bdd` for behavior-driven workflows.
- `browser_manager.py` supports local Chrome/Firefox and multiple Sauce Labs device/browser configurations.
- Locator mapping is centralized, so new page objects should follow the same pattern in `pages/*.py`.

## Extending the Framework

- Add new feature files under `tests/features/`.
- Add corresponding step definitions in `tests/step_definitions/`.
- Add page-specific locators and actions in `pages/<page>.py`.
- Add environment/site entries in `config/siteconfig.json`.
- Use `config/testconfig.json` to switch browsers and wait times.

