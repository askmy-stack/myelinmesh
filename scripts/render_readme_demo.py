from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# The README caps the asset at 840 CSS pixels wide and lets GitHub preserve its
# aspect ratio in narrower columns. Rendering at 2x keeps typography and rules
# sharp on high-density displays without changing layout.
WIDTH, HEIGHT = 1680, 944
DISPLAY_WIDTH, DISPLAY_HEIGHT = WIDTH // 2, HEIGHT // 2

BACKGROUND = "#07111F"
SURFACE = "#0C1728"
CARD = "#111F34"
CARD_ACTIVE = "#142941"
RULE = "#33445F"
TEXT = "#F5F8FF"
MUTED = "#B6C2D6"
SUBTLE = "#8190AA"
CYAN = "#62D7FF"
GREEN = "#68DBA5"
YELLOW = "#FFD166"
VIOLET = "#A99BFF"

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "docs" / "assets"

STAGES = ("sources", "normalize", "store", "retrieve")


def _font(size: int, *, mono: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        ("/System/Library/Fonts/SFNSMono.ttf" if mono else "/System/Library/Fonts/SFNS.ttf"),
        (
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
            if mono
            else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ),
    )
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


TITLE = _font(58)
SUBTITLE = _font(32)
EYEBROW = _font(30, mono=True)
CARD_TITLE = _font(38)
BODY = _font(30)
SMALL = _font(30)
MONO = _font(30, mono=True)


def _card(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    *,
    active: bool,
    accent: str,
) -> None:
    fill = CARD_ACTIVE if active else CARD
    outline = accent if active else RULE
    width = 4 if active else 2
    draw.rounded_rectangle(box, radius=28, fill=fill, outline=outline, width=width)


def _arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[int, int],
    end: tuple[int, int],
    *,
    active: bool,
    accent: str,
) -> None:
    color = accent if active else RULE
    width = 8 if active else 5
    draw.line((start, end), fill=color, width=width)
    x, y = end
    draw.polygon(((x, y), (x - 22, y - 14), (x - 22, y + 14)), fill=color)


def _stage_heading(
    draw: ImageDraw.ImageDraw,
    x: int,
    label: str,
    number: str,
    *,
    active: bool,
    accent: str,
) -> None:
    color = accent if active else SUBTLE
    draw.text((x, 245), number, font=EYEBROW, fill=color)
    draw.text((x + 62, 245), label, font=EYEBROW, fill=color)


def _source_card(
    draw: ImageDraw.ImageDraw,
    y: int,
    title: str,
    detail: str,
    *,
    active: bool,
) -> None:
    box = (72, y, 412, y + 118)
    _card(draw, box, active=active, accent=CYAN)
    draw.text((98, y + 25), title, font=BODY, fill=TEXT if active else MUTED)
    draw.text((98, y + 72), detail, font=SMALL, fill=MUTED if active else SUBTLE)


def _render(active_stage: str | None) -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((24, 24, WIDTH - 24, HEIGHT - 24), radius=36, fill=SURFACE)

    draw.text((72, 72), "MyelinMesh", font=TITLE, fill=TEXT)
    draw.text((72, 148), "Reliability evidence, connected.", font=SUBTITLE, fill=MUTED)
    draw.rounded_rectangle((1315, 78, 1598, 136), radius=18, fill=CARD, outline=RULE, width=2)
    draw.text((1456, 107), "v0.1 · LOCAL-FIRST", font=EYEBROW, fill=GREEN, anchor="mm")

    source_active = active_stage in (None, "sources")
    normalize_active = active_stage in (None, "normalize")
    store_active = active_stage in (None, "store")
    retrieve_active = active_stage in (None, "retrieve")

    _stage_heading(draw, 72, "SUPPORTED INPUTS", "01", active=source_active, accent=CYAN)
    _stage_heading(draw, 472, "NORMALIZE", "02", active=normalize_active, accent=VIOLET)
    _stage_heading(draw, 872, "LOCAL STORE", "03", active=store_active, accent=GREEN)
    _stage_heading(draw, 1252, "RETRIEVE", "04", active=retrieve_active, accent=YELLOW)

    _source_card(draw, 320, "Tool-Semantics", "tool changes", active=source_active)
    _source_card(draw, 462, "ImpactForge", "simulation tests", active=source_active)
    _source_card(draw, 604, "Parallax", "runtime incidents", active=source_active)

    normalize_box = (472, 320, 812, 722)
    _card(draw, normalize_box, active=normalize_active, accent=VIOLET)
    draw.text((508, 366), "Adapter", font=CARD_TITLE, fill=TEXT if normalize_active else MUTED)
    draw.text((508, 431), "producer JSON", font=SMALL, fill=MUTED)
    draw.line((508, 486, 776, 486), fill=RULE, width=2)
    draw.text((508, 526), "MER 0.1.0", font=CARD_TITLE, fill=VIOLET if normalize_active else MUTED)
    draw.text((508, 591), "schema validation", font=SMALL, fill=MUTED)
    draw.text((508, 638), "canonical SHA-256", font=SMALL, fill=MUTED)

    store_box = (872, 320, 1192, 722)
    _card(draw, store_box, active=store_active, accent=GREEN)
    draw.text((908, 366), ".myelinmesh/", font=MONO, fill=GREEN if store_active else MUTED)
    draw.line((908, 432, 1156, 432), fill=RULE, width=2)
    draw.text((908, 480), "records/", font=MONO, fill=TEXT if store_active else MUTED)
    draw.text((908, 526), "*.mer.json", font=MONO, fill=MUTED)
    draw.text((908, 596), "index.sqlite3", font=MONO, fill=TEXT if store_active else MUTED)
    draw.text((908, 657), "store.json", font=MONO, fill=MUTED)

    retrieve_box = (1252, 320, 1608, 722)
    _card(draw, retrieve_box, active=retrieve_active, accent=YELLOW)
    draw.text((1288, 366), "CLI", font=CARD_TITLE, fill=YELLOW if retrieve_active else MUTED)
    draw.text((1362, 376), "myelinmesh", font=MONO, fill=MUTED)
    commands = ("list", "show", "search", "stats")
    for index, command in enumerate(commands):
        y = 448 + (index * 61)
        draw.rounded_rectangle((1288, y, 1572, y + 45), radius=12, fill="#0A1423")
        draw.text((1312, y + 22), command, font=MONO, fill=TEXT, anchor="lm")

    _arrow(
        draw,
        (430, 521),
        (452, 521),
        active=source_active or normalize_active,
        accent=VIOLET,
    )
    _arrow(
        draw,
        (830, 521),
        (852, 521),
        active=normalize_active or store_active,
        accent=GREEN,
    )
    _arrow(
        draw,
        (1210, 521),
        (1232, 521),
        active=store_active or retrieve_active,
        accent=YELLOW,
    )

    draw.rounded_rectangle((72, 788, 1608, 872), radius=20, fill="#091422", outline=RULE, width=2)
    draw.text((106, 830), "Evidence, not proof", font=BODY, fill=TEXT, anchor="lm")
    draw.text(
        (1538, 830),
        "provenance · uncertainty · validation context",
        font=SMALL,
        fill=MUTED,
        anchor="rm",
    )
    return image


def main() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    frames = [_render(stage) for stage in STAGES]
    overview = _render(None)
    frames.append(overview)

    paletted = [
        frame.quantize(colors=64, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        for frame in frames
    ]

    gif_path = ASSET_DIR / "myelinmesh-evidence-flow.gif"
    paletted[0].save(
        gif_path,
        save_all=True,
        append_images=paletted[1:],
        duration=[1100, 1200, 1200, 1200, 1900],
        loop=0,
        optimize=True,
        disposal=2,
    )

    static_path = ASSET_DIR / "myelinmesh-evidence-flow-static.png"
    overview.save(static_path, optimize=True)
    print(
        f"{gif_path.relative_to(ROOT)} ({WIDTH}x{HEIGHT}; display {DISPLAY_WIDTH}x{DISPLAY_HEIGHT})"
    )
    print(static_path.relative_to(ROOT))


if __name__ == "__main__":
    main()
