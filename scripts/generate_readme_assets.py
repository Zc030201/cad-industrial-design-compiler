from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets"
CANVAS = (960, 420)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path(r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\simhei.ttf"),
        Path(r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"),
    ]
    names = ["DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"]
    for candidate in candidates:
        if candidate.exists():
            try:
                return ImageFont.truetype(str(candidate), size)
            except OSError:
                pass
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


def svg_text(locale: str) -> dict[str, str]:
    if locale == "zh":
        return {
            "file": "cad-agent-skill-hero.zh-CN.svg",
            "subtitle": "面向 CAD Agent 的隐私优先工作流技能层",
            "left_title": "文本需求",
            "left_desc": "自然语言设计意图",
            "left_line_1": "创建模块化",
            "left_line_2": "工业面板...",
            "core_top": "工作流",
            "core_bottom": "Skill",
            "guardrails": "Agent 约束层",
            "right_title": "验证交付",
            "right_desc": "结构化 CAD 产物",
            "catalog": "组件目录",
            "plan": "放置规划",
            "graph": "执行图",
            "validate": "验证",
        }
    return {
        "file": "cad-agent-skill-hero.svg",
        "subtitle": "A privacy-first workflow layer for agent-assisted CAD planning.",
        "left_title": "Text request",
        "left_desc": "Natural-language design intent",
        "left_line_1": "Create a modular",
        "left_line_2": "industrial panel...",
        "core_top": "Workflow",
        "core_bottom": "Skill",
        "guardrails": "agent guardrails",
        "right_title": "Validated handoff",
        "right_desc": "Structured CAD artifacts",
        "catalog": "Catalog",
        "plan": "Plan",
        "graph": "Graph",
        "validate": "Validate",
    }


def write_svg(locale: str) -> None:
    text = svg_text(locale)
    svg = f"""<svg width="960" height="420" viewBox="0 0 960 420" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="panel" x1="24" y1="24" x2="936" y2="396" gradientUnits="userSpaceOnUse">
      <stop stop-color="#F7FBFF"/>
      <stop offset="1" stop-color="#F6FFF8"/>
    </linearGradient>
    <linearGradient id="core" x1="370" y1="145" x2="590" y2="315" gradientUnits="userSpaceOnUse">
      <stop stop-color="#0E7C86"/>
      <stop offset="1" stop-color="#2A9D55"/>
    </linearGradient>
    <style>
      .title{{font:700 38px Arial, 'Microsoft YaHei', sans-serif;fill:#0F172A}}
      .subtitle{{font:400 18px Arial, 'Microsoft YaHei', sans-serif;fill:#475569}}
      .label{{font:700 19px Arial, 'Microsoft YaHei', sans-serif;fill:#0F172A}}
      .small{{font:400 15px Arial, 'Microsoft YaHei', sans-serif;fill:#475569}}
      .mono{{font:600 15px Consolas, 'Microsoft YaHei', monospace;fill:#0F766E}}
      .node{{font:700 16px Arial, 'Microsoft YaHei', sans-serif;fill:#0F172A}}
    </style>
  </defs>
  <rect width="960" height="420" rx="28" fill="#FFFFFF"/>
  <rect x="24" y="24" width="912" height="372" rx="26" fill="url(#panel)" stroke="#D8E2EA"/>
  <text x="54" y="82" class="title">CAD Agent Skill</text>
  <text x="56" y="112" class="subtitle">{text["subtitle"]}</text>

  <rect x="58" y="156" width="210" height="132" rx="18" fill="#FFFFFF" stroke="#CBD5E1"/>
  <text x="82" y="194" class="label">{text["left_title"]}</text>
  <text x="82" y="225" class="small">{text["left_desc"]}</text>
  <text x="82" y="253" class="mono">"{text["left_line_1"]}</text>
  <text x="82" y="276" class="mono">{text["left_line_2"]}"</text>

  <path d="M286 222 H365" stroke="#94A3B8" stroke-width="4" stroke-linecap="round"/>
  <path d="M353 210 L369 222 L353 234" stroke="#94A3B8" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>

  <rect x="370" y="140" width="220" height="166" rx="26" fill="url(#core)"/>
  <text x="480" y="200" text-anchor="middle" fill="#FFFFFF" style="font:700 28px Arial, 'Microsoft YaHei', sans-serif">{text["core_top"]}</text>
  <text x="480" y="237" text-anchor="middle" fill="#DDF8EE" style="font:700 28px Arial, 'Microsoft YaHei', sans-serif">{text["core_bottom"]}</text>
  <rect x="394" y="258" width="172" height="36" rx="18" fill="#FFFFFF" fill-opacity="0.18" stroke="#E5FFF4" stroke-opacity="0.45"/>
  <text x="480" y="281" text-anchor="middle" fill="#FFFFFF" style="font:700 15px Arial, 'Microsoft YaHei', sans-serif">{text["guardrails"]}</text>

  <path d="M596 222 H675" stroke="#94A3B8" stroke-width="4" stroke-linecap="round"/>
  <path d="M663 210 L679 222 L663 234" stroke="#94A3B8" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>

  <rect x="692" y="156" width="210" height="132" rx="18" fill="#FFFFFF" stroke="#CBD5E1"/>
  <text x="716" y="194" class="label">{text["right_title"]}</text>
  <text x="716" y="225" class="small">{text["right_desc"]}</text>
  <path d="M735 252 h96 v26 h-96 z" stroke="#0E7C86" stroke-width="3" fill="#E8FAF5"/>
  <path d="M759 252 v26M784 252 v26M809 252 v26" stroke="#0E7C86" stroke-width="2"/>
  <circle cx="855" cy="265" r="15" fill="#2A9D55"/>
  <path d="M847 265 l6 6 l12 -14" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>

  <g transform="translate(82 332)">
    <rect x="0" y="0" width="118" height="38" rx="19" fill="#E0F2FE"/><text x="35" y="25" class="node">CAD IR</text>
    <rect x="150" y="0" width="118" height="38" rx="19" fill="#ECFDF5"/><text x="178" y="25" class="node">{text["catalog"]}</text>
    <rect x="300" y="0" width="118" height="38" rx="19" fill="#FFF7ED"/><text x="328" y="25" class="node">{text["plan"]}</text>
    <rect x="450" y="0" width="118" height="38" rx="19" fill="#F1F5F9"/><text x="478" y="25" class="node">{text["graph"]}</text>
    <rect x="600" y="0" width="130" height="38" rx="19" fill="#F0FDF4"/><text x="630" y="25" class="node">{text["validate"]}</text>
  </g>
</svg>
"""
    (ASSET_DIR / text["file"]).write_text(svg, encoding="utf-8")


def draw_arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color: str) -> None:
    draw.line([start, end], fill=color, width=4)
    x, y = end
    draw.polygon([(x, y), (x - 14, y - 8), (x - 14, y + 8)], fill=color)


def frame_text(locale: str) -> dict:
    if locale == "zh":
        return {
            "file": "cad-agent-skill-demo.zh-CN.gif",
            "subtitle": "文本意图 -> 结构化 CAD 规划 -> 验证交付",
            "steps": [
                ("文本", "自然语言\nCAD 需求", "#E0F2FE"),
                ("IR", "需求\n约束", "#ECFDF5"),
                ("目录", "候选\n组件", "#FFF7ED"),
                ("规划", "放置\n记录", "#F1F5F9"),
                ("验证", "复核项\n和检查", "#F0FDF4"),
            ],
            "statuses": ["解析需求", "规范化 IR", "检索组件", "求解放置", "验证通过"],
            "agent": "agent",
        }
    return {
        "file": "cad-agent-skill-demo.gif",
        "subtitle": "Text intent -> structured CAD planning -> validated handoff",
        "steps": [
            ("Text", "natural-language\nCAD request", "#E0F2FE"),
            ("IR", "requirements\nconstraints", "#ECFDF5"),
            ("Catalog", "candidate\ncomponents", "#FFF7ED"),
            ("Plan", "placement\nrows", "#F1F5F9"),
            ("Validate", "review gaps\nand checks", "#F0FDF4"),
        ],
        "statuses": ["parsing request", "normalizing IR", "ranking catalog", "solving placement", "validation passed"],
        "agent": "agent",
    }


def make_demo_frame(active: int, locale: str) -> Image.Image:
    width, height = CANVAS
    text = frame_text(locale)
    image = Image.new("RGB", (width, height), "#F8FAFC")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((24, 24, width - 24, height - 24), radius=28, fill="#FFFFFF", outline="#D7E0EA", width=2)
    draw.text((54, 54), "CAD Agent Skill", font=font(30, True), fill="#0F172A")
    draw.text((54, 92), text["subtitle"], font=font(17), fill="#64748B")

    left, top, gap, card_w, card_h = 58, 155, 22, 156, 138
    for index, (title, body, color) in enumerate(text["steps"]):
        x = left + index * (card_w + gap)
        y = top
        fill = color if index <= active else "#F8FAFC"
        outline = "#0E7C86" if index == active else "#CBD5E1"
        width_line = 4 if index == active else 2
        draw.rounded_rectangle((x, y, x + card_w, y + card_h), radius=18, fill=fill, outline=outline, width=width_line)
        text_center(draw, (x + 12, y + 16, x + card_w - 12, y + 54), title, "#0F172A", 19, True)
        text_center(draw, (x + 14, y + 60, x + card_w - 14, y + card_h - 18), body, "#475569", 15)
        if index < len(text["steps"]) - 1:
            arrow_color = "#0E7C86" if index < active else "#CBD5E1"
            draw_arrow(draw, (x + card_w + 5, y + 69), (x + card_w + gap - 6, y + 69), arrow_color)

    preview_x, preview_y = 665, 304
    draw.rounded_rectangle((preview_x, preview_y, preview_x + 230, preview_y + 62), radius=16, fill="#0F172A")
    status = text["statuses"][active]
    draw.text((preview_x + 20, preview_y + 22), f'{text["agent"]}: {status}', font=font(17, True), fill="#DDF8EE")
    return image


def write_gif(locale: str) -> None:
    frames: list[Image.Image] = []
    text = frame_text(locale)
    for active in range(5):
        for _ in range(6):
            frames.append(make_demo_frame(active, locale))
    frames[0].save(
        ASSET_DIR / text["file"],
        save_all=True,
        append_images=frames[1:],
        duration=120,
        loop=0,
        optimize=True,
    )


def main() -> None:
    ASSET_DIR.mkdir(exist_ok=True)
    for locale in ["en", "zh"]:
        write_svg(locale)
        write_gif(locale)
    print(f"Wrote assets to {ASSET_DIR}")


if __name__ == "__main__":
    main()
