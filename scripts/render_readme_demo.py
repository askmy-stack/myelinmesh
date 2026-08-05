from __future__ import annotations

from pathlib import Path
from typing import TypedDict

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 840, 472
BACKGROUND = "#0B1020"
PANEL = "#11182B"
DIVIDER = "#2A3855"
TEXT = "#F2F6FF"
MUTED = "#AEBBD2"
CYAN = "#70D6FF"
GREEN = "#62D196"
YELLOW = "#FFD166"

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "docs" / "assets"


class Scene(TypedDict):
    step: str
    command: tuple[str, ...]
    result: tuple[str, str]
    accent: str


SCENES: tuple[Scene, ...] = (
    {
        "step": "01  INITIALIZE",
        "command": ("$ myelinmesh init .myelinmesh",),
        "result": ("Store ready", ".myelinmesh · local JSON + SQLite index"),
        "accent": CYAN,
    },
    {
        "step": "02  INGEST",
        "command": (
            "$ myelinmesh ingest",
            "  examples/records/tool-semantic-drift.mer.json",
        ),
        "result": ("mer-demo-tool-drift-001", "validated · provenance hashed · indexed"),
        "accent": GREEN,
    },
    {
        "step": "03  SEARCH",
        "command": ('$ myelinmesh search "semantic drift"',),
        "result": (
            "mer-demo-tool-drift-001",
            "critical · confidence 0.91 · tool-semantics",
        ),
        "accent": YELLOW,
    },
)


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        "/System/Library/Fonts/Menlo.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    )
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


FONT = _font(20)
SMALL = _font(16)
LABEL = _font(15)


def render_scene(scene: Scene, position: int) -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((18, 18, WIDTH - 18, HEIGHT - 18), radius=18, fill=PANEL)

    draw.ellipse((43, 42, 57, 56), fill="#FF6B65")
    draw.ellipse((67, 42, 81, 56), fill="#F6C453")
    draw.ellipse((91, 42, 105, 56), fill="#54C878")
    draw.text(
        (WIDTH // 2, 51), "MyelinMesh · evidence workflow", font=LABEL, fill=MUTED, anchor="mm"
    )
    draw.line((42, 78, WIDTH - 42, 78), fill=DIVIDER, width=2)

    accent = str(scene["accent"])
    draw.rounded_rectangle((43, 103, 222, 137), radius=8, fill="#19243C", outline=accent, width=2)
    draw.text((57, 120), str(scene["step"]), font=LABEL, fill=accent, anchor="lm")

    for step in range(len(SCENES)):
        x1 = 632 + (step * 52)
        fill = accent if step == position else DIVIDER
        draw.rounded_rectangle((x1, 116, x1 + 38, 123), radius=3, fill=fill)

    y = 177
    for line in scene["command"]:
        draw.text((48, y), str(line), font=FONT, fill=CYAN)
        y += 35

    result_top = 279
    draw.rounded_rectangle(
        (43, result_top, WIDTH - 43, 398), radius=12, fill="#0D1426", outline=DIVIDER, width=2
    )
    result_title, result_detail = scene["result"]
    draw.text((65, result_top + 38), str(result_title), font=FONT, fill=accent)
    draw.text((65, result_top + 78), str(result_detail), font=SMALL, fill=TEXT)
    draw.text(
        (WIDTH - 44, HEIGHT - 42),
        "local-first · evidence, not proof",
        font=LABEL,
        fill=MUTED,
        anchor="rm",
    )
    return image


def main() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    frames = [render_scene(scene, index) for index, scene in enumerate(SCENES)]
    paletted = [
        frame.quantize(colors=48, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        for frame in frames
    ]

    gif_path = ASSET_DIR / "myelinmesh-cli-demo.gif"
    paletted[0].save(
        gif_path,
        save_all=True,
        append_images=paletted[1:],
        duration=[1900, 2300, 2500],
        loop=0,
        optimize=True,
        disposal=2,
    )

    static_path = ASSET_DIR / "myelinmesh-cli-demo-static.png"
    frames[-1].save(static_path, optimize=True)
    print(gif_path.relative_to(ROOT))
    print(static_path.relative_to(ROOT))


if __name__ == "__main__":
    main()
