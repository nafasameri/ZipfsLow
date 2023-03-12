import PyPDF2 
import codecs
import sortedcollections
import math
import matplotlib.pyplot as plt
import encodings

filename = 'snort[WWW.JOZVE.ORG].pdf' 
#filename = 'Solutions_ComputerNetworkingATopDownApproach6Th_111018230632.pdf' 
#filename = 'finals2019solutions.pdf' 
#filename = 'HW1_Ameri_OSLab.pdf' 


with codecs.open(filename, mode='rb') as pdfFile:
    
    pdfReader = PyPDF2.PdfFileReader(pdfFile, strict=True)
    
    text = ''
    words = []
    for i in range(pdfReader.numPages):
        page = pdfReader.getPage(i)
        text += page.extractText()
        words += text.split()

    for i in range(len(words)):
        words[i] = words[i].lower()

    #from nltk.tokenize import word_tokenize
    #from nltk.corpus import stopwords
    #tokens = word_tokenize(text)
    #stop_words = stopwords.words('english')
    punctuations = ['(',')',';',':','[',']',',','.','-','+','=','*','/']
    keywords = [word for word in words if not word in punctuations]

    count_words = sortedcollections.ValueSortedDict()
    for i in range(len(keywords)):
        try:
            n = int(keywords[i]) or float(keywords[i])
        except:
            count_words.setdefault(keywords[i], keywords.count(keywords[i]))
        #finally:
            #keywords.remove(keywords[i])
    
    
    
    #i = 0
    #while i <= len(count_words):
        #count_words.setdefault(keywords[i], keywords.count(keywords[i]))
        #i += 1

    d = {}
    #i = len(count_words)
    for i in range(len(count_words), 0):
    #while i >= 0:
        #i -= 1
        d.setdefault(count_words.peekitem(i)[0], count_words.peekitem(i)[1]) 
    
    old = count_words
    count_words = d.items()

    log_count_words = {}
    for i in range(len(count_words)):
        #val = count_words.peekitem(i)
        #log_count_words.setdefault(val[0], math.log10(val[1]))
        #key = next((v for j, v in enumerate(count_words) if j == i))[0]
        key = math.log10(i + 1)
        val = next((v for j, v in enumerate(count_words) if j == i))[1]
        log_count_words.setdefault(key, math.log10(val))
    

    
    zipf = plt.figure()
    plt.plot(range(0, len(log_count_words)), d.values(), '-', label="without log")
    plt.title("Zipf's Low")
    plt.xlabel("words")
    plt.ylabel("count")
    plt.legend(loc="lower right")
    plt.savefig(filename +"zipf.png")

    zipf_log = plt.figure()
    plt.plot(log_count_words.keys(),log_count_words.values(),'-',label="with log")
    plt.title("Zipf's Low")
    plt.xlabel("words")
    plt.ylabel("count")
    plt.legend(loc="lower right")
    plt.savefig(filename +"_log.png")


    new_filename = 'result.csv'
    new_file = open(new_filename, 'w')

    for i in range(len(old)):
        val = old.peekitem(i)
        new_file.write(str(val[0]) + ',' + str(val[1])+ '\n')

    new_file.close()
