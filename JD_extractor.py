# JD_extractor.py
# script grabs JD out of a saved html file

import os, sys, codecs
import pathlib
from bs4 import BeautifulSoup, Comment

if sys.platform == "win32":
  import winsound

def Already_Done(fpath):
  if fpath.is_file() and os.path.getsize(str(fpath)) > 0:
    print("Already did", str(fpath))
    return True
  else:
    return False

def Bad_File(fn):
  if "." == fn[0]:
    return True
  if fn.endswith(".html") or fn.endswith(".htm"):
    return False
  return True

def Get_Angel_Ad(saved_from, ad_soup):
  # get employer
  name_div = ad_soup.find('div', {"class": "name_af83c"})
  employer = name_div.find('h1').get_text()

  # location
  location = ad_soup.find('span', {'class':'location_a70ea'})
  location = location.get_text()

  # find role
  try:
    role_div = ad_soup.find('div', {"class": "title_927e9"})
    role = role_div.find('h2').get_text()
    # fucking ui/ux jobs have a slash. Kill it!
    role = role.replace("/","-")
  except AttributeError:
    print("No role found. Is this a legit job ad?")
    print(saved_from)
    return False

  # find the description div
  JD_div = ad_soup.find('div', {"class": "description_c90c4"})
  # get the text and convert <br> elements to \n
  JD_text = saved_from + "\n" + location + "\n" + JD_div.get_text("\n")

  return employer, location, role, JD_text

def Get_Indeed_Ad(saved_from, ad_soup):
  # get employer
  company_info_div = ad_soup.find('div', {'class': 'jobsearch-InlineCompanyRating'})
  name_div = next(company_info_div.children, None)
  employer = name_div.get_text()

  # find location
  location = company_info_div.find('div', {'class': False}).string

  # find role
  role_div = ad_soup.find('h3', {"class": "jobsearch-JobInfoHeader-title"})
  role = role_div.get_text()
  # fucking ui/ux jobs have a slash. Kill it!
  role = role.replace("/","-")   

  # find the description div
  JD_div = ad_soup.find('div', {"id": "jobDescriptionText"})
  # get the text and convert <br> elements to \n
  JD_text = saved_from + "\n" + location + "\n" + JD_div.get_text("\n")

  return employer, location, role, JD_text

def Get_LinkedIn_Ad(saved_from, ad_soup):
  # get employer
  name_label = ad_soup.find("span", class_="a11y-text", string="Company Name")
  employer = name_label.find_next_sibling().string.strip().strip("\n")

  # location
  location = ad_soup.find("a", class_="jobs-top-card__exact-location")
  if location:
    location = location.string.strip().strip("\n")
  # sometimes LinkedIn doesn't have an "exact address" so they use this
  # jobs-top-card__bullet class
  # sadly, it's also used for count of applicants. But this is the 1st one.
  else:
    location = ad_soup.find("span", class_="jobs-top-card__bullet")
    location = location.string.strip().strip("\n")
    if not location:
      location = "-"

  # find role
  role_div = ad_soup.find('h1', {"class": "jobs-top-card__job-title"})
  role = role_div.get_text()
  # fucking ui/ux jobs have a slash. Kill it!
  role = role.replace("/","-")   

  # find the description div
  JD_div = ad_soup.find('div', {"id": "job-details"})
  # get the text and convert <br> elements to \n
  JD_text = saved_from + "\n" + location + "\n" + JD_div.get_text("\n")

  return employer, location, role, JD_text

def Get_Glassdoor_Ad(saved_from, ad_soup):
  employer_info_div = ad_soup.find('div', {'class': 'empInfo'})
  
  # get employer
  name_div = employer_info_div.find('div', {'class': 'employerName'})
  # get the name here, not the span that follows in the same element
  employer = name_div.contents[0]

  # find location
  location = employer_info_div.find('div', {'class': 'location'}).string

  # find role
  role_div = employer_info_div.find('div', {'class': 'title'})
  role = role_div.get_text()
  # fucking ui/ux jobs have a slash. Kill it!
  role = role.replace("/","-")   

  # find the description div
  JD_div = ad_soup.find('div', {'id': 'JobDescriptionContainer'})
  # get the text and convert <br> elements to \n
  JD_text = saved_from + "\n" + location + "\n" + JD_div.get_text("\n")

  return employer, location, role, JD_text

# main function called from letter_writer
def Extract_JD(source_dir, JD_folder):
  # JD_folder = "jd_files"
  # source_dir = "whole_job_ad_pages/"
  source_path = pathlib.Path(source_dir)
  JD_path = pathlib.Path(JD_folder)

  # if folder doesn't exist, create it
  if not JD_path.is_dir():
    JD_path.mkdir()

  # for all files in directory
  for each_file in os.listdir(str(source_path)):
    if Bad_File(each_file):
      # print("Ignoring,", each_file)
      continue
    print("\n")
    # ad_file = "whole_job_ad_pages/" + "Senior Product Designer at Mode _ AngelList.html"
    # ad_path = pathlib.Path(ad_file)
    ad_path = source_path / each_file

    # print("Let's open", ad_file)
    with ad_path.open('r', encoding='utf8') as ad_page:
      ad_contents = ad_page.read()
      ad_soup = BeautifulSoup(ad_contents, features="html5lib")    
      # get the url from a comment
      saved_from = ad_soup.findAll(text=lambda text:isinstance(text, Comment))[0]
      # this is weird, but ignore it. We're getting a clean url
      saved_from = "http" + saved_from.split("http")[1]
      # print(saved_from)

    # check if it's angellist
    if 'angel.co' in saved_from:
      job_board = 'AngelList'
      employer, location, role, description = Get_Angel_Ad(saved_from, ad_soup)
      if sys.platform == "win32":
        winsound.Beep(800,10)
    elif 'indeed.com' in saved_from:
      job_board = 'Indeed'
      employer, location, role, description = Get_Indeed_Ad(saved_from, ad_soup)
      if sys.platform == "win32":
        winsound.Beep(1000,10)
    elif 'linkedin.com' in saved_from:
      job_board = 'LinkedIn'
      employer, location, role, description = Get_LinkedIn_Ad(saved_from, ad_soup)
      if sys.platform == "win32":
        winsound.Beep(1200,10)
    elif 'glassdoor.com' in saved_from:
      job_board = 'Glassdoor'
      employer, location, role, description = Get_Glassdoor_Ad(saved_from, ad_soup)
      if sys.platform == "win32":
        winsound.Beep(1400,10)


    print("From", job_board)     
    print("Employer:", employer)
    print("Location:", location)
    print("Role:", role)

    # save clean JD text
    JD_name = JD_path / (employer + ' - ' + role + '.txt')
    if not Already_Done(JD_name):
      print("Saving", str(JD_name))
      # JD_text_file = open(JD_name,'w') 
      # JD_text_file.write(JD_text)
      # JD_text_file.close() 
      with codecs.open(str(JD_name), "w", "utf-8-sig") as temp:
        temp.write(description)
    else:
      pass



