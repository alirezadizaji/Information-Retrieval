import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Firefox()
driver.implicitly_wait(5)


def get_ID(url):
    return re.findall(r'\d+', url)[0]

def get_refs(size=10):
    IDs = {} #prevent duplicate refs
    ref_scr = scr["ref"]
    refs = driver.find_elements_by_css_selector(ref_scr)
    for ele in refs:
        try:
            href = ele.get_attribute("href")
            title = ele.text.lower()
            if re.search(r'\d+', href):
                ID = re.findall(r'\d+', href)[0]
                IDs[title] = ID
        except:
            continue
    IDs = list(IDs.values())[:size]
    return IDs

def wait_for(selector, max_time=2): #explicit wait
    WebDriverWait(driver, max_time).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )

def to_json(f, data):
    with open(f, 'w') as fp:
        fp.write(
            '[' +
            ',\n'.join(json.dumps(i) for i in data) +
            ']')

def extract(selector, attr=None, plural=False):
    if attr is not None:
        res = driver.find_element_by_css_selector(selector).get_attribute(attr)
    elif not plural:
        res = driver.find_element_by_css_selector(selector).text
    else:
        res = [ele.text for ele in driver.find_elements_by_css_selector(selector)]
    return res

root_url = "http://academic.microsoft.com/paper/"
scr = {"title": "h1.name",
       "date": "div.name-section span.year",
       "author": "div.name-section  a.author",
       "abstract": "div.name-section > p",
       "ref": "div.results a.title.au-target"}

size = int(input("article nums: "))
"""
NOTE: dead-end issue handled automatically by FIFO list('urls')
"""
with open("../datasets/phase3/start.txt", "r") as f:
    urls = f.read().split("\n")
visited, papers = set(), []

while len(visited) != size:
    url = urls[0]
    urls.pop(0)
    try:
        driver.get(url)
        wait_for(scr["ref"])
        ID = get_ID(url)
        title, abstract = extract(scr["title"]), extract(scr["abstract"])
        year, authors = extract(scr["date"]), extract(scr["author"], plural=True)
        refs = get_refs()
    except: #page not loaded correctly
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
                 "references": refs}
        print("i, info: {}, {}".format(len(visited), paper))
        papers.append(paper)
        to_json("articles.json", papers)
        urls.extend([root_url + str(ID) for ID in refs])
