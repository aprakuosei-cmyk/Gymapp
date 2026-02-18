import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. APP CONFIGURATION ---
st.set_page_config(
    page_title="Adams Inn Fitness & Gym Centre", 
    page_icon="🏋️‍♂️", 
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #1a1a1a; }
    [data-testid="stMetricValue"] { color: #d4ff00; }
    div.stButton > button { width: 100%; border-radius: 5px; height: 3em; background-color: #d4ff00; color: black; font-weight: bold; border: none; }
    div.stButton > button:hover { background-color: #e6ff66; color: black; }
    h1, h2, h3 { color: #d4ff00; font-family: 'Arial Black', sans-serif; }
    .stTable { background-color: #2d2d2d; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE INITIALIZATION ---
if 'members' not in st.session_state:
    # Starting with some sample data
    st.session_state.members = pd.DataFrame([
        {"Name": "John Doe", "Phone": "+233244123456", "Plan": "Pro ($50)", "Next Payment": "2026-03-01", "Status": "Active"},
        {"Name": "Jane Smith", "Phone": "+233201987654", "Plan": "Elite ($100)", "Next Payment": "2026-02-10", "Status": "Overdue"}
    ])

if 'sales_total' not in st.session_state:
    st.session_state.sales_total = 0.0

if 'goal' not in st.session_state:
    st.session_state.goal = 5000.0

# --- 3. SIDEBAR NAVIGATION & REGISTRATION ---
with st.sidebar:
    st.image("https://via.placeholder.com/150/d4ff00/000000?text=ADAMS+INN", width=150)
    st.title("Management Menu")
    
    with st.expander("📝 Register New Member", expanded=False):
        with st.form("reg_form", clear_on_submit=True):
            new_name = st.text_input("Full Name")
            new_phone = st.text_input("Phone (WhatsApp format)")
            new_plan = st.selectbox("Select Plan", ["Basic ($20)", "Pro ($50)", "Elite ($100)"])
            submit_reg = st.form_submit_button("Add Member")
            
            if submit_reg and new_name and new_phone:
                due_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
                new_entry = {
                    "Name": new_name, "Phone": new_phone, "Plan": new_plan,
                    "Next Payment": due_date, "Status": "Active"
                }
                st.session_state.members = pd.concat([st.session_state.members, pd.DataFrame([new_entry])], ignore_index=True)
                st.success(f"Added {new_name}!")

    st.divider()
    st.session_state.goal = st.number_input("Set Monthly Revenue Goal ($)", value=st.session_state.goal, step=500.0)

# --- 4. MAIN DASHBOARD ---
st.title("🏋️‍♂️ Adams Inn Fitness and Gym Centre")

# Metrics Row
m_revenue = sum([int(p.split('$')[1].replace(')', '')) for p in st.session_state.members['Plan']])
total_income = m_revenue + st.session_state.sales_total

col1, col2, col3, col4 = st.columns(4)
col1.metric("Active Members", len(st.session_state.members))
col2.metric("Membership Rev.", f"${m_revenue}")
col3.metric("Shop Sales", f"${st.session_state.sales_total}")
col4.metric("Total Income", f"${total_income}")

# Goal Progress Bar
st.subheader(f"🎯 Revenue Goal: ${st.session_state.goal}")
progress = min(total_income / st.session_state.goal, 1.0)
st.progress(progress)
st.write(f"{int(progress*100)}% of monthly target reached.")



# --- 5. VISUAL ANALYTICS ---
st.divider()
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # Bar Chart for Revenue Split
    fig_bar = px.bar(
        x=["Memberships", "Shop Sales"], 
        y=[m_revenue, st.session_state.sales_total],
        labels={'x': 'Source', 'y': 'Amount ($)'},
        title="Revenue Source Comparison",
        color_discrete_sequence=['#d4ff00']
    )
    fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig_bar, use_container_width=True)

with chart_col2:
    # Member Plan Distribution
    plan_counts = st.session_state.members['Plan'].value_counts()
    fig_pie = px.pie(
        names=plan_counts.index, 
        values=plan_counts.values, 
        title="Plan Distribution",
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.YlGnBu
    )
    fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig_pie, use_container_width=True)

# --- 6. MEMBER DIRECTORY & SEARCH ---
st.divider()
st.subheader("📋 Member Directory")
search_term = st.text_input("Search members by name...")

df_display = st.session_state.members.copy()
if search_term:
    df_display = df_display[df_display['Name'].str.contains(search_term, case=False)]

# Highlight Overdue Logic
def style_status(row):
    due_date = datetime.strptime(row['Next Payment'], "%Y-%m-%d")
    is_overdue = datetime.now() > due_date
    return ['color: #ff4d4d' if is_overdue else 'color: white'] * len(row)

if not df_display.empty:
    st.dataframe(df_display.style.apply(style_status, axis=1), use_container_width=True)
else:
    st.info("No members found.")

# --- 7. RETAIL SHOP ---
st.divider()
st.subheader("🥤 Supplement & Gear Shop")
shop_col1, shop_col2, shop_col3, shop_col4 = st.columns(4)

with shop_col1:
    if st.button("Sell Water ($1)"):
        st.session_state.sales_total += 1.0
        st.toast("Water Sold!")
with shop_col2:
    if st.button("Sell Protein ($5)"):
        st.session_state.sales_total += 5.0
        st.toast("Protein Shake Sold!")
with shop_col3:
    if st.button("Sell Energy Drink ($3)"):
        st.session_state.sales_total += 3.0
        st.toast("Energy Drink Sold!")
with shop_col4:
    if st.button("Reset Daily Sales"):
        st.session_state.sales_total = 0.0
        st.rerun()

# --- 8. EXPORT & FOOTER ---
st.divider()
st.download_button(
    label="📥 Download Adams Inn Full Report (CSV)",
    data=st.session_state.members.to_csv(index=False),
    file_name=f"Adams_Inn_Report_{datetime.now().strftime('%Y-%m-%d')}.csv",
    mime="text/csv"
)

st.markdown("""
    <div style="text-align: center; padding: 20px; color: #666;">
        <p>© 2026 Adams Inn Fitness and Gym Centre | Built with Python & Streamlit</p>
    </div>
    """, unsafe_allow_html=True)
