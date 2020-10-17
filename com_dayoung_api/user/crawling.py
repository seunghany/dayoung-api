from bs4 import BeautifulSoup
from urllib.request import urlopen
import os, shutil
from pandas import DataFrame
import pandas as pd

class Service:
    def __init__(self):
        self.entity = Entity()
        pass

    def bugs_music(self):
        pass

    def naver_movie(self):
        pass
    
    def naver_cartoon(self):
        pass

    def naver_cartoon(self, url):
        myparser = 'html.parser' # html.parser : 간단한 HTML과 XHTML 구문 분석기. 표준 라이브러리
        myurl = 'https://comic.naver.com/webtoon/weekday.nhn'
        response = urlopen(myurl)
        soup = BeautifulSoup(response, myparser)
        print(type(soup))

    def create_foler_weekend(self):
        weekday_dict = {'mon': '월요일', 'tue': '화요일', 'wed': '수요일', 'thu': '목요일', 'fri': '금요일', 'sat': '토요일', 'sun': '일요일'}
        # shutil : shell utility : 고수준 파일 연산. 표준 라이브러리
        
        myfolder = 'd:\\imsi\\' # 유닉스 기반은 '/'이 구분자

        try:
            if not os.path.exists(myfolder):
                os.mkdir(myfolder)

            for mydir in weekday_dict.values():
                mypath = myfolder + mydir

                if os.path.exists(mypath):
                    # rmtree : remove tree
                    shutil.rmtree(mypath)
                os.mkdir(mypath)

        except FileExistsError as err:
            print(err)
    # 네이버 웹툰 크롤링
    def naver_webtoon(self, soup):
        category = 'webtoon'
        mytarget = soup.find_all('div', attrs={'class':'thumb'})
        print(str(len(mytarget)) + '개의 {} 데이터 수집'.format(category))

        mylist = [] # 데이터를 저장할 리스트

        for abcd in mytarget:
            myhref = abcd.find('a').attrs['href']
            myhref = myhref.replace('/webtoon/list.nhn?', '')
            result = myhref.split('&')
            # print(myhref)
            # print(result)
            mytitleid = result[0].split('=')[1]
            myweekday = result[1].split('=')[1]
            # print(mytitleid)
            # print(myweekday)

            imgtag = abcd.find('img')
            mytitle = imgtag.attrs['title'].strip()
            mytitle = mytitle.replace('?', '').replace(':', '')
            # print(mytitle)

            mysrc = imgtag.attrs['src']
            # print(mysrc)

            service = Service()
            service.create_folder(mysrc, mytitle, category)
            # break

            sublist = []
            sublist.append(mytitleid)
            sublist.append(myweekday)
            sublist.append(mytitle)
            sublist.append(mysrc)
            mylist.append(sublist)

        mycolumns = ['타이틀번호', '요일', '제목', '링크']
        myframe = DataFrame(mylist, columns=mycolumns)

        filename = 'cartoon.csv'

        myframe.to_csv(filename, encoding='utf-8', index=False)
        print(filename + ' 파일로 저장됨')
        print(category + '사진 저장 완료')



    # 네이버 영화 랭킹 크롤링
    def naver_movie_rank(self, soup):
        category = 'movie_rank'    
        mytarget_title = soup.findAll('div', attrs={'class':'thumb'})
        mytarget_star = soup.findAll('dd', attrs={'class':'star'})

        print(str(len(mytarget_title)) + '개의 %s 데이터 수집' % (category))

        mylist0 = []
        mylist1 = []

        for aaa0 in mytarget_title:
            movie_name = aaa0.find('img').attrs['alt']
            movie_name = movie_name.replace('?', '').replace(':', '')
            movie_src_full = aaa0.find('img').attrs['src']
            movie_src = movie_src_full.replace('?type=m99_141_2', '')
            sublist = []

            sublist.append(movie_name)
            sublist.append(movie_src)

            mylist0.append(sublist)

            service = Service()
            service.create_folder(movie_src, movie_name, category)

        for aaa1 in mytarget_star:
            myhref0 = aaa1.find('a')
            movie_point_full = myhref0.find('span', attrs={'class':'num'})
            movie_point = movie_point_full.contents

            movie_reserve_full = aaa1.find('div', attrs={'class':'star_t1 b_star'})

            try:
                movie_reserve = movie_reserve_full.find('span', attrs={'class':'num'}).contents

            except AttributeError as err:
                # print(err)
                movie_reserve = '미개봉'

            sublist = []

            sublist.append(movie_point)
            sublist.append(movie_reserve)

            mylist1.append(sublist)

        # print(mylist0)
        # print('-'*30)
        # print(mylist1)

        mycolumns0 = ['제목', '스크린샷']
        mycolumns1 = ['별점', '예매율']
        myindex = range(0, len(mylist0))
        myframe0 = DataFrame(mylist0, index=myindex, columns=mycolumns0)
        myframe1 = DataFrame(mylist1, index=myindex, columns=mycolumns1)

        myframe = pd.concat([myframe0, myframe1],axis=1)
        filename = '0920_naver_movie_ranking.csv'
        myframe.to_csv(filename, encoding='utf-8')
        print(filename + ' 파일로 저장됨')

    if __name__ == '__main__':
        sa = Service()
        sa.naver_cartoon()
        