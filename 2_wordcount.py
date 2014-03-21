import csv
from collections import Counter
import re #  for regular expression
import string

with open('BLAST_data.csv', 'r') as f:

	reader = csv.reader(f, delimiter=',')

	# set up global major variables
	text = "" #  create a string to parse raw text
	words = [] #  create a list to consolidate words
	wordcount = {} #  create a dictionary for word count

	# set up exception lists
	words_to_ignore = [
	"that","what","with","this","would", "from","your","which","while","these",
	"and","the","blast","all","there","you","place","time","charset","gone",
	"finest","here","year","2014","are","two","being","years","need","again",
	"doing","ideas","tax","http","weekend","away","for","get","when","encourage",
	"melt","type","msg","emailmessagemessage","instance", "none", "can", 
	"business", "have", "text/plain","iso-8859-1","will","gsb","their","who",
	"has","mba","out","school", "help","looking","work", "but", 
	"more", "interested","n20140313","class","they","n20140312","new","see",
	"how","day","event","please","first","receiving","account","know",
	"companies","fund","below","about","some","any","like","sign","project",
	"graduate","candidate","social","multipart/alternative","company","been",
	"experience","one","mar","april","its","email","set","not","student",
	"students","n20140314","want","spring","san","someone","great","change",
	"good","calendar","other","others","because","n20140317","our","was",
	"n20140211","anyone","just","let","now","course","also","last","into",
	"bring","n20140115","windows-1252","make","along","invite",
	"working","take","research","jan","were","nhi","n<emailmessagemessage",
	"those","february","nov","come","over","2013","november","join","well",
	"stanford","youre","next","best","his","them","small","organizations",
	"love","events","group","happy","talk","many","world","learn","program",
	"people","global","forward","meet","could","than","most","opportunity",
	"week","very","look","through","market","friend","summer","reach","off",
	"big","where","around","back","community","thursday","impact","message",
	"john","12pm","today","only","sales","director","650","had","date",
	"strategic","then","building","both","way","forwarded","ceo","minutes",
	"currently","link","process","12e","january","point","details","strong",
	]

	things_to_strip = [
	".",",","?","!","(",")","{","}","$","&","[","]","'",
	]

	# set up process variables
	words_min_size = 3
	top_size = 10

	# get the range of the dataset
	date = {'date_max':'','date_min':''} #  create a dictionary
	
	line_total = sum(1 for line in reader)
	f.seek(0) #  set the iterator to initial position

	i = 0
	for line in reader:
		i += 1

		if i == 1: #  get the most recent date available
			date['date_max'] = line[0][2:10]
		elif i == line_total:
			date['date_min'] = line[0][2:10]
		else:
			pass

	print "\nThis dataset constains Stanford GSB BLAST emails from: "
	print "%s to %s\n" % (date['date_min'], date['date_max'])

	f.seek(0) #  reset the pointer again

	# get input from user for the date range
	date_beg = raw_input("Enter the beginning date in YYYYMMDD format: >>  ")
	date_end = raw_input("Enter the ending date in YYYYMMDD format: >>  ")

	# calculate word frequency
	i = 0 # counter for line in reader
	j = 0 # counter for entries captured within the date range

	for line in reader: #  control how many emails to read
		i += 1

		x = line[0][2:10] #  find the date from the string
		if x < date_beg:
			pass
		elif x > date_beg and x <= date_end:
			text += line[0][14:] #  line is a list, line[0][14:] is a string
			j += 1
		else:
			pass

	words = text.lower().split()
	for word in words:
		#  remove punctuation and whitespace
		word = word.strip(string.punctuation + string.whitespace)
		#  critical to use decode to get rid of escape chars in string here
		word = word.decode('string_escape')
		#  remove carriage return in string
		word = word.replace('\n','')

		for thing in things_to_strip:
			if thing in word:
				word = word.replace(thing, "")
			else:
				continue
		if word not in words_to_ignore and len(word) >= words_min_size:
			if word in wordcount:
				wordcount[word] += 1
			else:
				wordcount[word] = 1

	sortedword = sorted(wordcount, key=wordcount.get, reverse=True)

	print "\nFrom %s to %s, in total %s emails from Stanford GSB BLAST" % (
		date_beg, date_end, j),
	print "mailing listare analyzed, and the top %s most common" % top_size,
	print "words are the following:\n"

	k = 0
	for word in sortedword:
		k += 1
		if k <= top_size:
			print word, wordcount[word]

	print "\nEnd of the 'What's Hot in Stanford GSB' Analysis Report. Thank You!\n"


