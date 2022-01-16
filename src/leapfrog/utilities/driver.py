'''
Firefox, selenium webdriver class for scraping URLs

author(s): Derek Herincx, derek663@gmail.com
last_updated: 12/23/2021
'''
import os

from selenium import webdriver

class CustomDriver:
    """
    A Firefox, selenium driver. Note, current implementation only supports
    Firefox, so this module requires the geckodriver executable. Make sure
    geckodriver is placed in any locations specified in your PATH

    Args:
        url: str
            Webpage to scrape
        headless: bool
            Should selenium run in headless mode?
        executable_path: str
            Path to browser webdriver, if not in PATH
    """
    def __init__(
        self,
        url: str,
        headless: bool = False, # change when deployed in production
        executable_path: str = None
    ) -> "CustomDriver":
        self.url = url
        self.headless = headless
        self.executable_path=executable_path
        if not executable_path:
            self.executable_path = self.find_webdriver_path()

    def __call__(self):
        """Shortcut to HTML source method"""
        return self.open_driver()

    @staticmethod
    def find_webdriver_path(driver: str = 'geckodriver') -> str:
        """
        Some os magic to get executable path.

        This will also prevent us from getting a warning about
        a None value in the `executable_path` param when opening
        a context manager webdriver
        """

        os_paths = os.environ['PATH'].split(":")
        for path in os_paths:
            if driver in os.listdir(path):
                exec_path = f'{path}/{driver}'
        return exec_path

    def open_driver(self) -> "driver.CustomDriver":
        """Returns a driver, ready to retrieve content"""
        driver = webdriver.Firefox(
            executable_path=self.executable_path
        )
        driver.get(self.url)
        return driver
