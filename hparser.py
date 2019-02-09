import requests
from bs4 import BeautifulSoup



req = requests.get('https://beomi.github.io/beomi.github.io_old/')
# req = requests.get('https://www.python.org')

# print(req.url)
# print(req.text)
print(req)
html = req.text
status = req.status_code
is_ok = req.ok
encoding = req.encoding
header = req.headers
# print(html)
# print(status)
# print(is_ok)
# print(encoding)
# print(header)


bs = BeautifulSoup(html, 'html.parser')
my_titles = bs.select('h3 > a')

for title in my_titles :
	print(title.text)
	print(title.get('href'))

for title in my_titles:
	data[title.text] = title.get('href')
	with open(os.path.join(BASE_DIR, 'result.json'), 'w+') as json_file:
		json.dump(data, json_file)

