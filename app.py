import html
from typing import Optional

import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials


st.set_page_config(
    page_title="Sylva Weekend Itinerary",
    page_icon="🏔️",
    layout="centered"
)

# -------------------------
# App settings
# -------------------------

SHEET_ID = "1EVohk4RDve5QxR-xZQvJ9CR3X49rVfClFcQUEAo7upU"

REQUIRED_ITINERARY_COLUMNS = [
    "day", "time", "title", "category", "place_name", "description", "priority"
]

REQUIRED_PLACES_COLUMNS = [
    "name", "category", "address", "lat", "lon", "website",
    "map_url", "image_url", "image_credit", "notes"
]

REQUIRED_PACKING_COLUMNS = [
    "item", "category", "packed", "notes"
]

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
# General helpers
# -------------------------

def text(value) -> str:
    if value is None:
        return ""
    return html.escape(str(value))


def safe_read_csv(path: str, expected_columns: list[str]) -> pd.DataFrame:
    try:
        df = pd.read_csv(path).fillna("")
        for col in expected_columns:
            if col not in df.columns:
                df[col] = ""
        return df[expected_columns]
    except Exception:
        return pd.DataFrame(columns=expected_columns)


def place_button(label: str, url: str):
    if isinstance(url, str) and url.strip():
        st.link_button(label, url)


# -------------------------
# Google Sheets helpers
# -------------------------

@st.cache_resource
def get_gspread_client():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scopes
    )

    return gspread.authorize(credentials)


def get_worksheet(sheet_name: str):
    client = get_gspread_client()
    spreadsheet = client.open_by_key(SHEET_ID)
    return spreadsheet.worksheet(sheet_name)


def worksheet_to_df(sheet_name: str, expected_columns: list[str]) -> pd.DataFrame:
    worksheet = get_worksheet(sheet_name)
    records = worksheet.get_all_records()
    df = pd.DataFrame(records)

    if df.empty:
        df = pd.DataFrame(columns=expected_columns)

    for col in expected_columns:
        if col not in df.columns:
            df[col] = ""

    return df[expected_columns].fillna("")


def append_itinerary_event(event: dict):
    worksheet = get_worksheet("itinerary")
    row = [event.get(col, "") for col in REQUIRED_ITINERARY_COLUMNS]
    worksheet.append_row(row, value_input_option="USER_ENTERED")


def load_data_from_google_sheets():
    itinerary_df = worksheet_to_df("itinerary", REQUIRED_ITINERARY_COLUMNS)
    places_df = worksheet_to_df("places", REQUIRED_PLACES_COLUMNS)
    packing_df = worksheet_to_df("packing", REQUIRED_PACKING_COLUMNS)
    return itinerary_df, places_df, packing_df


def load_data():
    """
    Prefer Google Sheets. Fall back to local CSVs if Google Sheets is unavailable.
    """
    try:
        itinerary_df, places_df, packing_df = load_data_from_google_sheets()
        return itinerary_df, places_df, packing_df, "Google Sheets"
    except Exception as e:
    st.sidebar.warning("Using local CSV backup.")
    st.sidebar.error("Google Sheets connection failed.")
    st.sidebar.code(repr(e))

        itinerary_df = safe_read_csv("data/itinerary.csv", REQUIRED_ITINERARY_COLUMNS)
        places_df = safe_read_csv("data/places.csv", REQUIRED_PLACES_COLUMNS)
        packing_df = safe_read_csv("data/packing.csv", REQUIRED_PACKING_COLUMNS)

        return itinerary_df, places_df, packing_df, "local CSV backup"


def clear_sheet_cache():
    st.cache_resource.clear()


# -------------------------
# Load data
# -------------------------

itinerary, places, packing, data_source = load_data()

# -------------------------
# Data helpers
# -------------------------

def get_place(place_name: str) -> Optional[pd.Series]:
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
        st.write("No itinerary items yet.")
        return

    day_items = itinerary[itinerary["day"].str.lower() == day_name.lower()]

    if day_items.empty:
        st.write(f"No itinerary items found for {day_name}.")
        return

    st.markdown("<div class='timeline'>", unsafe_allow_html=True)

    for _, row in day_items.iterrows():
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
        st.write("No places loaded yet.")
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


def show_add_event_form():
    st.markdown(
        "<h2 class='section-title'>➕ Add Event</h2>",
        unsafe_allow_html=True
    )

    st.write(
        "Add a new itinerary item here. It will be saved to the Google Sheet "
        "and remain available after the app restarts."
    )

    if data_source != "Google Sheets":
        st.error(
            "The app is currently using the local CSV backup, so new events cannot be saved permanently. "
            "Check Streamlit Secrets and Google Sheet sharing."
        )
        return

    with st.form("add_event_form", clear_on_submit=True):
        day = st.selectbox("Day", ["Friday", "Saturday", "Sunday"])
        event_time = st.text_input("Time", placeholder="Example: 6:30 PM")
        title = st.text_input("Title", placeholder="Example: Dinner at ILDA")
        category = st.selectbox(
            "Category",
            ["Food", "Drink", "Brewery", "Shopping", "Event", "Lodging", "Coffee", "Side Trip", "Other"]
        )

        place_options = [""] + sorted([p for p in places["name"].dropna().unique().tolist() if str(p).strip()])
        place_name = st.selectbox("Place", place_options)

        description = st.text_area(
            "Description",
            placeholder="Add notes for this event..."
        )

        priority = st.selectbox("Priority", ["Optional", "Planned", "Confirmed"])

        submitted = st.form_submit_button("Save event")

        if submitted:
            if not title.strip():
                st.error("Please add a title before saving.")
                return

            new_event = {
                "day": day,
                "time": event_time.strip(),
                "title": title.strip(),
                "category": category,
                "place_name": place_name.strip(),
                "description": description.strip(),
                "priority": priority,
            }

            try:
                append_itinerary_event(new_event)
                st.success("Event saved to the itinerary.")
                st.info("Refresh the app or switch tabs to see the new event in the timeline.")
                st.cache_resource.clear()
            except Exception as e:
                st.error("Could not save the event to Google Sheets.")
                st.exception(e)


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
st.caption(f"Data source: {data_source}")

# -------------------------
# Tabs
# -------------------------

tabs = st.tabs([
    "Fri",
    "Sat",
    "Sun",
    "Add Event",
    "Food",
    "Shops",
    "Side Trips",
    "Packing"
])

with tabs[0]:
    show_day("Friday", "🎶")

with tabs[1]:
    show_day("Saturday", "🛍️")

with tabs[2]:
    show_day("Sunday", "☕")

with tabs[3]:
    show_add_event_form()

with tabs[4]:
    show_place_cards(
        ["Food", "Drink", "Brewery", "Coffee", "Sweets"],
        "Food & Drink",
        "🍽️"
    )

with tabs[5]:
    show_place_cards(
        ["Shopping", "Sweets"],
        "Boutique Shopping & Gifts",
        "🛍️"
    )

with tabs[6]:
    show_place_cards(
        ["Side Trip", "Standby Side Trip"],
        "Standby Side Trips",
        "🚗"
    )

with tabs[7]:
    st.markdown(
        "<h2 class='section-title'>🎒 Packing / Reminders</h2>",
        unsafe_allow_html=True
    )

    if packing.empty:
        st.write("No packing list loaded yet.")
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
