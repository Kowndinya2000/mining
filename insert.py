import sqlite3
fp = open('repo_ids','r')
ids = []
for id in fp:
    ids.append(id.replace("\n",""))
fp.close()
fp = open('repo_urls','r')
urls = []
for id in fp:
    urls.append(id.replace("\n",""))
fp.close()
conn = sqlite3.connect('mining.db')
for x in range(len(ids)):
    val = (int(ids[x]),urls[x],'0','0','0','0','0','0','0','0')
    QUERY = '''
    INSERT INTO `mining_results`
    (`repo_id`,`repository`,`community`,`downloads` ,`commits`,`open_issues` ,`closed_issues`,`total_issues` ,`readme_issues`,`readme_commits`)
    VALUES
    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    conn.execute(QUERY,val)

conn.commit()
print("Table github mining is ready!")
conn.close()
