#!/usr/bin/env python3
"""Generate the Men of the Spirit site from profiles.json.

Writes index.html plus one directory per man (e.g. /victor/index.html) so
each profile is reachable at a clean path. Run from anywhere:

    python3 _build/build.py
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "_build" / "profiles.json").read_text("utf-8"))

ORDINALS = [
    "One", "Two", "Three", "Four", "Five", "Six",
    "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve",
    "Thirteen", "Fourteen", "Fifteen", "Sixteen",
]

FLOURISH = (
    '<svg class="flourish" viewBox="0 0 460 26" aria-hidden="true">'
    '<path d="M0 13 H168 M292 13 H460 '
    'M168 13 c16 0 16 -10 32 -10 s16 20 32 20 s16 -20 32 -20 s16 10 28 10" />'
    "</svg>"
)


def head(title, description, depth):
    """Shared document head. `depth` is how many levels deep the page sits."""
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#06070f">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{up}assets/css/site.css">
</head>
<body>
<canvas class="beam" aria-hidden="true"></canvas>
<header class="masthead">
  <a href="{up}">{DATA['event']['orgShort']} <span class="masthead__mark">&#9670;</span> Men of the Spirit</a>
  <a href="{up}#the-roll">The Roll</a>
</header>
<main class="page">"""


def foot(depth):
    up = "../" * depth
    org = DATA["event"]["org"]
    return f"""</main>
<footer class="colophon">
  <div>{org}</div>
  <div>Men of the Spirit &#9670; A Celebration of Our Men</div>
</footer>
<script src="{up}assets/js/site.js"></script>
</body>
</html>
"""


def profile_page(man, index, men):
    """One man's page: hero, tribute, the call, and his neighbours."""
    ordinal = ORDINALS[index]
    prev_man = men[index - 1] if index > 0 else None
    next_man = men[index + 1] if index < len(men) - 1 else None
    name = man["name"]
    desc = f"{name} &#8212; {man['role']}. Celebrated at Men of the Spirit."

    out = [head(f"{name} &#183; Men of the Spirit", desc, 1)]

    out.append(f"""
<section class="hero">
  <p class="hero__eyebrow" data-step="eyebrow">Profile {ordinal}</p>
  <h1 class="hero__name" data-focus>{name}</h1>
  {FLOURISH}
  <p class="hero__role" data-step="role">{man['role']}</p>
  <div class="scroll-cue" data-step="cue">His story<span></span></div>
</section>""")

    if man.get("draft"):
        out.append(f"""
<section class="awaiting">
  <div class="awaiting__box reveal">
    <h2>His tribute is still being written</h2>
    <p>{name} is one of the men we are celebrating in this session. His
      profile is being prepared with the same care as the rest, and will
      appear here as soon as it is ready.</p>
    <p>If you know him well &#8212; his calling, his craft, the thing he is
      quietly brilliant at, the thing everyone teases him about &#8212;
      that is exactly what belongs on this page.</p>
  </div>
</section>""")
    else:
        paras = []
        for n, text in enumerate(man["body"]):
            cls = ' class="lead"' if n == 0 else ""
            paras.append(f"    <p{cls}>{text}</p>")
        facets = ""
        if man["facets"]:
            items = "".join(f"<li>{f}</li>" for f in man["facets"])
            facets = f'\n  <ul class="facets reveal">{items}</ul>'
        body = "\n".join(paras)
        out.append(f"""
<section class="tribute">
  <p class="tribute__label reveal">The Tribute</p>
  <div class="reveal">
{body}
  </div>{facets}
</section>""")

    out.append(f"""
<section class="call reveal">
  <p>{man['call']}</p>
</section>

<nav class="pager">""")

    if prev_man:
        out.append(f"""  <a class="pager__link" href="../{prev_man['slug']}/">
    <span class="pager__dir">Previous</span>
    <span class="pager__who">{prev_man['name']}</span>
  </a>""")
    else:
        out.append("  <span></span>")

    out.append('  <a class="pager__hall" href="../#the-roll">All the men</a>')

    if next_man:
        out.append(
            f"""  <a class="pager__link pager__link--next" href="../{next_man['slug']}/">
    <span class="pager__dir">Next</span>
    <span class="pager__who">{next_man['name']}</span>
  </a>"""
        )
    else:
        out.append("  <span></span>")

    out.append("</nav>")
    out.append(foot(1))
    return "\n".join(out)


def index_page(men):
    """The hall: the invocation, then every man as a lit plaque."""
    event = DATA["event"]
    desc = ("A celebration of the men of Christ Center Supernatural "
            "Ministry &#8212; their character, faith, craft and service.")
    out = [head(f"Men of the Spirit &#183; {event['orgShort']}", desc, 0)]

    out.append(f"""
<section class="hall-hero">
  <p class="hall-hero__org" data-step="eyebrow">{event['org']}</p>
  <h1 class="hall-hero__title" data-focus>Men of the Spirit</h1>
  {FLOURISH}
  <p class="hall-hero__sub" data-step="role">{event['session']}</p>
  <div class="scroll-cue" data-step="cue">Begin<span></span></div>
</section>

<section class="invocation">""")

    for n, text in enumerate(event["intro"]):
        cls = ' class="lead"' if n == 0 else ""
        out.append(f'  <div class="reveal"><p{cls}>{text}</p></div>')

    count = ORDINALS[len(men) - 1]
    out.append(f"""</section>

<section class="roll" id="the-roll">
  <p class="roll__label">The Roll &#9670; {count} Men</p>
  <div class="roll__grid">""")

    for i, man in enumerate(men):
        draft = " plaque--draft" if man.get("draft") else ""
        role = ("Profile in preparation" if man.get("draft")
                else man["role"])
        out.append(f"""    <article class="plaque{draft} reveal">
      <p class="plaque__no">Profile {ORDINALS[i]}</p>
      <div class="plaque__monogram" aria-hidden="true">
        <svg viewBox="0 0 76 76"><circle cx="38" cy="38" r="36"></circle>
        <circle class="arc" cx="38" cy="38" r="36"></circle></svg>
        {man['monogram']}
      </div>
      <h2 class="plaque__name">{man['name']}</h2>
      <p class="plaque__role">{role}</p>
      <a class="plaque__link" href="{man['slug']}/"
         aria-label="Read the tribute to {man['name']}"></a>
    </article>""")

    out.append("""  </div>
</section>""")
    out.append(foot(0))
    return "\n".join(out)


def favicon():
    """A gold diamond on the hall's ground, matching the masthead mark."""
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
            '<rect width="64" height="64" rx="10" fill="#06070f"/>'
            '<path d="M32 12 L48 32 L32 52 L16 32 Z" fill="none" '
            'stroke="#c9a44c" stroke-width="3"/>'
            '<circle cx="32" cy="32" r="4" fill="#f4e5b6"/></svg>')


def main():
    men = DATA["men"]

    (ROOT / "index.html").write_text(index_page(men), "utf-8")
    (ROOT / "assets" / "favicon.svg").write_text(favicon(), "utf-8")
    (ROOT / ".nojekyll").write_text("", "utf-8")

    for i, man in enumerate(men):
        folder = ROOT / man["slug"]
        folder.mkdir(exist_ok=True)
        (folder / "index.html").write_text(profile_page(man, i, men), "utf-8")

    print(f"built index.html + {len(men)} profile pages in {ROOT}")


if __name__ == "__main__":
    main()
