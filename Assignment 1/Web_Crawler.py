from bs4 import BeautifulSoup
import requests
import re
import random

url_global = "http://www.learnyouahaskell.com/"
visited_pages = []

s = url_global.split('.')
main_word = s[1]


def save_page(lol):
	check = requests.head(lol)
	print (lol)

	if check.status_code < 400:
			count = random.randint(0,100000)
			filename = 'data' + str(count) + '.txt'
			
			print (lol)

			file = requests.get(lol).text

			soup = BeautifulSoup(file, 'lxml')

			with open (filename, 'a') as f:
				f.write(str(soup))

def print_page(lol):
	check1 = requests.head(lol)
	if check1.status_code < 400 and '.php' not in lol:
		print (lol)

def check_link(lol):
	check = requests.head(lol)

	if check.status_code > 400:
		return False
	if 'java' in lol:
		return False
	elif 'mailto' in lol:
		return False
	elif 'pdf' in lol:
		return False
	elif 'csv' in lol:
		return False		
	elif '#' in lol:
	 	return False
	else:
		return True


def crawler(url):
	try:
		file = requests.get(url).text

		soup = BeautifulSoup(file, 'lxml')

		for link in soup.find_all('a'):
			link_new = link.get('href')

			if not link_new:
				continue

			if 'http' not in link_new: #case 1
				if link_new[0] == '/':
					link_new = link_new[1:]
				full_link = url_global + link_new
			else:
				if main_word in link_new: #case 2 & 4 #can use main_word here
					full_link = link_new
				else: #case 3
					continue

			if full_link not in visited_pages: 
				if check_link(full_link) == True:
					visited_pages.append(full_link)
					print_page(full_link)
					crawler(full_link)

	except Exception as e:
		return

print (url_global)
crawler(url_global)


'''
Cases:
1) extension of original link 
	i) '/' at start
	ii) '/' not at start
--> does not contain http (if 'http' not in url)

2) whole link from start
--> contains starting url (eg: apple.com)
--> contains http ((if 'http' in url))

3) other random sites
--> does not contain starting url (if starting_url not in url)
--> contains http ((if 'http' in url))



4) subdomain (eg: help.apple.com)
--> contains apple.com
--> contains http ((if 'http' in url))


'''













