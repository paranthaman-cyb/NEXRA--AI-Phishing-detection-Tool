from urllib.parse import urlparse

def extract_domain(url):

    if not isinstance(url, str) or url.strip() == "":
        return ""

    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)
    domain = parsed.netloc

    # phishing trick using @
    if "@" in domain:
        domain = domain.split("@")[-1]

    # remove IPv6 brackets
    domain = domain.replace("[", "").replace("]", "")

    return domain