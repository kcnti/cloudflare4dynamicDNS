import requests
import json

IP = requests.get("https://ipinfo.io/json").json()["ip"]
ZONE = "zone id"
DOMAIN_NAME = "***"
EMAIL = "your mail"
GLOBAL_KEY = "global key"

def dnsDetails():
    # Get dns record details
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE}/dns_records?type=A&proxied=true&page=1&per_page=20&order=type&direction=desc&match=all"

    header = {
        "X-Auth-Email"  : EMAIL,
        "X-Auth-Key"    : GLOBAL_KEY,
        "Content-Type"  : "application/json"
    }

    dns_dt = requests.get(url, headers=header)
    res_json = dns_dt.json()
    iden_lst = []
    identifer = res_json["result"] # change if there's type A more than 1 before you use this id
    for i in identifer:
        iden_lst.append(i['id'])

    return iden_lst

def dnsUpdater(identifier):
    # Update dns record
    sr = 0
    for id in identifier:
        url = f"https://api.cloudflare.com/client/v4/zones/{ZONE}/dns_records/{id}"

        header = {
            "X-Auth-Email"  : EMAIL,
            "X-Auth-Key"    : GLOBAL_KEY,
            "Content-Type"  : "application/json"
        }

        data = {
            "type"      :   "A",
            # "name"      :   DOMAIN_NAME,
            "content"   :   IP,
            "ttl"       :   1,
            "proxied"   :   True
        }

        r = requests.put(url, headers=header, data=json.dumps(data)).json()
        # print(r["success"])
        if r["success"] == True:
            sr+=1

    return True if sr else False

id = dnsDetails()
update = dnsUpdater(id)

if update:
    print("Success")
else:
    print("Failed")
