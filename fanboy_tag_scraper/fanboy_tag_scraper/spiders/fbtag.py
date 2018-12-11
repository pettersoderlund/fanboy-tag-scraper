# -*- coding: utf-8 -*-
import scrapy
import json
from datetime import datetime
import logging
import scrapy_mysql_pipeline
import html2text
import bs4
import argparse

class FbtagSpider(scrapy.Spider):
    name = "fbtag"
    allowed_domains = ['fbtag.net']
    start_urls = [
        'https://fbtag.net'
    ]

    def getFbtagJsonInfo(self, response):
        """
        there is a json string with all the info about all data present on page
        """
        s = response.xpath("//script")[-1].extract()
        s = s.split(');\n                } catch (e) {\n')[0]
        s = s.split('app.boot(')[1]
        j = json.loads(s)
        return j

    def getDiscussionLinks(self, json_info, tag_filter=[]):
        """
        Get links to discussions from thread list json info. 
        Optional parameter tags, an array of tag ids. Use this 
        to filter out only certain tagged discussions
        3 tin tuc (news)
        4 chat
        .
        .
        .
        8 cafe
        """
        discussion_links = []
        for t in json_info['document']['data']:
            if(t['type'] == 'discussions'):
                id = (t['id'])
                slug = t['attributes']['slug']
                tags = []
                for tag in t['relationships']['tags']['data']:
                    tags.append(int(tag['id']))
                    
                if(len(tag_filter) == 0 or len(list(set(tag_filter) & set(tags))) > 0):
                    discussion_links.append("https://fbtag.net/d/{id}-{slug}".format(id=id, slug=slug))
                else:
                    logging.debug(msg=(tags, 'not in filter ', tag_filter, 'link', id, slug))
                    pass
        
        return discussion_links
    
    def parse(self, response):
        # Possible sorts additional to default: 
        # top
        # newest
        # oldest

        j_data = self.getFbtagJsonInfo(response)


        # filter from options
        tag_filter = getattr(self,'tag_filter','3,8')
        #parse filter string
        tag_filter_list = tag_filter.split(',')
        #convert to int
        tag_filter_list_int = list(map(int, tag_filter_list))
        discussion_links = self.getDiscussionLinks(j_data, tag_filter=tag_filter_list_int)

        for url in discussion_links: 
            yield scrapy.Request(url, callback=self.parseDiscussion)
            
        # pagination
        # parse the pages
        discussions_next_url = response.xpath("//div[@class='container']/a[contains(text(), 'Next Page')]/@href").extract_first()
        if(discussions_next_url is not None):
            discussions_next_page_deep = discussions_next_url.split('=')[-1]
            discussion_max_deep = int(getattr(self,'discussion_list_deep',3))

            if(discussion_max_deep > int(discussions_next_page_deep)):
                yield scrapy.Request(discussions_next_url, callback=self.parse)
            else: 
                logging.debug(('Discussions list Max deep reached of ', discussion_max_deep, '. Will not parse ', discussions_next_url))
                
    def parseDiscussion(self, response):

        data = self.getFbtagJsonInfo(response)
        
        for item in data['document']['included']:
            if(item['type'] == 'posts'):
                
                # time created 
                post_created_datetime = datetime.strptime(item['attributes']['time'], '%Y-%m-%dT%H:%M:%S%z')
                
                # discussion tags 
                post_tags = []
                for included_item in data['document']['included']:
                    if(included_item['type'] == 'tags'):
                        post_tags.append(included_item['attributes']['name'])
                        
                # image urls
                image_urls = []
                soup = bs4.BeautifulSoup(item['attributes']['contentHtml'], "html.parser")
                for img_element in soup.find_all('img'):
                    image_urls.append(img_element['src'])
                    
                # Check for user id
                # In pagination page 2 and onwards holds the first post without relationships data
                if('relationships' not in item):
                    continue
                
                post = {"user_id": item['relationships']['user']['data']['id'],
                         "post_id": item['attributes']['id'],
                         "post_number" : item['attributes']['number'],
                         "created_time_text" : item['attributes']['time'],
                         "created_time": post_created_datetime,
                         "post_content_html" : item['attributes']['contentHtml'],
                         "post_content_text": html2text.html2text(item['attributes']['contentHtml']),
                         "discussion_tags" : ','.join(post_tags),
                         "discussion_id" : data['document']['data']['id'],
                         "discussion_title" : data['document']['data']['attributes']['title'],
                         "discussion_comments_count": data['document']['data']['attributes']['commentsCount'],
                         "discussion_participants_count": data['document']['data']['attributes']['participantsCount'],
                         "url": response.url,
                         "image_urls": ','.join(image_urls),
                        "inserted_time":datetime.now()
                          }
                yield post
        
        # pagination
        # is there a next page ? 
        # parse the next page! 
        next_url = response.xpath("//div[@class='container']/a[contains(text(), 'Next Page')]/@href").extract_first()
        if(next_url is not None):
            next_page_deep = next_url.split('=')[-1]
            max_deep = int(getattr(self,'discussion_deep',3))
            if(max_deep > int(next_page_deep)):
                yield scrapy.Request(next_url, callback=self.parseDiscussion)
            else: 
                logging.debug(('Max deep reached of ', max_deep, '. Will not parse ', next_url))
