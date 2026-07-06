from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = ["arialbd.ttf" if bold else "arial.ttf", "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def text_center(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, fill: str, size: int, bold: bool = False) -> None:
    selected = font(size, bold)
    bbox = draw.multiline_textbbox((0, 0), text, font=selected, spacing=6, align="center")
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    x = box[0] + (box[2] - box[0] - width) / 2
    y = box[1] + (box[3] - box[1] - height) / 2
    draw.multiline_text((x, y), text, font=selected, fill=fill, spacing=6, align="center")


def write_svg() -> None:
    svg = """<svg width="1200" height="620" viewBox="0 0 1200 620" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="panel" x1="80" y1="80" x2="1120" y2="540" gradientUnits="userSpaceOnUse">
      <stop stop-color="#F7FBFF"/>
      <stop offset="1" stop-color="#F6FFF8"/>
    </linearGradient>
    <linearGradient id="core" x1="470" y1="190" x2="730" y2="430" gradientUnits="userSpaceOnUse">
      <stop stop-color="#0E7C86"/>
      <stop offset="1" stop-color="#2A9D55"/>
    </linearGradient>
    <filter id="shadow" x="40" y="40" width="1120" height="540" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
      <feDropShadow dx="0" dy="18" stdDeviation="22" flood-color="#1F2937" flood-opacity="0.16"/>
    </filter>
    <style>
      .title{font:700 52px Arial, sans-serif;fill:#0F172A}
      .subtitle{font:400 22px Arial, sans-serif;fill:#475569}
      .label{font:700 20px Arial, sans-serif;fill:#0F172A}
      .small{font:400 16px Arial, sans-serif;fill:#475569}
      .mono{font:600 17px Consolas, monospace;fill:#0F766E}
      .node{font:700 18px Arial, sans-serif;fill:#0F172A}
    </style>
  </defs>
  <rect width="1200" height="620" rx="34" fill="#FFFFFF"/>
  <g filter="url(#shadow)">
    <rect x="70" y="70" width="1060" height="480" rx="28" fill="url(#panel)" stroke="#D8E2EA"/>
  </g>
  <text x="120" y="145" class="title">CAD Agent Skill</text>
  <text x="122" y="184" class="subtitle">A privacy-first workflow layer for agent-assisted CAD planning.</text>

  <rect x="120" y="245" width="245" height="170" rx="18" fill="#FFFFFF" stroke="#CBD5E1"/>
  <text x="148" y="288" class="label">Text request</text>
  <text x="148" y="322" class="small">Natural-language design intent</text>
  <text x="148" y="358" class="mono">"Create a modular</text>
  <text x="148" y="384" class="mono">industrial panel..."</text>

  <path d="M386 330 H470" stroke="#94A3B8" stroke-width="4" stroke-linecap="round"/>
  <path d="M458 318 L474 330 L458 342" stroke="#94A3B8" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>

  <rect x="475" y="220" width="250" height="220" rx="26" fill="url(#core)"/>
  <text x="520" y="284" fill="#FFFFFF" style="font:700 31px Arial, sans-serif">Workflow</text>
  <text x="544" y="324" fill="#DDF8EE" style="font:700 31px Arial, sans-serif">Skill</text>
  <rect x="520" y="355" width="160" height="38" rx="19" fill="#FFFFFF" fill-opacity="0.18" stroke="#E5FFF4" stroke-opacity="0.45"/>
  <text x="555" y="381" fill="#FFFFFF" style="font:700 16px Arial, sans-serif">agent guardrails</text>

  <path d="M730 330 H814" stroke="#94A3B8" stroke-width="4" stroke-linecap="round"/>
  <path d="M802 318 L818 330 L802 342" stroke="#94A3B8" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>

  <rect x="835" y="245" width="245" height="170" rx="18" fill="#FFFFFF" stroke="#CBD5E1"/>
  <text x="863" y="288" class="label">Validated handoff</text>
  <text x="863" y="322" class="small">Structured CAD artifacts</text>
  <path d="M875 360 h120 v36 h-120 z" stroke="#0E7C86" stroke-width="3" fill="#E8FAF5"/>
  <path d="M904 360 v36M935 360 v36M966 360 v36" stroke="#0E7C86" stroke-width="2"/>
  <circle cx="1018" cy="378" r="17" fill="#2A9D55"/>
  <path d="M1009 378 l6 6 l13 -15" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>

  <g transform="translate(158 470)">
    <rect x="0" y="0" width="130" height="42" rx="21" fill="#E0F2FE"/><text x="33" y="27" class="node">CAD IR</text>
    <rect x="172" y="0" width="130" height="42" rx="21" fill="#ECFDF5"/><text x="198" y="27" class="node">Catalog</text>
    <rect x="344" y="0" width="130" height="42" rx="21" fill="#FFF7ED"/><text x="367" y="27" class="node">Plan</text>
    <rect x="516" y="0" width="130" height="42" rx="21" fill="#F1F5F9"/><text x="539" y="27" class="node">Graph</text>
    <rect x="688" y="0" width="150" height="42" rx="21" fill="#F0FDF4"/><text x="717" y="27" class="node">Validate</text>
  </g>
</svg>
"""
    (ASSET_DIR / "cad-agent-skill-hero.svg").write_text(svg, encoding="utf-8")


def draw_arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color: str) -> None:
    draw.line([start, end], fill=color, width=4)
    x, y = end
    draw.polygon([(x, y), (x - 14, y - 8), (x - 14, y + 8)], fill=color)


def make_demo_frame(active: int) -> Image.Image:
    width, height = 960, 420
    image = Image.new("RGB", (width, height), "#F8FAFC")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((24, 24, width - 24, height - 24), radius=28, fill="#FFFFFF", outline="#D7E0EA", width=2)
    draw.text((54, 54), "CAD Agent Skill", font=font(30, True), fill="#0F172A")
    draw.text((54, 92), "Text intent -> structured CAD planning -> validated handoff", font=font(17), fill="#64748B")

    steps = [
        ("Text", "natural-language\nCAD request", "#E0F2FE"),
        ("IR", "requirements\nconstraints", "#ECFDF5"),
        ("Catalog", "candidate\ncomponents", "#FFF7ED"),
        ("Plan", "placement\nrows", "#F1F5F9"),
        ("Validate", "review gaps\nand checks", "#F0FDF4"),
    ]
    left, top, gap, card_w, card_h = 58, 155, 22, 156, 138
    for index, (title, body, color) in enumerate(steps):
        x = left + index * (card_w + gap)
        y = top
        fill = color if index <= active else "#F8FAFC"
        outline = "#0E7C86" if index == active else "#CBD5E1"
        width_line = 4 if index == active else 2
        draw.rounded_rectangle((x, y, x + card_w, y + card_h), radius=18, fill=fill, outline=outline, width=width_line)
        text_center(draw, (x + 12, y + 16, x + card_w - 12, y + 54), title, "#0F172A", 19, True)
        text_center(draw, (x + 14, y + 60, x + card_w - 14, y + card_h - 18), body, "#475569", 15)
        if index < len(steps) - 1:
            arrow_color = "#0E7C86" if index < active else "#CBD5E1"
            draw_arrow(draw, (x + card_w + 5, y + 69), (x + card_w + gap - 6, y + 69), arrow_color)

    preview_x, preview_y = 665, 304
    draw.rounded_rectangle((preview_x, preview_y, preview_x + 230, preview_y + 62), radius=16, fill="#0F172A")
    status = ["parsing request", "normalizing IR", "ranking catalog", "solving placement", "validation passed"][active]
    draw.text((preview_x + 20, preview_y + 22), f"agent: {status}", font=font(17, True), fill="#DDF8EE")
    return image


def write_gif() -> None:
    frames: list[Image.Image] = []
    for active in range(5):
        for _ in range(6):
            frames.append(make_demo_frame(active))
    frames[0].save(
        ASSET_DIR / "cad-agent-skill-demo.gif",
        save_all=True,
        append_images=frames[1:],
        duration=120,
        loop=0,
        optimize=True,
    )


def main() -> None:
    ASSET_DIR.mkdir(exist_ok=True)
    write_svg()
    write_gif()
    print(f"Wrote assets to {ASSET_DIR}")


if __name__ == "__main__":
    main()
