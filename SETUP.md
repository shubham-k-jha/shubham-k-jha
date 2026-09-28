# Living GitHub Portfolio System

## What this is

This package turns the profile README into a lightweight, automatically maintained portfolio.

- GitHub README = recruiter-facing entry point
- `generate_readme.py` = GitHub API → classification → README generator
- `config.yaml` = categories, keywords, weights, overrides, exclusions
- `data/repositories.json` = generated repository metadata
- `.github/workflows/update-readme.yml` = weekly automation
- `README.template.md` = human-maintained presentation layer

GitHub README Markdown cannot run arbitrary JavaScript or load a custom CSS application. The cards here therefore use GitHub-compatible Markdown/HTML. For true filtering, animation, or interactive dashboards, use a separate GitHub Pages site.

## 1. Put these files in the profile repository

For a GitHub profile README, the repository name must exactly match the GitHub username.

Copy:

```text
README.md
README.template.md
generate_readme.py
config.yaml
data/repositories.json
.github/workflows/update-readme.yml
```

## 2. Confirm the username

Edit `config.yaml`:

```yaml
username: your-github-username
```

The current configuration uses `shubham-k-jha`, the confirmed GitHub username.

## 3. Generate locally

```bash
python -m pip install requests pyyaml
export GITHUB_TOKEN="your-token"
python generate_readme.py
```

A token is recommended for API-rate-limit headroom. Do not put it in source files.

## 4. Enable GitHub Actions

Commit the workflow to:

```text
.github/workflows/update-readme.yml
```

The workflow uses GitHub's built-in `GITHUB_TOKEN`, so no personal access token needs to be stored in the repository.

It runs weekly and can also be started manually from the Actions tab.

## 5. How categorization works

The classifier checks:

1. Topics — 40%
2. Repository name — 20%
3. Description — 20%
4. README content — 10%
5. Primary language — 10%

The weights are configurable in `config.yaml`.

A repository can belong to multiple categories. If no category reaches the configured threshold, it is left uncategorized rather than forced into a misleading section.

## 6. Manual overrides

Use:

```yaml
overrides:
  my-repository:
    categories: [data_analytics, bi_visualization]
    featured: true
```

Overrides take precedence over automatic category assignment.

## 7. Exclusions

Use:

```yaml
exclude:
  - scratch-repository
  - archived-experiment
```

Excluded repositories are not rendered.

## 8. Add a category

Add a new block under `categories`:

```yaml
business_operations:
  title: "🧭 Business Operations"
  keywords:
    - operations
    - process
    - workflow
```

Then add a matching marker pair to `README.template.md`:

```html
<!-- AUTO:CATEGORY:business_operations:START -->
<!-- AUTO:CATEGORY:business_operations:END -->
```

The generator will populate it automatically.

## 9. Why the generated README does not hard-code repository counts

Repository counts are derived from the live API response during generation. This avoids stale numbers after repositories are added, renamed, archived, or deleted.

## 10. Ranking

Repository ordering is a configurable supporting-signal ranking, not a claim of project quality. Stars and forks are never treated as proof of quality.

## 11. GitHub Pages extension

If you want true clickable square cards, filters, search, animations, and category pages, create a Pages site using the same `data/repositories.json`.

Suggested architecture:

```text
GitHub API
    ↓
generate_readme.py
    ├── README.md
    └── data/repositories.json
                 ↓
          GitHub Pages
                 ↓
        Interactive portfolio
```

The README remains the fast recruiter entry point; Pages provides the richer UI.

## Username

The confirmed GitHub username is `shubham-k-jha`. All generated profile URLs, repository API calls, badges, and project links use this username.
