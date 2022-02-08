# Webtoon2Pdf

## What is it?

This is a simple script that pulls a comic from Webtoons.com and downloads a local copy. This copy is then stitched into one long .jpg and converted to a PDF file for easy reading.


## Installation

After downloading, navigate over to the folder. 

Type:

> pip install -r requirements.txt

Hit enter.



## Use

Run

> python3 webtoonRip.py \[url\]

If the link directs to a specific issue of the comic, only that issue will be grabbed. If the link directs to one of the main pages of the series, all issues will be downloaded from that page onward.