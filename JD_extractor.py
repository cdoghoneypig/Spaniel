# JD_extractor.py
# script grabs JD out of a saved html file

# LinkedIn, Indeed, Lensa, Angel


import os, sys, codecs
import pathlib
from bs4 import BeautifulSoup, Comment

if sys.platform == "win32":
  import winsound

def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

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

def Get_Wellfound_Ad(saved_from, ad_soup):

  # easier to build it via interpreter like this
  # import code; code.interact(local=locals())
  # get employer
  try:
    job_div = ad_soup.find('div', {'data-test': 'DiscoverModal'})

    # div containing company name and slogan
    # job_div_soup.find('div', {'class':'flex-wrap py-4 text-center text-black'})
    # this is just the name
    name_div = job_div.find('div', {'class':'text-lg font-[500]'})
    employer = name_div.get_text()
  except AttributeError:
    print("oops this wellfound ad is different! please fix the code here at", Exception)
    import code; code.interact(local=locals())


  # get location
  details_div = ad_soup.find('div', {'class':'mb-24 mt-6 flex h-4/5 w-full gap-12 overflow-scroll md:px-4'})
  location_div = details_div.find('span', text='Location').parent
  location = location_div.find_all('span')[1].get_text()



  # find roles
  # job_div.find('div', {'class': ['flex-wrap', 'justify-center', 'text-lg', 'md:gap-1']})
  role_like_divs = ad_soup.find_all('div', {'class': ['flex-wrap', 'justify-center', 'text-lg', 'md:gap-1']})
  role = role_like_divs[4].find_all('span')[0].get_text()
  # fucking ui/ux jobs have a slash. Kill it!
  role = role.replace("/","-")

  # description div
  JD_div = ad_soup.find('div', {'class': 'styles_description__bGSzH'})
  # get the text and convert <br> elements to \n
  JD_text = saved_from + "\n" + location + "\n" + JD_div.get_text("\n")

  return employer, location, role, JD_text



def Get_BuiltIn_Ad(saved_from, ad_soup):

  # easier to build it via interpreter like this
  # import code; code.interact(local=locals())
  # get employer

  name_div = ad_soup.find('div', {'class':'field--name-field-company'})
  employer = name_div.get_text()

  # get location
  location_span = ad_soup.find('span', {'class': 'company-address'})
  location = location_span.get_text()


  # find role, this has a nested child that is the location, so annoying
  job_title_element = ad_soup.find('span', class_='field--name-title')

    # <h1 class="node-title">
    #   <span class="field field--name-title field--type-string field--label-hidden">UX/UI Designer
    #     <span class="job-title-location">
    #       (San Francisco, CA)
    #     </span>
    #   </span>
    # </h1>

  # Remove the nested <span> with class 'job-title-location'
  job_title_element.find('span', class_='job-title-location').clear()
  role = job_title_element.get_text(strip=True)


  # role = job_title_element.get_text(strip=True) if job_title_element else input("Job title please: ")

  role = role.replace("/","-")

  # description div
  JD_div = ad_soup.find('div', {'class': 'job-description'})
  JD_bare = JD_div.get_text("\n", strip=True) if JD_div else input("Paste in the description pls: ")

  # add the first few lines of text to the JD
  JD_text = saved_from + "\n" + location + "\n" + JD_bare

  return employer, location, role, JD_text


def Get_Greenhouse_Ad(saved_from, ad_soup):

  # import code; code.interact(local=locals())

  # get employer
  name_span = ad_soup.find('span', {'class': 'company-name'})
  # they put "  at CompanyName  "
  # employer = name_span.get_text()[8:-4]
  employer = name_span.get_text()
  employer = employer.replace(' at','').strip()

  # location
  location_div = ad_soup.find('div', {'class':'location'})
  # location = location_div.get_text()[7:-5]
  location = location_div.get_text().strip()

  # find role
  role_h1 = ad_soup.find('h1', {'class': 'app-title'})
  role = role_h1.get_text().strip()
  role = role.replace("/","-")


  # find the description div
  JD_div = ad_soup.find('div', {"id": "content"})
  # get the text and convert <br> elements to \n
  JD_text = saved_from + "\n" + location + "\n" + JD_div.get_text("\n")

  # import code
  # print("greenhouse double check")
  # code.interact(local=locals())

  return employer, location, role, JD_text


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

  # updating the scraper Oct 2023
  # import code
  # code.interact(local=locals())


  # company_info_div = ad_soup.find('div', {'class': 'jobsearch-InlineCompanyRating'})
  # name_div = next(company_info_div.children, None)
  name_div = ad_soup.find('div', {'data-testid': 'inlineHeader-companyName'})

  employer = name_div.get_text()


  # find location
  # location = company_info_div.find('div', {'class': False}).string
  location_div = ad_soup.find('div', {'data-testid': 'inlineHeader-companyLocation'})
  location = location_div.get_text()

  # find role

  # role_div = ad_soup.find('h3', {"class": "jobsearch-JobInfoHeader-title"})
  role_div = ad_soup.find('h2', {'class': 'jobsearch-JobInfoHeader-title'})
  # they have a hidden child span that just says "- job post"
  role_div.find("span").find("span").clear()

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
  details_div = ad_soup.find('div', {'class': 'job-details-jobs-unified-top-card__primary-description'})
  employer = details_div.find('a').get_text()


  # location
  location_div = details_div.find('div')
  # annoying, they put the text in a div with many children, it's the 2nd text entry
  # and it has this weird dot before the location
  location = location_div.find_all(text=True, recursive=False)[1].strip('·')



  # location = ad_soup.find("a", class_="jobs-top-card__exact-location")
  # if location:
  #   location = location.string.strip().strip("\n")
  # sometimes LinkedIn doesn't have an "exact address" so they use this
  # jobs-top-card__bullet class
  # sadly, it's also used for count of applicants. But this is the 1st one.
  # else:
  #   location = ad_soup.find("span", class_="jobs-top-card__bullet")
  #   location = location.string.strip().strip("\n")
  #   if not location:
  #     location = "-"

  # find role
  # print("h1 job-details-jobs-unified-top-card__job-title")
  # import code; code.interact(local=locals())
  role_h1 = ad_soup.find("h1", {"class": "job-details-jobs-unified-top-card__job-title"})
  role = role_h1.get_text().strip()
  # fucking ui/ux jobs have a slash. Kill it!
  role = role.replace("/","-")

  # find the description div
  # JD_div = ad_soup.find('div', {"id": "job-details"})

  JD_div = ad_soup.find('article', {'class': 'jobs-description__container'})

  # get the text and convert <br> elements to \n
  JD_text = saved_from + "\n" + location + "\n" + JD_div.get_text("\n")

  job_board = "LinkedIn"

  # print(job_board, employer, location, role)
  # import code; code.interact(local=locals())

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

def Get_Lensa_Ad(saved_from, ad_soup):
  # get employer
  company_info_div = ad_soup.find('div', {'class': 'job-details-sub-title'})
  div_children = company_info_div.children
  name_span = next(div_children)
  name_anchor = name_span.find('a')
  employer = name_anchor.get_text()

  # find location
  location_span = next(div_children)
  location = location_span.get_text()

  # find role
  role_div = ad_soup.find('h1', {"class": "job-details-title"})
  role = role_div.get_text()
  # fucking ui/ux jobs have a slash. Kill it!
  role = role.replace("/","-")
  # Why is the word "job" in the title? Kill that
  role = role.replace(" job","")

  # find the description div
  JD_div = ad_soup.find('div', {"class": "description-main"})
  # get the text and convert <br> elements to \n
  JD_text = saved_from + "\n" + location + "\n" + JD_div.get_text("\n")

  return employer, location, role, JD_text

def Get_Lever_Ad(saved_from, ad_soup):
  # get employer
  # employer_div = ad_soup.find('div', {'class': 'department'})
  # employer = employer_div.get_text()
  # employer = employer.replace('/','').strip()

  # looks like we need to grab it from the page's title
  page_title_text = ad_soup.title.get_text()
  # Split the title based on the dash ("-")
  employer = page_title_text.split(' - ')[0]


  # find location
  location_div = ad_soup.find('div', {'class': 'location'})
  location = location_div.get_text()

  # find role
  role_div = ad_soup.find('div', {'class': 'posting-headline'})
  role_h2 = role_div.find('h2')
  role = role_h2.get_text()
  role = role.replace("/","-")

  # find the description div
  first_jd_div = ad_soup.find('div', {'data-qa': 'job-description'})
  JD_div = first_jd_div.parent

  # get the text and convert <br> elements to \n
  JD_text = saved_from + "\n" + location + "\n" + JD_div.get_text("\n")


  return employer, location, role, JD_text

def Get_Ashby_Ad(saved_from, ad_soup):

  # get employer
  # looks like we need to grab it from the page's title
  page_title_text = ad_soup.title.get_text()
  # Split the title based on the dash ("-")
  employer = page_title_text.split(' @ ')[1]

  # find location
  #
  leftpane = ad_soup.find('div', {'class': 'ashby-job-posting-left-pane'})
  location_section = leftpane.find('h2', string='Location')
  location = location_section.find_next('p').get_text(strip=True)

  # find role
  role_h1 = ad_soup.find('h1', {'class': 'ashby-job-posting-heading'})
  role = role_h1.get_text()
  role = role.replace("/","-")

  # find the description div
  JD_div = ad_soup.find('div', {'aria-labelledby': 'job-overview'})

  # get the text and convert <br> elements to \n
  JD_text = saved_from + "\n" + location + "\n" + JD_div.get_text("\n")

  # import code; code.interact(local=locals())

  return employer, location, role, JD_text

def Get_Manual_Input(saved_from, ad_soup):
  print("sorry I don't know how to scrape this site. You can copy paste it in though!")
  employer = input("Employer: ")
  location = input("Location: ")
  role = input("Role / Job Title: ")
  just_description = input ("Paste in the whole job description here: ")

  # get the text and convert <br> elements to \n
  JD_text = saved_from + "\n" + location + "\n" + just_description

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

  # delete anything in that folder!
  for filename in os.listdir(JD_path):
    del_file_path = os.path.join(JD_path, filename)
    try:
        if os.path.isfile(del_file_path) or os.path.islink(del_file_path):
            os.unlink(del_file_path)
        elif os.path.isdir(del_file_path):
            shutil.rmtree(del_file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (del_file_path, e))


  # for all files in directory
  for each_file in os.listdir(str(source_path)):
    if Bad_File(each_file):
      # print("Ignoring,", each_file)
      continue
    print("\n")
    # ad_file = "whole_job_ad_pages/" + "Senior Product Designer at Mode _ AngelList.html"
    # ad_path = pathlib.Path(ad_file)
    ad_path = source_path / each_file

    print("Let's open", ad_path)
    with ad_path.open('r', encoding='utf8') as ad_page:
      ad_contents = ad_page.read()
      ad_soup = BeautifulSoup(ad_contents, features="html5lib")
      # get the url from a comment
      saved_from = ad_soup.findAll(text=lambda text:isinstance(text, Comment))[0]
      # this is weird, but ignore it. We're getting a clean url
      saved_from = "http" + saved_from.split("http")[1]
      # print(saved_from)

    # determine which job board based on domain in url
    if 'wellfound.com' in saved_from:
      job_board = 'Wellfound'
      employer, location, role, description = Get_Wellfound_Ad(saved_from, ad_soup)
      if sys.platform == "win32":
        winsound.Beep(600,10)
    elif 'indeed.com' in saved_from:
      job_board = 'Indeed'
      employer, location, role, description = Get_Indeed_Ad(saved_from, ad_soup)
      if sys.platform == "win32":
        winsound.Beep(1000,10)
    elif 'boards.greenhouse.io' in saved_from:
      job_board = 'Greenhuose'
      employer, location, role, description = Get_Greenhouse_Ad(saved_from, ad_soup)
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
    elif 'lensa.com' in saved_from:
      job_board = 'Lensa'
      employer, location, role, description = Get_Lensa_Ad(saved_from, ad_soup)
      if sys.platform == "win32":
        winsound.Beep(1600,10)
    elif 'lever.co' in saved_from:
      job_board = "Lever"
      employer, location, role, description = Get_Lever_Ad(saved_from, ad_soup)
    elif 'jobs.ashby' in saved_from:
      job_board = "Ashby"
      employer, location, role, description = Get_Ashby_Ad(saved_from, ad_soup)
    elif 'builtinsf.com' in saved_from:
      job_board = "BuiltInSF"
      employer, location, role, description = Get_BuiltIn_Ad(saved_from, ad_soup)

    else:
      job_board = "NA"
      employer, location, role, description = Get_Manual_Input(saved_from, ad_soup)




    employer = deEmojify(employer)
    location = deEmojify(location)
    role = deEmojify(role)


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
