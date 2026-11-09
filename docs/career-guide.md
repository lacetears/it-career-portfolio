# Career guide: explain the evidence honestly

These are project descriptions and practice answers, not claims of employment or independent authorship. The engineering overhaul was implemented with an assistant. Before using action verbs such as “built,” “implemented,” or “tested,” review the changes, run the projects yourself, reproduce the tests and be able to explain the relevant code. Until then, use the neutral project bullets below. Do not claim the test runs in this audit as your personal work.

## IT Help Desk

### Three ATS-friendly project bullets

- Python/Flask ticket-management application with SQLite persistence, assignment, priorities, categories, status tracking and timestamped work notes.
- Server-side input validation, parameterized SQL, CSRF protection, escaped templates and indexed queue filtering with pagination.
- Automated regression coverage for ticket workflows, database migration, persistence, invalid input, security headers and search behavior.

### LinkedIn draft

My IT help desk project now has a clearer support workflow: categorize a request, assign it, document the investigation and follow it through resolution. The latest changes also add queue filters and tests around existing database upgrades. It runs locally with Flask and SQLite. The repository includes the code, setup steps and limitations: https://github.com/lacetears/it-helpdesk

Post after reviewing the PR. This wording describes the repository without claiming independent authorship or a production deployment.

### Interview explanation

“The project models a technician's ticket queue. Flask receives the form submission, validates the fields and CSRF token, then writes a ticket and its history to SQLite. Jinja renders the response with escaped content. The queue supports search and combined filters, and a category migration preserves existing tickets. It's a local single-operator lab. Authentication, authorization and concurrent-edit protection would be required before treating it as a shared service.”

### Five questions and sample answers

1. **Why SQLite?** It makes local setup simple and lets a reviewer inspect the schema without operating a database server. It fits this small lab. A shared service would require evaluating concurrent writes, backups and operational needs before deciding whether to move to a server database.
2. **Does CSRF make the app secure for multiple users?** No. It prevents a different site from submitting a valid form using a victim's session token, but it does not establish identity or permission. Anyone who can reach this app can access tickets. Parameterized SQL and escaped templates address different threats.
3. **How do old databases get the category field?** Startup checks the table columns and adds a constrained category with General as the default when it is missing. It then creates indexes and relationship-protection triggers. A regression test starts with an old schema, preserves a ticket and note, and repeats startup to check idempotence. Operational backup/restore still needs separate testing.
4. **What happens if the history insert fails after creating a ticket?** Both inserts are part of the same transaction and the code commits only after both succeed. Closing the uncommitted connection rolls back the transaction. That avoids a partially recorded operation. History still is not tamper-proof or attributed to an authenticated user.
5. **How would you handle two technicians updating the same ticket?** The current application is last-write-wins. A version column and conditional UPDATE could detect stale edits and return a conflict page. I would add a test with two clients reading the same version, then ensure the second save cannot silently overwrite the first.

### Understand before discussing

HTTP GET/POST and redirects; application factories; request context and teardown; sessions and CSRF; XSS versus SQL injection; SQLite transactions and constraints; additive migrations; indexes and LIKE-search limits; offset pagination; unit versus request-level integration tests; authentication versus authorization; last-write-wins concurrency.

## Retail Sales Analysis

### Three ATS-friendly project bullets

- Reproducible Python and SQL pipeline for 541,909 UCI Online Retail source rows, with signed-credit handling, Decimal rounding and documented data-quality exclusions.
- SQLite aggregates reconcile to cleaned-source totals, supporting £9,748,131.07 in net transaction value under the stated cleaning methodology.
- Generated HTML dashboard with country/month filtering, source-derived quality metrics and automated workbook-to-report and dashboard regression checks.

### LinkedIn draft

The most useful part of my retail analysis project is being able to trace a number back to the source. It separates positive sales from credits, documents excluded rows and checks the SQL totals against the cleaned records. The dashboard now regenerates with the analysis instead of remaining a separate saved page. It uses public historical UCI data, not business results from an employer: https://github.com/lacetears/sales-analytics

### Interview explanation

“The main pipeline reads the UCI workbook with openpyxl, validates its schema, removes exact duplicates and keeps negative quantities as credits. Decimal rounds each line to integer pence. SQLite produces monthly-country and stock-code aggregates, then the code reconciles those totals to an independent sum of cleaned records. JSON and CSV outputs feed a generated HTML dashboard. The synthetic electronics-sales exercise is separate and uses a different, simplified revenue model.”

### Five questions and sample answers

1. **Why not use floating point for money?** Binary floating point cannot represent many decimal fractions exactly. This pipeline uses Decimal for the source amount, rounds half-up per line and stores integer pence. That makes rounding explicit. It does not mean the result matches an accounting system with a different rounding policy.
2. **Why retain negative quantities?** They represent credits or adjustments. Dropping them would overstate net value. Positive sales minus credit magnitude equals signed net transaction value. I would confirm the source semantics before calling it recognized revenue.
3. **How do you know the dashboard isn't stale?** The pipeline renders it from the report and a template. A CI check regenerates it in a temporary directory and compares bytes. JavaScript tests execute its actual embedded script and check full totals, combined filters and empty selections against report data. They don't replace visual browser testing.
4. **What is risky about deduplication?** Identical source rows can be genuine repeated invoice lines. Exact deduplication is a documented assumption, not a proven business rule. With a reliable line ID I would deduplicate on that; without one, comparing results with and without deduplication would show sensitivity.
5. **What conclusions should you avoid?** No profit claims because costs are missing, no causal claims from descriptive aggregates, and no claim that December 2011 collapsed because the month contains only nine days. A row is an invoice line, not an order. Postage codes also appear in the stock-code ranking.

### Understand before discussing

Dataset grain; invoice versus line counts; signed adjustments; missing-value policy; exact versus conflicting duplicates; Decimal and rounding; SQL GROUP BY, CASE, COALESCE and COUNT DISTINCT; reconciliation and source hashes; repeatability versus correctness; partial-period bias; DOM text insertion; data privacy; dashboard filters and fixed-reference tables.

## Authentication Log Analyzer

### Three ATS-friendly project bullets

- Python JSONL authentication-log analyzer with schema/IP validation, UTC normalization and configurable rolling-window correlation.
- Detection scenarios for repeated login failures, success after failures and possible password spraying across users, using labeled synthetic events.
- Automated tests for time-window boundaries, duplicate handling, host isolation, malformed input and alert suppression, supported by documented triage limitations.

### LinkedIn draft

My authentication-log analyzer now looks for failures across multiple usernames as well as repeated failures against one account. The important part is the context: duplicates, shared IP addresses and normal user mistakes can all change what an alert means. The project uses synthetic logs and includes tests and investigation notes. It's a small detection exercise, not a deployed SIEM: https://github.com/lacetears/auth-log-analyzer

### Interview explanation

“The detector validates normalized JSONL, converts timestamps to UTC and sorts events before processing them. Per-host/IP/user queues track repeated failures and success-after-failure patterns. A separate per-host/IP queue counts distinct failing users for possible spraying. Thresholds and windows are configurable. Duplicate suppression and IP exclusions are explicit tuning decisions, and every alert still needs investigation.”

### Five questions and sample answers

1. **Why group on host, source IP and user?** It prevents failures from unrelated destinations or accounts from being combined into the single-account rule. The spray rule intentionally groups more broadly by host/IP and counts distinct usernames. Distributed attacks across many source IPs remain outside these rules.
2. **What is the window boundary?** Events exactly window seconds old are included; older events expire. Timezone normalization lets equivalent instants compare correctly. Equal timestamps keep source order, so a source event sequence number would help if causal ordering matters.
3. **Can a success prove a compromise?** No. It can be a legitimate user succeeding after mistakes. I would check the account owner, source, MFA, session details and endpoint evidence. The detector assigns triage priority, not a verdict.
4. **Why is deduplication configurable?** Duplicate ingestion can inflate failure counts, but exact records with coarse timestamp precision can represent separate attempts. The default suppresses identical normalized records; keep-duplicates preserves them. A trustworthy source event ID would support a better policy.
5. **Would this scale as a SIEM service?** Not as written. It loads and sorts the batch and retains keyed state, so memory grows with input. A streaming design would need state expiration, late-event policy, event provenance, persistent checkpoints and operational monitoring. No throughput or detection-accuracy benchmark is claimed.

### Understand before discussing

Authentication versus authorization; JSONL schema validation; UTC and offset-aware timestamps; stable sorting; deque-based rolling windows; correlation keys; brute-force versus password-spray patterns; suppression versus deduplication; false positives and false negatives; NAT/shared egress; precision/recall; input provenance; batch memory costs; incident triage versus confirmed compromise.

## Recruiter review across target roles

These are portfolio-evidence judgments, not hiring probabilities. A repository cannot establish actual support experience, communication quality or workplace delivery.

| Role | Strongest current evidence | Missing evidence / next practical proof |
| --- | --- | --- |
| IT Support Specialist | Help desk workflow; management background provides communication context | Real Windows troubleshooting, identity administration, escalation notes and customer-facing resolutions |
| Desktop Support Technician | Ticket documentation and priorities | OS installation, device enrollment, drivers, endpoint tooling and hardware diagnostics |
| Junior Software Developer | Flask/SQLite app, validation, migration and regression tests | Authenticated multi-user design, code review ownership, deployment and deeper algorithm/API work |
| QA Analyst | Reproducible regressions and integration/DOM checks across projects | A written test plan, exploratory testing, reproducible defect reports and real browser automation |
| Junior Data Analyst | Real-data pipeline, SQL, reconciliation and dashboard | Independent interpretation, Excel/Power BI delivery and a focused business-question write-up |
| Technical Support Analyst | Application troubleshooting context, log parsing and support queue | API/network diagnostics, customer explanations and unfamiliar-system debugging |
| Junior Cybersecurity Analyst | Synthetic detection, false-positive discussion and triage report | Native Windows/Linux ingestion, verified SIEM lab, endpoint/network correlation and measured detection quality |
| Network Support Technician | Some network-ticket vocabulary and stated CCNA study | Actual VLAN/routing/DNS/DHCP configurations, packet evidence and break/fix troubleshooting |

For a broad entry-level portfolio, lead with the help desk. For data applications, lead with sales analysis; it has the strongest source-to-output evidence. The security project is a foundational exercise, not enough by itself to present as operational SOC experience. The hub duplicates older code and should stay unfeatured.

## Highest-priority next work

1. Reproduce these projects locally and explain one regression per project. Keep a short dated verification log with commands, output and what you changed yourself.
2. Complete the CCNA path already underway rather than adding unrelated certification tracks. Cisco's official outline covers network fundamentals, access, IP connectivity/services, security fundamentals and automation: https://www.cisco.com/site/us/en/learn/training-certifications/exams/ccna.html. Check the active exam outline before booking.
3. Build one small office network break/fix lab: two VLANs, inter-VLAN routing, DHCP, DNS, an ACL and a troubleshooting ticket set. Save actual configurations and before/after ping, DNS and packet-capture evidence. Break a route, DHCP scope or ACL deliberately; document symptoms, hypotheses, tests, fix and verification. This recommendation addresses the clearest evidence gap in the current portfolio; it is not a claim that the lab has been built.
4. If support roles become the primary target, add a Windows identity/endpoint lab with account creation, group permissions and documented recovery tasks. If analyst roles become primary, finish one focused analysis with a stakeholder-style recommendation and uncertainty statement before starting another project.
5. Tailor applications to one role family at a time. Keep fitness job titles accurate; put technical labs in Projects, not disguised as IT employment. List the degree as expected December 2026 and CCNA as in progress until earned.
