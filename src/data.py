import pandas as pd
import os
class Transformer:
    def __init__(self,raw_data_file_path):
        self.raw_data_file_path = raw_data_file_path
        self.wd = "/".join(raw_data_file_path.split("/")[:-1])+"/"
        self.df = pd.read_excel(raw_data_file_path,skiprows=16,skipfooter=561,na_values="-")
        self.df = self.df.melt(id_vars=['Total de atenciones de urgencia'])
        self.df.columns = ["category","date","value"]
        self.df.date = pd.to_datetime(self.df.date)
        self.df.sort_values(["category","date"])
    def write(self,filename = "real_data.csv"):
        processed_data_file_path = self.wd + filename
        self.df.to_csv(processed_data_file_path,index=False)
        os.remove(self.raw_data_file_path)