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

Each entry in `facets` begins with an emoji, a space, then the label
(`"🎹 Keyboardist"`). The emoji is split out at build time: it
becomes the icon on the chip, and the emoji from all of a man's facets form
the signature row on his plaque in the roll.

## Photographs

Drop `assets/photos/<slug>.jpg` (or `.png`, `.webp`, `.avif`) and it is
picked up automatically &mdash; see `assets/photos/README.md`. A man with no
photograph gets a gold rosette drawn deterministically from his name, so the
same man always has the same figure.
