from utils.domain_utils import extract_domain

trusted_domains = [
    "google.com",
    "youtube.com",
    "github.com",
    "stackoverflow.com",
    "wikipedia.org",
    "microsoft.com",
    "apple.com",
    "amazon.com"
]


def check_domain_reputation(url):

    domain = extract_domain(url)

    for trusted in trusted_domains:
        if domain.endswith(trusted):
            return {
                "status": "trusted",
                "reason": "Known trusted domain"
            }

    return {
        "status": "unknown"
    }