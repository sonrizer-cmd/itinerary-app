import streamlit as st
import pandas as pd

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

    .trip-card {
        background: rgba(255, 255, 255, 0.88);
        padding: 1rem 1.1rem;
        border-radius: 18px;
        margin-bottom: 0.9rem;
        border: 1px solid rgba(36, 76, 58, 0.12);
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    }

    .time-pill {
        display: inline-block;
        background: #244c3a;
        color: white;
        padding: 0.25rem 0.65rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 700;
        margin-bottom: 0.45rem;
    }

    .category-pill {
        display: inline-block;
        background: #efe3c4;
        color: #5c4214;
        padding: 0.22rem 0.55rem;
        border-radius: 999px;
        font-size: 0.74rem;
        font-weight: 600;
        margin-left: 0.35rem;
    }

    .place-name {
        color: #244c3a;
        font-weight: 700;
        margin-top: 0.4rem;
    }

    .quick-note {
        background: #fff8e6;
        border-left: 5px solid #d9a441;
        padding: 0.9rem 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }

    .mini-card {
        background: rgba(255,255,255,0.9);
        padding: 0.85rem;
        border-radius: 16px;
        border: 1px solid rgba(0,0,0,0.06);
        margin-bottom: 0.7rem;
    }

    .section-title {
        color: #244c3a;
        margin-top: 1rem;
    }

    div[data-testid="stTabs"] button {
        font-size: 0.92rem;
        font-weight: 600;
    }

    .footer-note {
        color: #5f6b63;
        font-size: 0.85rem;
        text-align: center;
        margin-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------
# Helper functions
# -------------------------

def safe_read_csv(path):
    try:
        return pd.read_csv(path).fillna("")
    except Exception as e:
        st.error(f"Could not load {path}")
        st.exception(e)
        return pd.DataFrame()

def place_button(label, url):
    if isinstance(url, str) and url.strip():
        st.link_button(label, url)

def get_place(place_name):
    if places.empty or not place_name:
        return None

    match = places[places["name"].str.lower() == str(place_name).lower()]
    if not match.empty:
        return match.iloc[0]
    return None

def card_open():
    st.markdown('<div class="trip-card">', unsafe_allow_html=True)

def card_close():
    st.markdown('</div>', unsafe_allow_html=True)

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
        <strong>Weekend theme:</strong> park once, walk often, shop downtown, enjoy breweries, and anchor Friday night around Concerts on the Creek.
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
# Day itinerary display
# -------------------------

def show_day(day_name, emoji):
    st.markdown(f"<h2 class='section-title'>{emoji} {day_name}</h2>", unsafe_allow_html=True)

    if itinerary.empty:
        st.write("No itinerary data loaded.")
        return

    day_items = itinerary[itinerary["day"].str.lower() == day_name.lower()]

    if day_items.empty:
        st.write(f"No itinerary items found for {day_name}.")
        return

    for _, row in day_items.iterrows():
        time = row.get("time", "")
        title = row.get("title", "")
        description = row.get("description", "")
        category = row.get("category", "")
        place_name = row.get("place_name", "")

        st.markdown('<div class="trip-card">', unsafe_allow_html=True)

        st.markdown(
            f"""
            <span class="time-pill">{time}</span>
            <span class="category-pill">{category}</span>
            <h3 style="margin-top:0.35rem; margin-bottom:0.3rem;">{title}</h3>
            """,
            unsafe_allow_html=True
        )

        if place_name:
            st.markdown(f'<div class="place-name">📍 {place_name}</div>', unsafe_allow_html=True)

        if description:
            st.write(description)

        place = get_place(place_name)
        if place is not None:
            button_cols = st.columns(2)
            with button_cols[0]:
                place_button("Website", place.get("website", ""))
            with button_cols[1]:
                place_button("Open Map", place.get("map_url", ""))

        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# Place card display
# -------------------------

def show_place_cards(category_list, title, emoji):
    st.markdown(f"<h2 class='section-title'>{emoji} {title}</h2>", unsafe_allow_html=True)

    if places.empty:
        st.write("No places loaded.")
        return

    filtered = places[places["category"].isin(category_list)]

    if filtered.empty:
        st.write("No matching places found.")
        return

    for _, place in filtered.iterrows():
        st.markdown('<div class="mini-card">', unsafe_allow_html=True)
        st.markdown(
            f"""
            <h3 style="margin-bottom:0.25rem;">{place.get("name", "")}</h3>
            <span class="category-pill">{place.get("category", "")}</span>
            """,
            unsafe_allow_html=True
        )

        notes = place.get("notes", "")
        if notes:
            st.write(notes)

        button_cols = st.columns(2)
        with button_cols[0]:
            place_button("Website", place.get("website", ""))
        with button_cols[1]:
            place_button("Open Map", place.get("map_url", ""))

        st.markdown('</div>', unsafe_allow_html=True)

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
    st.markdown("<h2 class='section-title'>🎒 Packing / Reminders</h2>", unsafe_allow_html=True)

    if packing.empty:
        st.write("No packing list loaded.")
    else:
        for _, row in packing.iterrows():
            item = row.get("item", "")
            category = row.get("category", "")
            notes = row.get("notes", "")

            with st.container(border=True):
                st.checkbox(
                    item,
                    value=False,
                    key=f"packing_{item}"
                )

                if category or notes:
                    st.caption(f"{category} — {notes}")

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
