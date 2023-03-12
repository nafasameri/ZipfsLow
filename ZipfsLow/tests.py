
#I don't seem to be able to count the total number of words in a .pdf file. I assume one of the easiest ways is to count the number of spaces. I've tried the two following approaches:

#1). Open the file and count the number of spaces in each page:

import PyPDF2

filename = '373225c.pdf'

pdf_file = open(filename, 'r')

read_pdf = PyPDF2.PdfFileReader(filename)
number_of_pages = read_pdf.getNumPages()

pattern = ' '
total_number_of_spaces = 0

for page in range(number_of_pages):
    read_page = read_pdf.getPage(page)
    page_content = read_page.extractText()
    counted_spaces_per_page = page_content.count(pattern)
    total_number_of_spaces += counted_spaces_per_page

print(total_number_of_spaces)


#The problem here is that the text that I see in Python has additional spaces, as in "A 1 B 2" instead of "A1B2", "n umerous" instead of "numerous" or "[ 1 ]" instead of "[1]".

#2). Save the data in an intermediate file and read this file as a second step.

import re
import PyPDF2

filename = 'Text.pdf'

pdf_file = open(filename, 'r')

read_pdf = PyPDF2.PdfFileReader(filename)
number_of_pages = read_pdf.getNumPages()

new_filename = 'new_file.csv'

pattern = r'\s+'
repl = r' '

saved = []

for page in range(number_of_pages):
    read_page = read_pdf.getPage(page)
    page_content = read_page.extractText()
    to_be_saved = re.sub(pattern, repl, page_content)
    saved.append(to_be_saved)

new_file = open(new_filename, 'w')

for element in saved:
    new_file.write(str(element))

new_file.close()

with open(new_filename, 'r') as file:
    lines = file.readlines()
    print(lines)
    all_spaces = re.findall(repl, str(lines))
    print(len(all_spaces))


#But of course, the abovementioned problem persists.

#Probably the correct question to ask would be "How do I get rid of extra space constants in a .pdf document opened in Python?" but I guess someone may know a different method of counting words in a .pdf document using Python (unrelated to the number of spaces)?
