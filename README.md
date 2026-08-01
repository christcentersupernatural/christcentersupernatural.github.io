# Men of the Spirit

Profile pages for the *Men of the Spirit* session at Christ Center
Supernatural Ministry — one page per man, at `/<first-name>/`.

## Editing

All copy lives in `_build/profiles.json`. Nothing is written by hand in the
generated HTML.

1. Edit `_build/profiles.json`.
2. Rebuild: `python3 _build/build.py`
3. Commit and push. GitHub Pages serves `main` from the repository root.

Each man needs: `slug`, `name`, `monogram`, `role`, `facets`, `body`
(one string per paragraph) and `call`. Setting `"draft": true` renders the
"tribute still being written" page instead of a body.
