from src.scraper import Scraper
from src.data import Transformer
import os
from src.data import DatabaseWriter
wd = os.getcwd() + "/"
escreiper = Scraper(wd)
scraped_data_file_path = escreiper.scrape()
transformer = Transformer(scraped_data_file_path)
transformer.write()

dw = DatabaseWriter(wd+"/../urgency_predictor_data/data.sqlite","real",wd+"/real_data.csv")
dw.write()