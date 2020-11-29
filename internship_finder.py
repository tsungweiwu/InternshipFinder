from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.11 (KHTML, like Gecko) '
                      'Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
         
# gets the amount of pages in order to iterate through
url = 'https://www.glassdoor.com/Job/software-engineer-intern-jobs-SRCH_KO0,24.htm?jobType=internship&fromAge=14&radius=0&minRating=4.0'
req = Request(url, headers=headers)
page_html = urlopen(req).read()
page_soup = soup(page_html, "html.parser")
postings = page_soup.findAll("div", {"cell middle hideMob padVertSm"})
page_number_str = postings[0].text.split()
page_numbers = int(page_number_str[3]) + 1

filename = "internships.csv"
f = open(filename, "w")

hdr = "company, position, location, link\n"

f.write(hdr)

for page in range(1, page_numbers):
	my_url = 'https://www.glassdoor.com/Job/software-engineer-intern-jobs-SRCH_KO0,24_IP' + str(page) +'.htm?jobType=internship&fromAge=14&radius=0&minRating=4.0'

	# opening up connectionsm getting the request and reading it
	req = Request(my_url, headers=headers)
	page_html = urlopen(req).read()

	# html parser
	page_soup = soup(page_html, "html.parser")

	# grab each job posting
	postings = page_soup.findAll("div", {"class":"d-flex flex-column pl-sm css-nq3w9f"})

	for post in postings:
		company_name = post.span.text

		title_container = post.findAll("a", {"class":"jobInfoItem jobTitle css-13w0lq6 eigr9kq1 jobLink"})
		position_title = title_container[0].span.text
		
		location = post.findAll("div", {"class":"d-flex flex-wrap css-yytu5e e1rrn5ka1"})[0].span.text

		link = "https://www.glassdoor.com" + post.a["href"]

		# some filters for my standards
		if not "PhD" in position_title:
			f.write(company_name.replace(",", "|") + "," + position_title.replace(",", "|") + "," + location.replace(",", "|") + "," + link + "\n")
		

f.close()