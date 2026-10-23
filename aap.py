from datetime import datetime
import streamlit as st

# Configure the Streamlit page
st.set_page_config(
    page_title="RentProof - Renter Condition & Repair Tracker",
    page_icon="🏠",
    layout="wide",
)

# Initialize Session State to store mock data in memory
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

# App Header
st.title("🏠 RentProof")
st.caption(
    "A renter-owned record of property condition, maintenance problems, and communication history."
)
st.divider()

# Sidebar Navigation
st.sidebar.header("Navigation")
menu = st.sidebar.selectbox(
    "Go to", ["Dashboard", "Inspection Checklist", "Maintenance Issues"]
)

# ---------------------------------------------------------
# 1. DASHBOARD
# ---------------------------------------------------------
if menu == "Dashboard":
  st.header(f"Property Overview: {st.session_state.property_name}")

  col1, col2 = st.columns(2)
  with col1:
    st.metric("Total Rooms Tracked", len(st.session_state.rooms))
  with col2:
    open_issues = sum(
        1 for i in st.session_state.issues if i["status"] != "Resolved"
    )
    st.metric("Active Maintenance Issues", open_issues)

  st.subheader("Recent Activity & Timeline")
  if not st.session_state.issues:
    st.info("No maintenance issues logged yet.")
  else:
    for issue in st.session_state.issues:
      with st.expander(
          f"[{issue['status']}] {issue['title']} ({issue['room']})"
      ):
        st.write(f"**Logged Date:** {issue['date']}")
        st.write(f"**Notes:** {issue['notes']}")

  st.divider()
  if st.button("📥 Generate Summary Report (PDF Simulation)"):
    st.success(
        "Report generated successfully! (In a production app, this compiles your"
        " checklist and issues into a downloadable PDF)."
    )

# ---------------------------------------------------------
# 2. INSPECTION CHECKLIST
# ---------------------------------------------------------
elif menu == "Inspection Checklist":
  st.header("Room-by-Room Inspection Checklist")

  with st.form("add_room_form"):
    st.subheader("Add a New Room")
    new_room_name = st.text_input(
        "Room Name (e.g., Master Bedroom, Bathroom)"
    )
    new_room_condition = st.text_area(
        "Initial Condition Notes (e.g., walls clean, window latch works)"
    )
    uploaded_photo = st.file_uploader(
        "Upload Condition Photo", type=["jpg", "png", "jpeg"]
    )
    submitted = st.form_submit_button("Add Room Record")

    if submitted and new_room_name:
      st.session_state.rooms.append(
          {"name": new_room_name, "condition": new_room_condition}
      )
      st.success(f"Added {new_room_name} to property records!")

  st.subheader("Current Property Records")
  for idx, room in enumerate(st.session_state.rooms):
    with st.container():
      st.markdown(f"### 🚪 {room['name']}")
      st.write(f"**Condition Notes:** {room['condition']}")
      st.divider()

# ---------------------------------------------------------
# 3. MAINTENANCE ISSUES
# ---------------------------------------------------------
elif menu == "Maintenance Issues":
  st.header("Maintenance Issue Log")

  with st.form("add_issue_form"):
    st.subheader("Log a New Problem")
    issue_room = st.selectbox(
        "Select Room", [r["name"] for r in st.session_state.rooms]
    )
    issue_title = st.text_input(
        "Issue Summary (e.g., Broken window lock, leaking pipe)"
    )
    issue_status = st.selectbox(
        "Current Status", ["Open", "In Progress", "Resolved"]
    )
    issue_notes = st.text_area(
        "Communication & Details (e.g., sent message to landlord on chat)"
    )
    issue_submitted = st.form_submit_button("Log Issue")

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
      st.success("Maintenance issue successfully logged!")

  st.subheader("Logged Issues History")
  if not st.session_state.issues:
    st.info("No issues recorded.")
  else:
    for issue in st.session_state.issues:
      st.markdown(
          f"**Room:** {issue['room']} | **Issue:** {issue['title']} |"
          f" **Status:** `{issue['status']}`"
      )
      st.text(f"Logged on: {issue['date']} — Notes: {issue['notes']}")
      st.divider()
