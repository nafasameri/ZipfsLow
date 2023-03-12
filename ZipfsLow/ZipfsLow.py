import PyPDF2 
import codecs
import sortedcollections
import math
import matplotlib.pyplot as plt


def replace(text):

    text = text.replace('»', ' ')
    text = text.replace('«', ' ')
    text = text.replace('_', ' ')
    text = text.replace('-', ' ')
    text = text.replace('+', ' ')
    text = text.replace('=', ' ')
    text = text.replace('*', ' ')
    text = text.replace('"', ' ')
    text = text.replace('\'', ' ')
    text = text.replace('!', ' ')
    text = text.replace('؟', ' ')
    text = text.replace('?', ' ')
    text = text.replace(':', ' ')
    text = text.replace(',', ' ')
    text = text.replace('٫', ' ')
    text = text.replace('.', ' ')
    text = text.replace('(', ' ')
    text = text.replace(')', ' ')
    text = text.replace('[', ' ')
    text = text.replace(']', ' ')
    text = text.replace(')', ' ')
    text = text.replace('/', ' ')
    text = text.replace('،', ' ')
    text = text.replace('0', ' ')
    text = text.replace('1', ' ')
    text = text.replace('2', ' ')
    text = text.replace('3', ' ')
    text = text.replace('4', ' ')
    text = text.replace('5', ' ')
    text = text.replace('6', ' ')
    text = text.replace('7', ' ')
    text = text.replace('8', ' ')
    text = text.replace('9', ' ')
    text = text.replace('۰', ' ')
    text = text.replace('۱', ' ')
    text = text.replace('۲', ' ')
    text = text.replace('۳', ' ')
    text = text.replace('۴', ' ')
    text = text.replace('۵', ' ')
    text = text.replace('۶', ' ')
    text = text.replace('۷', ' ')
    text = text.replace('۸', ' ')
    text = text.replace('۹', ' ')
    
    return text


def readText(filename):

    with open(filename, mode='r', encoding='utf-8') as textFile:

        txt = textFile.readlines()
        text = ''
        for i in range(len(txt)):
            text += txt[i]

        text = replace(text)
        words = text.split()

        for i in range(len(words)):
            words[i] = words[i].lower()

    return words


def readPDF(filename):

    with codecs.open(filename, mode='rb') as pdfFile:
    #PyPDF2.pdf.PdfFileReader()
        pdfReader = PyPDF2.pdf.PdfFileReader(pdfFile, strict=True)
    
        text = ''
        words = []
        for i in range(pdfReader.numPages):
            page = pdfReader.getPage(i)
            text += page.extractText()

        text = replace(text)
        words += text.split()

        for i in range(len(words)):
            words[i] = words[i].lower()

        punctuations = ['(',')',';',':','[',']',',','.','-','+','=','*','/']
        keyword = [word for word in words if not word in punctuations]

    return keyword


def countWord(keywords):
    count_words = sortedcollections.ValueSortedDict()
    for i in range(len(keywords)):
        try:
            count_words.setdefault(keywords[i], keywords.count(keywords[i]))
            keywords.remove(keywords[i])
        except:
            pass
     
    order = {}
    i = len(count_words)
    while i >= 0:
        i -= 1
        order.setdefault(count_words.peekitem(i)[0], count_words.peekitem(i)[1]) 

    count_words = order.items()
    
    log_count_words = {}
    for i in range(len(count_words)):
        key = math.log10(i + 1)
        val = math.log10(next((v for j, v in enumerate(count_words) if j == i))[1])
        log_count_words.setdefault(key, val)

    return count_words, log_count_words, order


def plotZipf(x, y, x_log, y_log, filename):
    
    fig, z = plt.subplots(2, 1)   
    z[0].plot(x, y, '-', label="without log")
    z[1].plot(x_log, y_log,'-', label="with log")
    plt.title("Zipf's Low")
    plt.xlabel("words")
    plt.ylabel("count")
    plt.legend(loc="lower right")
    plt.savefig(filename +'.pdf')
    plt.savefig(filename +'.png')

    zipf = plt.figure()
    plt.plot(x, y, '-', label="without log")
    plt.title("Zipf's Low")
    plt.xlabel("words")
    plt.ylabel("count")
    plt.legend(loc="lower right")
    plt.savefig(filename +"_zipf.png")
    plt.savefig(filename +"_zipf.pdf")

    zipf_log = plt.figure()
    plt.plot(x_log, y_log,'-', label="with log")
    plt.title("Zipf's Low")
    plt.xlabel("words")
    plt.ylabel("count")
    plt.legend(loc="lower right")
    plt.savefig(filename +"_log.png")
    plt.savefig(filename +"_log.pdf")


def writeCSV(filename, count_words, log_count_words):

    with codecs.open(filename, 'wb', encoding='utf-32') as new_file:
        log = log_count_words.items()

        new_file.write("words,count,log(index),log(count)\n")
        for i in range(len(count_words)):
            v = next((v for j, v in enumerate(count_words) if j == i))
            l0 = next((v for j, v in enumerate(log) if j == i))[0]
            l1 = next((v for j, v in enumerate(log) if j == i))[1]
            new_file.write(str(v[0]) + ',' + str(v[1])+ ',' + str(l0) + ',' + str(l1) + '\n')

        new_file.close()      


if __name__ == '__main__':

    #filename = 'snort.pdf'
    filename = 'History Herodutus.txt'
    new_filename = filename + '_result.csv'

    #keywords = readPDF(filename)
    keywords = readText(filename)
    count_words, log_count_words, order = countWord(keywords)

    plotZipf(range(0, len(count_words)), order.values(), log_count_words.keys(), log_count_words.values(), filename)
    writeCSV(new_filename, count_words, log_count_words)