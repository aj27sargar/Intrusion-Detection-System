import streamlit as st
import pandas as pd
import joblib
from utils import preprocess_data
import matplotlib.pyplot as plt
from twilio.rest import Client
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file

# === SET BACKGROUND IMAGE ===
def set_bg_image():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("");
            background-attachment: fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
set_bg_image()
def send_sms_alert(message_body):
    account_sid = os.getenv("TWILIO_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_number = os.getenv("TWILIO_PHONE")
    target_number = os.getenv("TARGET_PHONE")

    if not all([account_sid, auth_token, twilio_number, target_number]):
        print("🚫 One or more required environment variables are missing.")
        return

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=message_body,
        from_=twilio_number,
        to=target_number
    )

    print("✅ SMS sent! SID:", message.sid)

# === LOGIN FUNCTION ===
def login():
    st.subheader("👤 Login")
    
    # Create a form to get username and password
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            # Check if the credentials are correct (hardcoded for this example)
            if username == "" and password == "":                              #username=admin, password=password123;
                st.session_state["logged_in"] = True
                st.success("🔐 Login Successful!")
            else:
                st.error("❌ Invalid credentials, please try again.")
    
# === CHECK IF USER IS LOGGED IN ===
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    login()  # Show login form if not logged in
else:
    # === LOAD MODEL ===
    model = joblib.load("nids_model.pkl")

    # === APP TITLE ===
    st.title("🔐 Network Intrusion Detection Dashboard")
    st.markdown("Upload a test dataset to detect anomalies using Isolation Forest")

    # === FILE UPLOAD ===
    uploaded_file = st.file_uploader("📁 Upload Test File (e.g., KDDTest+.txt)", type=["txt", "csv"])

    if uploaded_file is not None:
        # Load Data
        df = pd.read_csv(uploaded_file, names=[ 
            'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
            'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins',
            'logged_in', 'num_compromised', 'root_shell', 'su_attempted', 'num_root',
            'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds',
            'is_host_login', 'is_guest_login', 'count', 'srv_count', 'serror_rate',
            'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate', 'same_srv_rate',
            'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count',
            'dst_host_srv_count', 'dst_host_same_srv_rate', 'dst_host_diff_srv_rate',
            'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate',
            'dst_host_serror_rate', 'dst_host_srv_serror_rate', 'dst_host_rerror_rate',
            'dst_host_srv_rerror_rate', 'label', 'difficulty_level'
        ])

        # Preprocess and Predict
        X, y = preprocess_data(df)
        predictions = model.predict(X)
        df['prediction'] = [0 if p == 1 else 1 for p in predictions]  # 1 = normal, 0 = anomaly

        # Create Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["🛰 Network Traffic", "🔐 Protocol Violation", "⚠️ Anomaly Detection", "👤 User Behaviour"])

        # === TAB 1: Network Traffic ===
        with tab1:
            st.header("📡 Network Traffic Overview")
            st.write("Summary statistics of the uploaded network data.")
            st.write(df.describe())

            st.subheader("Top Services Used")
            st.bar_chart(df['service'].value_counts().head(10))

            st.subheader("Bytes Sent vs Received")
            st.line_chart(df[['src_bytes', 'dst_bytes']].head(100))

        # === TAB 2: Protocol Violation ===
        with tab2:
            st.header("🚦 Protocol Violation Detection")
            st.subheader("Protocol Type Usage")
            st.bar_chart(df['protocol_type'].value_counts())

            st.subheader("Flag Type Distribution")
            st.bar_chart(df['flag'].value_counts())

        # === TAB 3: Anomaly Detection ===
        with tab3:
            st.header("⚠️ ML-Based Anomaly Detection")
            st.success("✅ Detection Complete!")

            st.write("### 📊 Anomaly Summary")
            st.bar_chart(df['prediction'].value_counts())

            st.write("### 🔍 Anomaly Records")
            st.dataframe(df[df['prediction'] == 1].head(50))

            # Download CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Full Results CSV", data=csv, file_name="detection_results.csv", mime='text/csv')

            anomalies = df[df['prediction'] == 1]

            if not anomalies.empty:
                # Send SMS alert
                send_sms_alert(f"🚨 ALERT: {len(anomalies)} anomalies detected in your network!")

                st.info("📲 SMS alert sent successfully!")

        # === TAB 4: User Behaviour ===
        with tab4:
            st.header("👤 User Behaviour Analysis")
            st.subheader("Login Success Rate")
            st.bar_chart(df['logged_in'].value_counts())

            st.subheader("Failed Login Attempts (first 100 rows)")
            st.line_chart(df['num_failed_logins'].head(100))

            st.subheader("Guest Login Detection")
            guest_logins = df[df['is_guest_login'] == 1]
            st.write(f"🧑 Guest login attempts: {len(guest_logins)}")
            st.dataframe(guest_logins.head())

# Twilio Function

