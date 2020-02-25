# JD_extractor.py
# script grabs JD out of a saved html file

import os, sys, codecs
from bs4 import BeautifulSoup, Comment

def Already_Done(fpath):
  if os.path.isfile(fpath) and os.path.getsize(fpath) > 0:
    print("Already did", fpath)
    return True
  else:
    return False

def Bad_File(fn):
  if "." == fn[0]:
    return True
  if fn.endswith(".html"):
    return False
  return True

def Extract_JD(source_dir, JD_folder):
  # JD_folder = "jd_files"
  # source_dir = "whole_job_ad_pages/"

  # for all files in directory
  for each_file in os.listdir(source_dir):
    if Bad_File(each_file):
      # print("Ignoring,", each_file)
      continue
    print("\n")
    ad_file = source_dir + each_file
    # ad_file = "whole_job_ad_pages/" + "Senior Product Designer at Mode _ AngelList.html"

    # print("Let's open", ad_file)
    with open(ad_file, "r", encoding='utf8') as ad_page:
      ad_contents = ad_page.read()
      ad_soup = BeautifulSoup(ad_contents, features="html5lib")    
      # get the url from a comment
      saved_from = ad_soup.findAll(text=lambda text:isinstance(text, Comment))[0]
      # this is weird, but ignore it. We're getting a clean url
      saved_from = "http" + saved_from.split("http")[1]
      # print(saved_from)

    # check if it's angellist
    if "angel.co" in saved_from:
      print("From", "AngelList")

    # find the company name
    # div with class name_af83c
    name_div = ad_soup.find('div', {"class": "name_af83c"})
    employer = name_div.find('h1').get_text()
    print("Employer:", employer)

    # find the role name
    try:
      role_div = ad_soup.find('div', {"class": "title_927e9"})
      role_name = role_div.find('h2').get_text()
      role_name = role_name.replace("/","-")
      print("Role:", role_name)
    except AttributeError:
      print("No role found. Is this a legit job ad?")
      print(saved_from)
      return False

    # find the description div
    JD_div = ad_soup.find('div', {"class": "description_c90c4"})
    # get the text and convert <br> elements to \n
    JD_text = saved_from + "\n" + JD_div.get_text("\n")
    JD_text = JD_text

    # save clean JD text
    JD_name = JD_folder + '/' + employer + ' - ' + role_name + '.txt'
    if not Already_Done(JD_name):
      print("Saving", JD_name)
      # JD_text_file = open(JD_name,'w') 
      # JD_text_file.write(JD_text)
      # JD_text_file.close() 
      with codecs.open(JD_name, "w", "utf-8-sig") as temp:
        temp.write(JD_text)
    else:
      pass


