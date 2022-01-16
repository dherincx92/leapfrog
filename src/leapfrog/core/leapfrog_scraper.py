'''
Scraper for https://www.hospitalsafetygrade.org/

TODO: configure slug to create href?

author(s): Derek Herincx, derek663@gmail.com
last_updated: 12/24/2021
'''
from typing import List, Dict

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from leapfrog.utilities import CustomDriver

class LeapfrogScraper(CustomDriver):
    """Selenium scraper for  https://www.hospitalsafetygrade.org

    Args:
        pagination: bool
            Does the results page have multiple pages of results?
        class_name: str
            Classs name of HTML elements containing relevant data
        timeout: int
            Number of seconds before driver times out when opening webpage
    """
    def __init__(
        self,
        pagination: bool=False,
        *args,
        **kwargs
    ) -> "LeapfrogScraper":
        self.pagination = False
        self.class_name = "leapfrogSearchResult"
        self.timeout = 20 # seconds
        super().__init__(*args, **kwargs)

    @property
    def driver(self):
        """Driver, inherited from utils Driver class"""
        return CustomDriver(self.url)()

    def get_hospital_metadata(self, test=True) -> List[Dict[str, str]]:
        """
        Hospitals metadata, structured appropriately for easy export as
        JSON or into a csv, whatever user needs

        Args:
            test: bool
                Do we want to return a single review?

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

            # selenium 4.1.0 --> find_elements_by_* now deprecated
            params = (By.CLASS_NAME, self.class_name)
            if test:
                # single tag returned; mainly to test
                tags = list(driver.find_element(*params))
            else:
                tags = driver.find_elements(*params)

            data = []
            for tag in tags:
                # note: return statement ensures data is returned to Python env.
                metadata = driver.execute_script("return arguments[0].dataset", tag)

                address = tag.find_element(By.CLASS_NAME, "address") \
                        .get_attribute("innerText")
                metadata['address'] = address
                data.append(metadata)
            return data
        finally:
            driver.close()
