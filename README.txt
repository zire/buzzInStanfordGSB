This program aims to analyze the most common buzz words from Stanford Graduate School of Business (GSB)'s BLAST mailing list, which is subscribed by all GSB students (MBA, MSx and PhD) and used heavily by the student community to broadcast news, seeking help, etc. The idea is similar to Google Keyword Trend, except that it's applied to a very specific environment and audience.

The program is written in Python 2.7.5

Steps:

1) Download all the BLAST emails

Fortunately Google provides a very handy Datatool to download emails with specific labels. It's available from the Account Settings page. This archive has emails from 2012 (I recovered them from Trash), 2013, and 2014. Emails in 2012 and 2013 were not preserved universally and consistently so they will not be part of this analysis. Emails in 2014 are of better quality though I'm sure I've missed/deleted some BLAST messages already. Going forward I will keep all the BLAST emails and the data quality will be considerably better in more recent update

2) Extract emails and dates from the email archive

Google archives Gmail messages in mbox format - one single large file. Python's mailbox.mbox library provides an effective way to extract contents from it. 

>> Python 1_mbox2csv.py

There are three steps that need to be performed here:

a) figure out where is the email body with get_payload()

It turns out that all the BLAST emails are of multipart (so get_payload() will return a list, not a string). The email body is hidden in the first part of the first part in a message from mbox (quite nested).

b) clean up the date field

The raw date field needs clean-up. It's not in the standard ISO format and the day field is not zero-paddled. Datetime.strptime is used to deal with it. Eventually a raw date like "5 Nov 2013" is converted into "20131105" (YYYYMMDD) for easy sorting in the next step.

c) sort data by date

Self-explanatory. After this program is run, a cleaned up email archive will be created in csv format with only date and email body information, and is sorted by date.

3) Run the word frequency analysis

>> Python 2_wordcount.py

After all the maneuvers to get the data into the right format, the real crunching on word frequency is quite easy relatively speaking. The true magic that embodies both science and art is the exception list of words to ignore (words_to_ignore). A lot of time was spent to grow this list so that all the un-informational words are filtered out such as "when", "where", "to".. etc. There are A LOT of those.

It's only after filtering out those exception words, the real buzzwords for Stanford GSB will float to the surface, as you can see now.

Top-10 Most Common Words from Stanford GSB BLAST mailing list:

2014 January (82 emails)

(word, frequency)
design 20
team 19
product 12
job 10
startx 9
marketing 9
car 9
application 9
farber 8
dschool 8

2014 February (29 emails)

store 12
education 12
mountain 10
employee 10
hardwear 10
management 8
future 7
united 7
7=20
free 6

2014 March (77 emails)

google 18
team 15
management 15
energy 14
survey 12
reputation 11
partners 11
marketing 10
innovation 10
endurance 10

Do they reveal something useful? Maybe, but I'm not sure. Maybe I just need to continue to tinker with the exception word list to make more sense out of it.
