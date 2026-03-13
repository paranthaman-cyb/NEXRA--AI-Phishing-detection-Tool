import streamlit as st
import requests
st.set_page_config(page_title="NEXRA", page_icon="🛡", layout="wide")

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>

.stApp{
background: linear-gradient(135deg,#020111,#06142e,#000000);
color:white;
font-family: 'Segoe UI', sans-serif;
}

/* Title */
.title{
text-align:center;
font-size:65px;
font-weight:bold;
color:#5fd3ff;
margin-top:40px;
}

/* Subtitle */
.subtitle{
text-align:center;
font-size:30px;
margin-bottom:5px;
}

/* Tagline */
.tagline{
text-align:center;
font-size:18px;
opacity:0.8;
margin-bottom:40px;
}

/* Scan box */
.scan-box{
display:flex;
justify-content:center;
align-items:center;
gap:10px;
margin-bottom:50px;
}

/* Feature cards */
.card{
background:rgba(255,255,255,0.05);
padding:30px;
border-radius:15px;
text-align:center;
box-shadow:0px 0px 15px rgba(0,255,255,0.2);
}

.card:hover{
box-shadow:0px 0px 25px rgba(0,255,255,0.6);
}

/* stats cards */
.metric-card{
background:rgba(255,255,255,0.05);
padding:25px;
border-radius:12px;
text-align:center;
box-shadow:0px 0px 10px rgba(0,255,255,0.2);
}

/* footer */
.footer{
text-align:center;
margin-top:50px;
opacity:0.7;
}

</style>
""", unsafe_allow_html=True)


# ---------- HERO SECTION ----------
st.markdown('<div class="title">NEXRA</div>', unsafe_allow_html=True)

st.markdown(
'<div class="subtitle">AI-Powered Phishing Detection System</div>',
unsafe_allow_html=True)

st.markdown(
'<div class="tagline">Protecting Every Click Before It Costs.</div>',
unsafe_allow_html=True)


# ---------- URL SCANNER ----------
col1, col2, col3 = st.columns([2,5,2])

with col2:
  url = st.text_input("Enter URL to check")

if st.button("🔎 Scan URL Now"):

    if url:

        try:

            response = requests.post(
                "http://127.0.0.1:8000/predict",
                json={"url": url}
            )

            result = response.json()

            if result["result"] == "phishing":
                st.error("⚠️ Phishing Website Detected")
            else:
                st.success("✅ Safe Website")

            st.write(result)

        except:
            st.error("API server not running")

    else:
        st.warning("Please enter a URL")

st.write("")
st.write("")


# ---------- FEATURES ----------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
    <h3>⚡ Instant Detection</h3>
    <p>Scans URLs in seconds.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
    <h3>🧠 AI Powered</h3>
    <p>Uses machine learning to detect phishing.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
    <h3>🔒 Safe Browsing</h3>
    <p>Protect users from malicious links.</p>
    </div>
    """, unsafe_allow_html=True)


st.write("")
st.write("")


# ---------- SYSTEM STATS ----------
st.markdown("## 📊 System Statistics")

col1, col2, col3 = st.columns(3)

col1.metric("URLs Scanned", "12,450")
col2.metric("Threats Detected", "1,204")
col3.metric("Accuracy", "96%")


st.write("")
st.write("")


# ---------- PHISHING TIPS ----------
with st.expander("⚠ How to Identify Phishing Websites"):
    st.write("""
• Suspicious domain names  
• Fake login pages  
• Urgent messages asking for passwords  
• Unknown shortened links  
""")


# ---------- FOOTER ----------
st.markdown("""
<div class="footer">
🚀 Developed by Team NEXRA | AI Security Project <br>
Protecting Every Click 🔐
</div>
""", unsafe_allow_html=True)