from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ICON_SHEET = Path(r"C:\Users\kmkjk\.cursor\projects\f-bap-ce-compatch\assets\modpack_fixes_icons.jpg")
PREVIEW = Path(r"F:\bap ce compatch\workshop\preview.png")
OUT = ROOT / "images"
OUT.mkdir(parents=True, exist_ok=True)

FONT = r"C:\Windows\Fonts\BOOKOSB.TTF"
GOLD = (214, 182, 104, 255)
LINE = (214, 182, 104, 200)
RED = (150, 24, 24, 255)
WIDTH = 630


def header(text: str, name: str) -> None:
    big = ImageFont.truetype(FONT, 58)
    small = ImageFont.truetype(FONT, 36)
    img = Image.new("RGBA", (WIDTH, 80), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    x = 6
    baseline = 64
    for i, word in enumerate(text.split(" ")):
        if i:
            x += 14
        if word.lower() in {"of", "the", "it", "not"}:
            first, rest = "", word.upper()
        else:
            first, rest = word[0].upper(), word[1:].upper()
        if first:
            draw.text((x, baseline), first, font=big, fill=GOLD, anchor="ls")
            x += draw.textlength(first, font=big)
        if rest:
            draw.text((x + 2, baseline), rest, font=small, fill=GOLD, anchor="ls")
            x += draw.textlength(rest, font=small) + 2
    line_y = baseline - 13
    draw.line([(x + 16, line_y), (WIDTH - 6, line_y)], fill=LINE, width=2)
    img.save(OUT / f"header_{name}.png")


def disclaimer() -> None:
    title = ImageFont.truetype(FONT, 26)
    body = ImageFont.truetype(FONT, 17)
    img = Image.new("RGBA", (WIDTH, 112), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([1, 1, WIDTH - 2, 110], radius=6, fill=RED, outline=GOLD, width=2)
    draw.text((WIDTH // 2, 38), "DISCLAIMER: NOT A STANDALONE MOD", font=title, fill=GOLD, anchor="mm")
    draw.text(
        (WIDTH // 2, 78),
        "Use only inside Josheyer's Historical playset, loaded last.",
        font=body,
        fill=(240, 228, 200, 255),
        anchor="mm",
    )
    img.save(OUT / "disclaimer.png")


def split_box(left: str, right: str, name: str) -> None:
    font = ImageFont.truetype(FONT, 22)
    img = Image.new("RGBA", (WIDTH, 50), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([1, 1, WIDTH - 2, 48], outline=(190, 200, 210, 220), width=2)
    draw.text((16, 25), left, font=font, fill=GOLD, anchor="lm")
    draw.text((WIDTH - 16, 25), right, font=font, fill=GOLD, anchor="rm")
    draw.line([(WIDTH // 2, 10), (WIDTH // 2, 40)], fill=(190, 200, 210, 120), width=1)
    img.save(OUT / f"box_{name}.png")


def icons() -> None:
    sheet = Image.open(ICON_SHEET).convert("RGBA")
    w, h = sheet.size
    names = ["titles", "hair", "culture", "start"]
    inset = 0.02
    for i, name in enumerate(names):
        col, row = i % 2, i // 2
        box = (
            int((col * 0.5 + inset) * w),
            int((row * 0.5 + inset) * h),
            int((col * 0.5 + 0.5 - inset) * w),
            int((row * 0.5 + 0.5 - inset) * h),
        )
        crop = sheet.crop(box).resize((48, 48), Image.LANCZOS)
        mask = Image.new("L", (48, 48), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, 47, 47], fill=255)
        crop.putalpha(mask)
        crop.save(OUT / f"icon_{name}.png")


def banner() -> None:
    preview = Image.open(PREVIEW).convert("RGB")
    s = preview.width / 512
    band = preview.crop((0, int(150 * s), preview.width, int(355 * s)))
    band.resize((WIDTH, int(WIDTH * band.height / band.width)), Image.LANCZOS).save(
        OUT / "banner.jpg", quality=90
    )


if __name__ == "__main__":
    for text, name in [
        ("What It Is", "what"),
        ("Load Order", "load"),
        ("What It Fixes", "fixes"),
        ("What It Does Not Do", "not"),
        ("Compatibility", "compat"),
    ]:
        header(text, name)
    disclaimer()
    split_box("LOAD LAST", "REQUIRES THE PLAYSET", "load")
    icons()
    banner()
    print("ok", sorted(p.name for p in OUT.iterdir()))
