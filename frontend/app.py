import streamlit as st
import requests
import pandas as pd
import plotly.express as px

BASE = "https://blood-bank-management-1-nrdt.onrender.com"

st.set_page_config(page_title="Blood Bank", layout="wide")

# ---------- 🎨 ADVANCED CSS ----------
st.markdown("""
<style>

/* Background */
.main {
    background: linear-gradient(135deg, #eef2f7, #f8fafc);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #d72638, #8b0000);
    color: white;
}

section[data-testid="stSidebar"] .css-1d391kg {
    color: white;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Buttons */
.stButton>button {
    width: 100%;
    border-radius: 12px;
    height: 45px;
    background: #d72638;
    color: white;
    font-weight: 600;
}

/* Cards */
.card {
    padding: 18px;
    border-radius: 14px;
    background: white;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.08);
    text-align: center;
}

.metric-title {
    color: gray;
    font-size: 16px;
}

.metric-value {
    font-size: 28px;
    font-weight: bold;
    color: #d72638;
}

</style>
""", unsafe_allow_html=True)

st.title("🩸 Blood Bank Management Dashboard")

# ---------- 🧭 SIDEBAR UPGRADE ----------
st.sidebar.markdown("## 🏥 Navigation Panel")

menu = st.sidebar.radio(
    "",
    ["Dashboard", "Donors", "Requests", "Inventory"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 Manage blood bank efficiently")
st.sidebar.markdown("Made with ❤️ using Streamlit + FastAPI")

# ---------- RESPONSE HANDLER ----------
def handle_response(res):
    try:
        data = res.json()
        if res.status_code == 200:
            st.success(data.get("msg", "Success"))
        else:
            st.error(data.get("detail", "Error occurred"))
    except:
        st.error("Server not responding")


# ---------------- DASHBOARD ----------------
if menu == "Dashboard":
    donors = requests.get(f"{BASE}/donor/all").json()
    reqs = requests.get(f"{BASE}/request/all").json()
    blood = requests.get(f"{BASE}/blood/availability").json()

    col1, col2, col3 = st.columns(3)

    col1.markdown(f"""
    <div class="card">
        <div class="metric-title">👤 Donors</div>
        <div class="metric-value">{len(donors)}</div>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
    <div class="card">
        <div class="metric-title">🆘 Requests</div>
        <div class="metric-value">{len(reqs)}</div>
    </div>
    """, unsafe_allow_html=True)

    col3.markdown(f"""
    <div class="card">
        <div class="metric-title">🩸 Blood Types</div>
        <div class="metric-value">{len(blood)}</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    if donors:
        df = pd.DataFrame(donors)

        col1, col2 = st.columns(2)

        with col1:
            fig = px.pie(df, names="blood_group", hole=0.4)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            blood_df = pd.DataFrame(list(blood.items()), columns=["Group", "Units"])
            fig2 = px.bar(blood_df, x="Group", y="Units", text_auto=True)
            st.plotly_chart(fig2, use_container_width=True)

    st.subheader("⚠️ Low Stock Alerts")
    for grp, units in blood.items():
        if units < 5:
            st.error(f"{grp} is LOW ({units} units left)")


# ---------------- DONORS ----------------
elif menu == "Donors":

    tab1, tab2, tab3 = st.tabs(["➕ Add Donor", "📋 View Donors", "🔍 Search"])

    with tab1:
        col1, col2 = st.columns(2)
        name = col1.text_input("Name")
        group = col2.selectbox("Blood Group", ["A+", "B+", "O-", "AB+"])
        date = st.date_input("Last Donation")

        if st.button("Add Donor"):
            res = requests.post(f"{BASE}/donor/add", json={
                "name": name,
                "blood_group": group,
                "last_donation": str(date)
            })
            handle_response(res)

    with tab2:
        donors = requests.get(f"{BASE}/donor/all").json()
        df = pd.DataFrame(donors)
        st.dataframe(df, use_container_width=True)

    with tab3:
        group = st.selectbox("Select Blood Group", ["A+", "B+", "O-", "AB+"])
        eligible_only = st.checkbox("Show Only Eligible Donors")

        if st.button("Search"):
            if eligible_only:
                data = requests.get(f"{BASE}/donor/eligible").json()
                data = [d for d in data if d["blood_group"] == group]
            else:
                data = requests.get(f"{BASE}/donor/search?blood_group={group}").json()

            st.dataframe(pd.DataFrame(data))


# ---------------- REQUESTS ----------------
elif menu == "Requests":

    tab1, tab2 = st.tabs(["➕ Create Request", "📄 Request List"])

    with tab1:
        patient = st.text_input("Patient Name")
        group = st.selectbox("Blood Group", ["A+", "B+", "O-", "AB+"])
        units = st.number_input("Units", min_value=1)

        if st.button("Submit Request"):
            res = requests.post(f"{BASE}/request/add", json={
                "patient_name": patient,
                "blood_group": group,
                "units": units
            })
            handle_response(res)

    with tab2:
        reqs = requests.get(f"{BASE}/request/all").json()
        df = pd.DataFrame(reqs)
        st.dataframe(df, use_container_width=True)

        st.subheader("Fulfill Request")
        rid = st.number_input("Request ID", min_value=1)

        if st.button("Fulfill"):
            res = requests.put(f"{BASE}/request/fulfill/{rid}")
            handle_response(res)


# ---------------- INVENTORY ----------------
elif menu == "Inventory":

    tab1, tab2 = st.tabs(["➕ Add Blood", "📊 View Stock"])

    with tab1:
        group = st.selectbox("Blood Group", ["A+", "B+", "O-", "AB+"])
        units = st.number_input("Units", min_value=1)

        if st.button("Add Blood"):
            res = requests.post(f"{BASE}/blood/add", json={
                "blood_group": group,
                "units": units
            })
            handle_response(res)

    with tab2:
        blood = requests.get(f"{BASE}/blood/availability").json()
        df = pd.DataFrame(list(blood.items()), columns=["Blood Group", "Units"])

        st.dataframe(df, use_container_width=True)

        fig = px.bar(df, x="Blood Group", y="Units", text_auto=True)
        st.plotly_chart(fig, use_container_width=True)
