'''
Scraper for https://www.hospitalsafetygrade.org/

# TODO: add validation to ensure driver is closed

author(s): Derek Herincx, derek663@gmail.com
last_updated: 12/24/2021
'''
from typing import List, Dict

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utilities import Driver

# this is for easy testing
URL = "https://www.hospitalsafetygrade.org/search?findBy=state&zip_code=&city=&state_prov=AZ&hospital="

class LeapfrogScraper(Driver):
    """
    Scraper for  https://www.hospitalsafetygrade.org

    Args:
        pagination: bool
            Does the results page have multiple pages of results?
        class_name: str
            Classs name of HTML elements containing relevant data
        timeout: int
            Number of seconds before driver times out
    """
    def __init__(self, pagination=False, **kwargs):
        self.pagination = False
        self.class_name = "leapfrogSearchResult"
        self.timeout = 20 # seconds
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
        css_selector = (By.CSS_SELECTOR, f".resultsList > .{self.class_name}")

        try:
            # sometimes, webpage is slow and results are still loading; this
            # ensures we don't begin the scraping before the results load
            element = WebDriverWait(driver, self.timeout).until(
                EC.presence_of_element_located(css_selector)
            )

            tags = driver.find_elements_by_class_name(self.class_name)

            data = []
            for tag in tags:
                # note: return statement ensures data is returned to Python env.
                metadata = driver.execute_script("return arguments[0].dataset", tag)
                data.append(metadata)

            return data
        finally:
            driver.close()
