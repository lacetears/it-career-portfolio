# Caleb Ferretis | Technology portfolio

B.S. Computer Science student at Western Governors University, expected December 2026. Building toward CCNA. Previous management experience at Equinox and Crunch Fitness provides context for working with people, organizing requests and following through on operational problems; these repositories demonstrate separate technical practice.

| Project | Evidence to inspect | Scope |
| --- | --- | --- |
| [IT Help Desk](https://github.com/lacetears/it-helpdesk) | Flask routes, SQLite persistence/migration, support workflow, validation and regression tests | Local single-operator lab |
| [Retail Sales Analysis](https://github.com/lacetears/sales-analytics) | Source-to-report reconciliation, SQL, signed monetary calculations, reproducible dashboard | Public historical data plus a separate synthetic exercise |
| [Authentication Log Analyzer](https://github.com/lacetears/auth-log-analyzer) | JSONL validation, rolling-window correlation, suppression and triage tests | Synthetic batch detection lab |

[Browser demonstrations](https://lacetears.github.io/it-career-portfolio/) provide an introduction. Help desk and security pages are separate JavaScript demos, not hosted Python applications. Their features can lag the maintained repositories. The sales page is a generated report; update it from `sales-analytics/retail/output/dashboard.html` after reviewing a new source run.

## Maintenance boundary

The `helpdesk/`, `data-analytics/` and `cybersecurity/` directories are **legacy combined-project snapshots**. They remain runnable and are retained without deleting features. New engineering work belongs in the standalone repositories. Tests here cover legacy behavior and local hub links; they do not certify feature parity.

## Verify the retained snapshot and hub

```sh
python -m pip install -r requirements.txt
python -m pytest -q
node tests/test_dashboard.cjs
```

No production deployment, client engagement, incident response, certification completion or business impact is claimed.
