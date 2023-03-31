#Example: python main.py https://www.rowecasaorganics.com/

import requests # request img from web
import shutil # save img locally
import sys
import json
import os

if len(sys.argv) < 1:
    raise ValueError("Not enough commandline arguments! Please run with <executable> <server> <database> <username> <password> <folder_path>")

if os.path.exists('images') == False:
    os.mkdir('images')
raw_url = sys.argv[1]+'products.json?limit=250'
continueRequesting = True
pageCounter = 1
url = raw_url+'&page='+str(pageCounter)
while continueRequesting:
    pageCounter+=1
    res = requests.get(url, '')
    if res.status_code == 200:
        products = json.loads(res.content)['products']
        if len(products) > 0:
            for product in products:
                resImg = requests.get(product['images'][0]['src'], stream = True )
                if resImg.status_code == 200:
                    with open('./images/'+product['title'].replace("|", "").replace(' ','-')+'.png','wb') as f:
                        shutil.copyfileobj(resImg.raw, f)
                    print(product['title'].replace("|", "").replace(' ','-')+'.png')
                else:
                    print('Image Error')
            url=raw_url+'&page='+str(pageCounter)
        else:
            continueRequesting = False
    else:
        print(res.error)

print("Page Counter "+str(pageCounter))