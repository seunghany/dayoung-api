  
import os

from com_dayoung_api.user.dto import UserDto
from com_dayoung_api.review.dto import ReviewDto
from com_dayoung_api.utils.file_helper import FileReader
import pandas as pd
import numpy as np
baseurl = os.path.dirname(os.path.abspath(__file__))
class UserPro:
    def __init__(self):
        self.reader = FileReader()  
        # user columns 는 UserId	Password	name	Age	Date of Birth	Gender
    def hook(self):
        data = self.get_data()

    def get_data(self):
        reader = self.reader
        reader.context = os.path.join(baseurl,'data')
        reader.fname = 'user.csv'
        reader.new_file()
        data = reader.csv_to_dframe()
        print(data)
        return data

    def new_model(self, payload) -> object:
        this = self.fileReader
        this.data = self.data
        this.fname = payload
        return pd.read_csv(os.path.join(self.data))

if __name__ == '__main__':
    m = UserPro()
    m.hook()