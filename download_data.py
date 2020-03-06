from src.scraper import Scraper
from src.data import Transformer
import os
wd = os.getcwd() + "/"
escreiper = Scraper(wd)
scraped_data_file_path = escreiper.scrape()
transformer = Transformer(scraped_data_file_path)
transformer.write()