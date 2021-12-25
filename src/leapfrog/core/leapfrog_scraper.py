'''
Scraper for https://www.hospitalsafetygrade.org/

author(s): Derek Herincx, derek663@gmail.com
last_updated: 12/24/2021
'''
from typing import List, Dict
from selenium.webdriver.remote.webelement import WebElement

from utilities import Driver

# this is for easy testing
URL = "https://www.hospitalsafetygrade.org/search?findBy=state&zip_code=&city=&state_prov=AZ&hospital="

class LeapfrogScraper(Driver):
    """
    Scraper for  https://www.hospitalsafetygrade.org

    Args:
        pagination: bool
            Does the results page have multiple page results?
        class_name: str
            Classs name of HTML elements containing relevant data
    """
    def __init__(self, pagination=False, **kwargs):
        self.pagination = False
        self.class_name = "leapfrogSearchResult"
        super().__init__(**kwargs)

    @property
    def driver(self):
        """Driver, inherited from utils Driver class"""
        return Driver(self.url)()

    def get_hospital_metadata(self) -> List[Dict[str, str]]:
        """
        Hospitals metadata, structured appropriately for easy export as
        JSON or into a csv, whatever user needs

        Returns
            data: list
                Metadata as a list of Python dictionaries
        """
        driver = self.driver
        tags = driver.find_elements_by_class_name(self.class_name)
        data = []
        for tag in tags:
            # note: return statement ensures data is returned to Python env.
            metadata = driver.execute_script("return arguments[0].dataset", tag)
            data.append(metadata)

        return data
