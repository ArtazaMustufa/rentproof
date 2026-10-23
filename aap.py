from datetime import datetime
import streamlit as st

# Configure Streamlit Page
st.set_page_config(
    page_title="RentProof — Renter Condition & Repair Tracker",
    page_icon="🏠",
    layout="wide",
)

# Stunning Modern UI Styling (Custom CSS)
st.markdown(
    """
    <style>
    .main {
        background-color: #f1f5f9;
    }
    /* Force high-contrast dark text everywhere inside the app body */
    p, span, label, div, h1, h2, h3, h4, h5, h6 {
        color: #0f172a !important;
    }
    /* Specifically fix expander header text so it's super clear and dark */
    .streamlit-expanderHeader p {
        color: #0f172a !important;
        font-weight: 600 !important;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 16px;
        border-radius: 14px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
    }
    div.stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white !important;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        border: none;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Initialize Session State for Dynamic Customization
if "property_name" not in st.session_state:
  st.session_state.property_name = "My Rental Property"
if "rooms" not in st.session_state:
  st.session_state.rooms = [
      {"name": "Living Room", "condition": "Clean, minor scuff on baseboard"},
      {"name": "Kitchen", "condition": "Good, small scratch on counter"},
  ]
if "issues" not in st.session_state:
  st.session_state.issues = [
      {
          "id": 1,
          "room": "Kitchen",
          "title": "Leaking faucet under sink",
          "reporter": "Tenant",
          "contact": "Not Provided",
          "date": "2026-10-15",
          "status": "In Progress",
          "notes": "Notified landlord via WhatsApp.",
      }
  ]

# App Header
st.title("🏠 RentProof")
st.markdown(
    "##### ✨ *Your independent record for rental conditions, maintenance logs,"
    " and direct contacts.*"
)
st.divider()

# Sleek Sidebar Navigation & Property Customization
st.sidebar.markdown("### ⚙️ Property Setup")
user_property_input = st.sidebar.text_input(
    "Enter Your Apartment / Property Name", value=st.session_state.property_name
)
if user_property_input:
  st.session_state.property_name = user_property_input

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧭 Navigation Menu")
menu = st.sidebar.radio(
    "Go to",
    ["📊 Dashboard", "🚪 Inspection Checklist", "🛠️ Maintenance Issues"],
    label_visibility="collapsed",
)

if "📊 Dashboard" in menu:
  menu = "Dashboard"
elif "🚪 Inspection Checklist" in menu:
  menu = "Inspection Checklist"
else:
  menu = "Maintenance Issues"

# ---------------------------------------------------------
# 1. DASHBOARD
# ---------------------------------------------------------
if menu == "Dashboard":
  st.header("📍 Property Overview")
  st.subheader(f"*{st.session_state.property_name}*")

  col1, col2, col3 = st.columns(3)
  with col1:
    st.metric(label="🚪 Total Rooms Tracked", value=len(st.session_state.rooms))
  with col2:
    open_issues = sum(
        1 for i in st.session_state.issues if i["status"] != "Resolved"
    )
    st.metric(label="⚠️ Active Issues", value=open_issues)
  with col3:
    st.metric(label="✅ System Status", value="Protected 🛡️")

  st.write("")
  st.subheader("⏱️ Recent Activity & Timeline")

  if not st.session_state.issues:
    st.info("No maintenance issues logged yet.")
  else:
    for issue in st.session_state.issues:
      status_color = (
          "🟡"
          if issue["status"] == "In Progress"
          else ("🟢" if issue["status"] == "Resolved" else "🔴")
      )
      with st.expander(
          f"{status_color} [{issue['status']}] {issue['title']} —"
          f" *{issue['room']}*"
      ):
        st.write(f"👤 **Reported By:** {issue['reporter']}")
        st.write(f"📞 **Contact Number:** `{issue['contact']}`")
        st.write(f"📅 **Logged Date:** {issue['date']}")
        st.write(f"📝 **Details & Notes:** {issue['notes']}")

  st.divider()
  col_rep1, col_rep2 = st.columns([2, 1])
  with col_rep1:
    st.markdown("### 📄 Need an official report?")
    st.write(
        "Compile your room checklist, communication history, and issue details"
        " into a professional timestamped summary for "
        f"*{st.session_state.property_name}*."
    )
  with col_rep2:
    if st.button("📥 Download PDF Report"):
      st.success("Report successfully generated! 🎉")

# ---------------------------------------------------------
# 2. INSPECTION CHECKLIST
# ---------------------------------------------------------
elif menu == "Inspection Checklist":
  st.header("🚪 Room-by-Room Inspection Checklist")
  st.write(
      f"Log move-in conditions for **{st.session_state.property_name}** clearly"
      " to protect your deposit."
  )

  with st.form("add_room_form", clear_on_submit=True):
    st.subheader("➕ Add Room & Inspector Details")

    col_a, col_b = st.columns(2)
    with col_a:
      inspector_name = st.text_input(
          "Your Full Name", placeholder="e.g., Alex Johnson"
      )
    with col_b:
      inspector_contact = st.text_input(
          "Contact Number / WhatsApp", placeholder="e.g., +1 555-0199"
      )

    new_room_name = st.text_input(
        "Room Name", placeholder="e.g., Master Bedroom, Kitchen"
    )
    new_room_condition = st.text_area(
        "Condition Notes",
        placeholder="e.g., Clean floors, minor scuff on left baseboard.",
    )
    uploaded_photo = st.file_uploader(
        "Upload Condition Photo", type=["jpg", "png", "jpeg"]
    )

    submitted = st.form_submit_button("Save Room Record")

    if submitted and new_room_name and inspector_name:
      st.session_state.rooms.append(
          {
              "name": new_room_name,
              "condition": f"{new_room_condition} (Inspected by: {inspector_name} - {inspector_contact})",
          }
      )
      st.success(f"Successfully recorded {new_room_name}! ✨")

  st.divider()
  st.subheader("📋 Current Property Records")

  if not st.session_state.rooms:
    st.info("No rooms added yet.")
  else:
    for room in st.session_state.rooms:
      with st.container():
        st.markdown(f"### 🏠 {room['name']}")
        st.info(f"**Condition & Inspector Info:** {room['condition']}")

# ---------------------------------------------------------
# 3. MAINTENANCE ISSUES
# ---------------------------------------------------------
elif menu == "Maintenance Issues":
  st.header("🛠️ Maintenance Issue Log")
  st.write(
      "Easily document problems, attach your contact details, and maintain an"
      " objective repair trail."
  )

  with st.form("add_issue_form", clear_on_submit=True):
    st.subheader("📝 Report a New Problem")

    col_1, col_2 = st.columns(2)
    with col_1:
      reporter_name = st.text_input(
          "Your Name", placeholder="e.g., Sarah Jenkins"
      )
    with col_2:
      reporter_contact = st.text_input(
          "Your Phone / WhatsApp", placeholder="e.g., +1 (555) 019-2834"
      )

    issue_room = st.selectbox(
        "Select Room", [r["name"] for r in st.session_state.rooms]
    )
    issue_title = st.text_input(
        "Issue Summary", placeholder="e.g., Leaking faucet under sink"
    )
    issue_status = st.selectbox(
        "Current Status", ["Open", "In Progress", "Resolved"]
    )
    issue_notes = st.text_area(
        "Communication & Landlord Response",
        placeholder="e.g., Sent photo via WhatsApp, awaiting plumber callback.",
    )

    issue_submitted = st.form_submit_button("Log Maintenance Issue")

    if issue_submitted and issue_title and reporter_name:
      new_issue = {
          "id": len(st.session_state.issues) + 1,
          "room": issue_room,
          "title": issue_title,
          "reporter": reporter_name,
          "contact": reporter_contact,
          "date": datetime.today().strftime("%Y-%m-%d"),
          "status": issue_status,
          "notes": issue_notes,
      }
      st.session_state.issues.append(new_issue)
      st.success("Maintenance issue successfully logged with your contact! 🚀")

  st.divider()
  st.subheader("📜 Maintenance History & Contact Directory")

  if not st.session_state.issues:
    st.info("No maintenance issues recorded.")
  else:
    for issue in st.session_state.issues:
      status_badge = (
          f"`{issue['status']}`"
          if issue["status"] == "Open"
          else f"**{issue['status']}**"
      )
      st.markdown(
          f"### 🏷️ {issue['title']} ({issue['room']})"
          f" &nbsp;&nbsp;&nbsp;&nbsp; Status: {status_badge}"
      )
      st.caption(
          f"👤 **Reported By:** {issue.get('reporter', 'N/A')} &nbsp;|&nbsp; 📞"
          f" **Contact:** `{issue.get('contact', 'N/A')}` &nbsp;|&nbsp; 📅"
          f" **Date:** {issue['date']}"
      )
      st.write(f"💬 **Notes:** {issue['notes']}")
      st.divider()
