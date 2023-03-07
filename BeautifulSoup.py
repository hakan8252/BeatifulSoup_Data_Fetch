# pip install beautifulsoup4
# pip install lxml
import time

from bs4 import BeautifulSoup
import re

with open("Web-Scraping/home.html", "r", errors="ignore") as html_file:
    content = html_file.read() # read the file
    # print(content)

    #convert it to Beatifulsoup object by using lxml parser
    soup = BeautifulSoup(content, "lxml")
    # print(soup.prettify())

    #find search first object and stop execution. We can use find_all to get all tags that belongs our parameter.
    tags = soup.find_all("h3")
    print(tags)

    # fetch only text
    for tag in tags:
        print(tag.text)

    #find all li tags which have specific classes. split() method can make list for elements
    persons = soup.find_all("span", class_="name t-bold t-14 t-black")
    for person in persons:
        person_name = person.text
        print(person_name)

    persons_info = soup.find_all("div", class_="pv-browsemap-section__member-detail")
    for person_i in persons_info:
        person_name = person_i.find_next("span", class_="name t-bold t-14 t-black").text
        person_profession = person_i.find_next("div", class_="inline-show-more-text inline-show-more-text--is-collapsed inline-show-more-text--is-collapsed-with-line-clamp").text \
        .strip()
        print(f"Person name: {person_name} and Occupation: {person_profession}")

import requests

#response 200 request done succesfully
html_text = requests.get("https://jobs.apple.com/en-us/search?location=united-states-USA").text
soup = BeautifulSoup(html_text, "lxml")
jobs = soup.find_all("td", class_="table-col-1")
jobs_place = soup.select("[id*=storeName_container]")
job_dict = {"job_name": [], "service_type": [], "date": [], "jobs_place": []}

for job in jobs:
    job_name = job.find("a", class_="table--advanced-search__title").text.strip()#remove blanks
    service_type = job.find("span", class_ = "table--advanced-search__role").text.strip()
    date = job.find("span", class_="table--advanced-search__date").text.strip()
    job_dict["job_name"].append(job_name)
    job_dict["service_type"].append(service_type)
    job_dict["date"].append(date)
    #results only current page because of pagination.
    # print(f"Job Name: {job_name} \n Service Type: {service_type} \n Release Date : {date} \n")

for job_place in jobs_place:
    job_p = job_place.text.strip() # remove blanks
    job_dict["jobs_place"].append(job_p)

for value in list(zip(job_dict["job_name"], job_dict["service_type"], job_dict["date"], job_dict["jobs_place"])):
    print(f"Job Name: {value[0]} \n Service Type: {value[1]} \n Release Date : {value[2]} \n Jobs Place : {value[3]} \n")
    #yeni değişiklik. silindi.


# for https://jobs.apple.com/en-us/search?location=united-states-USA jobs
def find_jobs(no_of_jobtitle = 5):
    job_title = []
    for i in range(0, no_of_jobtitle):
        title_w = input(">")
        if title_w == "esc":
            break
        else:
            job_title.append(title_w)
    print(f"Filtering Out {job_title}")

    html_text = requests.get("https://jobs.apple.com/en-us/search?location=united-states-USA").text
    soup = BeautifulSoup(html_text, "lxml")
    jobs = soup.find_all("td", class_="table-col-1")
    job_details = soup.find_all("div", class_="expandable--advanced-search__right column large-6 small-12")

    # Filter search
    job_hours = []
    for job_d in job_details:
        job_detail = job_d.find_all_next("span")[1].text
        job_hours.append(job_detail)

    for index, job in enumerate(jobs):
        job_name = job.find("a", class_="table--advanced-search__title").text.strip()
        # if "Specialist" in job_name:
        service_type = job.find("span", class_="table--advanced-search__role").text.strip()
        date = job.find("span", class_="table--advanced-search__date").text.strip()
        # salary = job.find("span", class_="css-1xe2xww e1wijj242").text.split()[:2]
        # salary = " ".join(salary)
        # more_info = job.header.h2.a["href"] # gives specific job link
        # results only current page because of pagination.
        if any(ext in job_name for ext in job_title):
            with open(f"Web-Scraping/posts/{index}.txt", "w") as f:  # write file
                f.write(f"Job Name: {job_name} \n")
                f.write(f"Service Type: {service_type} \n")
                f.write(f"Release Date: {date} \n")
                f.write(f"Working Hours: {job_hours[index]} \n")

if __name__ == "__main__":
    while True:
        find_jobs()
        time_wait = 10
        print(f"Waiting {time_wait} minutes...")
        time.sleep(time_wait * 60)# run program every 10 min

#run command pannel python main.py







