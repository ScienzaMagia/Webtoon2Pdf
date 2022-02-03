# python chscrape.py "url]" Rips

import requests
#from requests.auth import HTTPBasicAuth 
import re
import sys
import os
from bs4 import BeautifulSoup




class webtoonRip:
    
    

    def main(self):
        url = sys.argv[1]
        #saveLoc = sys.argv[2]
        response = requests.get(url, headers={'referer': 'webtoons.com'})
        rawHtml = BeautifulSoup(response.content, 'html.parser')
        #print(rawHtml.prettify())
        title = rawHtml.title.contents[0]
        print(title)
        title = re.sub(r'[^a-zA-Z0-9_ ]','', title)
        if not os.path.exists(title):
            os.mkdir(title)
        
        
        print(title)
        imagelist = rawHtml.find("div", id = "_imageList").find_all("img")
        count = 1
        for img in imagelist:
            
            self.imageGrab(title, str(img['data-url']), count)
            count = count+1
        #print (imagelist)
        
        doc = open("imagelist.txt","w")
        #doc.writelines(str(imagelist))
        #doc.close()

    def imageGrab(self, directory,  url, pageNumber):
        with open(directory + "/" + str(pageNumber) + '.jpg', 'wb') as f:
            f.write(requests.get(url, headers={'referer': 'webtoons.com'}).content)




if __name__ == '__main__':
    webtoonRip().main()
    
    