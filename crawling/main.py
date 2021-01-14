import json
import re
from selenium import webdriver
driver = webdriver.Firefox()
driver.implicitly_wait(1)

def get_ID(url):
    return int(url.split("/")[-1])

def top_citations(size=10):
    IDs = []
    cites = driver.find_elements_by_css_selector("div.primary_paper > a.title.au-target")[:size]
    for ele in cites:
        try:
            href = ele.get_attribute("href")
            ID = href.split("/")[-2]
            if re.match(r'^\d+$', ID):
                IDs.append(ID)
        except:
            continue
    return IDs

def extract(selector, attr=None, plural=False):
    if attr is not None:
        res = driver.find_element_by_css_selector(selector).get_attribute(attr)
    elif not plural:
        res = driver.find_element_by_css_selector(selector).text
    else:
        res = [ele.text for ele in driver.find_elements_by_css_selector(selector)]
    return res


root_url = "http://academic.microsoft.com/paper/"
visited, papers = set(), []
size = int(input("article nums: "))

with open("../datasets/phase3/start.txt", "r") as f:
    urls = f.read().split("\n")

while len(visited) != size:
    url = urls[0]
    urls.pop(0)
    driver.get(url)
    ID = get_ID(url)
    try: #error in getting info
        title, abstract = extract("h1.name"), extract("div.name-section > p")
        year, authors = extract("span.year"), extract("a.author", plural=True)
        cites = top_citations()
    except:
        urls = [url] + urls
        continue

    if title not in visited:
        visited.add(title)
        paper = {"id": ID,
                 "title": title,
                 "abstract": abstract,
                 "date": year,
                 "authors": authors,
                 "references": cites}
        print("i, info: {}, {}".format(len(visited), paper))
        papers.append(paper)
        with open("articles.json", "w") as f:
            json.dump(papers, f)
        urls.extend([root_url + str(ID) for ID in cites])

