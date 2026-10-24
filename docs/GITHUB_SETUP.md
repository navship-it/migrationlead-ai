# Publish this portfolio on GitHub
Recommended repository name: `migrationlead-ai`. Description: “Excel-first lead prioritisation with an explainable workflow and a synthetic ML experiment.”

## Beginner route: browser upload
1. Sign in at https://github.com and choose New repository.
2. Enter the repository name. Choose Public for a portfolio containing only these synthetic files, or Private while preparing. Do not add an initial README because this project includes one.
3. Create the repository, then choose “uploading an existing file” (or Add file → Upload files).
4. Extract the downloaded ZIP. Open the `migrationlead-ai` folder and upload its CONTENTS, preserving `data`, `docs`, `reports`, `tests` and `.github` directories. Do not upload the ZIP or put everything inside an extra parent folder. Hidden files may need to be selected separately; CLI is more reliable for those.
5. Commit with “Initial portfolio: Excel-first lead prioritisation”. Verify README displays on the repository home page.
6. Inspect Actions → Python checks. Wait for the checks to finish. Add an actual app screenshot to README later if desired; do not invent a deployed demo URL.

## Git CLI route
From inside the extracted project folder:
```bash
git init
git add .
git commit -m "Initial portfolio: Excel-first lead prioritisation"
git branch -M main
```
Create an empty repository on GitHub. Copy its actual HTTPS URL, then run these commands with your real username:
```bash
git remote add origin https://github.com/YOUR_USERNAME/migrationlead-ai.git
git push -u origin main
```
Use GitHub's supported sign-in flow or GitHub Desktop; do not paste access tokens into the code, README or chat.

## Present it honestly
CV wording after you have run and reviewed it: “Built an independent Excel-first CRM analytics portfolio with explainable lead prioritisation, a synthetic-data ML experiment and an interactive Streamlit interface.”
Do not label this as freelance employment at Immatrix or actual client impact unless an engagement and measured results occur. The repository is source code; uploading it alone does not deploy an interactive app. A local demonstration is sufficient for a first meeting.
