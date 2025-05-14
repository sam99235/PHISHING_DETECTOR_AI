import requests,base64,os



#api to scan url reputation


API_KEY  = os.getenv('URL_SCANNER_API_KEY')  # Replace with your VirusTotal API key

def scan_url(url,debug=False):
    headers = {
        'x-apikey': API_KEY
    }

    # Endpoint to submit URL for analysis
    scan_url = 'https://www.virustotal.com/api/v3/urls'
    url_id = url.strip().encode('utf-8')  # URL must be encoded in base64 for the API
    url_id = base64.urlsafe_b64encode(url_id).decode().strip("=")

    response = requests.get(f'{scan_url}/{url_id}', headers=headers)

    if response.status_code == 200:
        data = response.json()
        analysis_stats = data['data']['attributes']['last_analysis_stats']
        
        malicious_count = analysis_stats['malicious']
        suspicious_count = analysis_stats['suspicious']
        undetected_count = analysis_stats['undetected']
        if debug:
            print("Scan results for:", url)
            print("Malicious:", malicious_count)
            print("Suspicious:", suspicious_count)
            print("Undetected:", undetected_count)

        # Logic to determine if URL is malicious or suspicious
        if (malicious_count or suspicious_count)>1:
             return True
        else:
            return False
            # print("✅ This URL appears to be CLEAN.")
    else:
            print(f"Error: {response.status_code}")
            print(response.text)

