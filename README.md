### playwright-test-framework

Plan:

- To select a stable website for automation
- To write test plan
- To set up test framework structure
- To incorportate UI and API tests scripts
- To integrate with reports and display the test report

- [ ] Setup venv
- [ ] Set up requirements.txt
- [ ] Set up pytest.ini :- helps in configuring the pytest configuration for log level, markers and default browser set up
- [ ] Set up conftest.py - for browser set up
- [ ] Set up utils folder - for holding common helper, contants, locators
- [ ] tests/smoke/test_homepage.py -

### Technical Details of Playwright:

| **Playwright Mode**     | **Best For**                         |
| ----------------------- | ------------------------------------ |
| **Sync (`sync_api`)**   | Smoke tests, quick sanity tests      |
| **Async (`async_api`)** | Regression, API, performance, mobile |
