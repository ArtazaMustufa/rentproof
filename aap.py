from datetime import datetime
import streamlit as st

# Configure the Streamlit page
st.set_page_config(
    page_title="RentProof — Renter Condition & Repair Tracker",
    page_icon="🏠",
    layout="wide",
)

# Custom CSS for modern styling, clean cards, and nice typography
st.markdown(
    """
    <style>
    .main {
        background-color: #f8fafc;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    .css-1544g2n {
        padding-top: 2rem;
    }
    div.stButton > button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #1d4ed8;
        color: white;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Initialize Session State
if "property_name" not in st.session_state:
    st.session_state.property_name = "Apartment 4B, Maple Street"
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
            "date": "2026-10-15",
            "status": "In Progress",
            "notes": "Notified landlord via WhatsApp.",
        }
    ]

# App Header with nicer visual presentation
st.title("🏠 RentProof")
st.markdown(
    "##### *Your independent record for rental conditions, maintenance, and"
    " landlord chats.*"
)
st.divider()

# Sidebar Navigation with friendly icons
st.sidebar.markdown("### 🧭 Menu")
menu = st.sidebar.radio(
    "Go to",
    ["📊 Dashboard", "🚪 Inspection Checklist", "🛠️ Maintenance Issues"],
    label_visibility="collapsed",
)

# Clean up sidebar text selection
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
  st.header(f"📍 Property Overview")
  st.subheader(f"*{st.session_state.property_name}*")
  format_space = st.empty()

  col1, col2, col3 = st.columns(3)
  with col1:
    st.metric(
        label="🚪 Total Rooms Tracked", value=len(st.session_state.rooms)
    )
  with col2:
    open_issues = sum(
        1 for i in st.session_state.issues if i["status"] != "Resolved"
    )
    st.metric(label="⚠️ Active Issues", value=open_issues)
  with col3:
    st.metric(label="✅ Status", value="Protected 🛡️")

  st.write("")
  st.subheader("⏱️ Recent Activity & Timeline")

  if not st.session_state.issues:
    st.info(
        "No maintenance issues logged yet. Head over to the Maintenance tab to"
        " add one!"
    )
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
        st.write(f"📅 **Logged Date:** {issue['date']}")
        st.write(f"📝 **Notes & History:** {issue['notes']}")

  st.divider()

  col_report1, col_report2 = st.columns([2, 1])
  with col_report1:
    st.markdown("### Need to share your records?")
    st.write(
        "Generate a clean, official timeline PDF report of all your checked"
        " rooms and unresolved issues to send to your landlord or housing"
        " authority."
    )
  with col_report2:
    if st.button("📥 Download PDF Report"):
      st.success("Report successfully compiled and downloaded! 🎉")

# ---------------------------------------------------------
# 2. INSPECTION CHECKLIST
# ---------------------------------------------------------
elif menu == "Inspection Checklist":
  st.header("🚪 Room-by-Room Inspection Checklist")
  st.write(
      "Document the exact condition of each room when you move in so there's"
      " never a dispute later."
  )

  with st.form("add_room_form", clear_on_submit=True):
    st.subheader("➕ Add a New Room")
    new_room_name = st.text_input(
        "Room Name", placeholder="e.g., Master Bedroom, Guest Bathroom"
    )
    new_room_condition = st.text_area(
        "Condition Notes",
        placeholder="e.g., Walls are freshly painted, minor scratch near door"
        " frame.",
    )
    uploaded_photo = st.file_uploader(
        "Upload Photo Evidence", type=["jpg", "png", "jpeg"]
    )
    submitted = st.form_submit_button("Save Room Record")

    if submitted and new_room_name:
      st.session_state.rooms.append(
          {"name": new_room_name, "condition": new_room_condition}
      )
      st.success(f"Successfully added {new_room_name} to your records! ✨")

  st.divider()
  st.subheader("📋 Current Property Records")

  if not st.session_state.rooms:
    st.info("No rooms added yet.")
  else:
    for room in st.session_state.rooms:
      with st.container():
        st.markdown(f"### 🏠 {room['name']}")
        st.info(f"**Condition Notes:** {room['condition']}")
        st.write("")

# ---------------------------------------------------------
# 3. MAINTENANCE ISSUES
# ---------------------------------------------------------
elif menu == "Maintenance Issues":
  st.header("🛠️ Maintenance Issue Log")
  st.write(
      "Keep an objective timeline of problems, when you reported them, and how"
      " the landlord responded."
  )

  with st.form("add_issue_form", clear_on_submit=True):
    st.subheader("📝 Log a New Problem")
    issue_room = st.selectbox(
        "Select Room", [r["name"] for r in st.session_state.rooms]
    )
    issue_title = st.text_input(
        "Issue Summary", placeholder="e.g., AC unit leaking water in bedroom"
    )
    issue_status = st.selectbox(
        "Current Status", ["Open", "In Progress", "Resolved"]
    )
    issue_notes = st.text_area(
        "Communication & Details",
        placeholder="e.g., Sent WhatsApp photo to property manager at 2:00 PM.",
    )
    issue_submitted = st.form_submit_button("Log Maintenance Issue")

    if issue_submitted and issue_title:
      new_issue = {
          "id": len(st.session_state.issues) + 1,
          "room": issue_room,
          "title": issue_title,
          "date": datetime.today().strftime("%Y-%m-%d"),
          "status": issue_status,
          "notes": issue_notes,
      }
      st.session_state.issues.append(new_issue)
      st.success("Issue successfully logged to your timeline! 🚀")

  st.divider()
  st.subheader("📜 Maintenance History")

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
          f"📅 Reported on: {issue['date']} &nbsp;|&nbsp; 💬 Details:"
          f" {issue['notes']}"
      )
      st.divider()
