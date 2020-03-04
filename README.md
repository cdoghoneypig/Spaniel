# spaniel
## Job Hunting Helper

### Dependencies:
- Python 3.5
- Selenium + webdriver
- BeautifulSoup

# Overview
Spaniel is a set of scripts that scans job ads and produces appropriate cover letters. It automatically scans ads and nominates talking points, but lets the user select which talking points and in what order to put them.

The core idea of this project is that a cover letter only needs a quick intro, a list of 3 bullet points showing why you're a fit for the job, and a quick outro. After writing lots of letters like this, I realized I could standardize my talking points, partially automate their selection, and put together letters much faster.

Ideally, this project would grow to include browser automation that would click all the buttons to apply for every saved job. I've backed away from this because job boards are well defended against bots.

## Workflow

1. Setup a spreadsheet of keywords to scan for, talking points, and boilerplate text.
2. Save job descriptions from job boards to a folder
3. Run letter_writer.py and it will
    * call JD_extractor.py to scrape the saved html pages for content, saving a text file of the JD with some metadata in that text file and in the filename
    * call keywords_csv_to_json.py which will scan your spreadsheet of keywords etc and load these up
    * display job descriptions in a browser window with keywords highlighted
    * suggest talking points based on keyword matches
    * ask for user input so you can pick talking points (or accept the recommended ones)
    * save cover letter with address of job ad as first line
    * continue through all the saved job descriptions

# Setting it up
## Code setup
Put all the code in some folder and get the dependencies

## Write your keywords
The spreadsheet here has to follow some specific rules to be parsed correctly.
I recommend you work from a copy of this
https://docs.google.com/spreadsheets/d/1rNRVr7AdRzMsM7kYIs2M-vlVgUJMs1WkDBnp9Cpnc0Q/edit?usp=sharing

Specific rules to know about
* Don't mess with the top 2 rows unless you want to customize how Spaniel scans csv files. Right now we use A1 cell value to determine how to use the csv.
* Add as many keywords as you want. The "Bullet" should always point to an item on the "Bullets" list
* I struggled with unicode errors when using special characters, so have eliminated them in this spreadsheet. If you add them, you'll have to fix up the scripts to process them safely.
* The "Weights" sheet is important but also still pretty uncertain. The scripts will just lift the Bullet Name and Weight, but I'm still figuring out how to determine weight values best. In the script, Spaniel multiplies a weight by the number of keywords that point to a bullet; this product is the basis for ranking recommendations. For example, lots of hits for a not very "special" keyword should not be recommended as highly as just a few hits for a very "special" keyword. In my case, talking about experience in enterprise SaaS is more important than talking about systems thinking, even if a job ad mentions both the same number of times.
* Textons build the rest of the letter. Please change these.

You'll need to download each sheet to the `keywords` folder.

### Job Types
Spaniel can handle multiple job types (such as "researcher" vs "designer"). Sotre the keyword sheets in subdirectories named for the job type.

If you do this, you could also add a bit of css to spaniel.css that restyles the background for the job type. Actually, this should be a feature in letter_writer, but I hardcoded it in spaniel.css for now! 


## Grab some good job ads
Find jobs that sound appealing. Go to the page that shows just that ad (if there is one!) and **save** that web page to a folder. Go ahead and grab a few ads to get this working for you.

Spaniel has been trained to parse
* LinkedIn
* Glassdoor
* AngelList
* Indeed

## Run letter_writer
This should fire up and 
1. Scan all your saved job ads, producing text files from them
2. Scan your keyword csv files and make json out of them
3. Show jobs, pulling from the text files it produced just prior, including a legend of all your keywords. You must decide which keywords to select for each job, but Spaniel recommends few and gives you its confidence in them.
4. Spaniel saves cover letters to a folder. To actually apply to the job, open up the cover letters one at a time. For each one, copy paste the url at the top to a browser. This should open the job ad and it's on you to paste in your LinkedIn page, upload your resume, and do all the other boring shit. But your cover letter is ready to go! I usually paste them in, but you could create .docx or .pdf from the text files as you please.

                 .--~~,__
    :-....,-------`~~'._.'
     `-,,,  ,_      ;'~U'
      _,-' ,'`-__; '--.
     (_/'~~      ''''(;

Woof!