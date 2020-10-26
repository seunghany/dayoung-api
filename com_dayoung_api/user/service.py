import os
from com_dayoung_api.utils.file_helper import FileReader
import pandas as pd
from pathlib import Path

class UserService:
    def __init__(self):
        self.fileReader = FileReader()  
        self.path = os.path.abspath("")
        self.odf = None
    def hook(self):
        data = self.new_model()
        # self.odf = pd.DataFrame(
        #     {
        #         'userid' : '1',
        #         'password' : '1',
        #         'name' : 'steve'
        #     }
        # )
        print(data)
        return data
    def new_model(self) -> object:
        path = os.path.abspath("")
        # \com_dayoung_api\
        fname = r"\data\user.csv"
        data = pd.read_csv(path + fname, encoding='utf-8')
        # print('***********')
        # data = data.head()
        # print(data)
        return data

if __name__ == '__main__':
    m = UserService()
    m.hook()