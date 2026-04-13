# ==========================================
# NEXRA AI PHISHING DETECTION SYSTEM
# Premium Streamlit Application
# Part 1 - Imports, API, CSS, Header, Buttons
# ==========================================

import streamlit as st
import requests
import time
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

# ==========================================
# API URLs (Recommended: Top of file)
# ==========================================

URL_API = "https://nexra-ai-phishing-detection-tool-5.onrender.com/predict"
QR_API = "https://nexra-ai-phishing-detection-tool-5.onrender.com/predict_qr"

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="NEXRA AI Phishing Detection",
    layout="wide",
    page_icon="🛡️"
)

# ==========================================
# SESSION STATE
# ==========================================

if "mode" not in st.session_state:
    st.session_state.mode = "dark"

if "section" not in st.session_state:
    st.session_state.section = None

if "history" not in st.session_state:
    st.session_state.history = []

# ==========================================
# DARK / LIGHT MODE SWITCH
# ==========================================

col1, col2 = st.columns([9,1])

with col1:
    st.markdown("")

with col2:
    if st.button("🌙"):
        if st.session_state.mode == "dark":
            st.session_state.mode = "light"
        else:
            st.session_state.mode = "dark"

# ==========================================
# CYBER CSS
# ==========================================

if st.session_state.mode == "dark":

    st.markdown("""
    <style>

    body {
        background-color: #0e0e0e;
    }

    .stApp {
        background: linear-gradient(180deg,#000000,#0e0e0e);
        color: white;
    }

    /* cyber grid */
    .stApp:before {
        content: "";
        position: fixed;
        width: 100%;
        height: 100%;
        background-image: 
        linear-gradient(rgba(0,255,255,0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,255,0.05) 1px, transparent 1px);
        background-size: 40px 40px;
        z-index: -1;
    }

    .title {
        text-align:center;
        font-size:60px;
        font-weight:700;
        color:#00f5ff;
        text-shadow:0 0 20px #00f5ff;
    }

    .subtitle {
        text-align:center;
        color:gray;
        font-size:20px;
    }

    .scan-btn {
        padding:20px;
        border-radius:15px;
        background:#111;
        border:1px solid #00f5ff;
        text-align:center;
    }

    </style>
    """, unsafe_allow_html=True)

else:

    st.markdown("""
    <style>

    .stApp {
        background:white;
        color:black;
    }

    .title {
        text-align:center;
        font-size:60px;
        font-weight:700;
        color:#000;
    }

    .subtitle {
        text-align:center;
        color:gray;
        font-size:20px;
    }

    </style>
    """, unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================

st.markdown('<div class="title">NEXRA</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI Phishing Detection System</div>',
    unsafe_allow_html=True
)

st.markdown("<br><br>", unsafe_allow_html=True)

# ==========================================
# PREMIUM BUTTONS (Side by Side)
# ==========================================

col1, col2 = st.columns(2)

with col1:
    if st.button("🌐 Scan URL", use_container_width=True):
        st.session_state.section = "url"

with col2:
    if st.button("📷 Scan QR", use_container_width=True):
        st.session_state.section = "qr"

st.markdown("<br>", unsafe_allow_html=True)
# ==========================================
# URL SCAN SECTION
# ==========================================

if st.session_state.section == "url":

    st.markdown("## 🌐 URL Threat Scanner")

    url = st.text_input("Enter URL to scan")
    if url and not url.startswith("http"):
      url = "https://" + url

    if st.button("Start URL Scan"):

        if url:

            st.markdown("### 🛰️ Initializing Scan...")

            terminal = st.empty()

            # hacker terminal animation
            messages = [
                "Connecting to NEXRA threat intelligence...",
                "Checking domain reputation...",
                "Analyzing SSL certificate...",
                "Scanning phishing database...",
                "Running AI threat model...",
                "Calculating confidence...",
                "Generating report..."
            ]

            for msg in messages:
                terminal.code(msg)
                time.sleep(0.8)

            # ==========================================
            # API CALL WITH RETRY
            # ==========================================
            result = None

            # Auto add https
            if url and not url.startswith("http"):
                url = "https://" + url

            for attempt in range(2):
                try:
                    response = requests.post(
                        URL_API,
                        json={"url": url},
                        timeout=10
                    )

                    if response.status_code == 200:
                        result = response.json()
                        st.write(result)  # remove later (debug)
                        break

                except Exception as e:
                    time.sleep(1)

            # ==============================
            # HANDLE RESPONSE SAFELY
            # ==============================

            if result:

                # API returned error
                if "error" in result:
                    st.error(result["error"])

                # API returned prediction
                elif "result" in result:

                    prediction = result["result"]

                    label = prediction.get("result", "unknown")
                    reason = prediction.get("reason", "No reason provided")
                    prob = prediction.get("probability", 0)

                    confidence = int(prob * 100)

                    if label == "safe":
                        confidence = 100 - confidence

                    st.success("Scan Completed")

                    st.session_state.last_result = {
                        "type": "URL",
                        "target": url,
                        "label": label,
                        "reason": reason,
                        "confidence": confidence
                    }

                    st.session_state.history.append(
                        {
                            "type": "URL",
                            "target": url,
                            "label": label,
                            "confidence": confidence
                        }
                    )

                else:
                    st.error("Unexpected API response format")

            else:
                st.error("API Error: Server not responding")
# ==========================================
# QR SCAN SECTION
# ==========================================

if st.session_state.section == "qr":

    st.markdown("## 📷 QR Threat Scanner")

    file = st.file_uploader("Upload QR Image", type=["png", "jpg", "jpeg"])

    if file:

        st.image(file, width=200)

        if st.button("Start QR Scan"):

            st.markdown("### 🛰️ Initializing QR Scan...")

            terminal = st.empty()

            messages = [
                "Extracting QR data...",
                "Decoding embedded link...",
                "Checking phishing database...",
                "Running AI model...",
                "Analyzing risk score...",
                "Generating report..."
            ]

            for msg in messages:
                terminal.code(msg)
                time.sleep(0.9)

            # ==========================================
            # API CALL
            # ==========================================

            files = {"file": file}

            result = None

            for attempt in range(2):

                try:
                    response = requests.post(
                        QR_API,
                        files=files,
                        timeout=10
                    )

                    if response.status_code == 200:
                        result = response.json()
                        break

                except:
                    time.sleep(1)

            if result:

                extracted = result["extracted_url"]

                prediction = result["prediction"]
                label = prediction["result"]
                reason = prediction["reason"]
                prob = prediction["probability"]

                confidence = int(prob * 100)

                if label == "safe":
                    confidence = 100 - confidence

                st.success("QR Scan Completed")

                st.markdown(
                    f"### 🔗 Extracted URL: [Open Link]({extracted})"
                )

                st.session_state.last_result = {
                    "type": "QR",
                    "target": extracted,
                    "label": label,
                    "reason": reason,
                    "confidence": confidence
                }

                st.session_state.history.append(
                    {
                        "type": "QR",
                        "target": extracted,
                        "label": label,
                        "confidence": confidence
                    }
                )

            else:
                st.error("QR API Error")
# ==========================================
# THREAT DASHBOARD & ANALYTICS
# ==========================================

if "last_result" in st.session_state:

    result = st.session_state.last_result

    st.markdown("## 🧪 Threat Intelligence Dashboard")

    # ==========================================
    # Neon Glowing Threat Ring
    # ==========================================

    status = result["label"]
    confidence = result["confidence"]
    reason = result["reason"]
    target = result["target"]

    if status == "phishing":
        color = "#ff3b3b"
        label_text = "THREAT"
    else:
        color = "#00ffcc"
        label_text = "SAFE"

    fig = go.Figure(go.Pie(
        values=[confidence, 100-confidence],
        hole=0.8,
        marker=dict(colors=[color, "#111"], line=dict(color="#000", width=3)),
        textinfo='none'
    ))

    fig.update_layout(
        showlegend=False,
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        annotations=[
            dict(
                text=f"<b>{confidence}%</b>",
                x=0.5, y=0.55,
                font_size=30,
                showarrow=False
            ),
            dict(
                text=f"{label_text}",
                x=0.5, y=0.42,
                font_size=18,
                font_color=color,
                showarrow=False
            )
        ]
    )

    st.plotly_chart(fig, use_container_width=True)

    # ==========================================
    # Threat Intelligence Details
    # ==========================================

    st.markdown(f"### 🎯 Target: {target}")
    st.markdown(f"**Result:** {status.upper()}")
    st.markdown(f"**Reason:** {reason}")

    # Animated confidence bar
    progress = st.progress(0)
    for i in range(confidence):
        progress.progress(i+1)
        time.sleep(0.01)

# ==========================================
# SCAN HISTORY GRAPHS
# ==========================================

if st.session_state.history:

    st.markdown("## 📊 Scan History")

    df = pd.DataFrame(st.session_state.history)

    # Confidence Line Graph
    st.markdown("### Confidence over Scans")
    line_fig = go.Figure()
    line_fig.add_trace(go.Scatter(
        x=df["target"],
        y=df["confidence"],
        mode="lines+markers",
        line=dict(color="#00ffcc", width=3)
    ))
    line_fig.update_layout(
        xaxis_title="Target",
        yaxis_title="Confidence (%)",
        paper_bgcolor='rgba(0,0,0,0)' if st.session_state.mode=="dark" else 'white',
        plot_bgcolor='rgba(0,0,0,0)' if st.session_state.mode=="dark" else 'white',
        font_color='white' if st.session_state.mode=="dark" else 'black'
    )
    st.plotly_chart(line_fig, use_container_width=True)

    # Safe vs Phishing Bar Chart
    st.markdown("### Safe vs Phishing Count")
    count_df = df.groupby("label").size().reset_index(name='count')
    bar_fig = go.Figure(go.Bar(
        x=count_df["label"],
        y=count_df["count"],
        marker_color=["#00ffcc" if l=="safe" else "#ff3b3b" for l in count_df["label"]]
    ))
    bar_fig.update_layout(
        xaxis_title="Result",
        yaxis_title="Count",
        paper_bgcolor='rgba(0,0,0,0)' if st.session_state.mode=="dark" else 'white',
        plot_bgcolor='rgba(0,0,0,0)' if st.session_state.mode=="dark" else 'white',
        font_color='white' if st.session_state.mode=="dark" else 'black'
    )
    st.plotly_chart(bar_fig, use_container_width=True)

# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div style='text-align:center; opacity:0.6; margin-top:40px;'>
© 2026 NEXRA AI Phishing Detection System | Developed by Team NEXRA
</div>
""", unsafe_allow_html=True)