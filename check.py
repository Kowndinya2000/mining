import requests
from tokens import *
from requests.auth import HTTPBasicAuth

releases_url = "https://api.github.com/repos/apache/incubator-seatunnel"
flag1 = False
for token in git_tokens:
    if(flag1 == True):
        break
    else:
        try:
            r_id = requests.get(releases_url, auth = HTTPBasicAuth(git_tokens[token], token)).json()
            print(r_id["default_branch"])
            download_url = releases_url + "/" + str(r_id[0]["id"]) + "/assets" 
            download_count = requests.get(download_url, auth = HTTPBasicAuth(git_tokens[token], token)).json()[0]["download_count"]
            flag1 = True
            break
        except:
            continue
if(flag1 == False):
    try:
        r_id = requests.get(releases_url, auth = HTTPBasicAuth(git_tokens[token], token)).json()["id"]
        download_url = releases_url + "/" + str(r_id) + "/assets" 
        download_count = requests.get(download_url, auth = HTTPBasicAuth(git_tokens[token], token)).json()["download_count"]
        print('without token - open issues - fetch ok')
    except:
        download_count = 0
print(download_count)
                    