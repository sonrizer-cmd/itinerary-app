import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Sylva Weekend Itinerary",
    page_icon="🏔️",
    layout="centered"
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

def section_divider():
    st.markdown("---")

# -------------------------
# Load data
# -------------------------

places = safe_read_csv("data/places.csv")
itinerary = safe_read_csv("data/itinerary.csv")
packing = safe_read_csv("data/packing.csv")

# -------------------------
# Header
# -------------------------

st.title("Sylva Weekend Itinerary")
st.caption("June 5–7, 2026 • Sylva, North Carolina")

st.info(
    "Home base: Airbnb loft at 498 W Main St. "
    "Check-in Friday at 4:00 PM. Check-out Sunday by 11:00 AM."
)

col1, col2 = st.columns(2)

with col1:
    st.link_button(
        "Airbnb Map",
        "https://www.google.com/maps/search/?api=1&query=498%20W%20Main%20St%20Sylva%20NC%2028779"
    )

with col2:
    st.link_button(
        "Concert Map",
        "https://www.google.com/maps/search/?api=1&query=Bridge%20Park%2076%20Railroad%20Ave%20Sylva%20NC%2028779"
    )

st.warning("Do not store the Airbnb door code in this public app.")

# -------------------------
# Tabs
# -------------------------

tabs = st.tabs([
    "Friday",
    "Saturday",
    "Sunday",
    "Food & Drink",
    "Shopping",
    "Side Trips",
    "Packing"
])

# -------------------------
# Day itinerary display
# -------------------------

def show_day(day_name):
    st.header(day_name)

    if itinerary.empty:
        st.write("No itinerary data loaded.")
        return

    day_items = itinerary[itinerary["day"].str.lower() == day_name.lower()]

    if day_items.empty:
        st.write(f"No itinerary items found for {day_name}.")
        return

    for _, row in day_items.iterrows():
        with st.container(border=True):
            time = row.get("time", "")
            title = row.get("title", "")
            description = row.get("description", "")
            category = row.get("category", "")
            place_name = row.get("place_name", "")

            st.subheader(f"{time} — {title}")
            if category:
                st.caption(category)
            if place_name:
                st.write(f"**Place:** {place_name}")
            if description:
                st.write(description)

            if place_name and not places.empty:
                match = places[places["name"].str.lower() == str(place_name).lower()]
                if not match.empty:
                    place = match.iloc[0]
                    button_cols = st.columns(2)
                    with button_cols[0]:
                        place_button("Website", place.get("website", ""))
                    with button_cols[1]:
                        place_button("Open Map", place.get("map_url", ""))

# -------------------------
# Friday
# -------------------------

with tabs[0]:
    show_day("Friday")

# -------------------------
# Saturday
# -------------------------

with tabs[1]:
    show_day("Saturday")

# -------------------------
# Sunday
# -------------------------

with tabs[2]:
    show_day("Sunday")

# -------------------------
# Food & Drink
# -------------------------

with tabs[3]:
    st.header("Food & Drink")

    if places.empty:
        st.write("No places loaded.")
    else:
        food_categories = ["Food", "Drink", "Brewery", "Coffee", "Sweets"]
        food_places = places[places["category"].isin(food_categories)]

        for _, place in food_places.iterrows():
            with st.container(border=True):
                st.subheader(place.get("name", ""))
                st.caption(place.get("category", ""))
                if place.get("notes", ""):
                    st.write(place.get("notes", ""))

                button_cols = st.columns(2)
                with button_cols[0]:
                    place_button("Website", place.get("website", ""))
                with button_cols[1]:
                    place_button("Open Map", place.get("map_url", ""))

# -------------------------
# Shopping
# -------------------------

with tabs[4]:
    st.header("Shopping")

    if places.empty:
        st.write("No places loaded.")
    else:
        shopping_categories = ["Shopping", "Sweets"]
        shopping_places = places[places["category"].isin(shopping_categories)]

        for _, place in shopping_places.iterrows():
            with st.container(border=True):
                st.subheader(place.get("name", ""))
                st.caption(place.get("category", ""))
                if place.get("notes", ""):
                    st.write(place.get("notes", ""))

                button_cols = st.columns(2)
                with button_cols[0]:
                    place_button("Website", place.get("website", ""))
                with button_cols[1]:
                    place_button("Open Map", place.get("map_url", ""))

# -------------------------
# Side Trips
# -------------------------

with tabs[5]:
    st.header("Standby Side Trips")

    if places.empty:
        st.write("No places loaded.")
    else:
        side_trip_categories = ["Side Trip", "Standby Side Trip"]
        side_trips = places[places["category"].isin(side_trip_categories)]

        for _, place in side_trips.iterrows():
            with st.container(border=True):
                st.subheader(place.get("name", ""))
                st.caption(place.get("category", ""))
                if place.get("notes", ""):
                    st.write(place.get("notes", ""))

                button_cols = st.columns(2)
                with button_cols[0]:
                    place_button("Website", place.get("website", ""))
                with button_cols[1]:
                    place_button("Open Map", place.get("map_url", ""))

# -------------------------
# Packing
# -------------------------

with tabs[6]:
    st.header("Packing / Reminders")

    if packing.empty:
        st.write("No packing list loaded.")
    else:
        for _, row in packing.iterrows():
            item = row.get("item", "")
            category = row.get("category", "")
            notes = row.get("notes", "")

            checked = st.checkbox(
                item,
                value=False,
                key=f"packing_{item}"
            )

            if category or notes:
                st.caption(f"{category} — {notes}")
