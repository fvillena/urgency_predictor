import pandas as pd
import os
import sqlite3
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Transformer:
    def __init__(self,raw_data_file_path):
        logger.info("transforming data")
        self.raw_data_file_path = raw_data_file_path
        self.wd = "/".join(raw_data_file_path.split("/")[:-1])+"/"
        self.df = pd.read_excel(raw_data_file_path,skiprows=16,skipfooter=561,na_values=["-",0])
        self.df = self.df.melt(id_vars=['Total de atenciones de urgencia'])
        self.df.columns = ["category","date","value"]
        self.df = self.df[self.df["value"] > 4000]
        self.df.date = pd.to_datetime(self.df.date)
        self.df.dropna(inplace=True)
    def write(self,filename = "real_data.csv"):
        logger.info("writing intermediate file")
        processed_data_file_path = self.wd + filename
        self.df.to_csv(processed_data_file_path,index=False)
        logger.info("removing downloaded file")
        os.remove(self.raw_data_file_path)

class DatabaseWriter:
    def __init__(self,db_location,table,processed_data_file_location):
        self.con = sqlite3.connect(db_location)
        self.cursor = self.con.cursor()
        self.table = table
        self.data = pd.read_csv(processed_data_file_location)
    def write(self):
        for _,row in self.data.iterrows():
            category = row["category"]
            date = row["date"]
            value = row["value"]
            count_rows_query = """SELECT COUNT(*) FROM '{}' WHERE category = '{}' AND date = '{}'""".format(self.table,category,date)
            number_of_rows = self.cursor.execute(count_rows_query).fetchone()[0] 
            if number_of_rows == 0:
                logger.info("inserting in {}: {}, {}, {}".format(self.table,category,date,value))
                insert_row_query = """INSERT INTO {}(category, date, value) VALUES('{}', '{}', '{}')""".format(self.table,category,date,value)
                self.cursor.execute(insert_row_query)
            elif number_of_rows==1:
                rowid_query = """SELECT id FROM '{}' WHERE category = '{}' AND date = '{}'""".format(self.table,category,date)
                rowid = self.cursor.execute(rowid_query).fetchone()[0]
                db_value_query = """SELECT * FROM '{}' WHERE id = '{}'""".format(self.table,rowid)
                db_value = self.cursor.execute(db_value_query).fetchone()[3]
                if db_value != value:
                    logger.info("updating value of {} in {}: from {} to {}".format(rowid, self.table, db_value, value))
                    self.cursor.execute("""UPDATE '{}' SET value = '{}' WHERE id = {}""".format(self.table,value,rowid))
            else:
                logging.error("integrity error")
        logging.info("writing changes")
        self.con.commit()