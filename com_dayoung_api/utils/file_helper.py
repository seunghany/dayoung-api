from dataclasses import dataclass
import os
import pandas as pd
import xlrd
import googlemaps
import json

@dataclass
class FileReader:
    # def __init__(self, context, fname, train, test, id, label):
    #     self._context = context  # _ 1개는 default 접근, _ 2개는 private 접근

    # 3.7부터 간소화되서 dataclass 데코 후, key: value 형식으로 써도 됨 (롬복 형식)
    context : str = ''
    fname: str = ''
    train: object = None
    test: object = None
    id : str = ''
    lable : str = ''
    

    def new_file(self) -> str:
        print(os.path.join(self.context,self.fname))
        
        return os.path.join(self.context,self.fname)

    def csv_to_dframe(self) -> object:
        return pd.read_csv(self.new_file(), encoding='UTF-8', thousands=',')

    def xls_to_dframe(self, header, usecols) -> object:
        print(f'PANDAS VERSION: {pd.__version__}')
        return pd.read_excel(self.new_file(), header = header, usecols = usecols)

    def create_gmaps(self):
        return googlemaps.Client(key='')

    def json_load(self):
        return json.load(open(self.new_file(), encoding='UTF-8'))