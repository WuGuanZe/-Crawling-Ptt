import requests
from bs4 import BeautifulSoup

ptt_url = "https://www.ptt.cc/bbs/Gossiping/M.1580810317.A.16C.html"
response = requests.get(ptt_url, cookies={'over18':'1'})
gossiping = BeautifulSoup(response.text, 'html5lib')

gossiping_divs = gossiping.find('div', id='main-content')
metas = gossiping_divs.find_all("span", class_="article-meta-value")

print("看板", metas[0].text)
print("作者", metas[1].text)
print("標題", metas[2].text)
print("時間", metas[3].text)


ms = gossiping_divs.find_all("div", ['article-metaline', 'article-metaline-right', 'push'])   # 扣掉 看板作者、標題、時間、推文

for m in ms:
    m.extract()

gossiping_divs = gossiping.find('div', id='main-content')
print(gossiping_divs.text)
