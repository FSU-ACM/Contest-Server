# Extra Credit
The extra credit script is located in the project root, `extra_credit.py`.

For the script, you will need copies of the results (one for each division) and the extra credit survey. The script works by linking the score to the team, the team to the student, and the student to the courses. See comments in the script for further details.

## Setup
There's two ways to run the extra credit script -- run it remotely in the Docker container for the webapp, or locally with a remote connection to the database.

Running locally means you need to configure Flask to connect to the database running on the remote host. This can be done by overriding your config to use an SSH tunnel which connects to the server DB. Since the default development config already points to `localhost:27017`, opening a tunnel there would be preferable. **Do not commit changes to the development config**.

### 1. Get the source files
First, get a copy of the extra credit survey results. This should be a CSV where the second column (index 1) is an FSUID, and the third column (index 2) is a string of comma-delimted coursecodes (e.g. COP3014).

Next, download a copy of each division's results. You can find this under "Import/Export", then click the "results.tsv" link to download. Use the dropdown in the top right to switch between divisions.

Put these files somewhere the script can read them, i.e. if you're executing in the Docker container these need to be readable inside the container. Coping through the `share/` volume from the `docker-compose.yml` is a good way to transfer them. Consider storing them in the project root's `credit/` folder, as this path is ignored in the `.gitignore`. Furthermore, the script expects the survey CSV file to be stored as `credit/survey.csv`.  Remember, **do not commit these files**.

### 2. Optional: Get inside the container
If you're running the script from inside the container, you can enter the container using `docker-compose exec webapp bash` to create a bash terminal inside the container.

### 3. Run the script
Using the `invoke` library, you can call the extra credit script very easily. See `tasks.py` for additional parameter details.

```sh
$ inv extracredit -d upper -r credit/results_upper.tsv
Reading results_tsv...
Matching teams to scores...
Reading extra credit survey...
Writing class files...
Processing orphan scores...
```

This will spit out several CSVs under `{cwd}/credit/{division}`

