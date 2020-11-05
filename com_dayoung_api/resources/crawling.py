import requests
from bs4 import BeautifulSoup
import re # 정규식 사용
import csv
from pandas import DataFrame
import random

class Crawling:
    '''
        Crawls data from wikipedia with following information
        attributes: ['사진', '나이','이름','본명','종교','소속사', '배우자', '자녀','데뷔년도']
        returns Dataframe with above attributes
        '''
    def __init__(self, actors_name = ['이병헌'], gender = 'm'):
        self.actors_name = [(actors_name, gender)]
        self.gender = 'm'

    def crawl(self):
        # columns=['사진', '나이','이름','본명','종교','소속사', '배우자', '자녀','데뷔년도']
        # url = "https://ko.wikipedia.org/wiki/"
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}
        
        actors_name = self.actors_name
        actors_name =[("이병헌","m"),("전지현","f"),("손예진","f"), ("안소희","f"),("강동원","m"),("하정우","m"),
                    ("김혜수","f"),("현빈","m") ,("유해진","m"),("송강호","m") ,("지창욱","m"), ("이민정","f") 
                    , ("한효주","f"), ("박보영","f"), ("정해인","m")]
        
        # actors_url = "https://namu.wiki/w/%EB%B0%B0%EC%9A%B0/%ED%95%9C%EA%B5%AD"
        actors_name_2 = self.crawl_actors_name()
        actors_name.extend(actors_name_2)
        actor_id = 1
        # actors_name = ["이병헌", "이진욱"]
        actors_name = [('이병헌', "m")]
        data = self.actors_to_df(actors_name, actor_id)
        return data

    def crawl_actors_name(self):
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}
        # url = self.url
        url = "https://namu.wiki/w/%EB%B0%B0%EC%9A%B0/%ED%95%9C%EA%B5%AD"
        res = requests.get(url, headers=headers)
        res.raise_for_status() # 혹시 문제가 있을시 에러)
        soup = BeautifulSoup(res.text, 'lxml')
        # 여기 까진 크롤링 하기 전 기본
        #---------------------------------------------------------------------
        # 여기부터 크롤링 시작
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}
        res = requests.get(url, headers=headers)
        res.raise_for_status() # 혹시 문제가 있을시 에러
        soup = BeautifulSoup(res.text, 'lxml')
        list_div = soup.find_all('div', {'class': 'wiki-heading-content'})
        elements = ""
        actor = ""
        actors_list = ""
        actors2 = []
        for elements in list_div:
            actors_list = elements.find_all('li')
            for actor in actors_list:
                if len(actor.text) == 3:
                    actors2.append(actor.text)
        return actors2

    
    def actors_to_df(self, actors_name, actor_id):
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}
        
        actors = []
        for name in actors_name :
            actor_info = {}
            if type(name) == tuple:
                # 첫 화면에 보여줄 배우들
                self.gender = name[1] # gender
                name = name[0] # name
            if name == "갈소원": # 여기 부터 여성 배우들 출력
                self.gender = 'f'
            url = "https://ko.wikipedia.org/wiki/"
            url += name
            res = requests.get(url, headers=headers)
            try: 
                res.raise_for_status()
            except:
                continue
            soup = BeautifulSoup(res.text, 'lxml')
            # --------------------------------------------- 위키 드감
            table = soup.find('table', attrs = {"class":"infobox"})
            
            # if table.has_next
            if not table:
                # print(name, "이름의 유명인이 많음으로 인해 제외 합니다")
                continue
            tables = table.find_all("tr")
            url_table = tables[1].find('a',attrs={"class":"image"})
            if not url_table:
                # print("문제 있음")
                continue
            url2 = url_table.find('img')['src']
            if len(url2) > 200:
                continue
            actor_info['photo_url'] = url2
            
            tables = tables[2:]
            actor = {}
            for table in tables:
                if table.th or table.td is None:
                    th = table.th.get_text()
                    if not table.td:
                        continue
                    td = table.td.get_text()
                    actor[th] = td
            # 데이터 정리
            # 출생 -> 나이
            # print(name)
            # print(actor)
            p = re.compile("..세") # 30세 56세 등등
            if '출생' not in actor.keys():
                continue
            if not p.search(actor['출생']):
                continue
            age = p.search(actor['출생']).group(0)
            age = age[:-1]
            actor_info['age'] = age
            actor_info['actor_id'] = actor_id
            
            
            # 가명 없을 시 없다고 표시 본명에 가명 없음 이라고 표시
            actor_info['name'] = name
            if '본명' not in actor.keys():
                actor_info['real_name'] = 'no real name'
            else:
                actor_info['real_name'] = actor['본명']
            # 종교
            if '종교' not in actor.keys():
                actor_info['religion'] = 'no religion'
            else:
                actor_info['religion'] = actor['종교']
            # 소속사
            if '소속사' not in actor.keys():
                actor_info['agency'] = 'no angency'
            else:
                if len(actor['소속사']) > 30:
                    continue
                actor_info['agency'] = actor['소속사']
            # 배우자
            if '배우자' not in actor.keys():
                actor_info['spouse'] = 'no spouse'
            else:
                if len(actor['배우자']) > 30:
                    continue
                actor_info['spouse'] = actor['배우자']
            # 자녀

            if '자녀' not in actor.keys():
                actor_info['children'] = 'no child'
            else:
                if len(actor['자녀'])>100:
                    continue
                actor_info['children'] = actor['자녀']
                
            
            # 활동 기간 - 정규식 이용
            # 데뷔년도
            p = re.compile('....년')
            if '활동 기간' not in actor.keys():
                continue
            if not p.findall(actor['활동 기간']):
                continue
            debut_year = p.findall(actor['활동 기간'])[0][:-1]
            actor_info['debut_year'] = debut_year
            actor_info['gender'] = self.gender
            actors.append(actor_info)
            actor_id +=1
            if actor_id < 13:
                actor_info['state'] = "1"
            else:
                actor_info['state'] = "0"
            if actor_id%50 == 10:
                print("working on it", actor_id)
                print("하고 있어!!!!!!!")
                print("하고 있어!!!!!!!")
                print("하고 있어!!!!!!!")
                print("하고 있어!!!!!!!")
                print("하고 있어!!!!!!!")
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

        # dict_keys(['photo_url', 'age', 'actor_id', 'name', 'real_name', 'religion', 'agency', 'spouse', 'children', 'debut_year', 'gender'])
        data = DataFrame(actors, columns=['photo_url', 'age', 'actor_id', 'name', 'real_name', 'religion', 'agency', 'spouse', 'children', 'debut_year', 'gender','state'])
        return data



# if __name__ == '__main__':
#     c = Crawling()
#     c.crawl()