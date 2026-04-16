import streamlit as st
import pandas as pd
import os

FILE_NAME = "users.csv"

if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=[
        "Name", "Age", "Gender", "Phone", "Gmail", "City", "Budget",
        "Food", "Sleep", "Cleanliness", "Smoking", "Drinking", "StudyHabit", "SharingPreference"
    ])
    df.to_csv(FILE_NAME, index=False)

def load_data():
    return pd.read_csv(FILE_NAME)

def save_data(data):
    data.to_csv(FILE_NAME, index=False)

def calculate_match_score(user, other):
    score = 0
    if user["City"] == other["City"]: score += 20
    if abs(user["Budget"] - other["Budget"]) <= 2000: score += 20
    if user["Food"] == other["Food"]: score += 10
    if user["Sleep"] == other["Sleep"]: score += 10
    if user["Cleanliness"] == other["Cleanliness"]: score += 10
    if user["Smoking"] == other["Smoking"]: score += 10
    if user["Drinking"] == other["Drinking"]: score += 10
    if user["StudyHabit"] == other["StudyHabit"]: score += 5
    if user["SharingPreference"] == other["SharingPreference"]: score += 5
    return score

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="StayMate", page_icon="🏠", layout="wide")

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── Background ── */
.stApp { background: #0f1117; color: #e2e8f0; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1f2e 0%, #141824 100%);
    border-right: 1px solid #2d3748;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 16px;
    padding: 40px 48px;
    margin-bottom: 32px;
    box-shadow: 0 20px 60px rgba(102,126,234,0.3);
}
.hero h1 { font-size: 2.6rem; font-weight: 700; color: #fff; margin: 0 0 8px; }
.hero p  { font-size: 1.1rem; color: rgba(255,255,255,0.85); margin: 0; }

/* ── Section card ── */
.section-card {
    background: #1a1f2e;
    border: 1px solid #2d3748;
    border-radius: 14px;
    padding: 28px 32px;
    margin-bottom: 24px;
}
.section-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #a78bfa;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid #2d3748;
}

/* ── Inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] > div > div {
    background: #0f1117 !important;
    border: 1px solid #3d4a63 !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-size: 0.95rem !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102,126,234,0.2) !important;
}
label { color: #94a3b8 !important; font-size: 0.85rem !important; font-weight: 500 !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 32px !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(102,126,234,0.4) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(102,126,234,0.5) !important;
}

/* ── Form submit button ── */
[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 32px !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    width: 100% !important;
    margin-top: 8px !important;
    box-shadow: 0 4px 15px rgba(102,126,234,0.4) !important;
}

/* ── Stat cards ── */
.stat-card {
    background: linear-gradient(135deg, #1e2a3a, #1a2332);
    border: 1px solid #2d3748;
    border-radius: 12px;
    padding: 20px 24px;
    text-align: center;
}
.stat-number { font-size: 2rem; font-weight: 700; color: #667eea; }
.stat-label  { font-size: 0.85rem; color: #64748b; margin-top: 4px; }

/* ── Match card ── */
.match-card {
    background: #1a1f2e;
    border: 1px solid #2d3748;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 16px;
    transition: border-color 0.2s;
}
.match-card:hover { border-color: #667eea; }
.match-name  { font-size: 1.15rem; font-weight: 600; color: #e2e8f0; }
.match-score {
    display: inline-block;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: #fff;
    font-weight: 700;
    font-size: 0.9rem;
    padding: 4px 14px;
    border-radius: 20px;
}
.match-detail { font-size: 0.85rem; color: #64748b; margin-top: 6px; }
.badge {
    display: inline-block;
    background: #1e2a3a;
    border: 1px solid #3d4a63;
    color: #94a3b8;
    font-size: 0.78rem;
    padding: 3px 10px;
    border-radius: 20px;
    margin: 3px 2px;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }
.stDataFrame thead tr th { background: #1e2a3a !important; color: #a78bfa !important; }
.stDataFrame tbody tr:hover td { background: #1e2a3a !important; }

/* ── Alerts ── */
.stSuccess { background: #0d2818 !important; border-left: 4px solid #22c55e !important; border-radius: 8px !important; }
.stError   { background: #2d0f0f !important; border-left: 4px solid #ef4444 !important; border-radius: 8px !important; }
.stWarning { background: #2d1f0a !important; border-left: 4px solid #f59e0b !important; border-radius: 8px !important; }
.stInfo    { background: #0d1f2d !important; border-left: 4px solid #3b82f6 !important; border-radius: 8px !important; }

/* ── Sidebar nav ── */
.nav-item {
    padding: 10px 16px;
    border-radius: 8px;
    margin-bottom: 4px;
    cursor: pointer;
    font-weight: 500;
    color: #94a3b8;
}
.nav-item:hover { background: #2d3748; color: #e2e8f0; }

/* ── Divider ── */
hr { border-color: #2d3748 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0f1117; }
::-webkit-scrollbar-thumb { background: #3d4a63; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 28px;'>
        <div style='font-size:2.5rem;'>🏠</div>
        <div style='font-size:1.4rem; font-weight:700; color:#e2e8f0; margin-top:8px;'>StayMate</div>
        <div style='font-size:0.8rem; color:#64748b; margin-top:4px;'>Smart Roommate Finder</div>
    </div>
    <hr style='margin-bottom:20px;'>
    """, unsafe_allow_html=True)

    menu = st.selectbox(
        "Navigation",
        ["🏠  Dashboard", "📝  Register Profile", "🔍  Find Matches", "👥  All Users"],
        label_visibility="collapsed"
    )

    df_side = load_data()
    total = len(df_side)
    cities = df_side["City"].nunique() if not df_side.empty else 0

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='padding: 0 8px;'>
        <div style='font-size:0.75rem; color:#64748b; text-transform:uppercase; letter-spacing:1px; margin-bottom:12px;'>Quick Stats</div>
        <div style='display:flex; justify-content:space-between; margin-bottom:10px;'>
            <span style='color:#94a3b8; font-size:0.85rem;'>👤 Total Users</span>
            <span style='color:#667eea; font-weight:600;'>{total}</span>
        </div>
        <div style='display:flex; justify-content:space-between;'>
            <span style='color:#94a3b8; font-size:0.85rem;'>🏙️ Cities</span>
            <span style='color:#667eea; font-weight:600;'>{cities}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
page = menu.split("  ")[1] if "  " in menu else menu

if page == "Dashboard":
    st.markdown("""
    <div class='hero'>
        <h1>🏠 StayMate</h1>
        <p>Find your perfect roommate based on lifestyle, habits & preferences — intelligently matched.</p>
    </div>
    """, unsafe_allow_html=True)

    df = load_data()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='stat-card'><div class='stat-number'>{len(df)}</div><div class='stat-label'>Total Profiles</div></div>", unsafe_allow_html=True)
    with c2:
        cities_count = df["City"].nunique() if not df.empty else 0
        st.markdown(f"<div class='stat-card'><div class='stat-number'>{cities_count}</div><div class='stat-label'>Cities Covered</div></div>", unsafe_allow_html=True)
    with c3:
        male = len(df[df["Gender"] == "Male"]) if not df.empty else 0
        st.markdown(f"<div class='stat-card'><div class='stat-number'>{male}</div><div class='stat-label'>Male Users</div></div>", unsafe_allow_html=True)
    with c4:
        female = len(df[df["Gender"] == "Female"]) if not df.empty else 0
        st.markdown(f"<div class='stat-card'><div class='stat-number'>{female}</div><div class='stat-label'>Female Users</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-card'><div class='section-title'>🏙️ Top Cities</div>", unsafe_allow_html=True)
        if not df.empty:
            top_cities = df["City"].value_counts().head(5)
            for city, count in top_cities.items():
                pct = int(count / len(df) * 100)
                st.markdown(f"""
                <div style='margin-bottom:12px;'>
                    <div style='display:flex; justify-content:space-between; margin-bottom:4px;'>
                        <span style='color:#e2e8f0; font-size:0.9rem;'>{city}</span>
                        <span style='color:#667eea; font-size:0.85rem; font-weight:600;'>{count}</span>
                    </div>
                    <div style='background:#0f1117; border-radius:4px; height:6px;'>
                        <div style='background:linear-gradient(90deg,#667eea,#764ba2); width:{pct}%; height:6px; border-radius:4px;'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='section-card'><div class='section-title'>🍽️ Food Preferences</div>", unsafe_allow_html=True)
        if not df.empty:
            food_counts = df["Food"].value_counts()
            colors = {"Veg": "#22c55e", "Non-Veg": "#ef4444", "Both": "#f59e0b"}
            for food, count in food_counts.items():
                pct = int(count / len(df) * 100)
                color = colors.get(food, "#667eea")
                st.markdown(f"""
                <div style='margin-bottom:12px;'>
                    <div style='display:flex; justify-content:space-between; margin-bottom:4px;'>
                        <span style='color:#e2e8f0; font-size:0.9rem;'>{food}</span>
                        <span style='color:{color}; font-size:0.85rem; font-weight:600;'>{pct}%</span>
                    </div>
                    <div style='background:#0f1117; border-radius:4px; height:6px;'>
                        <div style='background:{color}; width:{pct}%; height:6px; border-radius:4px;'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ── Register Profile ──────────────────────────────────────────────────────────
elif page == "Register Profile":
    st.markdown("""
    <div class='hero'>
        <h1>📝 Create Profile</h1>
        <p>Fill in your details to find the most compatible roommate.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("profile_form"):
        st.markdown("<div class='section-card'><div class='section-title'>👤 Personal Information</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: name = st.text_input("Full Name", placeholder="e.g. Rahul Sharma")
        with c2: age = st.number_input("Age", min_value=18, max_value=60, step=1)
        with c3: gender = st.selectbox("Gender", ["Male", "Female"])

        c4, c5 = st.columns(2)
        with c4: phone = st.text_input("Phone Number", placeholder="e.g. 9876543210")
        with c5: gmail = st.text_input("Gmail", placeholder="e.g. rahul@gmail.com")

        c6, c7 = st.columns(2)
        with c6: city = st.text_input("City", placeholder="e.g. Mumbai")
        with c7: budget = st.number_input("Monthly Budget (₹)", min_value=1000, max_value=100000, step=500)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-card'><div class='section-title'>🌿 Lifestyle Preferences</div>", unsafe_allow_html=True)
        c8, c9, c10 = st.columns(3)
        with c8: food = st.selectbox("Food Preference", ["Veg", "Non-Veg", "Both"])
        with c9: sleep = st.selectbox("Sleep Schedule", ["Early Sleeper", "Night Owl"])
        with c10: cleanliness = st.selectbox("Cleanliness Level", ["Low", "Medium", "High"])

        c11, c12, c13, c14 = st.columns(4)
        with c11: smoking = st.selectbox("Smoking", ["No", "Yes"])
        with c12: drinking = st.selectbox("Drinking", ["No", "Yes"])
        with c13: study_habit = st.selectbox("Study/Work Habit", ["Quiet", "Moderate", "Flexible"])
        with c14: sharing = st.selectbox("Room Preference", ["Single Room", "Shared Room"])
        st.markdown("</div>", unsafe_allow_html=True)

        submitted = st.form_submit_button("🚀 Save Profile")

        if submitted:
            if not all([name.strip(), city.strip(), phone.strip(), gmail.strip()]):
                st.error("⚠️ Please fill all required fields.")
            elif not phone.strip().isdigit() or len(phone.strip()) != 10:
                st.error("⚠️ Enter a valid 10-digit phone number.")
            elif "@gmail.com" not in gmail.strip():
                st.error("⚠️ Enter a valid Gmail address.")
            else:
                df = load_data()
                new_user = pd.DataFrame([{
                    "Name": name, "Age": age, "Gender": gender,
                    "Phone": phone, "Gmail": gmail, "City": city,
                    "Budget": budget, "Food": food, "Sleep": sleep,
                    "Cleanliness": cleanliness, "Smoking": smoking,
                    "Drinking": drinking, "StudyHabit": study_habit,
                    "SharingPreference": sharing
                }])
                df = pd.concat([df, new_user], ignore_index=True)
                save_data(df)
                st.success(f"✅ Profile for **{name}** saved successfully!")

# ── Find Matches ──────────────────────────────────────────────────────────────
elif page == "Find Matches":
    st.markdown("""
    <div class='hero'>
        <h1>🔍 Find Matches</h1>
        <p>Discover your most compatible roommates based on smart scoring.</p>
    </div>
    """, unsafe_allow_html=True)

    df = load_data()

    if df.empty:
        st.warning("No users found. Please register profiles first.")
    else:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        c1, c2 = st.columns([3, 1])
        with c1:
            selected_name = st.selectbox("Select Your Profile", df["Name"].unique(), label_visibility="visible")
        with c2:
            st.markdown("<br>", unsafe_allow_html=True)
            find_btn = st.button("🔍 Find Matches")
        st.markdown("</div>", unsafe_allow_html=True)

        if find_btn:
            current_user = df[df["Name"] == selected_name].iloc[0]

            # Show current user card
            st.markdown(f"""
            <div class='section-card'>
                <div class='section-title'>Your Profile</div>
                <div style='display:flex; align-items:center; gap:20px;'>
                    <div style='width:56px; height:56px; border-radius:50%; background:linear-gradient(135deg,#667eea,#764ba2);
                                display:flex; align-items:center; justify-content:center; font-size:1.4rem; font-weight:700; color:#fff;'>
                        {current_user['Name'][0].upper()}
                    </div>
                    <div>
                        <div style='font-size:1.2rem; font-weight:600; color:#e2e8f0;'>{current_user['Name']}</div>
                        <div style='color:#64748b; font-size:0.85rem;'>{current_user['City']} · ₹{int(current_user['Budget']):,}/mo · {current_user['SharingPreference']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            others = df[df["Name"] != selected_name].copy()
            others = others[
                (others["City"].str.strip().str.lower() == str(current_user["City"]).strip().lower()) &
                (abs(others["Budget"].astype(int) - int(current_user["Budget"])) <= 5000) &
                (others["SharingPreference"] == current_user["SharingPreference"])
            ].copy()

            if others.empty:
                st.warning("😕 No matching users found within your preferences range.")
            else:
                others["Match Score"] = others.apply(lambda row: calculate_match_score(current_user, row), axis=1)
                others = others.sort_values(by="Match Score", ascending=False)

                st.markdown(f"""
                <div style='margin: 8px 0 20px;'>
                    <span style='color:#22c55e; font-weight:600; font-size:1rem;'>✅ Found {len(others)} compatible roommate(s)</span>
                </div>
                """, unsafe_allow_html=True)

                for _, row in others.iterrows():
                    score = int(row["Match Score"])
                    score_color = "#22c55e" if score >= 70 else "#f59e0b" if score >= 40 else "#ef4444"
                    bar_pct = min(score, 100)
                    st.markdown(f"""
                    <div class='match-card'>
                        <div style='display:flex; justify-content:space-between; align-items:flex-start;'>
                            <div style='display:flex; align-items:center; gap:14px;'>
                                <div style='width:48px; height:48px; border-radius:50%; background:linear-gradient(135deg,#1e2a3a,#2d3748);
                                            display:flex; align-items:center; justify-content:center; font-size:1.2rem; font-weight:700;
                                            color:#a78bfa; border:2px solid #3d4a63;'>
                                    {row['Name'][0].upper()}
                                </div>
                                <div>
                                    <div class='match-name'>{row['Name']}</div>
                                    <div class='match-detail'>{row['City']} · Age {int(row['Age'])} · {row['Gender']}</div>
                                </div>
                            </div>
                            <div style='text-align:right;'>
                                <div style='font-size:1.5rem; font-weight:700; color:{score_color};'>{score}%</div>
                                <div style='font-size:0.75rem; color:#64748b;'>Match Score</div>
                            </div>
                        </div>
                        <div style='margin: 12px 0 10px; background:#0f1117; border-radius:4px; height:5px;'>
                            <div style='background:{score_color}; width:{bar_pct}%; height:5px; border-radius:4px; transition:width 0.5s;'></div>
                        </div>
                        <div style='margin-top:10px;'>
                            <span class='badge'>💰 ₹{int(row['Budget']):,}/mo</span>
                            <span class='badge'>🍽️ {row['Food']}</span>
                            <span class='badge'>🌙 {row['Sleep']}</span>
                            <span class='badge'>🧹 {row['Cleanliness']}</span>
                            <span class='badge'>🚬 Smoking: {row['Smoking']}</span>
                            <span class='badge'>🍺 Drinking: {row['Drinking']}</span>
                            <span class='badge'>📚 {row['StudyHabit']}</span>
                            <span class='badge'>🛏️ {row['SharingPreference']}</span>
                        </div>
                        <div style='margin-top:10px; padding-top:10px; border-top:1px solid #2d3748; display:flex; gap:20px;'>
                            <span style='color:#64748b; font-size:0.82rem;'>📞 {row['Phone']}</span>
                            <span style='color:#64748b; font-size:0.82rem;'>✉️ {row['Gmail']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# ── All Users ─────────────────────────────────────────────────────────────────
elif page == "All Users":
    st.markdown("""
    <div class='hero'>
        <h1>👥 All Users</h1>
        <p>Browse all registered profiles on StayMate.</p>
    </div>
    """, unsafe_allow_html=True)

    df = load_data()

    if df.empty:
        st.info("No users registered yet.")
    else:
        # Search & filter bar
        st.markdown("<div class='section-card'><div class='section-title'>🔎 Search & Filter</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: search = st.text_input("Search by Name", placeholder="Type a name...")
        with c2: city_filter = st.selectbox("Filter by City", ["All"] + sorted(df["City"].unique().tolist()))
        with c3: gender_filter = st.selectbox("Filter by Gender", ["All", "Male", "Female"])
        st.markdown("</div>", unsafe_allow_html=True)

        filtered = df.copy()
        if search: filtered = filtered[filtered["Name"].str.contains(search, case=False, na=False)]
        if city_filter != "All": filtered = filtered[filtered["City"] == city_filter]
        if gender_filter != "All": filtered = filtered[filtered["Gender"] == gender_filter]

        st.markdown(f"<div style='color:#64748b; font-size:0.85rem; margin-bottom:12px;'>Showing {len(filtered)} of {len(df)} users</div>", unsafe_allow_html=True)
        st.dataframe(
            filtered.reset_index(drop=True),
            use_container_width=True,
            height=500
        )
