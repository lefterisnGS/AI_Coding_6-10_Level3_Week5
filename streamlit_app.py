import html
from collections import Counter
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="Our AI Team Showcase",
    page_icon="🤖",
    layout="wide",
)

BASE_DIR = Path(__file__).parent
KIDS_DIR = BASE_DIR / "kids"
ASSETS_DIR = BASE_DIR / "assets"
COURSE_FILE = BASE_DIR / "course.txt"

DEFAULT_COURSE = {
    "title": "Our AI Team Showcase",
    "subtitle": "A class team project",
    "hero_message": "We worked together to make one team webpage. Each child adds a few favorite things, and the page updates for the whole class.",
    "mascot_name": "Grandy",
    "mascot_message": "I am proud of this team. They used creativity, teamwork, and brave thinking.",
    "closing_message": "Thank you for visiting our class showcase.",
    "highlight_1": "We learned to ask AI clear questions.",
    "highlight_2": "We made creative ideas together.",
    "highlight_3": "We tried coding and simple web apps.",
    "highlight_4": "We learned how GitHub can save our changes.",
    "highlight_5": "We learned how Streamlit can show an app online.",
    "highlight_6": "We practiced speaking about our project.",
    "highlight_7": "We learned to be safe and kind online.",
    "highlight_8": "We worked as one team.",
}

DEFAULT_KID = {
    "name": "Friend",
    "emoji": "🌟",
    "favorite_color": "Blue",
    "favorite_1": "robots",
    "favorite_2": "games",
    "favorite_3": "drawing",
    "favorite_course_part": "making fun projects",
    "i_learned": "I learned that good questions help AI.",
    "dream_app": "a helpful app for kids",
    "superpower": "creative ideas",
    "order": 999,
}

COLOR_MAP = {
    "blue": "#60a5fa",
    "green": "#34d399",
    "pink": "#f472b6",
    "purple": "#a78bfa",
    "orange": "#fb923c",
    "red": "#f87171",
    "yellow": "#facc15",
    "teal": "#2dd4bf",
    "rainbow": "#8b5cf6",
}

def safe(value):
    return html.escape(str(value or ""))

def normalize_key(key):
    return str(key or "").strip().lower().replace(" ", "_").replace("-", "_")

def read_key_value_file(path):
    data = {}
    if not path.exists():
        return data

    text = path.read_text(encoding="utf-8")
    for raw_line in text.splitlines():
        line = raw_line.strip().replace("：", ":")
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[normalize_key(key)] = value.strip()

    return data

def pick_first(data, keys, default=""):
    for key in keys:
        value = str(data.get(key, "")).strip()
        if value:
            return value
    return default

def parse_int(value, default=999):
    try:
        return int(str(value).strip())
    except Exception:
        return default

def split_items(text):
    text = str(text or "").replace(";", ",").replace("|", ",")
    return [item.strip() for item in text.split(",") if item.strip()]

def dedupe(items):
    seen = set()
    result = []
    for item in items:
        clean = str(item).strip()
        key = clean.lower()
        if clean and key not in seen:
            seen.add(key)
            result.append(clean)
    return result

def collect_favorites(raw):
    items = []
    for key in ("favorite_things", "favorites", "likes"):
        items.extend(split_items(raw.get(key, "")))
    for i in range(1, 6):
        items.extend(split_items(raw.get(f"favorite_{i}", "")))
    return dedupe(items)

def load_course():
    course = DEFAULT_COURSE.copy()
    course.update(read_key_value_file(COURSE_FILE))
    highlights = []
    for i in range(1, 13):
        value = str(course.get(f"highlight_{i}", "")).strip()
        if value:
            highlights.append(value)
    course["highlights"] = highlights
    return course

def normalize_kid(raw, filename):
    kid = DEFAULT_KID.copy()
    kid["name"] = pick_first(raw, ["name", "child_name", "student_name"], kid["name"])
    kid["emoji"] = pick_first(raw, ["emoji"], kid["emoji"])
    kid["favorite_color"] = pick_first(raw, ["favorite_color", "color"], kid["favorite_color"])
    favorites = collect_favorites(raw)
    if not favorites:
        favorites = [
            kid["favorite_1"],
            kid["favorite_2"],
            kid["favorite_3"],
        ]
    kid["favorite_list"] = favorites
    kid["favorite_course_part"] = pick_first(
        raw,
        ["favorite_course_part", "best_part", "course_part"],
        kid["favorite_course_part"],
    )
    kid["i_learned"] = pick_first(raw, ["i_learned", "learned"], kid["i_learned"])
    kid["dream_app"] = pick_first(raw, ["dream_app", "app_idea"], kid["dream_app"])
    kid["superpower"] = pick_first(raw, ["superpower", "strength"], kid["superpower"])
    kid["order"] = parse_int(pick_first(raw, ["order"], "999"), 999)
    kid["file_name"] = filename
    return kid

def load_kids():
    kids = []
    if not KIDS_DIR.exists():
        return kids

    for path in sorted(KIDS_DIR.glob("*.txt")):
        if path.name.startswith("_") or path.name.startswith("."):
            continue
        raw = read_key_value_file(path)
        kids.append(normalize_kid(raw, path.name))

    kids.sort(key=lambda item: (item.get("order", 999), item.get("name", "").lower()))
    return kids

def color_for(name):
    return COLOR_MAP.get(str(name or "").strip().lower(), "#8b5cf6")

def top_favorites(kids):
    counter = Counter()
    for kid in kids:
        for item in kid.get("favorite_list", []):
            counter[item.title()] += 1
    return counter.most_common(12)

def total_favorites(kids):
    total = 0
    for kid in kids:
        total += len(kid.get("favorite_list", []))
    return total

def show_optional_image(filename):
    path = ASSETS_DIR / filename
    if path.exists():
        st.image(str(path), use_column_width=True)
        return True
    return False

def stat_box(label, value):
    return f"""
    <div class="stat-box">
        <div class="stat-number">{safe(value)}</div>
        <div class="stat-label">{safe(label)}</div>
    </div>
    """

def build_kid_card(kid):
    accent = color_for(kid.get("favorite_color", ""))
    chips = "".join(
        f"<span class='mini-chip'>{safe(item)}</span>"
        for item in kid.get("favorite_list", [])
    )
    return f"""
    <div class="kid-card" style="border-top: 8px solid {accent};">
        <div class="kid-top">
            <div class="emoji-bubble">{safe(kid.get("emoji", "🌟"))}</div>
            <div>
                <div class="kid-name">{safe(kid.get("name", "Friend"))}</div>
                <div class="kid-sub">Favorite color: {safe(kid.get("favorite_color", "Blue"))}</div>
            </div>
        </div>
        <div class="line"><strong>I like:</strong> {safe(", ".join(kid.get("favorite_list", [])))}</div>
        <div class="line"><strong>Best course part:</strong> {safe(kid.get("favorite_course_part", ""))}</div>
        <div class="line"><strong>I learned:</strong> {safe(kid.get("i_learned", ""))}</div>
        <div class="line"><strong>Dream app:</strong> {safe(kid.get("dream_app", ""))}</div>
        <div class="line"><strong>My superpower:</strong> {safe(kid.get("superpower", ""))}</div>
        <div class="chip-row">{chips}</div>
    </div>
    """

st.markdown(
    """
    <style>
    #MainMenu, header, footer {
        visibility: hidden;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 1rem;
        padding-bottom: 4rem;
    }

    .hero-box {
        background: linear-gradient(135deg, #7c3aed 0%, #2563eb 50%, #06b6d4 100%);
        color: white;
        border-radius: 30px;
        padding: 28px;
        box-shadow: 0 18px 40px rgba(37, 99, 235, 0.20);
    }

    .eyebrow {
        display: inline-block;
        padding: 10px 16px;
        border-radius: 999px;
        background: rgba(255,255,255,0.18);
        font-size: 1rem;
        font-weight: 900;
        margin-bottom: 12px;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 900;
        line-height: 1.05;
        margin: 0;
    }

    .hero-subtitle {
        font-size: 1.4rem;
        font-weight: 800;
        margin-top: 10px;
    }

    .hero-text {
        font-size: 1.15rem;
        line-height: 1.8;
        margin-top: 14px;
    }

    .section-box {
        background: white;
        border-radius: 26px;
        padding: 24px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
        margin-top: 16px;
    }

    .section-box h2 {
        margin-top: 0;
        font-size: 2rem;
    }

    .placeholder-box {
        background: linear-gradient(135deg, #fdf2f8, #eff6ff);
        border: 2px dashed #c4b5fd;
        border-radius: 24px;
        min-height: 260px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 24px;
        font-size: 1.15rem;
        font-weight: 800;
        color: #334155;
    }

    .stat-box {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 22px;
        padding: 18px;
        text-align: center;
        border: 1px solid #e5e7eb;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.06);
    }

    .stat-number {
        font-size: 2.2rem;
        font-weight: 900;
        color: #1d4ed8;
    }

    .stat-label {
        font-size: 1rem;
        font-weight: 800;
        color: #334155;
    }

    .big-chip-wrap,
    .chip-row,
    .learn-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 12px;
    }

    .big-chip {
        display: inline-flex;
        align-items: center;
        padding: 10px 14px;
        border-radius: 999px;
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        color: #1e3a8a;
        font-weight: 900;
    }

    .mini-chip {
        display: inline-flex;
        align-items: center;
        padding: 8px 12px;
        border-radius: 999px;
        background: #f5f3ff;
        border: 1px solid #ddd6fe;
        color: #6d28d9;
        font-weight: 800;
        font-size: 0.95rem;
    }

    .learn-card {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 20px;
        border: 1px solid #e5e7eb;
        padding: 16px;
        min-width: 220px;
        flex: 1 1 220px;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
    }

    .learn-icon {
        font-size: 1.6rem;
        margin-bottom: 8px;
    }

    .learn-text {
        font-size: 1rem;
        font-weight: 800;
        line-height: 1.7;
        color: #1f2937;
    }

    .kid-card {
        background: white;
        border-radius: 24px;
        padding: 20px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
        margin-bottom: 1rem;
        min-height: 360px;
    }

    .kid-top {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 10px;
    }

    .emoji-bubble {
        width: 58px;
        height: 58px;
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #fef3c7, #dbeafe);
        font-size: 1.8rem;
    }

    .kid-name {
        font-size: 1.6rem;
        font-weight: 900;
        color: #111827;
    }

    .kid-sub {
        font-size: 0.98rem;
        font-weight: 800;
        color: #475569;
    }

    .line {
        margin-top: 10px;
        font-size: 1rem;
        line-height: 1.7;
        color: #1f2937;
    }

    .footer-box {
        background: linear-gradient(135deg, #0f172a, #1d4ed8);
        color: white;
        border-radius: 28px;
        padding: 28px;
        margin-top: 18px;
        text-align: center;
    }

    .footer-box h2 {
        margin: 0;
        font-size: 2rem;
    }

    .footer-box p {
        margin-top: 10px;
        font-size: 1.1rem;
        line-height: 1.7;
    }

    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.2rem;
        }

        .kid-card {
            min-height: auto;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

course = load_course()
kids = load_kids()
favorite_items = top_favorites(kids)

left_col, right_col = st.columns([1.3, 1], gap="large")

with left_col:
    st.markdown(
        f"""
        <div class="hero-box">
            <div class="eyebrow">TEAM PROJECT • GITHUB + STREAMLIT</div>
            <div class="hero-title">{safe(course.get("title", ""))}</div>
            <div class="hero-subtitle">{safe(course.get("subtitle", ""))}</div>
            <div class="hero-text">{safe(course.get("hero_message", ""))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right_col:
    if not show_optional_image("hero-banner.png"):
        st.markdown(
            """
            <div class="placeholder-box">
                Add assets/hero-banner.png here
            </div>
            """,
            unsafe_allow_html=True,
        )

stat1, stat2, stat3 = st.columns(3)
with stat1:
    st.markdown(stat_box("Team members", len(kids)), unsafe_allow_html=True)
with stat2:
    st.markdown(stat_box("Favorite ideas", total_favorites(kids)), unsafe_allow_html=True)
with stat3:
    st.markdown(stat_box("Top topics", len(favorite_items)), unsafe_allow_html=True)

chips_html = "".join(
    f"<span class='big-chip'>{safe(item)} ({count})</span>"
    for item, count in favorite_items
)

if not chips_html:
    chips_html = "<span class='big-chip'>Add favorite things in student files</span>"

st.markdown(
    f"""
    <div class="section-box">
        <h2>Our Favorite Things</h2>
        <div class="big-chip-wrap">{chips_html}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-box">
        <h2>Meet Our Team</h2>
        <p>Each child edits only one tiny file in the kids folder. The app reads the files and updates the page.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if kids:
    cols = st.columns(3)
    for index, kid in enumerate(kids):
        with cols[index % 3]:
            st.markdown(build_kid_card(kid), unsafe_allow_html=True)
else:
    st.info("No student files found yet. Add files inside the kids folder.")

learn_html = ""
icons = ["💬", "🎨", "🐍", "🌐", "🤝", "🎤", "🚀", "🛡️", "💡", "🧩"]
for index, item in enumerate(course.get("highlights", [])):
    learn_html += f"""
    <div class="learn-card">
        <div class="learn-icon">{icons[index % len(icons)]}</div>
        <div class="learn-text">{safe(item)}</div>
    </div>
    """

st.markdown(
    f"""
    <div class="section-box">
        <h2>What We Learned</h2>
        <div class="learn-grid">{learn_html}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

mascot_col, speech_col = st.columns([1, 1.3], gap="large")

with mascot_col:
    if not show_optional_image("grandy.png"):
        st.markdown(
            """
            <div class="placeholder-box">
                Add assets/grandy.png here
            </div>
            """,
            unsafe_allow_html=True,
        )

with speech_col:
    st.markdown(
        f"""
        <div class="section-box">
            <h2>{safe(course.get("mascot_name", "Grandy"))} says...</h2>
            <p>{safe(course.get("mascot_message", ""))}</p>
            <p>{safe(course.get("closing_message", ""))}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

if not show_optional_image("team-stickers.png"):
    st.markdown(
        """
        <div class="section-box">
            <h2>Sticker Area</h2>
            <div class="placeholder-box">Add assets/team-stickers.png here</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="footer-box">
        <h2>We are young creators and future builders 🚀</h2>
        <p>Thank you for visiting our class showcase.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.button("Celebrate our team 🎉"):
    st.balloons()

with st.expander("Teacher helper"):
    st.write("Loaded files:", [kid.get("file_name", "") for kid in kids])
    st.write("Missing images are okay while you are still building the project.")