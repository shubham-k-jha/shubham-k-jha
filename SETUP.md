# Setup — Real v5 Portfolio System

1. Copy these files into `shubham-k-jha/shubham-k-jha`:
   - `README.md`
   - `generate_readme.py`
   - `config.json`
   - `data/repositories.json`
   - `.github/workflows/update-readme.yml`
2. Commit and push.
3. GitHub Actions will refresh the README every Monday or when manually dispatched.
4. The generator uses the public GitHub API and `GITHUB_TOKEN` in Actions; no token is hard-coded.
5. `config.json` controls categories, weights, exclusions, featured projects and overrides.
6. `portfolio/` is a real JavaScript dashboard. Copy it to the `shubham-k-jha.github.io` repository if you want the interactive layer on your public website.

## Local test

```bash
python3 generate_readme.py
```

## Windows CMD upload

```bat
git clone https://github.com/shubham-k-jha/shubham-k-jha.git
cd shubham-k-jha
:: copy the package files into this folder
git add .
git commit -m "Rebuild portfolio automation"
git push origin main
```

If your profile repo uses another default branch, replace `main` with that branch.
