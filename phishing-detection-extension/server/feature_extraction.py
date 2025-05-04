import tldextract


def extract_features(url):
    ext = tldextract.extract(url)
    sum_upper = sum(1 for ch in url if ch.isupper())
    subdomain_length = len(ext.subdomain)
    phishing_keywords = ["secure", "account", "login", "bank", "verify", "update"]
    keyword_flag = int(any(word in url.lower() for word in phishing_keywords))

    encoded_chars = url.count("%")
    dot_to_length_ratio = url.count('.') / len(url)

    return [
        len(url),
        url.count('-'),
        url.count('_'),
        url.count('@'),
        url.count('?'),
        url.count('%'),
        url.count('.'),
        sum_upper,
        sum_upper / len(url),
        subdomain_length,
        keyword_flag,
        encoded_chars,
        dot_to_length_ratio
    ]
