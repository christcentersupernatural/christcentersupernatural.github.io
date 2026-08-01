# Photographs

Drop a photograph in here named after the man's slug and it appears on both
his page and his plaque in the roll. Nothing else needs editing.

    assets/photos/victor.jpg
    assets/photos/cosmas.jpg
    assets/photos/raphael.png

Accepted: `.jpg` `.jpeg` `.png` `.webp` `.avif`

Slugs: victor, david, christopher, phronesis, baraka, cosmas, amos,
gregory, caleb, fredrick, joseph, raphael

**Shape** — the portrait is a circle, so square-ish crops work best. A
head-and-shoulders photograph around 800x800 is ideal; anything larger is
scaled down by the browser and only costs load time.

Any man without a photograph shows a gold rosette drawn from his name
instead, so the roll always reads evenly.

After adding photographs, rebuild and push:

    python3 _build/build.py
    git add -A && git commit -m "Add photographs" && git push
