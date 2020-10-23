from com_dayoung_api.actor.crawling import Crawling

class ActorService:
    
    def __init__(self):
        
        actors_name = ['전지현', "이병한", "손예진"]
        actors_name = ['전지현']
        actors_name =["수지", "이병헌","전지현","손예진","안소희","강동원","하정우","김혜수","현빈" ,"송강호"]
        
        self.crawl = Crawling(actors_name) # 이병헌 is given as default
        # print(self.dataFrame)
        
    def hook(self):
        self.dataFrame = self.crawl.crawl()
        print(self.dataFrame)
        return self.dataFrame



if __name__ == '__main__':
    # actors_name =["수지", "이병헌","전지현","손예진","안소희","하지원","강동원","하정우","김혜수","현빈" ,"유해진","송강호"]
    m = ActorService()
    m.hook()
    