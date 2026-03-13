import re

suspicious_words = ['login', 'verify', 'secure', 'account', 'update', 'bank']


def rule_based_detection(url):

    if '@' in url:
        return "Phishing detected (@ symbol trick)"

    if re.search(r'\d+\.\d+\.\d+\.\d+', url):
        return "Phishing detected (IP address in URL)"

    if url.count('-') >= 2:
        return "Suspicious URL (too many hyphens)"

    url_lower = url.lower()

    if any(word in url_lower for word in suspicious_words) and '?' in url:
        return "Suspicious login page with query"

    if any(word in url_lower for word in suspicious_words) and "https" not in url:
        return "Login page without HTTPS"

    return None