#! /usr/bin/env python
# encoding=utf-8

"""
爬取豆瓣好评电影Top250
"""
import codecs
from bs4 import BeautifulSoup
import requests

download_url = 'http://movie.douban.com/top250/'
#解析页面内容
def download_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    data = requests.get(url, headers).content
    return data
#根据页面元素特征,解析所需电影名称和下一页面网址
def parse_html(html):
    soup = BeautifulSoup(html,"html.parser")
    movie_list_soup = soup.find('ol',attrs={'class':'grid_view'})
    movie_name_list = []
    for movie_li in movie_list_soup.find_all('li'):
        detail = movie_li.find('div',attrs={'class','hd'})
        #movie_name = detail.find('span',attrs={'class','title'}).getText()
        movie_name = detail.find_all('span',attrs={'class','title'})

        for a in movie_name:
            #get_text() 是取得除标签外的标签里面的内容
            movie_name_list.append(a.get_text())
            #movie_name_list.append(a.next.text)


    next_page = soup.find('span',attrs={'class','next'}).find('a')
    if next_page:
        return movie_name_list, download_url + next_page['href']
    return movie_name_list, None


def main():
    url = download_url
    with codecs.open('test','wb',encoding='utf-8') as fp:
        while url:
            html = download_page(url)
            movies, url =parse_html(html)
            #将所得电影名称写入movies这个文件夹
            fp.write(u'{test}\n'.format(test='\n'.join(movies)))


if __name__=='__main__':
    main()
