import requests
import json
import csv
import os
from bs4 import BeautifulSoup

###############################################
# ptt gossiping 板的當頁面的所有貼文，抓取相關資料#
###############################################
ptt_url_01 = 'https://www.ptt.cc/bbs/Gossiping/index.html'
ptt_html_01 = requests.get(ptt_url_01, cookies={'over18':'1'})
ptt_Soup_01 = BeautifulSoup(ptt_html_01.text, 'html5lib')

articles = []           # 本頁面文章
pttdivs = ptt_Soup_01.find_all('div', 'r-ent')
for p in pttdivs:
    if p.find('a'):
       articles.append({'title':p.find('a').text,                          # 文章標題
                        'author':p.find('div', 'author').text,             # 文章作者
                        'href':p.find('a')['href'],                        # 文章連結
                        'ptime':p.find('div', 'date').text,                # 貼文時間
                        'push_num':p.find('div', 'nrec').text,             # 推文數量
                        })

# 寫入 JSON 檔案
with open('scrpttgosdatpic.json', 'w', encoding='utf-8') as fnObj:
    json.dump(articles, fnObj, ensure_ascii= False, indent=2)

# 寫入 CSV 檔案
with open('scrpttgosdatpic.csv', 'w', newline='', encoding='utf-8-sig') as csvFile:

        fields = ['title', 'author', 'href', 'ptime', 'push_num']                           # 定義欄位
        dictWriter = csv.DictWriter(csvFile, fieldnames=fields)                             # 將 dictionary 寫入 CSV 檔案
        dictWriter.writeheader()                                                            # 寫入標題
        for inputArticle in articles:                                                       # 寫入資料
            dictWriter.writerow(inputArticle)

##########################################################################
# 進入 ptt gossiping 板的當頁面的第一則貼文，抓取相關資料，以及把圖片下載並儲存 #
##########################################################################

ptt_url_02 = 'https://www.ptt.cc'
gossiping = '/bbs/Gossiping/index.html'

ptt_html_02 = requests.get(ptt_url_02+gossiping, cookies={'over18':'1'})
ptt_Soup_02 = BeautifulSoup(ptt_html_02.text, 'html5lib')

ptt_divs = ptt_Soup_02.find_all('div', 'r-ent')
href = ptt_divs[0].find('a')['href']                                                # 文章超連結
gossiping_html = requests.get(ptt_url_02+href, cookies={'over18':'1'})              # 進入超連結

gossiping_soup = BeautifulSoup(gossiping_html.text, 'html5lib')
gossiping_divs = gossiping_soup.find('div', id='main-content')
metas = gossiping_divs.find_all("span", class_="article-meta-value")

print("看板", metas[0].text)
print("作者", metas[1].text)
print("標題", metas[2].text)
print("時間", metas[3].text)

ms = gossiping_divs.find_all("div", ['article-metaline', 'article-metaline-right', 'push'])   # 扣掉 看板作者、標題、時間、推文

for m in ms:
    m.extract()

gossiping_divs = gossiping_soup.find('div', id='main-content')
print(gossiping_divs.text)

photos = []                                                     # 圖片網址
url_photos = gossiping_divs.find_all('a')                                                    # 找尋所有圖片
for photo in url_photos:
    href_photo = photo['href']
    if href_photo.startswith('https://i.imgur'):                                             # 判斷圖片網址
        photos.append(href_photo)

for photo in photos:                                                                         # 列印圖片網址
    print(photo)

destDir = 'scrpttgosdatpicture'
if os.path.exists(destDir) == False:                                                        # 如果沒有此資料夾就建立
    os.mkdir(destDir)
print("搜尋到圖片數量 = ", len(photos))                                                       # 列出搜尋到的圖片數量
for photo in photos:                                                                        # 迴圈下載圖片與儲存
    picture = requests.get(photo)                                                           # 下載圖片
    print("%s 圖片下載成功" % photo)

    pictFile = open(os.path.join(destDir, os.path.basename(photo)), 'wb')                   # 先開啟檔案, 再儲存圖片
    for diskStorage in picture.iter_content(10240):
        pictFile.write(diskStorage)
    pictFile.close()                                                                        # 關閉檔案
