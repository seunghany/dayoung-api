import requests
from bs4 import BeautifulSoup
import re # 정규식 사용
import csv
from pandas import DataFrame

class Crawling:
    '''
        Crawls data from wikipedia with following information
        attributes: ['사진', '나이','이름','본명','종교','소속사', '배우자', '자녀','데뷔년도']
        returns Dataframe with above attributes
        '''
    def __init__(self, actors_name = ['이병헌']):
        self.actors_name = actors_name

    def crawl(self):
        # columns=['사진', '나이','이름','본명','종교','소속사', '배우자', '자녀','데뷔년도']
        # url = "https://ko.wikipedia.org/wiki/"
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}
        # actors_name =["수지", "이병헌","전지현","손예진","안소희","하지원","강동원","하정우","김혜수","현빈" ,"유해진","송강호"]
        # actors_name = ["손예진"]
        actors = []
        actors_name = self.actors_name
        actorid = 1
        for name in actors_name :
            url = "https://ko.wikipedia.org/wiki/"
            url += name
            res = requests.get(url, headers=headers)
            res.raise_for_status() # 혹시 문제가 있을시 에러
            soup = BeautifulSoup(res.text, 'lxml')
            # --------------------------------------------- 위키 드감
            table = soup.find('table', attrs = {"class":"infobox"})
            actor_info = {}
            # if table.has_next
            if table:
                tables = table.find_all("tr")
                url_table = tables[1].find('a',attrs={"class":"image"})
                url2 = url_table.find('img')['src']
                actor_info['photoUrl'] = url2
                tables = tables[2:]
                actor = {}
                for table in tables:
                    th = table.th.get_text()
                    td = table.td.get_text()
                    actor[th] = td
                # 데이터 정리
                # 출생 -> 나이
                p = re.compile("..세") # 30세 56세 등등
                age = p.search(actor['출생']).group(0)
                age = age[:-1]
                actor_info['age'] = age
                actor_info['actorid'] = actorid
                actorid +=1
                
                # 가명 없을 시 없다고 표시 본명에 가명 없음 이라고 표시
                actor_info['name'] = name
                if '본명' not in actor.keys():
                    actor_info['realName'] = 'no real name'
                else:
                    actor_info['realName'] = actor['본명']
                # 종교
                if '종교' not in actor.keys():
                    actor_info['religion'] = 'no religion'
                else:
                    actor_info['religion'] = actor['종교']
                # 소속사는 다 있음
                actor_info['agency'] = actor['소속사']
                # 배우자
                if '배우자' not in actor.keys():
                    actor_info['spouse'] = 'no spouse'
                else:
                    actor_info['spouse'] = actor['배우자']
                # 자녀
                if '자녀' not in actor.keys():
                    actor_info['children'] = 'no child'
                else:
                    actor_info['children'] = actor['자녀']
                # 활동 기간 - 정규식 이용
                # 데뷔년도
                p = re.compile('....년')
                debutYear = p.findall(actor['활동 기간'])[0][:-1]
                actor_info['debutYear'] = debutYear
                actors.append(actor_info)

            else:
                print(name, "이름의 유명인이 많음으로 인해 제외 합니다")
        data = DataFrame(actors, columns=['photoUrl', 'age','name','realName','religion','agency', 'spouse', 'children','debutYear','actorid'])
        return data

