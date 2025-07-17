# script for reading fitted cross sections from the AMJUEL or HYDHEL databases
# I apologize in advance to anyone who knows more about Python than me who happens to read this code

## inputs

# input pdf file name
file = 'HYDHEL.pdf'

# database 
# enter database as integer
# 1 for AMJUEL, 2 for HYDHEL
db = 2

# reaction selection
# create a dict of tuples for each section you wish to extract reactions from
# names are for sections, tuples are for reaction selection
# three options for list formatting:
#   1: discrete, individual reactions:                        ('discrete', '2.1.1', '2.1.7', '2.3.1a')
#   2: range of reactions with defined start and end points:  ('range', '2.1.2', '2.2.8')
#   3: all reactions in a section:                            ('a')
# e.g. {'H.1': ('discrete', '2.1.1', '2.1.7', '2.3.1a'), 'H.2':  ('range', '2.1.2', '2.2.8'), 'H.3': ('a')}
rxns = {'H.1': ('discrete', '2.1.1'), 'H.2':  ('range', '2.1.2', '2.2.8'), 'H.3': ('a')}

# import
from pypdf import PdfReader

# read pdf
reader = PdfReader(file)

## find page indices for sections
# initialize index list
indices = []

# start at first page
start = 0

# generate section list
if db == 1:
  sections = ('H.0', 'H.1', 'H.2', 'H.3', 'H.4', 'H.5', 'H.6', 'H.7', 'H.8', 'H.9', 'H.10', 'H.11', 'H.12')
  cind = ('p', 'a', 'b', '.', '.', '.', '.', '.', 'h', '.', '.', 'k', '.')
elif db == 2:
  sections = ('H.1', 'H.2', 'H.3', 'H.8')
  cind = ('a', 'b', '.', 'h')

# loop through selected sections
for i in range(len(sections)):
  # loop through pages
  for j in range(start, len(reader.pages)):
    # load page
    page = reader.pages[j]

    # extract page text
    text = page.extract_text(extraction_mode='layout', layout_mode_space_vertically=False)

    # check if page is the start of a section
    if text[4:4+len(sections[i])] == sections[i]:
      # save section index
      indices = indices + [j]

      # adjust start point for subsequent index searches to save time
      start = j
      break

# add last page as end index
indices = indices + [len(reader.pages) - 1]
print(indices)


## extracting fits
# initialize fits dict
fits = {}

# check selected database
if db == 1:
  print('Configured for AMJUEL database.')

elif db == 2:
  print('Configured for HYDHEL database.')

  # loop though selected sections
  for key, value in rxns.items():
    print('Searching through section ' + key + '...')
    #print(value[0])

    # initialize coefficient index list
    coeff_index = []

    # find section indices
    if key == 'H.8':
      page_indices = [indices[3], indices[4]] # idk why HYDHEL skips from H.3 to H.8, but I don't want to rewrite this logic so this will be hardcoded
      coeff_index = range(9)
      coeff_type = 'int'
    else:
      page_indices = [indices[int(key[2:len(key)]) - 1], indices[int(key[2:len(key)])]]
      if cind[int(key[2:len(key)]) - 1] == '.':
        coeff_index = range(9)
        coeff_type = 'int'
      else:
        for n in range(9):
          coeff_index = coeff_index + [cind[int(key[2:len(key)]) - 1] + str(n)]
        coeff_type = 'str'
    print(page_indices)
    print(coeff_index)

    # loop through pages in section
    for j in range(page_indices[0], page_indices[1]):
      # load page
      page = reader.pages[j]

      # extract page text
      text = page.extract_text(extraction_mode='layout', layout_mode_space_vertically=False)

      # discrete reaction list selection scheme
      if value[0] == 'discrete':
        print('Searching through input list of reactions... Currently on page ' + str(j + 1) + '...')

        # loop through reaction list
        for k in range(1, len(value)):
          # check if reaction is on page
          if value[k] in text:
            print('Found reaction ' + value[k] + ' on page ' + str(j + 1) + '.')

            # initialize coefficient list
            coeffs = []

            # reaction start index
            rxn_index = text.find(value[k])

            # loop through text
            for l in range(rxn_index, len(text)):
              counter = 0

              # check coefficient delimeter
              if coeff_type == 'str':
                # identify first delimeter
                if text[l:l+2] == coeff_index[counter]:
                  ####################################################### STOPPED HERE ###########################################

      # reaction range selection scheme
      elif value[0] == 'range':
        print('Searching reactions from ' + str(value[1]) + ' to ' + str(value[2]) + '... Currently on page ' + str(j + 1) + '...')
        

      # all reactions selection scheme
      elif value[0] == 'a':
        print('Searching all reactions... Currently on page ' + str(j + 1) + '...')











#print(rxns['H.1'])

#print(len(rxns))



page = reader.pages[11]

number_of_pages = len(reader.pages)
#print(number_of_pages)

text = page.extract_text(extraction_mode='layout', layout_mode_space_vertically=False)

print(text)

print(text[4:4+len(key)])

#print(len(text))


#print(type(text))

'''
for i in range(len(text) - 2):
  if text[i:i+2] == 'a0':
    print(text[i:i+2])
'''


'''
test1 = '12345test'

print(test1)

print(test1[6:6+2])

if test1[6:6+2] == 'es':
  print('pass')

for i in range(len(test1) - 2):
  if test1[i:i+2] == 'es':
    print('pass2')

'''