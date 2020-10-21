  
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
baseurl = os.path.dirname(os.path.abspath(__file__))
from com_dayoung_api.utils.file_helper import FileReader
import pandas as pd
import numpy as np
class UserPro:
    def __init__(self):
        self.fileReader = FileReader()  
        self.data = './data' # 안에 user.csv 있음
        # user columns 는 UserId	Password	name	Age	Date of Birth	Gender

    def new_model(self, payload) -> object:
        this = self.fileReader
        this.data = self.data
        this.fname = payload
        return pd.read_csv(os.path.join(self.data, this.fname))

if __name__ == '__main__':
    m = UserPro()
    print(m.new_model, 'user.csv')
    