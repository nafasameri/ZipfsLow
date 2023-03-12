import textract, re
text = textract.process("sample.pdf") # http://www.africau.edu/images/default/sample.pdf
words = re.findall(r"[^\W_]+", text, re.MULTILINE) # regex demo and explanation - https://regex101.com/r/U7WMSA/1
print(len(words))
print(words)




import re
from operator import itemgetter    
 
frequency = {}
open_file = open('d2016.bin', 'r')
file_to_string = open_file.read()
words = re.findall(r'(\b[A-Za-z][a-z]{2,9}\b)', file_to_string)
 
for word in words:
    count = frequency.get(word,0)
    frequency[word] = count + 1
     
for key, value in reversed(sorted(frequency.items(), key = itemgetter(1))):
    print key, value