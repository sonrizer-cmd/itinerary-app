import html
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Sylva Weekend Itinerary",
    page_icon="🏔️",
    layout="centered"
)

# -------------------------
# Custom styling
# -------------------------

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #f7f4ed 0%, #eef4ef 45%, #f7f4ed 100%);
    }

    .hero {
        background: linear-gradient(135deg, #244c3a 0%, #3f7d5d 55%, #d9a441 100%);
        padding: 1.6rem;
        border-radius: 24px;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    }

    .hero h1 {
        color: white;
        margin-bottom: 0.2rem;
        font-size: 2.1rem;
    }

    .hero p {
        color: #f7f4ed;
        font-size: 1.05rem;
        margin-bottom: 0;
    }

    .quick-note {
        background: #fff8e6;
        border-left: 5px solid #d9a441;
        padding: 0.9rem 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }

    .section-title {
        color: #244c3a;
        margin-top: 1rem;
        margin-bottom: 0.6rem;
    }

    .day-note {
        background: rgba(255, 255, 255, 0.72);
        border: 1px solid rgba(36, 76, 58, 0.10);
        padding: 0.85rem 1rem;
        border-radius: 16px;
        margin-bottom: 1rem;
        color: #35453b;
        font-size: 0.95rem;
        box-shadow: 0 3px 12px rgba(0,0,0,0.035);
    }

    .timeline {
        position: relative;
        margin-left: 0.35rem;
        padding-left: 1.25rem;
        border-left: 3px solid rgba(36, 76, 58, 0.22);
    }

    .timeline-item {
        position: relative;
        margin-bottom: 0.95rem;
        padding-bottom: 0.15rem;
    }

    .timeline-dot {
        position: absolute;
        left: -1.63rem;
        top: 0.35rem;
        width: 0.85rem;
        height: 0.85rem;
        background: #d9a441;
        border: 3px solid #f7f4ed;
        border-radius: 50%;
        box-shadow: 0 0 0 2px rgba(36, 76, 58, 0.2);
    }

    .timeline-card {
        background: rgba(255, 255, 255, 0.84);
        padding: 0.95rem 1rem;
        border-radius: 18px;
        border: 1px solid rgba(36, 76, 58, 0.10);
        box-shadow: 0 4px 14px rgba(0,0,0,0.045);
    }

    .timeline-time {
        display: inline-block;
        color: #244c3a;
        font-weight: 800;
        font-size: 0.82rem;
        letter-spacing: 0.01rem;
        margin-bottom: 0.2rem;
    }

    .timeline-category {
        display: inline-block;
        background: #efe3c4;
        color: #5c4214;
        padding: 0.15rem 0.5rem;
        border-radius: 999px;
        font-size: 0.68rem;
        font-weight: 700;
        margin-left: 0.35rem;
        vertical-align: middle;
    }

    .timeline-title {
        margin-top: 0.15rem;
        margin-bottom: 0.35rem;
        font-size: 1.12rem;
        color: #20362c;
        font-weight: 800;
    }

    .timeline-place {
        color: #3f7d5d;
        font-weight: 700;
        margin-bottom: 0.35rem;
        font-size: 0.92rem;
    }

    .timeline-description {
        color: #26332c;
        font-size: 0.96rem;
        line-height: 1.45;
        margin-bottom: 0.2rem;
    }

    .mini-card {
        background: rgba(255,255,255,0.9);
        padding: 0.9rem 0.95rem;
        border-radius: 16px;
        border: 1px solid rgba(0,0,0,0.06);
        margin-bottom: 0.75rem;
        box-shadow: 0 4px 14px rgba(0,0,0,0.04);
    }

    .mini-card h3 {
        margin-bottom: 0.25rem;
        color: #20362c;
    }

    .category-pill {
        display: inline-block;
        background: #efe3c4;
        color: #5c4214;
        padding: 0.18rem 0.55rem;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 700;
        margin-bottom: 0.35rem;
    }

    .packing-note {
        background: rgba(255,255,255,0.86);
        border-radius: 14px;
        border: 1px solid rgba(36, 76, 58, 0.10);
        padding: 0.3rem 0.6rem;
        margin-bottom: 0.45rem;
    }

    .footer-note {
        color: #5f6b63;
        font-size: 0.85rem;
        text-align: center;
        margin-top: 2rem;
    }

    div[data-testid="stTabs"] button {
        font-size: 0.9rem;
        font-weight: 700;
    }

    div.stButton > button {
        border-radius: 999px;
    }

    a[data-testid="stLinkButton"] {
        border-radius: 999px;
        text-decoration: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------
# Helper functions
# -------------------------

def safe_read_csv(path: str) -> pd.DataFrame:
    try:
        return pd.read_csv(path).fillna("")
    except Exception as e:
        st.error(f"Could not load {path}")
        st.exception(e)
        return pd.DataFrame()


def text(value) -> str:
    """Safely convert values to display text and escape HTML."""
    if value is None:
        return ""
    return html.escape(str(value))


def place_button(label: str, url: str):
    if isinstance(url, str) and url.strip():
        st.link_button(label, url)


def get_place(place_name: str):
    if places.empty or not place_name:
        return None

    if "name" not in places.columns:
        return None

    match = places[places["name"].str.lower() == str(place_name).lower()]
    if not match.empty:
        return match.iloc[0]

    return None


def day_theme(day_name: str) -> str:
    themes = {
        "Friday": (
            "<strong>Theme:</strong> arrive, settle into the loft, enjoy a relaxed downtown evening, "
            "and anchor the night around Concerts on the Creek."
        ),
        "Saturday": (
            "<strong>Theme:</strong> boutique shopping, downtown wandering, breweries, "
            "and a nice dinner."
        ),
        "Sunday": (
            "<strong>Theme:</strong> slow morning, checkout, final shops, "
            "or a short Dillsboro add-on."
        ),
    }
    return themes.get(day_name, "")


def show_day(day_name: str, emoji: str):
    st.markdown(
        f"<h2 class='section-title'>{emoji} {text(day_name)}</h2>",
        unsafe_allow_html=True
    )

    theme = day_theme(day_name)
    if theme:
        st.markdown(
            f"<div class='day-note'>{theme}</div>",
            unsafe_allow_html=True
        )

    if itinerary.empty:
        st.write("No itinerary data loaded.")
        return

    required_columns = {"day", "time", "title", "category", "place_name", "description"}
    missing = required_columns - set(itinerary.columns)

    if missing:
        st.error(f"Your itinerary.csv is missing these columns: {', '.join(sorted(missing))}")
        return

    day_items = itinerary[itinerary["day"].str.lower() == day_name.lower()]

    if day_items.empty:
        st.write(f"No itinerary items found for {day_name}.")
        return

    st.markdown("<div class='timeline'>", unsafe_allow_html=True)

    for index, row in day_items.iterrows():
        item_time = text(row.get("time", ""))
        title = text(row.get("title", ""))
        description = text(row.get("description", ""))
        category = text(row.get("category", ""))
        place_name = text(row.get("place_name", ""))

        html_card = f"""
        <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="timeline-card">
                <div>
                    <span class="timeline-time">{item_time}</span>
                    <span class="timeline-category">{category}</span>
                </div>
                <div class="timeline-title">{title}</div>
        """

        if place_name:
            html_card += f'<div class="timeline-place">📍 {place_name}</div>'

        if description:
            html_card += f'<div class="timeline-description">{description}</div>'

        html_card += """
            </div>
        </div>
        """

        st.markdown(html_card, unsafe_allow_html=True)

        raw_place_name = row.get("place_name", "")
        place = get_place(raw_place_name)

        if place is not None:
            website = place.get("website", "")
            map_url = place.get("map_url", "")

            if website or map_url:
                button_cols = st.columns(2)
                with button_cols[0]:
                    place_button("Website", website)
                with button_cols[1]:
                    place_button("Open Map", map_url)

    st.markdown("</div>", unsafe_allow_html=True)


def show_place_cards(category_list, title: str, emoji: str):
    st.markdown(
        f"<h2 class='section-title'>{emoji} {text(title)}</h2>",
        unsafe_allow_html=True
    )

    if places.empty:
        st.write("No places loaded.")
        return

    required_columns = {"name", "category", "notes", "website", "map_url"}
    missing = required_columns - set(places.columns)

    if missing:
        st.error(f"Your places.csv is missing these columns: {', '.join(sorted(missing))}")
        return

    filtered = places[places["category"].isin(category_list)]

    if filtered.empty:
        st.write("No matching places found.")
        return

    for _, place in filtered.iterrows():
        name = text(place.get("name", ""))
        category = text(place.get("category", ""))
        notes = text(place.get("notes", ""))

        st.markdown(
            f"""
            <div class="mini-card">
                <h3>{name}</h3>
                <div class="category-pill">{category}</div>
                <div>{notes}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        button_cols = st.columns(2)
        with button_cols[0]:
            place_button("Website", place.get("website", ""))
        with button_cols[1]:
            place_button("Open Map", place.get("map_url", ""))


# -------------------------
# Load data
# -------------------------

places = safe_read_csv("data/places.csv")
itinerary = safe_read_csv("data/itinerary.csv")
packing = safe_read_csv("data/packing.csv")

# -------------------------
# Header / Hero
# -------------------------

st.markdown(
    """
    <div class="hero">
        <h1>🏔️ Sylva Weekend Itinerary</h1>
        <p>June 5–7, 2026 • Downtown Sylva, North Carolina</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="quick-note">
        <strong>Home base:</strong> Airbnb loft at 498 W Main St.<br>
        <strong>Check-in:</strong> Friday at 4:00 PM &nbsp; • &nbsp;
        <strong>Check-out:</strong> Sunday by 11:00 AM<br>
        <strong>Weekend theme:</strong> park once, walk often, shop downtown,
        enjoy breweries, and anchor Friday night around Concerts on the Creek.
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    st.link_button(
        "📍 Airbnb Map",
        "https://www.google.com/maps/search/?api=1&query=498%20W%20Main%20St%20Sylva%20NC%2028779"
    )

with col2:
    st.link_button(
        "🎶 Concert Map",
        "https://www.google.com/maps/search/?api=1&query=Bridge%20Park%2076%20Railroad%20Ave%20Sylva%20NC%2028779"
    )

st.warning("Security reminder: do not store the Airbnb door code in this public app.")

# -------------------------
# Tabs
# -------------------------

tabs = st.tabs([
    "Fri",
    "Sat",
    "Sun",
    "Food",
    "Shops",
    "Side Trips",
    "Packing"
])

# -------------------------
# Friday
# -------------------------

with tabs[0]:
    show_day("Friday", "🎶")

# -------------------------
# Saturday
# -------------------------

with tabs[1]:
    show_day("Saturday", "🛍️")

# -------------------------
# Sunday
# -------------------------

with tabs[2]:
    show_day("Sunday", "☕")

# -------------------------
# Food & Drink
# -------------------------

with tabs[3]:
    show_place_cards(
        ["Food", "Drink", "Brewery", "Coffee", "Sweets"],
        "Food & Drink",
        "🍽️"
    )

# -------------------------
# Shopping
# -------------------------

with tabs[4]:
    show_place_cards(
        ["Shopping", "Sweets"],
        "Boutique Shopping & Gifts",
        "🛍️"
    )

# -------------------------
# Side Trips
# -------------------------

with tabs[5]:
    show_place_cards(
        ["Side Trip", "Standby Side Trip"],
        "Standby Side Trips",
        "🚗"
    )

# -------------------------
# Packing
# -------------------------

with tabs[6]:
    st.markdown(
        "<h2 class='section-title'>🎒 Packing / Reminders</h2>",
        unsafe_allow_html=True
    )

    if packing.empty:
        st.write("No packing list loaded.")
    else:
        required_columns = {"item", "category", "notes"}
        missing = required_columns - set(packing.columns)

        if missing:
            st.error(f"Your packing.csv is missing these columns: {', '.join(sorted(missing))}")
        else:
            for _, row in packing.iterrows():
                item = row.get("item", "")
                category = row.get("category", "")
                notes = row.get("notes", "")

                st.markdown("<div class='packing-note'>", unsafe_allow_html=True)

                st.checkbox(
                    str(item),
                    value=False,
                    key=f"packing_{item}"
                )

                if category or notes:
                    st.caption(f"{category} — {notes}")

                st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Footer
# -------------------------

st.markdown(
    """
    <div class="footer-note">
        Built as a mobile-friendly weekend trip guide • Best viewed from Safari and added to the iPhone Home Screen.
    </div>
    """,
    unsafe_allow_html=True
)
