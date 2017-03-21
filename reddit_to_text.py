from html.parser import HTMLParser
from html.entities import name2codepoint
import urllib.request
import uuid

class MyHTMLParser(HTMLParser):

	def __init__(self):
		super().__init__()
		self.isData = False
		self.lastPost = ''
		self.listData = list()

	def handle_starttag(self, tag, attrs):
		if tag == "a":
			for attr in attrs:
				if attr[0] == 'data-inbound-url':
					attr_split = attr[1].split('/')
					self.lastPost = attr_split[4]

				if attr[0] == 'class':
					if attr[1] == 'title may-blank ':
						# print(attr)
						# print('\n----------------------------------------\n')
						self.isData = True

	def handle_data(self, data):
		if self.isData == True:
			print("- ", data)
			self.listData.append(data)
			self.isData = False

	def save_data(self, file_name):
		textFile = open(file_name, 'a', encoding="utf-8")
		for data in self.listData:
			textFile.write('- ' +data +'\n')

		textFile.close()



#--------------------------------
# CONFIG
#--------------------------------

# how many page you want to read? (25 comments/ page)
MAX_PAGE = 3
LINK_TOPIC = 'https://www.reddit.com/r/Showerthoughts/top/'
FILE_NAME = 'reddit_' + str(uuid.uuid4().hex) + '.txt'
#---------------------------------


parser = MyHTMLParser()
current_page = 0
last_post = ''


while current_page <= MAX_PAGE:
	comment_index = current_page * 25
	link = LINK_TOPIC + '?count=' + str(comment_index) + '&after=' + last_post
	#print('===== link: ' + link)
	req = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
	response = urllib.request.urlopen(req)
	parser.feed(response.read().decode("utf-8"))
	parser.save_data(FILE_NAME)
	last_post = 't3_' + parser.lastPost
	current_page += 1
