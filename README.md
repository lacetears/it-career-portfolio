# IT Career Portfolio
Three practical projects: security event detection, sales analytics, and a help desk application.

| Project | Deliverable | Main skills |
| --- | --- | --- |
| [Security monitoring](cybersecurity/) | Working Python detector, synthetic authentication logs, incident report, Wazuh configuration and deployment guide | Log correlation, triage, defensive security |
| [Sales analytics](data-analytics/) | Reproducible cleaning pipeline, SQL analysis, interactive HTML dashboard, Power BI measures and build guide | Python, SQL, data validation, business analysis |
| [IT help desk](helpdesk/) | Working Flask application with persistent tickets, assignment, search and activity history | Python, Flask, SQLite, HTML/CSS, testing |

## Quick start
Python 3.12 recommended. All commands below run from the repository root.

```sh
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell instead: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python data-analytics/generate_data.py
python data-analytics/analyze.py
python cybersecurity/detect.py
python -m pytest -q
python helpdesk/seed.py
python helpdesk/app.py
```
Open http://127.0.0.1:5000 for the ticketing app. Open `data-analytics/output/dashboard.html` directly in a browser for analytics, with no server or external CDN required. The security report is in `cybersecurity/reports/`.

## Scope and evidence
- All sales, authentication events, and seeded tickets are synthetic.
- The security detector is tested locally. A live Windows/Linux Wazuh deployment has **not** been performed; follow the lab guide and capture your own evidence.
- The data project includes a working HTML dashboard and Power BI DAX/build instructions. It does **not** include a completed or validated `.pbix` or Excel workbook.
- The help desk is a local single-operator demonstration. It has no authentication, user roles, email, or SLA engine. Do not expose it publicly without implementing those controls.
- Tests and verification details: [validation](docs/validation.md).

## Interview and résumé preparation
Read [project walkthrough](docs/interview-guide.md) and [résumé wording](docs/resume-bullets.md). Describe what you personally understand and completed. Do not claim live SIEM deployment or Power BI experience from configuration files alone.

## Design choices
SQLite keeps setup accessible and queries inspectable. Integer cents avoid floating-point drift. Synthetic deterministic data makes tests repeatable. The security detector uses a rolling time window and correlates by host, source, and user. Flask templates escape user content, queries use parameters, and state changes require a CSRF token.

## References
- [Flask testing](https://flask.palletsprojects.com/en/stable/testing/)
- [Wazuh custom rules](https://documentation.wazuh.com/current/user-manual/ruleset/rules/custom.html)
- [Wazuh rule syntax](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html)
- [Power BI learning](https://learn.microsoft.com/en-us/training/powerplatform/power-bi)
