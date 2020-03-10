import sqlite3
import pandas as pd
from fbprophet import Prophet
import datetime
from src.data import DatabaseWriter

class Predictor:
    def __init__(self,db_location, category = "TOTAL CAUSAS SISTEMA RESPIRATORIO"):
        self.category = category
        self.db_location = db_location
        con = sqlite3.connect(db_location)
        self.real_data = pd.read_sql_query("""select * from real where date between date("now", "-3 years") AND date("now", "-7 days") and category = "{}" """.format(category), con)
        self.real_data["date"] = pd.to_datetime(self.real_data["date"])
        self.real_data = self.real_data[["date","value"]].sort_values("date")
        self.real_data.columns = ["ds","y"]
        self.last_date = self.real_data["ds"].max()
        self.current_date = pd.to_datetime(datetime.date.today())
        self.days_difference = (self.current_date - self.last_date).days
        self.m = Prophet()
        
    def fit(self):
        self.m.fit(self.real_data)
    
    def predict(self, periods):
        self.future = self.m.make_future_dataframe(periods+self.days_difference)[-(periods+self.days_difference):]
        self.forecast = self.m.predict(self.future)
        self.forecast["category"] = self.category
        self.forecast.rename(columns={"yhat":"value","ds":"date"}, inplace=True)
        self.forecast[["category","date","value"]].to_csv("forecasted_data.csv",index=False)
    def write(self):
        w = DatabaseWriter(self.db_location,"forecasted","forecasted_data.csv")
        w.write()