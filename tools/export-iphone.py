"""Build the offline, single-file version from the main quiz page."""

import re
from base64 import b64encode
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = (root / "index.html").read_text(encoding="utf-8")
source = source.split("<!-- preview:end -->", 1)[0].replace("<!-- preview:start -->\n", "")
css = (root / "assets/show.css").read_text(encoding="utf-8")
source = re.sub(
    r'<link rel="stylesheet" href="assets/show\.css(?:\?[^"]*)?">',
    lambda _: f"<style>\n{css}</style>",
    source,
    count=1,
)
for alphabet in ("cyrillic", "latin"):
    font = f"assets/fonts/manrope-{alphabet}.woff2"
    data = b64encode((root / font).read_bytes()).decode("ascii")
    source = source.replace(f'url("{font}")', f'url("data:font/woff2;base64,{data}")')

license_text = (root / "assets/fonts/OFL.txt").read_text(encoding="utf-8")
license_text = license_text.replace("--", "—")
source = source.replace('<div id="quiz-stage">', f'<!--\n{license_text}-->\n<div id="quiz-stage">', 1)
(root / "quiz-iphone.html").write_text(source + "</html>\n", encoding="utf-8")
