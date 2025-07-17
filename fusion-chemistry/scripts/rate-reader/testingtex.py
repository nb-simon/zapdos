file_name = "hydhel.tex"  # Replace with the actual path to your .tex file


## preprocessing
# import
import numpy as np
import re
import os

# open and read file
file_info = open(file_name, 'r', encoding='utf-8')
file = file_info.readlines()

# clean lines
lines = [line for line in file if line.strip()]

# count lines
line_count = 0
for line in lines:
  line_count += 1


print(lines[495])

print(re.split(' ', lines[495]))

truetest = True

if '\\rightarrow' in lines[495] and truetest == True:
  print('yes')
else:
  print('no')

print(os.path.exists('HYDHEL'))

#os.mkdir('HYDHEL')