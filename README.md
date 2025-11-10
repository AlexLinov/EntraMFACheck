# EntraMFACheck
Identify Azure AD resources that issue tokens without MFA enforcement using the ROPC grant flow.

[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Azure](https://img.shields.io/badge/Platform-Azure%20AD-blue)]()

---

## Overview

**EntraMFACheck** helps assess conditional access enforcement across Azure AD resources by attempting Resource Owner Password Credential (ROPC) logins against well-known client IDs and resource endpoints.

It detects which resources return tokens **without MFA** and dumps valid access & refresh tokens for further validation (against Microsoft Graph, Outlook, OneDrive, etc.).

**Authorized use only.** This tool is meant for red/purple team testing and internal security validation — not exploitation.

---

## Features
- Tests dozens of **Microsoft cloud resources** for ROPC MFA enforcement.
- Enumerates **client IDs** across resources.
- Dumps **access + refresh tokens** for confirmed MFA-free endpoints.
- Supports **random user-agents** and proxy configuration.
- Colorized output:
  - 🟢 **MFA Not Required** → Token issued  
  - 🔴 **MFA Required** → Enforcement detected  
- Exports results to JSON (`tokens.json`).

## Example Output

```yaml
[+] Scanning 19 resources for MFA enforcement...

[+] Azure Management API: MFA Not Required (Token Issued)
[-] Outlook: MFA Required
[-] Office Apps: MFA Required
[+] Microsoft Graph API: MFA Not Required (Token Issued)

[+] Enumerating client_ids for 2 no-MFA resources...
[TOKEN] Microsoft Graph API <- Microsoft Office
[TOKEN] Azure Management API <- Azure CLI

[+] Tokens and results saved to tokens.json
```
```json
{
  "tokens": [
    {
      "resource": "Microsoft Graph API",
      "client_name": "Microsoft Office",
      "client_id": "d3590ed6-52b3-4102-aeff-aad2292ab01c",
      "aud": "https://graph.microsoft.com",
      "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJ...",
      "refresh_token": "0.AAA..."
    }
  ]
}
```
---
## Credit
https://github.com/absolomb/FindMeAccess

https://github.com/maester365/maester
