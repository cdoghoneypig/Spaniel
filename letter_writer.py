# letter_writer.py
# script composes cover letters based on
# 1 extract metadata from filename
# 2 scan JD for keywords
# 3 display JD in separate window
# 4 recommend top bullet point matches to user
# 5 user accepts or choose to change selection
# 6 program writes new cover letter, saves it
# 7 log what went down

# basic tools
import os, itertools, sys, json, csv
import configparser
import re, pathlib
from collections import defaultdict, Counter
from datetime import datetime

# libraries i wrote
import keywords_csv_to_json, JD_extractor

# webdriver and html parsing
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup



def Bad_File(fn):
  if "." == fn[0]:
    return True
  if fn.endswith(".txt"):
    return False
  return True

def Get_Frequency(word_index):
  d = defaultdict(lambda: 0)
  for each_word in word_index:
    bullet_name = word_index[each_word]
    d[bullet_name] += 1
  return d

def Get_Distance(w1, w2, source_text):
  # Not actually using this function yet
  if w1 in source_text and w2 in source_text:
    w1_indexes = [index for index, value in enumerate(source_text) if value == w1]    
    w2_indexes = [index for index, value in enumerate(source_text) if value == w2]    
    distances = [abs(item[0] - item[1]) for item in itertools.product(w1_indexes, w2_indexes)]
    # should be a list of all distances
    print(distances)
    return {'min': min(distances), 'avg': sum(distances)/float(len(distances))}

def Get_Bullets(nom_counter, nom_list):
  # function to collect bullets
  l = ['','','']
  
  # first ask if they just want to accept the recommendations
  first_bullet = input("Enter to accept; or anything else to enter your own ")
  # if they hit enter, give them the rex
  if first_bullet == '' and len(nom_list) >= 3:
    l = nom_list[:3]
  # q for quit, mostly for testing!
  elif first_bullet == 'q':
    driver.quit()
    sys.exit()
  # alright, now let them enter text, but validate it
  else:
    # validation by this while loop
    # don't advance counter unless entry validated
    which_bullet = 0

    # ok, if we can recommend only 0-2 bullets, enter those
    # and then make user input more
    if len(nom_list) < 3:
      print("Spaniel unable to find 3 good bullets! Pls help.")
      for each_rec in nom_list:
        l[which_bullet] = each_rec
        which_bullet += 1
      print("Please provide", 3- len(nom_list), "more!!" )

    while which_bullet < 3:
      typed_in = input("bullet #" + str(which_bullet + 1) + ": ")
      # if valid, store the input and advance the counter
      if typed_in in kw[job_type]["bullets"].keys():
        l[which_bullet] = typed_in
        which_bullet += 1
      # otherwise, show the acceptable options and try again
      else:
        print(typed_in, "not recognized. Options are:")   
        for each_bullet in sorted(kw[job_type]["bullets"].keys()):
          print("  *", each_bullet)


  # print("Great, we'll run with", ", ".join(l))
  return l

def Write_Letter(final_bullets, url):
  letter_file_name = "letter " + employer + " - " + role + ".txt"
  letter_file = (letter_path / letter_file_name).open("w")
  letter_file.write(url)
  letter_file.write("\n\n")
  letter_file.write(kw[job_type]["textons"]["Greeting"])
  letter_file.write("\n\n")
  letter_file.write(kw[job_type]["textons"]["Intro"])
  letter_file.write("\n\n")
  letter_file.write(kw[job_type]["textons"]["Start Bullets"])
  letter_file.write((role + " at " + employer))
  letter_file.write("\n\n")
  # where the magic happens. Use the bullets as keys to grab copy
  for i in range (0,3):
    letter_file.write(kw[job_type]["bullets"][final_bullets[i]])
    letter_file.write("\n\n")
  letter_file.write(kw[job_type]["textons"]["Outro"])
  letter_file.write("\n\n")
  letter_file.write(kw[job_type]["textons"]["Sign off"])
  letter_file.write("\n")
  letter_file.write(kw[job_type]["textons"]["Name"])
  letter_file.close()


def Display_JD(where, who, what):
  employer = portal_soup.find('h1',id='employer')
  employer.string.replace_with(where)

  role = portal_soup.find('h2',id='role')
  role.string.replace_with(who)

  # to insert the JD from a text file, we gotta replace \n with <br>
  jd_with_br = what.replace("\n","<br>")

  # now we turn this into a soup object
  jd_html = BeautifulSoup(jd_with_br, 'html5lib')
  # unfortunately this wraps it in html, head/head, body
  # so I'll extract the body
  jd_html = jd_html.find('body')
 
  JD = portal_soup.find('div',id='description')
  # import code; code.interact(local = locals())
  JD.clear()
  JD.insert(0,jd_html)


  with open(portal_file, "w", encoding = 'utf-8-sig') as outf:
    outf.write(portal_soup.prettify())
  # lame but we use Selenium refresh command to load the altered html document
  driver.refresh()
  driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)

def Span_Keyword(a_word, a_bullet, jd):
  # this function has a bug. It can get false positives
  # for text it inserts in. potentially a LOT of insertions
  # though not actually infinite
  real_hits = re.findall(a_word, jd, re.IGNORECASE)
  for each_hit in real_hits:
    # defining spanned_word here so it can
    # match case with original
    # <span class="cross-functional" title="cross-functional">
    #     work closely with
    #    </span>
    spanned_word = ('<span class="' 
                + bullet_class[a_bullet] 
                + '" title="'
                + bullet_class[a_bullet] 
                +'">' 
                + each_hit 
                + '</span>')
    jd = jd.replace(each_hit, spanned_word)
  return jd

def Set_Bullet_Class(bullet_list, colors):
  bullet_class = {}
  bullet_css = open(cfg['BulletCSS'],'w')
  for each_bullet in bullet_list:
    bullet_class[each_bullet] = each_bullet.replace(' ','-')
    bullet_css.write('.' + bullet_class[each_bullet] + ' {')
    bullet_css.write('\n\t')
    # should use real color set!
    bullet_css.write('background-color: ' + colors[each_bullet] + ';')
    bullet_css.write('\n')
    bullet_css.write('}\n\n')

    bullet_css.write('.' + bullet_class[each_bullet] + ':hover {')
    bullet_css.write('\n\t')
    # should use real color set!
    bullet_css.write('background-color: ' 
                      + colors[each_bullet].replace('.1','.5') + ';')
    bullet_css.write('\n')
    bullet_css.write('}\n\n')
  bullet_css.close()
  return bullet_class
    
def Build_Legend(bullets):
  ul_soup = BeautifulSoup('', 'html.parser')
  new_ul = ul_soup.new_tag('ul', attrs={'id': 'bullet-legend'})
  # add a bunch of list items
  for i, each_item in enumerate(bullets):
    newtag = ul_soup.new_tag('li', attrs={'class': bullet_class[each_item]})
    newtag.string = each_item
    new_ul.insert(i+1, newtag)
  return new_ul

def Set_Color_CSS(bullet_list):
  # needs input of sorted(kw[job_type]['bullets'].keys())
  
  # set up bullet to color palette dictionary
  with open(cfg['PaletteJSON'], "r") as read_file:
          palette = json.load(read_file)
  colors = {}
  for i, each_bullet in enumerate(bullet_list):
    try:
      colors[each_bullet] = palette[i]
    except IndexError:
      print("No palette color for", each_bullet, i)
      print("Using same color as", bullet_list[0])
      colors[each_bullet] = palette[0]  
  # this dict maps bullets, which may have spaces, to css class names
  # and assigns colors based on the colors dict
  bullet_class = Set_Bullet_Class(bullet_list, colors)

  return colors, bullet_class

config = configparser.ConfigParser()
config.read('spaniel.cfg')
cfg = {}
# import code; code.interact(local = locals())
cfg['Webdriver'] = config.get('DEFAULT', 'Webdriver')
cfg['InputFolder'] = config.get('DEFAULT', 'InputFolder')
cfg['TextFileFolder'] = config.get('DEFAULT', 'TextFileFolder')
cfg['KeywordFolder'] = config.get('DEFAULT', 'KeywordFolder')
cfg['OutputFolder'] = config.get('DEFAULT', 'OutputFolder')
cfg['LogFile'] = config.get('DEFAULT', 'LogFile')
cfg['KeywordJson'] = config.get('DEFAULT', 'KeywordJson')
cfg['HTMLPage'] = config.get('DEFAULT', 'HTMLPage')
cfg['BulletCSS'] = config.get('DEFAULT', 'BulletCSS')
cfg['PaletteJSON'] = config.get('DEFAULT', 'PaletteJSON')
cfg['JobAppCSVFolder'] = config.get('DEFAULT', 'JobAppCSVFolder')

today = datetime.now().strftime("%Y-%m-%d")
now = datetime.now().strftime("%Y-%m-%d %H-%M")

# append to the log of letters Spaniel wrote
try:
  with open(cfg['LogFile'], "r") as read_file:
        letters_written = json.load(read_file)
except FileNotFoundError:
  print("No history log found. Starting new one!")
  letters_written = {}

# create a csv for today's run with headers
# applied_to_date, role, employer, location, notes, ad_url
# start with this blank list
job_app_csv_path = pathlib.Path(cfg['JobAppCSVFolder']) / (now + '.csv')

# if folder doesn't exist, create it
if not pathlib.Path(cfg['JobAppCSVFolder']).is_dir():
  pathlib.Path(cfg['JobAppCSVFolder']).mkdir()

with job_app_csv_path.open(mode='w') as app_tracker:
  app_writer = csv.writer(app_tracker)
  app_writer.writerow(['Date', 'Role', 'Employer', 'Location', 'Notes', 'URL'])

# extract JD text files from original html
JD_extractor.Extract_JD(cfg['InputFolder'], cfg['TextFileFolder'])

# 'False' sets function to quiet mode, vs verbose
kw = keywords_csv_to_json.Build_Keyword_Dict(
                                            cfg['KeywordFolder'], 
                                            cfg['KeywordJson'], 
                                            False)
# kw["keywords] = {"spicy" : "tasty"}
# kw["bullets"] = {"tasty": "I am a very tasty noodle!"}
# kw["textons"] = {"greeting": "Hey there,"}
# kw["proximity"] = [["collaborate","teams",15,"cross-functional"]]



source_path = pathlib.Path(cfg['TextFileFolder'])
letter_path = pathlib.Path(cfg['OutputFolder']) / today

# source_path = pathlib.Path("jd_files/")
# letter_path = pathlib.Path("Letters/" + str(today))
if not letter_path.is_dir():
  letter_path.mkdir(parents = True)

print("\n\nScript scans", str(source_path), "and composes cover letters for each job!")

driver = webdriver.Chrome(cfg['Webdriver'])
driver.set_window_size(1200, 1000)
portal_file = cfg['HTMLPage']
portal_url = "file:" + os.getcwd() + '/' + portal_file
# print("Loading", portal_url)
driver.get(portal_url)


with open(portal_file, encoding = 'utf-8-sig') as portal_html:
  # make soup from it
  portal_soup = BeautifulSoup(portal_html, 'html5lib')


for each_file in os.listdir(str(source_path)):
  if Bad_File(each_file):
    # print("Ignoring,", each_file)
    continue
  print("\n- - - - - - -")
  try:
    employer, role = each_file.split(" - ")  
    role = role.split(".txt")[0]
  except ValueError:
    print("* * * *")
    print("Problem with employer and role names here")
    print(each_file)
    employer = input("Input good employer name: ")
    role = input("Input good role name: ")
    print("* * * *\n\n")
  print(role, "at", employer)

  # first loop should trigger the error and get 'tbd' for job_type
  try:
    job_type
  except NameError:
    job_type = 'tbd'

  # now decide what job_type should be
  if 'researcher' in role.lower():
    new_job_type = 'uxr'    
  else:
    new_job_type = 'uxd'
  
  print("Job type:", new_job_type)
  print(role)

  # if that's different from before, do stuff
  # if it's the SAME don't rebuild the legend and css
  if job_type != new_job_type:
    job_type = new_job_type
    # set colors
    colors, bullet_class = Set_Color_CSS(sorted(kw[job_type]['bullets'].keys()))

    # build legend
    portal_soup.find('ul', id='bullet-legend') \
                .replace_with(
                  Build_Legend(sorted(kw[job_type]['bullets'].keys()))
                  )
    # restyle page for job
    portal_soup.find('body')['class'] = job_type

  JD_file = (source_path / each_file).open('r', encoding = 'utf-8-sig')
  JD_formatted = JD_file.read()
  JD_text = JD_formatted.lower()

  # check if we already wrote a letter for this shit
  letter_file_name = "letter " + employer + " - " + role + ".txt"
  if (letter_path / letter_file_name).is_file():
    print("Already have a letter! Skipping it.")
    continue

  # really this is metadata, but I've stashed it in the first 2 lines
  # of the JD text file.
  ad_url = JD_text.split("\n")[0]
  location = JD_text.split("\n")[1]

  # keyword scanner
  topic_votes = defaultdict(lambda: 0)
  for each_keyword in kw[job_type]['keywords']:
    hit_count = len(re.findall(each_keyword,JD_formatted,re.IGNORECASE))
    # hit_count = JD_text.count(each_keyword)
    if hit_count > 0:
      # one nomination per appearance of the keyword
      nominee = kw[job_type]['keywords'][each_keyword]
      topic_votes[nominee] += hit_count
      JD_formatted = Span_Keyword(each_keyword, 
                                  kw[job_type]['keywords'][each_keyword], 
                                  JD_formatted)
  
  weighted_votes = {}
  # Here we weight by an arbitrary dict from a spreadsheet
  # in the spreadsheet, I calculate weight by how special a topic is
  # and how many keywords trigger its nomination
  # eg "get it done" is worth 6 special points and has 13 triggers, so 
  # the total weight is 6/13 vs design system with 4/3
  # Idk if this will work better, but the previous weighting sucked.
  for each_nom in topic_votes:
    # if this line is failing, perhaps the weights csv does not match
    # the keywords or bullets sheets.
    weighted_votes[each_nom] = round(topic_votes[each_nom] 
                                    * float(kw[job_type]['weights'][each_nom])
                                    , 2)
  weighted = Counter(weighted_votes)
  # import code; code.interact(local = locals())

  # extract the nominees with most votes as strings in a list
  print("Recommended bullet points are")
  top_weighted = []
  for each_nom in weighted.most_common(6):
    print('\t' + each_nom[0] + ': ' + '{0:.0%}'.format(each_nom[1]))
    top_weighted.append(each_nom[0])

  # display job ad
  Display_JD(employer, role, JD_formatted)
  

  # Let the user decide
  # arguments should be (counter object, list object)
  three_bullets = Get_Bullets(weighted, top_weighted)
  
  # Now use the bullets to compose a letter!
  Write_Letter(three_bullets, ad_url)
  letters_written[(employer + " - " + role)] = [today]
  letters_written[(employer + " - " + role)].extend(three_bullets)
  
  # log that Spaniel wrote this letter
  with open(cfg['LogFile'], 'w') as outfile:
    json.dump(letters_written, outfile, indent=2, sort_keys=True)
  
  # log this as a job app in a csv
  # applied_to_date, role, employer, location, notes, ad_url
  app_row = ['',role,employer,location,','.join(three_bullets), ad_url]
  with job_app_csv_path.open('a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(app_row)



print("\n\nWoof Woof! Huzzah!")
driver.quit()



