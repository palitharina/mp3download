# import requests
import re
import base64
from urllib.parse import quote, urlparse, parse_qs
import time
import json
from pathlib import Path
from curl_cffi import requests

# session = requests.Session()
session = requests.Session(impersonate="chrome120")
print(
"Public IP:",
requests.get("https://api.ipify.org", timeout=10).text
)

downloads = Path("/tmp")

###########################################################################

# headers = {
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'accept-language': 'en-US,en;q=0.9',
#     'cache-control': 'max-age=0',
#     'priority': 'u=0, i',
#     'referer': 'https://www.google.com/',
#     'sec-ch-ua': '"Google Chrome";v="153", "Not_A Brand";v="8", "Chromium";v="153"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'document',
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-site': 'cross-site',
#     'sec-fetch-user': '?1',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36',
# }

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=0, i',
    'referer': 'https://www.google.com/',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

################# main page, get api key ###################################################################################
response = session.get(
    'https://freemp3juice.com/',
    headers=headers,
    timeout=30
)

print(f"Main page status: {response.status_code}")

html = response.text
match = re.search(r"var\s+apiKey\s*=\s*['\"]([^'\"]+)['\"]", html)

if match:
    api_key = match.group(1)
else:
    raise RuntimeError("API key not found")

print("API Key:", api_key)
        
################### search, get result list ###################################################################################

text = "prinsipal missing felimon"
url_encoded = quote(text, safe='')
encoded = base64.b64encode(url_encoded.encode("utf-8")).decode("ascii")
timestamp = int(time.time() * 1000)

search_headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://freemp3juice.com/',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

response = session.get(
    f'https://freemp3juice.com/s/?api_key={api_key}&y=y&q={encoded}&_={timestamp}',
    headers=search_headers,
    timeout=30
)

print(f"Search page status: {response.status_code}")

data = response.json()
first = data["yt"][0]
resultid = first["id"]
result_title = first["title"]
print("Title:", result_title)
print("ID:", resultid)

################ auth, get bearer ###################################################################################
auth_headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'origin': 'https://freemp3juice.com',
    'priority': 'u=1, i',
    'referer': 'https://freemp3juice.com/',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

params = {
    'api_key': api_key,
    '_': int(time.time() * 1000),
}

# Requesting through curl_cffi session to carry cookies and browser fingerprint
response = session.get(
    "https://theta.thetacloud.org/api/v1/auth",
    params=params,
    headers=auth_headers,
    timeout=30
)

print(f"Auth status: {response.status_code}")
print(response.text[:1000])

exit()

# response.raise_for_status()

data = response.json()

key = data["key"]
#print(f"key :  {key}")


exit()
################# init 1 ###################################################################################
timestamp = int(time.time() * 1000)
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'access-control-request-headers': 'authorization',
    'access-control-request-method': 'GET',
    'origin': 'https://freemp3juice.com',
    'priority': 'u=1, i',
    'referer': 'https://freemp3juice.com/',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36',
}

params = {
    '_': f'{timestamp}',
}

response = requests.options('https://theta.thetacloud.org/api/v1/init', params=params, headers=headers, timeout=30)

print(f" init 1 : {response.status_code}")
# print(f"{response.headers}")
#print(f"key : {api_key}")

########### init 2 ###################################################################################

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': f'Bearer {key}',
    'origin': 'https://freemp3juice.com',
    'priority': 'u=1, i',
    'referer': 'https://freemp3juice.com/',
    'sec-ch-ua': '"Google Chrome";v="153", "Not_A Brand";v="8", "Chromium";v="153"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36',
}

params = {
    '_': f'{timestamp}',
}

response = requests.get('https://theta.thetacloud.org/api/v1/init', params=params, headers=headers, timeout=30)

print(f" init 2 : {response.status_code}")
# print(response.headers)
data = response.json()
convert_url = data["convertURL"]
# print(convert_url)
convert_url = data["convertURL"]
sig = parse_qs(urlparse(convert_url).query)["sig"][0]
# print("sig --------")
# print(sig)

##################### convert 1
timestamp = int(time.time() * 1000)
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'origin': 'https://freemp3juice.com',
    'priority': 'u=1, i',
    'referer': 'https://freemp3juice.com/',
    'sec-ch-ua': '"Google Chrome";v="153", "Not_A Brand";v="8", "Chromium";v="153"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36',
}

params = {
    'sig': f'{sig}',
    'v': f'{resultid}',
    'f': 'mp3',
    '_': f'{timestamp}',
}

response = requests.get('https://cooocc.thetacloud.org/api/v1/convert', params=params, headers=headers, timeout=30)
print(f" convert 1 : {response.status_code}")
# print(response.text)


############## convert 2
download_url=""

timestamp = int(time.time() * 1000)
headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://freemp3juice.com',
        'priority': 'u=1, i',
        'referer': 'https://freemp3juice.com/',
        'sec-ch-ua': '"Google Chrome";v="153", "Not_A Brand";v="8", "Chromium";v="153"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36',
}

params = {
        "sig": sig,
        "v": resultid,
        "f": "mp3",
        "_": str(timestamp),
}

response = requests.get(
        "https://ooocoo.thetacloud.org/api/v1/convert",
        params=params,
        headers=headers,
        timeout=30,
)

print(f" convert 2 : {response.status_code}")
response.raise_for_status()

data = response.json()
if data.get("error") != 0:
    raise RuntimeError(f"Conversion failed: {data}")

if data.get("downloadURL"):
    download_url = data["downloadURL"]
    title = data["title"]

elif data.get("redirect") == 1 and data.get("redirectURL"):
    redirect_url = data["redirectURL"]

    # print("Following redirect:", redirect_url)
    #send get request using the redirect url
    redirect_response = requests.get(
            redirect_url,
            headers=headers,
            timeout=60,
    )

    redirect_response.raise_for_status()

    # print("Redirect status:", redirect_response.status_code)
    # print("Redirect content type:",
    #     redirect_response.headers.get("content-type"))
    # print("Redirect response:", repr(redirect_response.text))

    redirect_data = redirect_response.json()

    download_url = redirect_data.get("downloadURL")
    title = redirect_data["title"]

else:
    raise RuntimeError(f"Unexpected API response: {data}")

if not download_url:
    raise RuntimeError(
            f"API did not provide a download URL. Response: {data}"
    )

print("Downloading...")
file_response = requests.get(
        download_url,
        headers=headers,
        timeout=60,
)

file_response.raise_for_status()

# print("Downloaded:", len(file_response.content), "bytes")

safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
safe_title = safe_title[:100]

#filename = Path("/tmp") / f"{safe_title}.mp3"
filename = downloads / f"{safe_title}.mp3"

####### downloading #######################################
with open(filename, "wb") as f:
    for chunk in file_response.iter_content(chunk_size=1024 * 1024):
        if chunk:
            f.write(chunk)

print(f"Saved to: {filename}")

if filename.exists():
    print("Saved successfully")
    print("Size:", filename.stat().st_size, "bytes")
