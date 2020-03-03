# spaniel
 Job Hunting Helper

Python 3.3

Dependencies:
Selenium + webdriver
BeautifulSoup

Still a work in progress but basic workflow is

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

Spaniel currently parses
* LinkedIn
* Glassdoor
* AngelList
* Indeed

Spaniel can handle multiple job types (such as "researcher" vs "designer"), if you make multiple subdirectories storing your keywords.

I should provide sample files for keyword spreadsheets etc, but right now it's just a tool I'm using so pls reach out!

