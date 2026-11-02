"""asciiforge CLI: render text as ASCII art with pyfiglet."""
import argparse
import shutil
import sys

import pyfiglet

STYLES = [
    "standard", "slant", "banner3", "big", "block", "bubble", "digital",
    "doom", "isometric1", "larry3d", "shadow", "small", "starwars", "3-d",
]
DEFAULT_FONT = "standard"


def render(text, font=DEFAULT_FONT, width=80):
    """Render text in a font, wrapping words so each block fits width."""
    fig = pyfiglet.Figlet(font=font, width=10**6)
    blocks, line = [], ""
    for word in text.split():
        trial = f"{line} {word}" if line else word
        if line and _width(fig.renderText(trial)) > width:
            blocks.append(fig.renderText(line).rstrip("\n"))
            line = word
        else:
            line = trial
    if line:
        blocks.append(fig.renderText(line).rstrip("\n"))
    return "\n".join(b for b in blocks if b.strip())


def _width(art):
    return max((len(l) for l in art.splitlines()), default=0)


def boxed(art):
    lines = art.splitlines() or [""]
    w = max(len(l) for l in lines)
    top = "+" + "-" * (w + 2) + "+"
    return "\n".join([top] + [f"| {l.ljust(w)} |" for l in lines] + [top])


def main(argv=None):
    p = argparse.ArgumentParser(prog="asciiforge", description="Turn a sentence into ASCII art.")
    p.add_argument("text", nargs="*", help="text to render (or pipe it on stdin)")
    p.add_argument("-f", "--font", default=DEFAULT_FONT, help="style name (any pyfiglet font)")
    p.add_argument("--list", action="store_true", help="list curated styles")
    p.add_argument("--all", action="store_true", help="preview the text in every curated style")
    p.add_argument("--width", type=int, default=shutil.get_terminal_size((80, 24)).columns)
    p.add_argument("--border", action="store_true", help="draw a box around the output")
    p.add_argument("-o", "--output", help="also save the output to this file")
    a = p.parse_args(argv)

    if a.list:
        print("\n".join(STYLES))
        return 0

    text = " ".join(a.text)
    if not text and not sys.stdin.isatty():
        text = sys.stdin.read()
    text = " ".join(text.split())
    if not text:
        p.error("give some text, or pipe it in")

    avail = set(pyfiglet.FigletFont.getFonts())
    fonts = STYLES if a.all else [a.font]
    unknown = [f for f in fonts if f not in avail]
    if unknown and not a.all:
        print(f"asciiforge: unknown font '{a.font}' (try --list)", file=sys.stderr)
        return 2

    inner = a.width - 4 if a.border else a.width
    parts = []
    for f in fonts:
        if f not in avail:
            continue
        art = render(text, f, inner)
        if a.border:
            art = boxed(art)
        parts.append(f"[{f}]\n{art}" if a.all else art)
    out = "\n\n".join(parts)
    print(out)
    if a.output:
        with open(a.output, "w", encoding="utf-8") as fh:
            fh.write(out + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
