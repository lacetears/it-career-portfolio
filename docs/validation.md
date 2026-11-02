# Validation record

Validated locally on 2026-11-01 with Python 3.12.

- 15 pytest tests passed.
- Help desk: create/update/search/filter workflow, CSRF rejection, invalid priority rejection, escaped HTML, SQL injection-shaped search, and missing-ticket handling.
- Security: expected alert pair, out-of-order input, expired window, separate hosts, and timezone validation.
- Data: half-up rounding, deduplication, rejected invalid values/dates, zero revenue for returns, row reconciliation, and agreement between SQL monthly totals and clean CSV totals.
- Data pipeline: 1,213 raw rows → 1,200 valid orders + 10 duplicate rows + 3 rejected rows.
- Recognized synthetic revenue: $1,014,040.65; gross profit: $303,958.65.

Run `python -m pytest -q` after generating the data outputs to reproduce the test result. GitHub Actions is configured but has not been run remotely. Wazuh VM deployment and native Power BI/Excel verification have not been performed.

Browser screenshot verification was unavailable because the local browser download failed. No screenshots are included or claimed. Flask pages were rendered through its test client.

A Node.js DOM-stub test passed for dashboard totals, combined region/product filtering, the filtered product table, and empty selections. It checks script logic, not visual layout or native browser behavior. Run `node tests/test_dashboard.cjs` (Node.js 22+) to reproduce.
