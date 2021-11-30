from .models import Notice
import requests
import re
import bs4
import hashlib
import urllib
from urllib.parse import urlparse

SOURCE_URL = 'http://dsc.du.ac.in/'
NOTICES_URL = SOURCE_URL


def update_db():
	""""Update databse with new Notices from the College website
	and return the key of the updated notices"""

	all_notices = Notice.objects.all()
	used_keys = [notice.key for notice in all_notices]

	print("Fetching New Notices")
	new_notices = getNewNotices(used_keys)
	new_notices = new_notices[-10:]

	if len(new_notices) != 0:
		# Get notice content
		for notice in reversed(new_notices):
			header = f"<strong>{notice['title']}</strong>"
			footer = f"\n\n<i>Source:</i> <a href='{notice['link']}'>{notice['link']}</a>"
			notice_content = header + notice['content'] + footer
			b = Notice( title=notice['title'],key=notice['key'],content=notice_content, url=notice['link'] )
			b.save()
		print(str(len(new_notices))+ " Notices Added")
		return [ notice['key'] for notice in reversed(new_notices) ]
	else:
		print("No New Notices")
		return []


def getNewNotices(used_keys):
	request = requests.get(NOTICES_URL)
	soup = bs4.BeautifulSoup(request.text, 'html.parser')
	data = soup.find_all(id='recent-posts-2')
	notices = []
	for d in data:
		for notice in d.find_all('a'):
			notices.append(notice)
	new_notices = []
	for notice in notices:
		text = notice.text.strip()
		p_url = urlparse(notice.attrs['href'])
		p_url = p_url._replace(path=urllib.parse.quote(p_url.path))
		url =  p_url.geturl()
		if url[:4] != 'http':
			url =  SOURCE_URL + url[1:]
		content = f'\n\n<a href="{url}">{url}</a>'
		key = hashlib.md5((text+url).encode('utf-8')).hexdigest()
		if key not in used_keys:
			request = requests.get(url)
			contentValid = request.status_code >= 200 and request.status_code < 400
			if not contentValid:
				continue
			new_notices.append({'title': text, 'content':content, 'link': NOTICES_URL, 'key': key})
	return new_notices
