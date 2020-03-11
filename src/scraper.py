from selenium import webdriver
import os
from pyvirtualdisplay import Display
import logging
import datetime
import time
from selenium.webdriver.common.keys import Keys
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class Scraper:
    def __init__(self,wd):
        logger.info("starting scraper")
        self.wd = wd
        display = Display(visible=0, size=(2880, 1800)).start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        prefs = {'download.default_directory' : wd}
        options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(options=options)
    def scrape(self, url=r"http://cognos.deis.cl/ibmcognos/cgi-bin/cognos.cgi?b_action=cognosViewer&ui.action=run&ui.object=%2fcontent%2ffolder%5b%40name%3d%27PUB%27%5d%2ffolder%5b%40name%3d%27REPORTES%27%5d%2ffolder%5b%40name%3d%27Atenciones%20de%20Urgencia%27%5d%2freport%5b%40name%3d%27Atenciones%20Urgencia%20-%20Vista%20diaria%20-%20Servicios%27%5d&ui.name=Atenciones%20Urgencia%20-%20Vista%20diaria%20-%20Servicios&run.outputFormat=&run.prompt=true"):
        logger.info("initial page")
        self.driver.get(url)
        days = 30
        offset = 0
        current_date = datetime.date.today()
        starting_date = str(current_date - datetime.timedelta(days=days+offset))
        end_date = str(current_date - datetime.timedelta(days=offset))
        logger.info("entering dates")
        input_start = self.driver.find_elements_by_xpath("//input[@class='clsSelectDateEditBox']")[0]
        input_start.clear()
        input_start.send_keys(starting_date)
        input_end = self.driver.find_elements_by_xpath("//input[@class='clsSelectDateEditBox']")[1]
        input_end.clear()
        input_end.send_keys(end_date)
        logger.info("pressing continue")
        self.driver.find_element_by_xpath("//button[text()='Continuar']").click()
        logger.info("waiting for page to load")
        start_time = time.time()
        while True:
            current_time = time.time()
            if self.driver.find_elements_by_xpath("//*[text()='Descargar como Excel']"):
                self.driver.find_element_by_xpath("//*[text()='Descargar como Excel']").click()
                break
            if (current_time - start_time) > 30:
                raise TimeoutError('button timeout') 
        logger.info("downloading file")
        start_time = time.time()
        download_ready=False
        while ((download_ready == False)):
            current_time = time.time()
            for filename in os.listdir(self.wd):
                if filename.endswith("xlsx"):
                    downloaded_file_path = self.wd+filename
                    download_ready=True
                if (current_time - start_time) > 30:
                    raise TimeoutError('download timeout')
        self.driver.quit()
        logger.info("closing scraper")
        return (downloaded_file_path)