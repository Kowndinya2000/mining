from tokens import *
import os
import sys
import time
from requests.auth import HTTPBasicAuth
import multiprocessing
from bs4 import BeautifulSoup
import requests
import os as inner_os
import sqlite3

from subprocess import Popen, PIPE
# https://api.github.com/repos/apache/incubator-seatunnel/contributors?per_page=1&anon=true
def community():
    try:
        num_core_contributors = 0
        num_commits = 0
        commitList = []
        os.chdir(root_directory)
        os.chdir("path/"+str(repo_id)+"/")
        stream = []
        for repos in os.listdir():
            if(repos == repoName):
                os.chdir(repos)
                with Popen(r'git log --pretty="%ae" | sort',shell=True,
                    stdout=PIPE, stderr=PIPE) as p:
                    output, errors = p.communicate()
                stream = output.decode('utf-8-sig',errors='ignore').splitlines()
                unique_words = set(stream)
                for words in unique_words :
                    stream.count(words)
                    commitList.append(int(stream.count(words)))
                    num_commits += int(stream.count(words))
                break
        num_core_contributors = len(commitList)
        if(num_core_contributors > 0):
            os.chdir(root_directory)
            val = (str(num_core_contributors), str(num_commits),repo_id)
            QUERY = '''UPDATE `mining_results` SET `community`=?, `commits` =? WHERE `repo_id`=?'''
            try:
                os.chdir(root_directory)
                conn = sqlite3.connect('mining.db',timeout=180)
                conn.execute(QUERY,val)
                conn.commit()
                print("Contributors: ",num_core_contributors, " Commits: ",num_commits)
                conn.close()
            except Exception as ex:
                print(ex)
                os.chdir(root_directory)
                conn = sqlite3.connect('mining.db',timeout=180)
                conn.execute(QUERY,val)
                conn.commit()
                print("[Tried again.. OK]Contributors: ",num_core_contributors, " Commits: ",num_commits)
                conn.close()
    except Exception as ex:
        print(ex)

def downloads():
    os.chdir(root_directory)
    try:
        os.chdir(root_directory)
        download_count = 0
        releases_url = URL + "/releases"
        flag1 = False
        for token in git_tokens:
            if(flag1 == True):
                break
            else:
                try:
                    r_id = requests.get(releases_url, auth = HTTPBasicAuth(git_tokens[token], token)).json()[0]["id"]
                    download_url = releases_url + "/" + str(r_id) + "/assets" 
                    download_count = requests.get(download_url, auth = HTTPBasicAuth(git_tokens[token], token)).json()[0]["download_count"]
                    flag1 = True
                    break
                except:
                    continue
        if(flag1 == False):
            try:
                r_id = requests.get(releases_url, auth = HTTPBasicAuth(git_tokens[token], token)).json()[0]["id"]
                download_url = releases_url + "/" + str(r_id) + "/assets" 
                download_count = requests.get(download_url, auth = HTTPBasicAuth(git_tokens[token], token)).json()[0]["download_count"]
                print('without token - open issues - fetch ok')
            except:
                download_count = 0
        if(download_count > 0):
            val = (str(download_count),repo_id)
            QUERY = '''UPDATE `mining_results` SET `downloads`=? WHERE `repo_id`=?'''
            try:
                os.chdir(root_directory)
                conn = sqlite3.connect('mining.db',timeout=180)
                conn.execute(QUERY,val)
                conn.commit()
                print('Downloads: ',download_count)
                conn.close()
            except Exception as ex:
                print(ex)
                os.chdir(root_directory)
                conn = sqlite3.connect('mining.db',timeout=180)
                conn.execute(QUERY,val)
                conn.commit()
                print('Downloads: ',download_count,' >> trying again.. ok')
                conn.close()
    except Exception as ex:
        print(ex)
def issuesFunc():
    openIssues = 0
    closedIssues = 0
    totalIssues = 0
    try:
        open_url = URL.replace("api.","").replace("repos/","") + "/issues?q=is%3Aopen+is%3Aissue"
        closed_url = URL.replace("api.","").replace("repos/","") + "/issues?q=is%3Aissue+is%3Aclosed"
        flag1 = False
        for token in git_tokens:
            if(flag1 == True):
                break
            else:
                try:
                    r = requests.get(open_url, auth = HTTPBasicAuth(git_tokens[token], token))
                    dom = BeautifulSoup(r.content,'html5lib')
                    openIssues = int(dom.body.find_all('a',class_='btn-link selected')[0].text.replace("\n","").split("Open")[0])
                    flag1 = True
                    break
                except:
                    continue
        if(flag1 == False):
            try:
                r = requests.get(open_url)
                dom = BeautifulSoup(r.content,'html5lib')
                openIssues = int(dom.body.find_all('a',class_='btn-link selected')[0].text.replace("\n","").split("Open")[0])
                print('without token - open issues - fetch ok')
            except:
                print("")
        flag2 = False
        for token in git_tokens:
            if(flag2 == True):
                break
            else:
                try:
                    r = requests.get(closed_url, auth = HTTPBasicAuth(git_tokens[token], token))
                    dom = BeautifulSoup(r.content,'html5lib')
                    closedIssues = int(dom.body.find_all('a',class_='btn-link selected')[0].text.replace("\n","").split("Closed")[0])
                    flag2 = True
                    break
                except:
                    continue
        if(flag2 == False):
            try:
                r = requests.get(closed_url)
                dom = BeautifulSoup(r.content,'html5lib')
                closedIssues = int(dom.body.find_all('a',class_='btn-link selected')[0].text.replace("\n","").split("Closed")[0])
                print('without token - closed issues - fetch ok')
            except:
                print("")
        totalIssues = openIssues + closedIssues
        val = (str(openIssues), str(closedIssues), str(totalIssues),repo_id)
        QUERY = '''UPDATE `mining_results` SET `open_issues`=?, `closed_issues`=?, `total_issues`=? WHERE `repo_id`=?'''
        try:
            os.chdir(root_directory)
            conn = sqlite3.connect('mining.db',timeout=180)
            conn.execute(QUERY,val)
            conn.commit()
            conn.close()
            print('Open Issues: ',openIssues, "Closed Issues: ", closedIssues)
        except Exception as ex:
            print(ex)
            os.chdir(root_directory)
            conn = sqlite3.connect('mining.db',timeout=180)
            conn.execute(QUERY,val)
            conn.commit()
            conn.close()
            print('Open Issues: ',openIssues, "Closed Issues: ", closedIssues,'trying again.. ok')
    except Exception as ex:
        print(ex)
def getReadmeFileName():
    os.chdir(root_directory)
    os.chdir("path/"+repo_id+"/")
    for repos in os.listdir():
        if(repos == repoName):
            os.chdir(repos)
            for files in inner_os.listdir():
                if("readme.md" == files.lower()):   
                    return files 
    return "" 
def getbranch():
    flag1 = False
    branch = ""
    for token in git_tokens:
        if(flag1 == True):
            break
        else:
            try:
                branch = requests.get(URL, auth = HTTPBasicAuth(git_tokens[token], token)).json()["default_branch"]
                flag1 = True
                break
            except:
                continue
    if(flag1 == False):
        try:
            branch = requests.get(URL, auth = HTTPBasicAuth(git_tokens[token], token)).json()["default_branch"]
        except:
            print("")
    return branch
def issue_looper():
    getIssues = 0
    historyURL = URL.replace("api.","").replace("repos/","") + "/commits/" + getbranch() + "/" + getReadmeFileName()
    print("historyURL: ",historyURL)
    getIssues += readme_issues(historyURL)
    try:
        flag1 = False
        for token in git_tokens:
            if(flag1 == True):
                break
            else:
                try:
                    r = requests.get(historyURL, auth = HTTPBasicAuth(git_tokens[token], token))
                    dom = BeautifulSoup(r.content,'html5lib')
                    anchors  = dom.body.find_all('a')
                    for a in anchors:
                        if(a.text == "Older"):
                            print("One extra loop inside", a["href"])
                            getIssues += readme_issues(a["href"])
                    flag1 = True
                    break
                except:
                    continue
        if(flag1 == False):
            try:
                r = requests.get(historyURL, auth = HTTPBasicAuth(git_tokens[token], token))
                dom = BeautifulSoup(r.content,'html5lib')
                anchors  = dom.body.find_all('a')
                for a in anchors:
                    if(a.text == "Older"):
                        print("Inside", a["href"])
                        getIssues += readme_issues(a["href"])
            except:
                print("")
        if(getIssues > 0):
            val = (str(getIssues),repo_id)
            QUERY = '''UPDATE `mining_results` SET `readme_issues`=? WHERE `repo_id`=?'''
            try:
                os.chdir(root_directory)
                conn = sqlite3.connect('mining.db',timeout=180)
                conn.execute(QUERY,val)
                conn.commit()
                conn.close()
                print("Readme Issues: ",getIssues)
            except Exception as ex:
                os.chdir(root_directory)
                conn = sqlite3.connect('mining.db',timeout=180)
                conn.execute(QUERY,val)
                conn.commit()
                conn.close()
                print("Readme Issues: ",getIssues,' trying again.. ok')
    except:
        print("")       
def readme_issues(history_url):
    getIssues = 0
    try:
        flag1 = False
        for token in git_tokens:
            if(flag1 == True):
                break
            else:
                try:
                    r = requests.get(history_url, auth = HTTPBasicAuth(git_tokens[token], token))
                    dom = BeautifulSoup(r.content,'html5lib')
                    anchors  = dom.body.find_all('a')
                    for a in anchors:
                        if(github_url + "/issues/" in a["href"]):
                            getIssues += 1            
                    flag1 = True
                    break
                except:
                    continue
        if(flag1 == False):
            try:
                r = requests.get(history_url, auth = HTTPBasicAuth(git_tokens[token], token))
                dom = BeautifulSoup(r.content,'html5lib')
                anchors  = dom.body.find_all('a')
                for a in anchors:
                    if(github_url + "/issues/" in a["href"]):
                        getIssues += 1
                print('without token - fetch ok')
            except:
                print("")
        return getIssues
    except:
        print("")
def readmeInfo():
    try:
        readme_commits = 0
        committer_dates = []
        os.chdir(root_directory)
        os.chdir("path/"+repo_id+"/")
        for repos in os.listdir():
            if(repos == repoName):
                os.chdir(repos)
                for files in os.listdir():
                    if("readme.md" == files.lower()):
                        stream = os.popen("git log --pretty=format:'%h | %cd' " + files)
                        for cd in stream:
                            committer_dates.append(cd)
                        committer_dates = list(set(committer_dates))
                        readme_commits = len(committer_dates)
                        if(readme_commits > 0):
                            val = (str(readme_commits),repo_id)
                            QUERY = '''UPDATE `mining_results` SET `readme_commits`=? WHERE `repo_id`=?'''
                            try:
                                os.chdir(root_directory)
                                conn = sqlite3.connect('mining.db',timeout=180)
                                conn.execute(QUERY,val)
                                conn.commit()
                                conn.close()
                                print("Readme Commits: ",readme_commits)
                            except Exception as ex:
                                os.chdir(root_directory)
                                conn = sqlite3.connect('mining.db',timeout=180)
                                conn.execute(QUERY,val)
                                conn.commit()
                                conn.close()
                                print("Readme Commits: ",readme_commits,' trying again.. ok')                
    except:
        print("")
        



arg_len = len(sys.argv)
repo_id = str(sys.argv[1])
URL = str(sys.argv[2])
print(URL)
github_url = URL.replace("api.","").replace("repos/","")
repoName = str(sys.argv[arg_len-1])
repo_path = "path/" + repo_id + "/"
def main():
    processes = []
    p = multiprocessing.Process(target=community,args=())
    processes.append(p)
    p.start()
    p = multiprocessing.Process(target=downloads,args=())
    processes.append(p)
    p.start()
    p = multiprocessing.Process(target=issuesFunc,args=())
    processes.append(p)
    p.start()
    p = multiprocessing.Process(target=readmeInfo,args=())
    processes.append(p)
    p.start()
    p = multiprocessing.Process(target=issue_looper,args=())
    processes.append(p)
    p.start()
    for process in processes:
        process.join()
if __name__ == "__main__":
    starttime = time.time()
    main()
    print('Total time {} seconds'.format(time.time()-starttime))
