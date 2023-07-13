import sqlite3
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime

start_time = time.time()

conn = sqlite3.connect("job_ads.db")
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS job_ads (
        role TEXT,
        company TEXT,
        salary TEXT,
        salary_calculation TEXT,
        link TEXT,
        days_in INTEGER DEFAULT 0,
        UNIQUE(role, company, salary)
    )
''')

url = f"https://www.cvbankas.lt/?padalinys%5B0%5D=76&page=1"
page = requests.get(url).text
soup = BeautifulSoup(page, "html.parser")
pages = soup.find(class_="pages_ul_inner")
last_page = int(pages.select("li:last-child")[0].text)

filter_list = ["Python", "Junior"]

job_links = []

for page in range(1, last_page + 1):
    url = f"https://www.cvbankas.lt/?padalinys%5B0%5D=76&page={page}"

    page_content = requests.get(url).text
    soup = BeautifulSoup(page_content, "html.parser")

    job_ads = soup.find_all("article",
                            class_="list_article list_article_rememberable jobadlist_list_article_rememberable")

    for ad in job_ads:
        list_h3_element = ad.find(class_="list_h3")
        company = ad.find(class_="dib mt5")
        salary = ad.find(class_="salary_amount")
        salary_calculation = ad.find(class_="salary_calculation")
        link = ad.find(class_="list_a can_visited list_a_has_logo")

        if list_h3_element:
            text_inside_company = company.text.strip() if company else ""
            text_role = list_h3_element.text.strip()
            text_role_split = text_role.split()
            text_salary = salary.text.strip() if salary else "Neatskleista"
            text_salary_calculation = salary_calculation.text.strip() if salary_calculation else ""
            text_link = link['href'] if link else ""

            if any(element in text_role_split for element in filter_list):
                print("Rolė:", text_role)
                print("Kompanija:", text_inside_company)

                if salary:
                    print("Alga:", text_salary)
                else:
                    print("Alga: Neatskleista")

                print("Algos skaičiavimas:", text_salary_calculation)
                print("Linkas:", text_link)
                print("-----------------------")

                c.execute('''
                    SELECT * FROM job_ads
                    WHERE role=? AND company=? AND salary=?
                ''', (text_role, text_inside_company, text_salary))

                existing_record = c.fetchone()

                if not existing_record:
                    c.execute('''
                        INSERT INTO job_ads (role, company, salary, salary_calculation, link)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (text_role, text_inside_company, text_salary, text_salary_calculation, text_link))

                else:
                    c.execute('''
                        UPDATE job_ads
                        SET days_in = days_in + 1
                        WHERE role=? AND company=? AND salary=? AND salary_calculation=? AND link=?
                    ''', (text_role, text_inside_company, text_salary, text_salary_calculation, text_link))

                job_links.append(text_link)

    conn.commit()


c.execute('SELECT link FROM job_ads')
db_job_links = [row[0] for row in c.fetchall()]

links_to_delete = set(db_job_links) - set(job_links)

for link in links_to_delete:
    c.execute('DELETE FROM job_ads WHERE link=?', (link,))

conn.commit()
conn.close()

end_time = time.time()
execution_time = end_time - start_time

current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

with open("runs_datetime.txt", "a") as f:
    f.write(formatted_datetime + "\n")

print(f"Execution time: {execution_time} seconds")

input("Press Enter to exit...")