This repository contains pytest-based UI and API automation focused on Selenium and small utility modules. The guidance below helps an AI coding agent be productive quickly.

Key context
- Tests live under `tests/` with UI Selenium tests in `tests/ui/selenium/` and general test helpers in `tests/ui/conftest.py`.
- Runtime configuration is in `src/config/` (notably `ui_config.py` and `settings.py`). Tests import `src` by inserting it into `sys.path` in `tests/ui/conftest.py`.
- Virtualenv lives in `ai_qa_env/` and a pinned `requirements.txt` lists required packages (including Selenium, pytest, webdriver-manager, Playwright, Allure).

How to run tests locally
- Activate the project virtualenv before running tests. Example (macOS zsh):
  - source ai_qa_env/bin/activate
- Run a single test file with pytest:
  - pytest -q tests/ui/selenium/test_automation_friendly.py -k test_saucedemo_full_flow
- Run the whole UI suite with increased verbosity and HTML report:
  - pytest tests/ui -q --html=reports/ui_test_report.html

Important fixtures and patterns
- `tests/ui/conftest.py` defines the `selenium` fixture. It uses `webdriver-manager` to install ChromeDriver and reads configuration from `src/config/ui_config.py`. Preferred approach for changes:
  - Modify `UIConfig` values or environment variables (UI_HEADLESS, UI_WINDOW_SIZE, etc.) rather than editing fixtures.
  - Tests expect the fixture to yield a `selenium.webdriver.Chrome` instance and close it in teardown.

Project conventions
- Tests add `src/` to `sys.path` at runtime (see `tests/ui/selenium/test_structure_verification.py`). When adding new modules, place them under `src/` and expose them via `src/<package>/__init__.py`.
- Configuration lives in `src/config/`. Prefer reading config via `from config import ui_config` or `from config import settings`.
- Use environment variables for secrets or toggles (OPENAI_API_KEY, UI_HEADLESS, UI_BROWSER). `.env` is supported via `python-dotenv` in `src/config/settings.py`.

Debugging and CI notes
- WebDriver: `webdriver-manager` installs ChromeDriver at runtime. On CI, ensure Chrome is available or replace with a container image that includes Chrome. Use `UIConfig.HEADLESS=True` for headless runs.
- If a test cannot find pages/elements, capture screenshots with `driver.save_screenshot('reports/screenshots/<name>.png')` — tests already do this in some places.
- Reports: tests write HTML reports to `reports/` by default when pytest is invoked with `--html=`. Allure is installed; if using Allure, follow Allure's CLI/report generation steps (not included here).

Code examples (patterns to follow)
- Reading config in tests or helpers:
  - from config import ui_config
  - browser = ui_config.UIConfig.BROWSER
- Using selenium fixture in tests (already used across tests):
  - def test_example(selenium):
      selenium.get(ui_config.UIConfig.BASE_URL)

Files to inspect when changing behavior
- `tests/ui/conftest.py` — Selenium fixture and webdriver setup.
- `src/config/ui_config.py` — UI-level configuration and env var keys.
- `src/config/settings.py` — general settings, dotenv usage, AI model keys.
- `tests/ui/selenium/test_structure_verification.py` — conventions for test import paths and basic checks.
- `requirements.txt` — pinned packages; update carefully and run tests.

When submitting changes
- Keep tests and fixtures stable: prefer adding new fixtures over modifying global test setup unless necessary.
- Run `pytest tests/ui -q` locally before pushing. Attach failing HTML reports/screenshots when asking for help.

If anything above is unclear or you want more detail about CI steps or Allure integration, tell me which area to expand.
