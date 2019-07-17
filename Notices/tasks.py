from .models import Notice
import requests
import re
import bs4
from celery import Celery

SOURCE_URL = 'http://dsc.du.ac.in/'
NOTICES_URL = SOURCE_URL + 'AllNewsDetails.aspx'

app = Celery()

@app.task
def update_db():
	""""Update databse with new Notices from the College website
	and return the key of the updated notices"""
	latest_key = 0
	all_objects = Notice.objects.order_by('-key')
	if len(all_objects) is not 0:
		latest_object = all_objects[0]
		latest_key = latest_object.key
	
	# print("Fetching New Notices")
	new_notices = getNewNotices(latest_key)

	if len(new_notices) is not 0:
		# Get notice content
		for notice in new_notices:
			try:
				notice_content = getNoticeContent(notice)
			except Exception:
				notice_content = ""
				raise
			header = f"<strong>{notice['title']}</strong>"
			footer = f"\n\n<i>Source:</i> <a href='{notice['link']}'>{notice['link']}</a>"
			notice_content = header + notice_content + footer
			b = Notice( title=notice['title'],key=notice['key'],content=notice_content, url=notice['link'] )
			b.save()
			# print("Notice " + str(notice['key'])+ " added")
		# print(str(len(new_notices))+ " Notices Added")
		return [ notice['key'] for notice in new_notices ]
	else:
		# print("No New Notices")
		return []


def getNewNotices(latest_key):
	request = requests.get(NOTICES_URL)
	soup = bs4.BeautifulSoup(request.text, 'html.parser')
	td = soup.find('td', valign='top')
	tables = td.find_all('table')
	new_notices = []
	unique_list = []
	for ind_notice in tables:
		little_cleaner = ind_notice.find('span', class_='a2')
		more_clean = little_cleaner.ul.li.h4
		notice_title = more_clean.get_text()
		title = notice_title.strip()
		title = title.split('\r\n')[0]
		link = SOURCE_URL+more_clean.span.a.attrs['href']
		key = re.findall(r'\d+',link)	# Extract the digits from link
		key = int(key[0])
		# Make sure all notices are unique and new
		if key not in unique_list and key > latest_key:
			new_notices.append({'title': title,'link': link,'key': key})
			unique_list.append(key)
	return new_notices


def getNoticeContent(notice):
	request = requests.get(notice['link'])
	soup = bs4.BeautifulSoup(request.text, 'html.parser')
	return cleanContent(soup)


def cleanContent(soup):
	td = soup.find('td', valign='top')
	tables = td.find_all('table')
	content_table = tables[-1]
	content_span = content_table.tr.td.contents[3].span
	content = ""
	for line in content_span.children:
		if type(line) is not bs4.element.NavigableString:
			data_found = False
			for tag in line.descendants:
				if tag.name == 'a' and tag.getText() is not None:
					link = tag['href']
					if link.find('http') == -1:
						if link[0] == '/':
							link = link[1:]
						link = SOURCE_URL + link
					content += '\n\n<a href="' + link  + '">' + tag.getText().strip() + '</a>'
					data_found = True
					break
			if data_found:
				continue
			if line.getText() is not None and line.getText().strip() != "":
				content += "\n\n" + line.getText().strip()
	return content
