import requests
import re
import sys
import os
from PIL import Image
from bs4 import BeautifulSoup
import img2pdf



class webtoonRip:

    def main(self):
        url = sys.argv[1]
        response = requests.get(url, headers={'referer': 'webtoons.com'})
        rawHtml = BeautifulSoup(response.content, 'html.parser')

        title = rawHtml.title.contents[0]
        #print(title)
        title = re.sub(r'[^a-zA-Z0-9_ ]','', title)
        if not os.path.exists(title):
            os.mkdir(title)
        
        print(title)
        imagelist = rawHtml.find("div", id = "_imageList").find_all("img")
        
        mergedImage = Image.new('RGB', (0,0), color=0)
        i = 0
        while i < len(imagelist):
            #print(i)
            #print (imagelist[i]['data-url'])
            self.imageGrab(title, imagelist[i]['data-url'], i)
            image2Merge = Image.open(title + "/" + str(i+1) + ".jpg")
            mergedImage = self.imageStitch(mergedImage, image2Merge)
            image2Merge.close()
            i = i+1

        mergedImage.save("merged.jpg", quality=100)

    # Gets image at "url" and saves it as a .jpg to "directory"
    def imageGrab(self, directory,  url, pageNumber):
        with open(directory + "/" + str(pageNumber+1) + '.jpg', 'wb') as f:
            f.write(requests.get(url, headers={'referer': 'webtoons.com'}).content)
        f.close()


    def imageStitch(self, mergeInto, image2Merge):
        #meme
        (width1, height1) = mergeInto.size
        (width2, height2) = image2Merge.size
        mergedWidth = max(width1, width2)
        mergedHeight = height1 + height2
        
        #print (str(width1) + ", " + str(height1) + " : " +str(width2) + ", " + str(height2))
        #print (str(mergedWidth) + ", " + str(mergedHeight))

        mergedImage = Image.new('RGB', (mergedWidth, mergedHeight), color=0)
        mergedImage.paste(im=mergeInto, box=(0, 0))
        mergedImage.paste(im=image2Merge, box=(0, height1))        
        return mergedImage
        
    


if __name__ == '__main__':
    webtoonRip().main()
    
    