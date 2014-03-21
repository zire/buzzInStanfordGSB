import mailbox
import csv
import time
from datetime import datetime
from operator import itemgetter
import collections

#  This is to make sure the body of the message can be accuratedly extracted
#  from get_payload command. Messages in this particular mbox (Stanford GSB's
#  BLAST email group are found to be always multipart and the first part of the
#  first part of the message.get_payload should be the body of email. 

with open('BLAST_raw.csv', 'w') as infile:
	w = csv.writer(infile) #  get a writer object

	k = 0
	for message in mailbox.mbox('BLAST_20140321.mbox'):
		k += 1

	#  extract email body with get_payload()
		if message.is_multipart():
			msg_body = {}
			i = 0
			for part in message.get_payload():
				i += 1
				if part.is_multipart():
					if i == 1:
						x = 0
						for p in part.get_payload():
							x += 1
							if x == 1:
								msg_body = p.get_payload()
								msg_type = p.get_content_type()
								msg_charset = p.get_content_charset()
							else:
								continue
					else:
						continue
				else:
					continue
		else:
			continue

	#  clean up the date field
		date_raw = message['date']
		position_colon = date_raw.index(":") #  the position of the first ':'
		date_clean = date_raw[5:position_colon-3]
		position_space = date_clean.index(" ")
		if position_space == 1: # means the day number is single digit
			date_clean = "0" + date_clean 
		else: # means the day number is double-digit
			pass
		date_format = datetime.strptime(date_clean,"%d %b %Y")
		date_final = date_format.strftime("%Y%m%d")
	#	print date_final

	#  write out to the output csv file	
		w.writerow([
			date_final,
			msg_body,
			"BLAST Msg %s is of type '%s' and charset '%s'" % (
				k,
				msg_type,
				msg_charset
				),
			"\n"
			])

	print "There are %s messages in 'BLAST_raw.csv'" % k
	print

#  sort data by date
with open('BLAST_raw.csv','r') as infile, open("BLAST_data.csv",'w') as outfile:
	data_input = csv.reader(infile, delimiter = ',')
	data_output = csv.writer(outfile)

	#  use itemgetter(0) to get key value date and sort it by date
	data = sorted(data_input, key=itemgetter(0), reverse=True)

	i = 0
	for row in data:
		i += 1
		data_output.writerow([row])
	print "There are %s messages in 'BLAST_data.csv'" % i
	print

	with open("BLAST_date.csv", 'wb') as f:
		data_date = csv.writer(f)
		k = 0
		for row in data:
			k += 1
			data_date.writerow([row[0]])
		print "There are %s dates in 'BLAST_date.csv'" % k
		print

#  create a visual table for dates to see if the data is reasonable
with open('BLAST_date.csv', 'r') as a, open("BLAST_datecheck.csv", 'w') as b:
	data_in = csv.reader(a)
	date_out = csv.writer(b)

	date_count = {} #  set up a dictionary

	for row in data_in:
		x = ''.join(row)
		if x in date_count:
			date_count[x] += 1
		else:
			date_count[x] = 1

	data = collections.OrderedDict(sorted(date_count.items(), reverse=True))

	for key, value in data.iteritems():
		date_out.writerow([key, value])









	





