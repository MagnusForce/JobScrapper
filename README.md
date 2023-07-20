# Job Ads Scraper

This is a Python script that scrapes job ads from the website "cvbankas.lt" and stores them in an SQLite database. The script utilizes the `sqlite3` library for database operations and the `BeautifulSoup` library for web scraping.

# Installation

This program can be used as is by simply running the Python script.

Most modules used in this project are pre-installed with Python. The only modules you need to install are bs4, requests and datetime. To install these modules, run these commands in CMD:

`pip install bs4`
`pip install requests`
`pip install datetime`

# Usage

Clone this repository or download the script file.

Script is intended to run on each computer startup (it still can be used manually). To achieve this you can follow these steps:
1. Create a shortcut to your Python script.
2. Open the Startup folder (Press Win + R to open the "Run" dialog box.Type "shell:startup" and click "OK.") 
3. Move the shortcut to the Startup folder.
4. Test your script by restarting your computer.

You can modify the `filter_list` variable to include specific keywords that the job ads should match. By default, it includes "Python" and "Junior". Only the job ads containing any of the keywords in their titles will be saved in the database. Script also times how long it took to run, giving precise time at the end.

#### Database Schema

The script creates a table named `job_ads` in the SQLite database with the following columns:

- `role` (TEXT): The role/title of the job ad.
- `company` (TEXT): The name of the hiring company.
- `salary` (TEXT): The salary offered for the job. If not disclosed, it will be set as "Neatskleista".
- `salary_calculation` (TEXT): Additional information about salary calculation, if provided.
- `link` (TEXT): The URL link to the job ad.
- `days_in` (INTEGER): The number of days the job ad has been stored in the database. Initially set to 0.
- Unique constraint: The combination of `role`, `company`, and `salary` must be unique to avoid duplicate entries.

