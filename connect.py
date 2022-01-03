import sqlite3

conn = sqlite3.connect('mining.db')

conn.execute('''CREATE TABLE `mining_results` (
  `repo_id` int(11) NOT NULL,
  `repository` varchar(255) NOT NULL,
  `community` double DEFAULT NULL,
  `downloads` double DEFAULT NULL,
  `commits` double DEFAULT NULL,
  `open_issues` double DEFAULT NULL,
  `closed_issues` double DEFAULT NULL,
  `total_issues` double DEFAULT NULL,
  `readme_issues` double DEFAULT NULL,
  `readme_commits` double DEFAULT NULL,
  PRIMARY KEY (`repo_id`)
);''')
print("Database schema ready!")

conn.close()
