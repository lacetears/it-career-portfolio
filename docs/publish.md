# Publish to GitHub
Create a repository named `it-career-portfolio` under your account. Use an empty repository (no generated README). From this extracted project folder:

```sh
git init -b main
git add .
git commit -m "Add cybersecurity, data analytics and help desk portfolio projects"
git remote add origin https://github.com/lacetears/it-career-portfolio.git
git push -u origin main
```
If using the GitHub CLI while signed in:
```sh
gh repo create it-career-portfolio --public --source=. --remote=origin --push
```
Choose only one publishing path. Do not run a second `git remote add` if origin already exists. Review files before publishing. Database files and secrets are excluded by `.gitignore`. Enable Actions to run the included workflow; a local passing test run is not proof of hosted CI passing.
