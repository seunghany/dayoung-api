import os
from com_dayoung_api.utils.file_helper import FileReader
import pandas as pd
from pathlib import Path

class UserPro:
    def __init__(self):
        self.fileReader = FileReader()  
        self.path = os.path.abspath("")
    def hook(self):
        data = self.new_model()
        print(data)
        return data
    def new_model(self) -> object:
        path = os.path.abspath("")
        fname = r"\data\user.csv"
        data = pd.read_csv(path + fname, encoding='utf-8')
        # print('***********')
        # data = data.head()
        # print(data)
        return data

if __name__ == '__main__':
    m = UserPro()
    m.hook()