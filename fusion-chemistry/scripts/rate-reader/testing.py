file = 'HYDHEL.pdf'

# import
from pypdf import PdfReader

# read pdf
reader = PdfReader(file)


#print(rxns['H.1'])

#print(len(rxns))



page = reader.pages[175]

number_of_pages = len(reader.pages)
#print(number_of_pages)

text = page.extract_text(extraction_mode='layout', layout_mode_space_vertically=False)

print(text)

index = text.find('a0')

print(index)

print(text[index:index+2])

rtest = range(8)
for n in rtest:
  print(n)