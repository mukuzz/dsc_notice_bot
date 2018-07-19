from .models import Notice
import requests
import re
from bs4 import BeautifulSoup

SOURCE_URL = 'http://dsc.du.ac.in/'
NOTICES_URL = SOURCE_URL+'AllNewsDetails.aspx'

def update_db():
	all_notices = get_notices()

	if len(all_notices) is not 0:
		Notice.objects.all().delete()
		
		bulk_objects = [
			Notice( title=notice['title'],key=notice['key'],content=notice['link'] )
			for notice in all_notices
		]

		Notice.objects.bulk_create(bulk_objects)


def get_notices():
	request = requests.get(NOTICES_URL)
	soup = BeautifulSoup(request.text, 'html.parser')
	td = soup.find('td', valign='top')
	tables = td.find_all('table')
	data = []
	unique_list = []
	for ind_notice in tables:
		little_cleaner = ind_notice.find('span', class_='a2')
		more_clean = little_cleaner.ul.li.h4
		notice_title = more_clean.get_text()
		title = notice_title.strip()
		title = title.split('\r\n')[0]
		link = SOURCE_URL+more_clean.span.a.attrs['href']
		key = re.findall(r'\d+',link)	# Extract the number from link
		if key not in unique_list:	# To make sure all notices are unique
			data.append({'title':title,'link':link,'key':int(key[0])})
			unique_list.append(key)
	return data

