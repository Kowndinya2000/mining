# Steps to run the tool RepoQuester
> 1. Install python libraries
````
pip install -r requirements.txt
````
> 2. Open the file ```repo_urls``` 
````
Add username/repositoryname in newlines. 
````
> 3. Open the file ```tokens.py``` 
````
Alteast provide one Github Personal Access Token. 
Format to provide token can be viewed in the file.
````
> 4. Initialize the database
````
python3 generate_ids.py
python3 connect.py
python3 insert.py
````
> 5. Run the script to analyze the repositories
````
python3 run.py
chmod +x *sh
./score.sh
````
> 8. Check the results in the database file ```mining.db```

> 9. To re-run the analysis without modyfing repository information
````
chmod +x *sh
./clean.sh
./run.sh
(Sample results are present in mining_results.xlsx)
````
> 10. To empty the repository information and results.
````
chmod +x *sh
./empty.sh
(This also deletes the database file. Only retains the usable tool template)
Follow the steps 4-7 again.  
````
> 11. To run a particular repository.
````
For example, to analyze repository with repo_id = 2 : run the below two commands
chmod +x script2.sh
./script2.sh
````