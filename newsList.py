from crawllib.crawler import Crawler
from bs4 import BeautifulSoup
from selenium import webdriver as WebDriver
import pandas as pd
import re


# Daum News search Url
# https://search.daum.net/search?w=news&DA=STC&enc=utf8&cluster=y&cluster_page=1&q={search_word}&p={page_no}&sd={start_date}000000&ed={end_date}235959&period=u


"""
: 네이버 뉴스는 결과물을 최대 4000개까지만 반환한다 
: 따라서 한번에 date를 길게 넣으면 모든 결과를 못얻는다 
: 모든 결과를 수집하기 위한 추가 로직이 필요하다 !
: 1) date 단위를 나누면서 request
: 2) paging시 마지막 page_no 에서 반복문 나가기
"""

# # 노드 탐색
# def bfs(start_node : BeautifulSoup, match, graph):
#     visit = list()
#     queue = list()

#     queue.append(start_node)
#     while queue:
#         node = queue.pop(0)
#         if node not in visit:
#             visit.append(node)
#             queue.extend(graph[node])
#     return visit
   

    # if len(start_node.text) > len(match):
    #     return start_node
    # else:
    #     if start_node.next_sibling is None and len(soupData.children) > 0:
    #         for child in start_node
    #         .children:
    #             search(child, match)
    #     elif start_node.next_sibling is not None:
    #         search(start_node.next_sibling, match)


rate_best_data = pd.read_csv('data/급등주포착_최종.csv', index_col=[0])


for code in set(rate_best_data.code):
    mark = rate_best_data.code==code
    rate_best_data[mark]
    try:

        code_sise_data = rate_best_data[mark].values
        search_word = rate_best_data[mark]
        search_word = search_word['한글 종목약명']    # Series
        search_word = list(search_word.values)[0].replace('보통주','').strip()  # index 매치가 안되어서 list로 형변환
    except Exception as e:
        print('krx_code와 매치되지않음(종목명X) : ', code)
        continue
    date_list = list(rate_best_data[mark]['date'].values)
    start_date = date_list[0]
    end_date = date_list[-1]
    result = [""]
    for date in date_list:
        sort_type = Crawler.Sort_Best
        max_page = 4000   # 4000
        last_line = ""
        for page_no in range(1,max_page,10):
            url = f'https://search.naver.com/search.naver?where=news&query={search_word}&sort={str(sort_type)}&pd=3&ds={date}&de={date}&start={page_no}'
            print(url)
            crawler = Crawler()
            res = crawler.get_url_data(url)
            soupData = BeautifulSoup(res.content, 'html.parser')

            news_list = soupData.select('.news_tit')
            desc = soupData.select('.api_txt_lines.dsc_txt_wrap')
            news_row = ""
            for title_addr, content in zip(news_list, desc):
                print(title_addr['href'])
                print(title_addr['title'])
                #print(content.text)
                
                news_row = [code, date, title_addr['title'] ,title_addr['href'] , content.text]
            #    
            print(last_line != news_row)
            if(last_line != news_row):      # is not  : id  / != : operator
                result.append(news_row)
                last_line = news_row
            else:
                break

                ###########
                # news_res = crawler.get_url_data(title_addr['href'])
                # news_detail = BeautifulSoup(news_res.content, 'html.parser')
                # article = search(news_detail, content.text)
                # print(article)
        # end : for range(1,max_page,10):
    # end : for list(rate_best_data[mark]['date'].values):
    print(result)
    df_news = pd.DataFrame(result[1:], columns=['code', 'date', 'title', 'link', 'content'])
    df_news.to_csv('data/news/%s_네이버_뉴스목록_%s-%s.csv'%(search_word, start_date, end_date))
# end : for set(rate_best_data.code):
           

# for link in df_news.link[:2]:
#     print(link)
#     res = crawler.get_url_data(link)
#     soupData = BeautifulSoup(res.content, 'html.parser')
#     for item in soupData.div:
#         print(item)
#     print('*'*50)


# js -> document.defaultView.getComputedStyle(document.querySelectorAll('div')[40])['fontSize']
