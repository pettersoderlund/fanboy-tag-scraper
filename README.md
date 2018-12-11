# fanboy-tag-scraper

A scraper to collect posts from https://fbtag.net
I have tested to run this on cygwin on a windows machine and ubuntu. 

## Requirements 
- Python 3.7
- optional: MYSQL server (if you want a mysql pipeline)

## Python modules (from requirements.txt)
- bs4==0.0.1
- html2text==2018.1.9
- PyMySQL==0.9.2
- Scrapy==1.5.1
- scrapy-mysql-pipeline==2017.10.10

## Installation
- Clone this repository (git clone .... )
- Enter directory
- Install requirements (pip install -r requirements.txt)
- Copy settings file and edit to your settings (cp settings.example.py settings.py)

## Usage
scrapy crawl fbtag <-a tag_filter="3,8"> <-a discussion_list_deep=5> <-a discussion_deep=2>

Parameters explained: 
### tag_filter
Only collect posts from given tags ids. Commaseparated tagid 

tag id | tag name 
--- | --- 
2 | Lập trình
3 | Tin tức
4 | Chat
5 | Truyện
6 | Super
7 | Giải Trí
8 | Cafe
9 | Quân sự
10 | Xây dựng
11 | Nhiếp ảnh
12 | Tài chính
13 | Chứng khoán
14 | Sức khỏe


### discussion_list_deep
How many pages to parse through in the discussion list navigation. 

### discussion_deep
How many pages to parse through in every discussion. 

## Next steps
I would like to implement sorting on the discussion list. 
