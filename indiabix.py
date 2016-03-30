import requests
import pdfkit
import os
from bs4 import BeautifulSoup
base_url="http://www.indiabix.com"

def get_source(url):
	response=requests.get(url)
	parse=response.text
	source=BeautifulSoup(parse,"html.parser")
	return source

def find_pagination(topic):
	source=get_source(topic)
	paginate_links=[]
	links=source.find("p", class_="ib-pager").find_all("a")
	links.pop()
	for link in links:
		paginate_links.append(link)
	return paginate_links

def question(page_source):
    questions = page_source.find_all("div", class_="bix-div-container")
    q=""
    for ques in questions:
        q=q+"<br>"+ ques.find("table").find("tr").find("p").get_text()+"<br>"
        answers=ques.find_all("td", class_="bix-td-option")
        ans = []
        for answer in answers:
            ans.append(answer.get_text())
        string=' '.join(ans)
        q=q+"<br>"+string+"<br>"
    return q


def convert():
	source=get_source(base_url+"/aptitude/questions-and-answers/")
	links=source.find("table", id="ib-tbl-topics").find_all("a")
	i=1;
	for link in links:
		topic=base_url+link["href"]
		topic_name=link["href"].split('/')
		paginate=find_pagination(topic)
		source=get_source(topic)
		q=question(source)
		
		for page in paginate:
			soup=get_source(base_url+page["href"])
			tmp=question(soup)
			q=q+"<br>"+tmp+"<br>"
		if not os.path.exists('Indiabix/'+topic_name[2]):
			os.makedirs('Indiabix/'+topic_name[2])
		pdfkit.from_string(q,'Indiabix/'+topic_name[2]+'/'+topic_name[2]+'.pdf')
		i=i+1	
		print("Saved Topic:"+topic_name[2]+"\n")
		
convert()