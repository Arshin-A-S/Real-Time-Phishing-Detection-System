# Flask API Server
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import tldextract
import whois
import difflib
import requests
import time
from feature_extraction import extract_features

app = Flask(__name__)
CORS(app)  # Allow Chrome Extension to access this

try:
    model = joblib.load(r"C:\Users\arshi\OneDrive\Desktop\Mini Project\Chome Extension\phishing-detection-chrome-extension\phishing-detection-extension\server\model\phishing_model.pkl")
    scaler = joblib.load(r"C:\Users\arshi\OneDrive\Desktop\Mini Project\Chome Extension\phishing-detection-chrome-extension\phishing-detection-extension\server\model\scaler.pkl")
except:
    model, scaler = None, None

# List of trusted domains for comparison
trusted_domains = ['google.com', 'microsoft.com', 'amazon.com', 'facebook.com', 'apple.com']
# Function to check domain reputation from external services (e.g., Google Safe Browsing)
def check_reputation(domain_name):
    try:
        # Google Safe Browsing or similar services can be used here.
        # For illustration, we use a simple API or URL to check reputation.
        response = requests.get(f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key=YOUR_API_KEY", params={"url": domain_name})
        if response.status_code == 200 and 'matches' in response.json():
            return "Suspicious"
        else:
            return "Safe"
    except Exception as e:
        print(f"Error checking reputation: {e}")
        return "Unknown"
    
# Function to check domain via WHOIS information (using creation date)
def check_whois_registration(domain_name):
    try:
        # Use WHOIS to get domain registration info
        domain_info = whois.whois(domain_name)
        creation_date = domain_info.creation_date
        
        if isinstance(creation_date, list):
            creation_date = creation_date[0]  # Some domains have a list of creation dates
        
        # Check domain age
        domain_age = (time.time() - creation_date.timestamp()) / (60 * 60 * 24)  # Age in days
        print(f"Domain age based on WHOIS: {domain_age:.2f} days")
        if domain_age < 30:  # If domain is less than 30 days old, flag it as suspicious
            return "New Domain, suspicious"
        return "Old Domain, safe"
    except Exception as e:
        print(f"Error checking WHOIS registration: {e}")
        return "Unknown"

def is_suspicious(url):
    # Extract domain using tldextract
    ext = tldextract.extract(url)
    domain_name = ext.domain + '.' + ext.suffix  # Combining domain and suffix
    
    if domain_name:
        # Check for typos by comparing the domain to trusted domains
        for trusted_domain in trusted_domains:
            # Calculate similarity ratio using SequenceMatcher
            matcher = difflib.SequenceMatcher(None, domain_name, trusted_domain)
            similarity = matcher.ratio()  # Similarity score between 0 and 1
            
            # If similarity is high, check domain registration
            if similarity < 1.0 and similarity > 0.7:  # Similarity threshold of 70%
                print(f"Suspicious domain detected: {domain_name} -> {trusted_domain} (Similarity: {similarity:.2f})")
                
                # First, check if the domain reputation is flagged by external services
                reputation = check_reputation(domain_name)
                if reputation == "Suspicious":
                    return True
                
                # If WHOIS information is available, check registration age
                whois_check = check_whois_registration(domain_name)
                if whois_check == "New Domain, suspicious":
                    return True

        # Check for dangerous file extensions in URL
        dangerous_extensions = ['.exe', '.bat', '.sh', '.js', '.php']
        if any(url.endswith(ext) for ext in dangerous_extensions):
            return True

        # Check for common phishing-related keywords in the URL path or query parameters
        phishing_keywords = ['login', 'verify', 'update', 'account', 'secure', 'banking', 'signin', 'password']
        if any(keyword in url.lower() for keyword in phishing_keywords):
            print(f"Suspicious URL detected due to phishing keywords: {url}")
            return True
    return False

@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    
    if model is None or scaler is None:
        return jsonify({"error": "Model not loaded"}), 500

    data = request.get_json()
    urls = data.get('urls')
    if not urls or not isinstance(urls, list):
        return jsonify({"error": "No URL provided"}), 400
    
    results = []
    for url in urls:
        if is_suspicious(url):
            results.append({"url": url, "prediction": 1})
            continue
          
        url_features = extract_features(url)

        # Match feature names with training data
        feature_names = [
            "url_length", "num_hyphens", "num_underscores", "num_at", "num_question",
            "num_percent", "num_dots", "num_uppercase", "uppercase_ratio",
            "subdomain_length", "keyword_flag", "encoded_chars", "dot_to_length_ratio"
        ]

        # Create DataFrame with correct column names
        df_features = pd.DataFrame([url_features], columns=feature_names)

        # Ensure the columns are in the correct order
        df_features = df_features[[
            "url_length", "num_hyphens", "num_underscores", "num_at", "num_question",
            "num_percent", "num_dots", "num_uppercase", "uppercase_ratio",
            "subdomain_length", "keyword_flag", "encoded_chars", "dot_to_length_ratio"
        ]]

        # Scale the features before prediction
        scaled_features = scaler.transform(df_features)

        # Make prediction
        prediction = model.predict(scaled_features)[0]

        print("{DEBUG} URL:", url)
        print(f"Extracted Features for {url}: {url_features}")
        print(f"Scaled Features: {scaled_features.tolist()}")
        print("Prediction:", prediction)
        results.append({"url": url, "prediction": int(prediction)})
    return results

if __name__ == "__main__":
    app.run(debug=True)
