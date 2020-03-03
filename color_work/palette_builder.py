# ,05fec1,"rgb(2.1%, 99.2%, 75.7%)",bright teal

import csv, json

colorCSV = open('colors.csv')
color_in = csv.reader(colorCSV)
color_list = []
for each_row in color_in:
  rgb = each_row[2]
  stringPercent_list = rgb[4:-1].split(',')
  rgba_list = []
  for each_percent in stringPercent_list:
    bad_number = each_percent.strip('%')
    bad_number = round(255 * float(bad_number)/100)
    # convert to 0-255 value then append to list
    rgba_list.append(str(bad_number))
  rgba_list.append('.25')
  good_color = 'rgba(' + ','.join(rgba_list) + ')'
  print(good_color)
  color_list.append(good_color)

with open('color_palette.json', 'w') as outfile:
  json.dump(color_list, outfile, indent=2, sort_keys=True)
