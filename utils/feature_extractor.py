import re
import pandas as pd
from urllib.parse import urlparse
from utils.domain_utils import extract_domain

suspicious_words = ['login', 'verify', 'secure', 'account', 'update', 'bank']


def extract_features(url, feature_columns):

    url_length = len(url)
    dot_count = url.count('.')
    has_at = 1 if '@' in url else 0
    has_https = 1 if 'https' in url else 0
    has_ip = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0
    hyphen_count = url.count('-')
    digit_count = sum(c.isdigit() for c in url)
    subdomain_count = max(0, url.count('.') - 1)
    has_query = 1 if '?' in url else 0
    has_path = 1 if '/' in url.replace("http://", "").replace("https://", "") else 0

    domain = extract_domain(url)

    domain_length = len(domain)
    is_short_domain = 1 if domain_length <= 12 else 0

    url_lower = url.lower()
    domain_lower = domain.lower()
    path_lower = urlparse(url).path.lower()

    has_suspicious_word = 1 if any(
        word in url_lower or word in domain_lower or word in path_lower
        for word in suspicious_words
    ) else 0

    features = pd.DataFrame([{
        'url_length': url_length,
        'dot_count': dot_count,
        'subdomain_count': subdomain_count,
        'has_at': has_at,
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

    features = features[feature_columns]

    return features