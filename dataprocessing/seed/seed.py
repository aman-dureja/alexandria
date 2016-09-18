import sys
import urllib2
import json
import subprocess

# firebase = firebase.FirebaseApplication('https://alexandria-c0235.firebaseio.com/', None)

second_layer = sys.argv[1]
file_name = second_layer + '.txt'

file = open('../ingestion/raw/1/0/0/0/' + second_layer + '/' + file_name, 'r')

book_title = ""
author = ''
language = ''
difficulty = ''
start_line_num = 0
end_line_num = 0
raw_snippets = []

for num, line in enumerate(file, 1):

    words = line.split(" ")
    if words[0] == "Title:":
        words.remove("Title:")
        book_title = " ".join(words)
        book_title = book_title.replace('\n', '')
    elif words[0] == "Author:":
        words.remove("Author:")
        author = " ".join(words)
        author = author.replace('\n', '')
    elif words[0] == "Language:":
        words.remove("Language:")
        language = " ".join(words)
        language = language.replace('\n', '')
    elif words[0] == "***":
        start_line_num = num
        break

for num, line in enumerate(file, 1):

    # prevents putting the non-book text at end of each raw data file into snippet object in database
    if line.split(" ")[0] == "***":
        break

    elif len(line.split(" ")) > 1:
        raw_snippets.append(line.replace('\r\n', ''))

snippets = [raw_snippets[x:x+10] for x in xrange(0, len(raw_snippets), 10)]

snippets_length = len(snippets)

if snippets_length < 80:
    difficulty = 'easy'
elif snippets_length < 150:
    difficulty = 'medium'
else:
    difficulty = 'hard'

resolved_snippets = []


print book_title
# book_title += ".json"
# print str(book_title) + ".json"
book_title_1 = "%s.json" % (book_title)
# book_title += '.json'
# print book_title_1
book_file_firebase = book_title.replace(' ', '')

for num, snippet in enumerate(snippets, 1):
    resolved_snippet = "".join(snippet)
    print resolved_snippet
    resolved_snippets.append(resolved_snippet)
    print
    if num == 5:
        break
    # subprocess.call(['./seed.sh', book_title, snippet, num])
    # SET snippet
    # print resolved_snippet
    # print

# print book_file_firebase
# subprocess.call(['./seed.sh', book_title, book_file_firebase])
