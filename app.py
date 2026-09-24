import base64
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from pathlib import Path
import re
import sys
import threading
import time
from urllib.parse import parse_qs, quote, urlparse
from curl_cffi import requests

# 1. Android Phone's Tailscale IP & Every Proxy Port
PHONE_TAILSCALE_IP = os.environ.get("PHONE_TAILSCALE_IP", "100.96.38.127")
EVERY_PROXY_PORT = os.environ.get("EVERY_PROXY_PORT", "8080")

# 2. Proxy target: Point directly to Every Proxy on your Android phone
# If using Every Proxy's SOCKS5 option instead of HTTP, change to: f"socks5://{PHONE_TAILSCALE_IP}:1080"
PHONE_PROXY = f"http://{PHONE_TAILSCALE_IP}:{EVERY_PROXY_PORT}"

PROXIES = {
    "http": PHONE_PROXY,
    "https": PHONE_PROXY,
}

downloads = Path("/tmp")


def check_ip(session):
    for attempt in range(1, 6):
        try:
            print(
                f"--> [Attempt {attempt}/5] Checking Exit IP...", flush=True
            )
            res = session.get("https://api.ipify.org?format=json", timeout=10)
            data = res.json()
            print("==========================================", flush=True)
            print(f"   SUCCESSFUL EXIT IP: {data.get('ip')}", flush=True)
            print("==========================================", flush=True)
            return True
        except Exception as e:
            print(
                f"--> Connection attempt failed ({e}), retrying in 3s...",
                flush=True,
            )
            time.sleep(3)
    return False


def make_request():
    time.sleep(3)

    session = requests.Session(impersonate="chrome120", proxies=PROXIES)

    if not check_ip(session):
        print("--> Error: Phone proxy connection failed.", flush=True)
        return

    # Base browser headers for navigating main site
    site_headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Sec-Ch-Ua": (
            '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"'
        ),
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
    }

    try:
        # Step 1: Visit main page and fetch API Key dynamically
        print("--> Step 1: Visiting freemp3juice.com...", flush=True)
        main_resp = session.get(
            "https://freemp3juice.com/", headers=site_headers, timeout=15
        )

        match = re.search(
            r"var\s+apiKey\s*=\s*['\"]([^'\"]+)['\"]", main_resp.text
        )
        if not match:
            print("--> Error: Could not extract apiKey from main page.")
            return

        api_key = match.group(1)
        print(f"--> Extracted API Key: {api_key}", flush=True)

        time.sleep(1)

        # Step 2: Request Auth Endpoint with CORS & Fetch Metadata Headers
        api_headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Origin": "https://freemp3juice.com",
            "Referer": "https://freemp3juice.com/",
            "Sec-Ch-Ua": (
                '"Not_A Brand";v="8", "Chromium";v="120", "Google'
                ' Chrome";v="120"'
            ),
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
        }

        params = {"api_key": api_key, "_": int(time.time() * 1000)}

        print(
            "--> Step 2: Requesting theta.thetacloud.org auth endpoint...",
            flush=True,
        )
        response = session.get(
            "https://theta.thetacloud.org/api/v1/auth",
            params=params,
            headers=api_headers,
            timeout=20,
        )

        print(f"--> Status Code: {response.status_code}", flush=True)
        print(f"--> Response Body: {response.text[:300]}", flush=True)

    except Exception as e:
        print(f"Request failed: {e}", flush=True)


class HealthCheckHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format, *args):
        return


def start_render_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()


if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    worker_thread = threading.Thread(target=make_request, daemon=True)
    worker_thread.start()
    start_render_health_server()

# # import requests
# import re
# import base64
# from urllib.parse import quote, urlparse, parse_qs
# import time
# import json
# from pathlib import Path
# from curl_cffi import requests

# # session = requests.Session()
# session = requests.Session(impersonate="chrome120")
# print(
# "Public IP:",
# requests.get("https://api.ipify.org", timeout=10).text
# )

# downloads = Path("/tmp")

# ###########################################################################

# # headers = {
# #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
# #     'accept-language': 'en-US,en;q=0.9',
# #     'cache-control': 'max-age=0',
# #     'priority': 'u=0, i',
# #     'referer': 'https://www.google.com/',
# #     'sec-ch-ua': '"Google Chrome";v="153", "Not_A Brand";v="8", "Chromium";v="153"',
# #     'sec-ch-ua-mobile': '?0',
# #     'sec-ch-ua-platform': '"Windows"',
# #     'sec-fetch-dest': 'document',
# #     'sec-fetch-mode': 'navigate',
# #     'sec-fetch-site': 'cross-site',
# #     'sec-fetch-user': '?1',
# #     'upgrade-insecure-requests': '1',
# #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36',
# # }

# headers = {
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
#     'accept-language': 'en-US,en;q=0.9',
#     'priority': 'u=0, i',
#     'referer': 'https://www.google.com/',
#     'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'document',
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-site': 'cross-site',
#     'sec-fetch-user': '?1',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
# }

# ################# main page, get api key ###################################################################################
# response = session.get(
#     'https://freemp3juice.com/',
#     headers=headers,
#     timeout=30
# )

# print(f"Main page status: {response.status_code}")

# html = response.text
# match = re.search(r"var\s+apiKey\s*=\s*['\"]([^'\"]+)['\"]", html)

# if match:
#     api_key = match.group(1)
# else:
#     raise RuntimeError("API key not found")

# print("API Key:", api_key)
        
# ################### search, get result list ###################################################################################

# text = "prinsipal missing felimon"
# url_encoded = quote(text, safe='')
# encoded = base64.b64encode(url_encoded.encode("utf-8")).decode("ascii")
# timestamp = int(time.time() * 1000)

# search_headers = {
#     'accept': '*/*',
#     'accept-language': 'en-US,en;q=0.9',
#     'priority': 'u=1, i',
#     'referer': 'https://freemp3juice.com/',
#     'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-origin',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
# }

# response = session.get(
#     f'https://freemp3juice.com/s/?api_key={api_key}&y=y&q={encoded}&_={timestamp}',
#     headers=search_headers,
#     timeout=30
# )

# print(f"Search page status: {response.status_code}")

# data = response.json()
# first = data["yt"][0]
# resultid = first["id"]
# result_title = first["title"]
# print("Title:", result_title)
# print("ID:", resultid)

# ################ auth, get bearer ###################################################################################
# auth_headers = {
#     'accept': '*/*',
#     'accept-language': 'en-US,en;q=0.9',
#     'origin': 'https://freemp3juice.com',
#     'referer': 'https://freemp3juice.com/',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'cross-site',
# }

# auth_params = {
#     'api_key': api_key,
#     '_': int(time.time() * 1000)
# }

# auth_resp = session.get(
#     "https://theta.thetacloud.org/api/v1/auth",
#     params=auth_params,
#     headers=auth_headers,
#     timeout=30
# )

# print(f"Auth Endpoint Status Code: {auth_resp.status_code}")

# # Check content type before parsing JSON to prevent JSONDecodeError crashes
# content_type = auth_resp.headers.get("Content-Type", "")
# if auth_resp.status_code == 200 and "application/json" in content_type:
#     auth_data = auth_resp.json()
#     bearer_token = auth_data.get("key")
#     print("Successfully retrieved Bearer Token:", bearer_token)
# else:
#     print("Error Payload Received (HTML/Blocked):")
#     print(auth_resp.text[:300])  # Prints initial HTML error output

# exit()
# auth_headers = {
#     'accept': '*/*',
#     'accept-language': 'en-US,en;q=0.9',
#     'origin': 'https://freemp3juice.com',
#     'priority': 'u=1, i',
#     'referer': 'https://freemp3juice.com/',
#     'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'cross-site',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
# }

# params = {
#     'api_key': api_key,
#     '_': int(time.time() * 1000),
# }

# # Requesting through curl_cffi session to carry cookies and browser fingerprint
# response = session.get(
#     "https://theta.thetacloud.org/api/v1/auth",
#     params=params,
#     headers=auth_headers,
#     timeout=30
# )

# print(f"Auth status: {response.status_code}")
# print(response.text[:1000])

# exit()

# # response.raise_for_status()

# data = response.json()

# key = data["key"]
# #print(f"key :  {key}")


# exit()
# ################# init 1 ###################################################################################
# timestamp = int(time.time() * 1000)
# headers = {
#     'accept': '*/*',
#     'accept-language': 'en-US,en;q=0.9',
#     'access-control-request-headers': 'authorization',
#     'access-control-request-method': 'GET',
#     'origin': 'https://freemp3juice.com',
#     'priority': 'u=1, i',
#     'referer': 'https://freemp3juice.com/',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'cross-site',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36',
# }

# params = {
#     '_': f'{timestamp}',
# }

# response = requests.options('https://theta.thetacloud.org/api/v1/init', params=params, headers=headers, timeout=30)

# print(f" init 1 : {response.status_code}")
# # print(f"{response.headers}")
# #print(f"key : {api_key}")

# ########### init 2 ###################################################################################

# headers = {
#     'accept': '*/*',
#     'accept-language': 'en-US,en;q=0.9',
#     'authorization': f'Bearer {key}',
#     'origin': 'https://freemp3juice.com',
#     'priority': 'u=1, i',
#     'referer': 'https://freemp3juice.com/',
#     'sec-ch-ua': '"Google Chrome";v="153", "Not_A Brand";v="8", "Chromium";v="153"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'cross-site',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36',
# }

# params = {
#     '_': f'{timestamp}',
# }

# response = requests.get('https://theta.thetacloud.org/api/v1/init', params=params, headers=headers, timeout=30)

# print(f" init 2 : {response.status_code}")
# # print(response.headers)
# data = response.json()
# convert_url = data["convertURL"]
# # print(convert_url)
# convert_url = data["convertURL"]
# sig = parse_qs(urlparse(convert_url).query)["sig"][0]
# # print("sig --------")
# # print(sig)

# ##################### convert 1
# timestamp = int(time.time() * 1000)
# headers = {
#     'accept': '*/*',
#     'accept-language': 'en-US,en;q=0.9',
#     'origin': 'https://freemp3juice.com',
#     'priority': 'u=1, i',
#     'referer': 'https://freemp3juice.com/',
#     'sec-ch-ua': '"Google Chrome";v="153", "Not_A Brand";v="8", "Chromium";v="153"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'cross-site',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36',
# }

# params = {
#     'sig': f'{sig}',
#     'v': f'{resultid}',
#     'f': 'mp3',
#     '_': f'{timestamp}',
# }

# response = requests.get('https://cooocc.thetacloud.org/api/v1/convert', params=params, headers=headers, timeout=30)
# print(f" convert 1 : {response.status_code}")
# # print(response.text)


# ############## convert 2
# download_url=""

# timestamp = int(time.time() * 1000)
# headers = {
#         'accept': '*/*',
#         'accept-language': 'en-US,en;q=0.9',
#         'origin': 'https://freemp3juice.com',
#         'priority': 'u=1, i',
#         'referer': 'https://freemp3juice.com/',
#         'sec-ch-ua': '"Google Chrome";v="153", "Not_A Brand";v="8", "Chromium";v="153"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"Windows"',
#         'sec-fetch-dest': 'empty',
#         'sec-fetch-mode': 'cors',
#         'sec-fetch-site': 'cross-site',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36',
# }

# params = {
#         "sig": sig,
#         "v": resultid,
#         "f": "mp3",
#         "_": str(timestamp),
# }

# response = requests.get(
#         "https://ooocoo.thetacloud.org/api/v1/convert",
#         params=params,
#         headers=headers,
#         timeout=30,
# )

# print(f" convert 2 : {response.status_code}")
# response.raise_for_status()

# data = response.json()
# if data.get("error") != 0:
#     raise RuntimeError(f"Conversion failed: {data}")

# if data.get("downloadURL"):
#     download_url = data["downloadURL"]
#     title = data["title"]

# elif data.get("redirect") == 1 and data.get("redirectURL"):
#     redirect_url = data["redirectURL"]

#     # print("Following redirect:", redirect_url)
#     #send get request using the redirect url
#     redirect_response = requests.get(
#             redirect_url,
#             headers=headers,
#             timeout=60,
#     )

#     redirect_response.raise_for_status()

#     # print("Redirect status:", redirect_response.status_code)
#     # print("Redirect content type:",
#     #     redirect_response.headers.get("content-type"))
#     # print("Redirect response:", repr(redirect_response.text))

#     redirect_data = redirect_response.json()

#     download_url = redirect_data.get("downloadURL")
#     title = redirect_data["title"]

# else:
#     raise RuntimeError(f"Unexpected API response: {data}")

# if not download_url:
#     raise RuntimeError(
#             f"API did not provide a download URL. Response: {data}"
#     )

# print("Downloading...")
# file_response = requests.get(
#         download_url,
#         headers=headers,
#         timeout=60,
# )

# file_response.raise_for_status()

# # print("Downloaded:", len(file_response.content), "bytes")

# safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
# safe_title = safe_title[:100]

# #filename = Path("/tmp") / f"{safe_title}.mp3"
# filename = downloads / f"{safe_title}.mp3"

# ####### downloading #######################################
# with open(filename, "wb") as f:
#     for chunk in file_response.iter_content(chunk_size=1024 * 1024):
#         if chunk:
#             f.write(chunk)

# print(f"Saved to: {filename}")

# if filename.exists():
#     print("Saved successfully")
#     print("Size:", filename.stat().st_size, "bytes")
