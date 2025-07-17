# script for reading fitted cross sections from the AMJUEL or HYDHEL databases
# I apologize in advance to anyone who knows more about Python than me (not a high bar) who happens to read this code

## inputs
# input file name where reactions can be found
file_name = 'hydhel.tex'
#file_name = 'amjuel.tex'

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
#rxns = {'H.1': ('discrete', '2.1.1', '2.1.2'), 'H.2':  ('range', '2.1.1', '2.1.3'), 'H.3': ('a')}
rxns = {'H.1': ('a'), 'H.2': ('a'), 'H.3': ('a'), 'H.8': ('a')}



#################################################
########## NO INPUTS BEYOND THIS POINT ##########
#################################################



## preprocessing
# import
import numpy as np
import re
import os
import shutil

# open and read file
file_info = open(file_name, 'r', encoding='utf-8')
file = file_info.readlines()

# clean lines
lines = [line for line in file if line.strip()]

# count lines
line_count = 0
for line in lines:
  line_count += 1

## find line indices for sections
# initialize index list
indices = []

# start at first line
start = 0

# generate section list and folders to store output
if db == 1:
  sections = ('H.0', 'H.1', 'H.2', 'H.3', 'H.4', 'H.5', 'H.6', 'H.7', 'H.8', 'H.9', 'H.10', 'H.11', 'H.12')
  cind = ('p', 'a', 'b', '.', '.', '.', '.', '.', 'h', '.', '.', 'k', '.')
  if os.path.exists('AMJUEL Rates') == False:
    os.mkdir('AMJUEL Rates')
  else:
    shutil.rmtree('AMJUEL Rates/')
    os.mkdir('AMJUEL Rates')
  for section in sections:
    if os.path.exists('AMJUEL Rates/' + section) == False:
      os.makedirs('AMJUEL Rates/' + section)
elif db == 2:
  sections = ('H.1', 'H.2', 'H.3', 'H.8')
  cind = ('a', 'b', '.', 'h')
  if os.path.exists('HYDHEL Rates') == False:
    os.mkdir('HYDHEL Rates')
  else:
    shutil.rmtree('HYDHEL Rates/')
    os.mkdir('HYDHEL Rates')
  for section in sections:
    if os.path.exists('HYDHEL Rates/' + section) == False:
      os.makedirs('HYDHEL Rates/' + section)

# loop through selected sections
for section in sections:
  # loop through lines
  for line in range(start, line_count):
    # check if line is the start of a section
    if lines[line][1:9+len(section)] == 'section{' + section:
      # save section index
      indices = indices + [line]

      # adjust start point for subsequent searches and exit loop
      start = line
      break

# add last page as end index
indices += [len(lines) - 1]

## extracting fit coefficients
# initialize fit coefficients dict
fit_coeffs = {}

# check selected database
if db == 1:
  print('Configured for AMJUEL database.')

elif db == 2:
  print('Configured for HYDHEL database.')

  # loop through selected sections
  for section, selections in rxns.items():
    # initalize section dict for fits
    fit_coeffs[section] = {}

    # initialize coefficient index list
    coeff_index = []

    # find section indices
    if section == 'H.8':
      line_indices = [indices[3], indices[4]] # idk why HYDHEL skips from H.3 to H.8, but I don't want to rewrite this logic so this will be hardcoded
      for n in range(9):
        coeff_index = coeff_index + [cind[sections.index(section)] + str(n)]
      coeff_type = 'str'
    else:
      line_indices = indices[sections.index(section):sections.index(section)+2]
      if cind[sections.index(section)] == '.':
        coeff_index = [str(num) + ' ' for num in range(9)]
        coeff_type = 'int'
      else:
        for n in range(9):
          coeff_index = coeff_index + [cind[sections.index(section)] + str(n)]
        coeff_type = 'str'

    # check selection scheme
    if selections[0] == 'discrete':
    
      print('Searching through input list of reactions in section ' + section + '...')
      selection_mode = 1
    elif selections[0] == 'range':
    
      print('Searching for reactions from ' + str(selections[1]) + ' to ' + str(selections[2]) + ' in section ' + section + '...')
      selection_mode = 2
      full_list = False
      in_range = False
      rxn_found = False
    elif selections[0] == 'a':
    
      print('Searching through all reactions in section ' + section + '...')
      selection_mode = 3
      rxn_found = False

    # loop through lines in section
    for line in range(line_indices[0], line_indices[1]):
    
      # discrete reaction list selection scheme
      if selection_mode == 1:
    
        # loop through reaction list
        for reaction in range(1, len(selections)):
    
          # check if reaction is on line
          if selections[reaction] + ' ' in lines[line]:
            print('Found reaction ' + selections[reaction] + ' starting on line ' + str(line + 1) + '.')

            # initialize coefficient matrix
            coeffs = []

            # string delimiters
            if coeff_type == 'str':
            
              # find where fit data starts
              started = False
              data_start = line
            
              while started == False:
            
                # identify when reaction data starts
                if coeff_index[0] + ' ' in lines[data_start]:
            
                  started = True
                  print('The data for reaction ' + selections[reaction] + ' starts on line ' + str(data_start + 1) + '.')
                else:
            
                  data_start += 1

              # loop over lines
              for i in range(0, 3):
              
                # set delimiters
                delimiters = '|'.join(map(re.escape, coeff_index))

                # delimit
                delimit = re.split(delimiters, lines[data_start + i])

                # clean
                remove = [' ', '\n', ',']
                clean = []
              
                for s in delimit:
              
                  for rm in remove:
              
                    s = s.replace(rm, '')
              
                  clean.append(s)

                # filter
                filtered = [item for item in clean if item]

                # convert
                final = list(map(float, filtered))

                # add to coefficient matrix
                coeffs += final

              # add reaction's coefficients to dict
              fit_coeffs[section][selections[reaction]] = coeffs

              # write reacton's coefficients to text file
              with open('HYDHEL Rates/' + section + '/' + selections[reaction] + '.txt', 'w') as rxn_file:
                rxn_file.write(', '.join(map(str, coeffs)))
            # integer delimiters
            elif coeff_type == 'int':
            
              # set delimiters
              delimiters = '|'.join(map(re.escape, coeff_index))

              # find where fit data starts
              started = False
              data_start = line
              
              while started == False:
              
                if 'T Index' in lines[data_start]:
              
                  started = True
                  data_start += 1
                  print('The data for reaction ' + selections[reaction] + ' starts on line ' + str(data_start + 1) + '.')
                else:
              
                  data_start += 1

              # loop over lines
              for i in range(0, 9):
              
                # set delimiters
                delimiters = ' '

                # delimit
                delimit = re.split(delimiters, lines[data_start + i] + lines[data_start + i + 11] + lines[data_start + i + 22])

                # clean
                remove = [' ', '\n', ',']
                clean = []
                
                for s in delimit:
                
                  for rm in remove:
                
                    s = s.replace(rm, '')
                
                  clean.append(s)

                # filter empty items
                filtered = [item for item in clean if item]

                # filter leftover delimeter
                filtered = [item for item in filtered if item != str(coeff_index[i][0])]

                # convert
                final = list(map(float, filtered))

                # add to coefficient matrix
                coeffs.append(final)

                # add to text file
                if i == 1:
                  with open('HYDHEL Rates/' + section + '/' + selections[reaction] + '.txt', 'w') as rxn_file:
                    rxn_file.write(', '.join(map(str, final)))
                else:
                  with open('HYDHEL Rates/' + section + '/' + selections[reaction] + '.txt', 'a') as rxn_file:
                    rxn_file.write('\n')
                    rxn_file.write(', '.join(map(str, final)))

              # add reaction's coefficients to dict
              fit_coeffs[section][selections[reaction]] = coeffs
      # reaction range selection scheme
      elif selection_mode == 2:
      
        # loop until full range is found
        if full_list == False:

          # check if first reaction is on line
          if selections[1] + ' ' in lines[line]:
      
            print('Found reaction ' + selections[1] + ' starting on line ' + str(line + 1) + '.')

            in_range = True
            first_rxn = True

            # initialize coefficient matrix
            coeffs = []
          
          # begin processing if in selected range
          if in_range == True:
            
            # extract reaction number if necessary
            if '\\rightarrow' in lines[line] and first_rxn == False:

              rxn_found = True
              
              # delimit line
              rxn_line = re.split(' ', lines[line])
              
              # save number
              rxn_number = rxn_line[1]

              print('Found reaction ' + rxn_number + ' starting on line ' + str(line + 1) + '.')

              # initialize coefficient matrix
              coeffs = []

              # check if reaction is the last one
              if rxn_number == selections[2]:
                
                full_list = True

            # string delimiters
            if coeff_type == 'str' and rxn_found or coeff_type == 'str' and first_rxn:
              
              # find where fit data starts
              started = False
              data_start = line
              
              while started == False:
                
                # identify when reaction data starts
                if coeff_index[0] + ' ' in lines[data_start]:
                
                  started = True
                
                  if first_rxn == True:
                
                    print('The data for reaction ' + selections[1] + ' starts on line ' + str(data_start + 1) + '.')
                  elif first_rxn == False:
                
                    print('The data for reaction ' + rxn_number + ' starts on line ' + str(data_start + 1) + '.')

                else:
                
                  data_start += 1

              # loop over lines
              for i in range(0, 3):
              
                # set delimiters
                delimiters = '|'.join(map(re.escape, coeff_index))

                # delimit
                delimit = re.split(delimiters, lines[data_start + i])

                # clean
                remove = [' ', '\n', ',']
                clean = []
               
                for s in delimit:
                
                  for rm in remove:
                  
                    s = s.replace(rm, '')
                  
                  clean.append(s)

                # filter
                filtered = [item for item in clean if item]

                # convert
                final = list(map(float, filtered))

                # add to coefficient matrix
                coeffs += final

              # add reaction's coefficients to dict and write to text file
              if first_rxn == True:
              
                fit_coeffs[section][selections[1]] = coeffs
                first_rxn = False
                rxn_found = False

                with open('HYDHEL Rates/' + section + '/' + selections[1] + '.txt', 'w') as rxn_file:
                  rxn_file.write(', '.join(map(str, coeffs)))
              elif first_rxn == False:
              
                fit_coeffs[section][rxn_number] = coeffs
                rxn_found = False

                with open('HYDHEL Rates/' + section + '/' + rxn_number + '.txt', 'w') as rxn_file:
                  rxn_file.write(', '.join(map(str, coeffs)))
            # integer delimiters
            elif coeff_type == 'int' and rxn_found or coeff_type == 'int' and first_rxn:
          
              # set delimiters
              delimiters = '|'.join(map(re.escape, coeff_index))

              # find where fit data starts
              started = False
              data_start = line
              
              while started == False:
              
                if 'T Index' in lines[data_start]:
                
                  started = True
                  data_start += 1
                
                  if first_rxn == True:
                
                    print('The data for reaction ' + selections[1] + ' starts on line ' + str(data_start + 1) + '.')
                  elif first_rxn == False:
                
                    print('The data for reaction ' + rxn_number + ' starts on line ' + str(data_start + 1) + '.')
                else:
                  data_start += 1

              # loop over lines
              for i in range(0, 9):
                # set delimiters
                delimiters = ' '

                # delimit
                delimit = re.split(delimiters, lines[data_start + i] + lines[data_start + i + 11] + lines[data_start + i + 22])

                # clean
                remove = [' ', '\n', ',']
                clean = []
                
                for s in delimit:
                
                  for rm in remove:
                
                    s = s.replace(rm, '')
                
                  clean.append(s)

                # filter empty items
                filtered = [item for item in clean if item]

                # filter leftover delimeter
                filtered = [item for item in filtered if item != str(coeff_index[i][0])]

                # convert
                final = list(map(float, filtered))

                # add to coefficient matrix
                coeffs.append(final)

                # add to text file
                if first_rxn == True:
                  if i == 1:
                    with open('HYDHEL Rates/' + section + '/' + selections[1] + '.txt', 'w') as rxn_file:
                      rxn_file.write(', '.join(map(str, final)))
                  else:
                    with open('HYDHEL Rates/' + section + '/' + selections[1] + '.txt', 'a') as rxn_file:
                      rxn_file.write('\n')
                      rxn_file.write(', '.join(map(str, final)))
                elif first_rxn == False:
                  if i == 1:
                    with open('HYDHEL Rates/' + section + '/' + rxn_number + '.txt', 'w') as rxn_file:
                      rxn_file.write(', '.join(map(str, final)))
                  else:
                    with open('HYDHEL Rates/' + section + '/' + rxn_number + '.txt', 'a') as rxn_file:
                      rxn_file.write('\n')
                      rxn_file.write(', '.join(map(str, final)))

              # add reaction's coefficients to dict
              if first_rxn == True:
              
                fit_coeffs[section][selections[1]] = coeffs
                first_rxn = False
                rxn_found = False
              elif first_rxn == False:
              
                fit_coeffs[section][rxn_number] = coeffs
                rxn_found = False
      # full section selection scheme
      elif selection_mode == 3:
          
        # extract reaction number if necessary
        if '\\rightarrow' in lines[line] and '\\rightarrow' not in lines[line - 1]:

          rxn_found = True
          
          # delimit line
          rxn_line = re.split(' ', lines[line])
          
          # save number
          rxn_number = rxn_line[1]

          print('Found reaction ' + rxn_number + ' starting on line ' + str(line + 1) + '.')

          # initialize coefficient matrix
          coeffs = []

        # string delimiters
        if coeff_type == 'str' and rxn_found == True:
          
          # find where fit data starts
          started = False
          data_start = line
          
          while started == False:
            
            # identify when reaction data starts
            if coeff_index[0] + ' ' in lines[data_start]:
            
              started = True
          
              print('The data for reaction ' + rxn_number + ' starts on line ' + str(data_start + 1) + '.')

            else:
            
              data_start += 1

          # loop over lines
          for i in range(0, 3):
          
            # set delimiters
            delimiters = '|'.join(map(re.escape, coeff_index))

            # delimit
            delimit = re.split(delimiters, lines[data_start + i])

            # clean
            remove = [' ', '\n', ',']
            clean = []
            
            for s in delimit:
            
              for rm in remove:
              
                s = s.replace(rm, '')
              
              clean.append(s)

            # filter
            filtered = [item for item in clean if item]

            # convert
            final = list(map(float, filtered))

            # add to coefficient matrix
            coeffs += final

          # add reaction's coefficients to dict
          fit_coeffs[section][rxn_number] = coeffs
          rxn_found = False

          # write reacton's coefficients to text file
          with open('HYDHEL Rates/' + section + '/' + rxn_number + '.txt', 'w') as rxn_file:
            rxn_file.write(', '.join(map(str, coeffs)))
        # integer delimiters
        elif coeff_type == 'int' and rxn_found:
      
          # set delimiters
          delimiters = '|'.join(map(re.escape, coeff_index))

          # find where fit data starts
          started = False
          data_start = line
          
          while started == False:
          
            if 'T Index' in lines[data_start]:
            
              started = True
              data_start += 1

              print('The data for reaction ' + rxn_number + ' starts on line ' + str(data_start + 1) + '.')
            else:
              data_start += 1

          # loop over lines
          for i in range(0, 9):
            # set delimiters
            delimiters = ' '

            # delimit
            delimit = re.split(delimiters, lines[data_start + i] + lines[data_start + i + 11] + lines[data_start + i + 22])

            # clean
            remove = [' ', '\n', ',']
            clean = []
            
            for s in delimit:
            
              for rm in remove:
            
                s = s.replace(rm, '')
            
              clean.append(s)

            # filter empty items
            filtered = [item for item in clean if item]

            # filter leftover delimeter
            filtered = [item for item in filtered if item != str(coeff_index[i][0])]

            # convert
            final = list(map(float, filtered))

            # add to coefficient matrix
            coeffs.append(final)

            # add to text file
            if i == 1:
              with open('HYDHEL Rates/' + section + '/' + rxn_number + '.txt', 'w') as rxn_file:
                rxn_file.write(', '.join(map(str, final)))
            else:
              with open('HYDHEL Rates/' + section + '/' + rxn_number + '.txt', 'a') as rxn_file:
                rxn_file.write('\n')
                rxn_file.write(', '.join(map(str, final)))

          # add reaction's coefficients to dict
          fit_coeffs[section][rxn_number] = coeffs
          rxn_found = False

        #print(fit_coeffs)


