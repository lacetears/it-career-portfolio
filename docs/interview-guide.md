# Learn and explain the projects

## Security
Trace a single event through `detect()`. Explain the grouping key, rolling five-minute window, why success is suspicious only after enough failures, and why it is not proof of compromise. Change the threshold and add a benign-user fixture. Explain why distributed attacks evade this detector. Complete the Wazuh guide and compare actual rules with the Python implementation.

## Data
Run the generator and explain why 1,213 source rows become 1,200 valid orders. Inspect rejected records. Explain the grain, why COUNT is appropriate here, how duplicates are handled, and why integer cents plus half-up rounding are used. Run a SQL query yourself. Add average order value per region, verify it manually, then rebuild the dashboard in Power BI.

## Coding
Create and resolve a ticket. Read the route handling that change. Explain GET versus POST, the role of SQLite, why bound parameters prevent SQL injection, what template escaping protects against, and how CSRF tokens work. Add a small feature such as a category field with a migration and tests. Explain why CSRF protection does not replace authentication.

## Demonstration sequence
1. Show the root README and explain the scope honestly.
2. Run tests and explain one meaningful case per project.
3. Demonstrate a ticket lifecycle and a dashboard filter.
4. Open the security findings and discuss a false positive.
5. Show a change you made personally and explain the tradeoff.
