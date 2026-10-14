# Repository notes

This repository holds the GitHub profile README and source for a small portfolio explorer.

## Profile README

GitHub displays the root `README.md` on the `shubham-k-jha` profile.

## Contribution animation

The workflow at `.github/workflows/contribution-snake.yml` creates the contribution animation and publishes it to the `output` branch.

1. Open **Settings → Actions → General**.
2. Under **Workflow permissions**, allow read and write repository permissions if required.
3. Open **Actions → Generate contribution animation → Run workflow**.
4. Confirm the run succeeds and that the `output` branch contains `github-contribution-grid-snake.svg`.

The animation will not appear until a workflow run completes successfully. The workflow also runs daily.

## Portfolio explorer

`portfolio/index.html` is the interactive project browser and `portfolio/projects.json` holds its project list. The explorer must be served over HTTP (for example, via GitHub Pages or a local web server); opening the HTML directly with `file://` prevents the browser from fetching the JSON file.
