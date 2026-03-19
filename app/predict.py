import joblib
import pandas as pd
import re
import os
from urllib.parse import urlparse

# ---------- Load Model ----------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model_path = os.path.join(BASE_DIR, "model", "phishing_model.pkl")
columns_path = os.path.join(BASE_DIR, "model", "feature_columns.pkl")

model = joblib.load(model_path)
feature_columns = joblib.load(columns_path)


# ---------- Domain Extraction ----------
def extract_domain(url):

    if not isinstance(url, str) or url.strip() == "":
        return ""

    if not url.startswith(('http://', 'https://')):
        url = "http://" + url

    parsed = urlparse(url)
    domain = parsed.netloc

    # remove phishing trick before domain
    if '@' in domain:
        domain = domain.split('@')[-1]

    return domain


# ---------- Main Prediction Function ----------
def predict_url(url):

    if not isinstance(url, str) or url.strip() == "":
        return {"error": "Invalid URL"}

    url = url.strip()

    # ---------- Feature Extraction ----------

    url_length = len(url)
    dot_count = url.count('.')
    has_https = 1 if 'https' in url else 0
    has_ip = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0
    hyphen_count = url.count('-')
    digit_count = sum(c.isdigit() for c in url)
    subdomain_count = max(0, url.count('.') - 1)
    has_query = 1 if '?' in url else 0
    has_path = 1 if '/' in url.replace("http://","").replace("https://","") else 0

    domain = extract_domain(url)

    domain_length = len(domain)
    is_short_domain = 1 if domain_length <= 12 else 0

    suspicious_words = [
        "login","verify","secure","account","update","bank"
    ]

    url_lower = url.lower()
    has_suspicious_word = 1 if any(word in url_lower for word in suspicious_words) else 0


    # ---------- Rule Based Detection ----------

    # Rule 1: @ phishing trick (ONLY in domain)
    if "@" in urlparse(url).netloc:
        return {
            "result": "phishing",
            "reason": "@ symbol trick in domain",
            "probability": 1.0
        }

    # Rule 2: IP address URL
    if has_ip == 1:
        return {
            "result": "phishing",
            "reason": "IP address used in URL",
            "probability": 1.0
        }

    # Rule 3: suspicious login page
    if has_suspicious_word == 1 and has_query == 1:
        return {
            "result": "phishing",
            "reason": "suspicious login keyword + query",
            "probability": 0.9
        }

    # Rule 4: login page without HTTPS
    if has_suspicious_word == 1 and has_https == 0:
        return {
            "result": "phishing",
            "reason": "login keyword without HTTPS",
            "probability": 0.9
        }

    # Rule 5: too many hyphens
    if hyphen_count >= 2:
        return {
            "result": "phishing",
            "reason": "too many hyphens in URL",
            "probability": 0.8
        }


    # ---------- Trusted Domain Detection ----------

    trusted_domains = [
        "google.com",
        "youtube.com",
        "github.com",
        "stackoverflow.com",
        "wikipedia.org"
    ]

    if domain in trusted_domains or any(domain.endswith("." + td) for td in trusted_domains):
        return {
            "result": "safe",
            "reason": "trusted domain",
            "probability": 0.0
        }


    # ---------- ML Feature DataFrame ----------

    features = pd.DataFrame([{

        'url_length': url_length,
        'dot_count': dot_count,
        'subdomain_count': subdomain_count,
        'has_at': 1 if "@" in urlparse(url).netloc else 0,
        'has_https': has_https,
        'has_ip': has_ip,
        'hyphen_count': hyphen_count,
        'digit_count': digit_count,
        'has_query': has_query,
        'has_path': has_path,
        'has_suspicious_word': has_suspicious_word,
        'domain_length': domain_length,
        'is_short_domain': is_short_domain

    }])

    # Ensure correct feature order
    features = features[feature_columns]


    # ---------- ML Prediction ----------

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]


    # ---------- Final Result ----------

    if prediction == 1:
        return {
            "result": "phishing",
            "probability": float(probability)
        }

    else:
        return {
            "result": "safe",
            "probability": float(probability)
        }