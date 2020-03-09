from src.scraper import Scraper
from src.data import Transformer
import os
from src.data import DatabaseWriter
from src.predictor import Predictor
wd = os.getcwd() + "/"
escreiper = Scraper(wd)
scraped_data_file_path = escreiper.scrape()
transformer = Transformer(scraped_data_file_path)
transformer.write()

dw = DatabaseWriter(wd+"../urgency_predictor_data/data.sqlite","real",wd+"real_data.csv")
dw.write()

wd = os.getcwd() + "/"
p = Predictor(wd+"../urgency_predictor_data/data.sqlite")
p.fit()
p.predict(60)
p.write()