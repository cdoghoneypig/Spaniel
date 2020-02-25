# this is a library for letter_writer
# it grabs the csv files in keywords/
# turns them into json
# saves the json
# and returns the json too

import os, json, csv
from collections import defaultdict

# keywords: {"spicy" : "tasty"}
# bullets: {"tasty": "I am a very tasty noodle!"}
# textons: {"greeting": "Hey there,"}
# proximity: {["collaborate","teams",15,"cross-functional"]}

# proximity feature to be done later

def Build_Keyword_Dict(verbose):
  keyword_dict = defaultdict(lambda: {})

  csv_folder = 'keywords/'
  json_file_path = 'keyword_dict.json'
   
  if verbose:
    print("\n\nThis script will scan keyword csv files from", csv_folder, end = "\n\n")

  counter = defaultdict(lambda: 0)

  for each_file in os.listdir(csv_folder):
    if each_file.endswith(".csv"): 
      with open(csv_folder + each_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # get the first key for our dict from the first row
        which_csv_is_this = next(csv_reader)[0].lower()
        # display headers
        if verbose:
          print(which_csv_is_this, next(csv_reader))
        else:
          next(csv_reader)
        for row in csv_reader:
          # skip if the value is blank
          if row[1] == '':
            continue
          this_key = row[0]
          this_value = row[1]
          # import code; code.interact(local=locals())
          
          keyword_dict[which_csv_is_this][this_key] = this_value
          counter[which_csv_is_this] += 1
    if verbose:
      print(which_csv_is_this, counter[which_csv_is_this], "records scanned", end = "\n\n")
            
  if verbose:
    print("Done. Saving to", json_file_path)

  with open(json_file_path, "w") as write_file:
    json.dump(keyword_dict, write_file, indent=2, sort_keys=True) 

  return keyword_dict
