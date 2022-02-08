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
        
        with open('url.txt', 'w') as f:
            f.write(requests.get(url, headers={'referer': 'webtoons.com'}).text)
        
        #determines if url is a table of contents, a specific issue, or neither
        
        if url.find("page=") != -1:
            #print ("Title Page")
            issues = self.findIssues(url,[])
            i = len(issues) -1
            while i >= 0:
                self.issueGrab(issues[i])
                i = i-1
            
        elif url.find("episode_no=") != -1:
            #print ("Episode")
            self.issueGrab(url)
        else:
            print ("Invalid link")
        
        
        
        #self.findIssues(url,[])
        #self.issueGrab(url)
       
        
        
    #Crawls through the episode lists to grab a complete list of issues.
    def findIssues(self, url, issues):
        #finds page number from url
        pageIndex = int(url.find("page="))
        pageNumber = int(url[pageIndex+5:len(url)])
        strippedUrl = url[0:pageIndex+5]
        
        #pulls and parses page contents
        page = requests.get(url, headers={'referer': 'webtoons.com'})
        pageHtml = BeautifulSoup(page.content, 'html.parser')
        
        #finds list of episodes on page
        i = 0
        issuesOnPage = pageHtml.find('ul', id = '_listUl')
        for child in issuesOnPage.children:  
            if (str(child)) != "\n":
                issues.append(str(child.a['href']))
                if child['data-episode-no'] == "1":
                    return issues
                i = i+1
                

        issues = self.findIssues(strippedUrl + str(pageNumber + 1), issues)
        return issues
        
        
    def issueGrab(self, url):
        response = requests.get(url, headers={'referer': 'webtoons.com'})
        rawHtml = BeautifulSoup(response.content, 'html.parser')
        infobox = rawHtml.find("div", class_ = "subj_info")
        series = infobox.a['title']
        title = infobox.h1['title']
        series = re.sub(r'[^a-zA-Z0-9_ .-]','', series)
        title = re.sub(r'[^a-zA-Z0-9_ .-]','', title)
        print(series + ": " + title)
        directory = "rip/" + series + "/" + title + "/"
        if not os.path.exists(directory + "raw/"):
            os.makedirs(directory + "raw/")

			
        
        imagelist = rawHtml.find("div", id = "_imageList").find_all("img")
        
        mergedImage = Image.new('RGB', (0,0), color=0)
        i = 0
        while i < len(imagelist):
            #print(i)
            #print (imagelist[i]['data-url'])
            self.imageGrab(directory, imagelist[i]['data-url'], i)
            image2Merge = Image.open(directory + "/raw/" + str(i+1).zfill(4) + ".jpg")
            mergedImage = self.imageStitch(mergedImage, image2Merge)
            image2Merge.close()
            print(title + " Image: "  + str(i+1) + "/" +  str(len(imagelist)), end = "\r")
            i = i+1
        
        mergedImage.save(directory + title +".jpg", quality=100)
        
        with open(directory + title + ".pdf","wb") as f:
            f.write(img2pdf.convert(directory + title + ".jpg"))
      
      
        print("\nComplete")

    # Gets image at "url" and saves it as a .jpg to "directory"
    def imageGrab(self, directory,  url, pageNumber):
        with open(directory + "raw/" + str(pageNumber+1).zfill(4) + '.jpg', 'wb') as f:
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
    
    