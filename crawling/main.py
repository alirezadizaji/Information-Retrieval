import json
import re
from selenium import webdriver
driver = webdriver.Firefox()
driver.implicitly_wait(2)


def get_ID(url):
    return re.findall(r'\d+', url)[0]


def top_citations(size=10):
    """
    NOTE: dead-end handled automatically by FIFO list('urls')
    """
    IDs = []
    cites = driver.find_elements_by_css_selector("div.results a.title.au-target")[:size]
    for ele in cites:
        try:
            href = ele.get_attribute("href")
            if re.search(r'\d+', href):
                ID = re.findall(r'\d+', href)[0]
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
    try:
        driver.get(url)
        ID = get_ID(url)
        title, abstract = extract("h1.name"), extract("div.name-section > p")
        year, authors = extract("span.year"), extract("a.author", plural=True)
        cites = top_citations()
    except: #error in getting info
        print("connect again...")
        urls = [url] + urls
        continue

    tl = title.lower()
    if tl in visited:
        print("duplicate title: {}".format(tl))
    else:
        visited.add(tl)
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

