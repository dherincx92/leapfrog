'''
Selenium webdriver class for scraping URLs

author(s): Derek Herincx, derek663@gmail.com
last_updated: 12/23/2021
'''
import os

from selenium import webdriver

class Driver:
    """
    A selenium driver class retrieving a webpage's HTML code

    Args:
        url: str
            Webpage to scrape
        executable_path: str
            Path to browser webdriver, if not in PATH
    """
    def __init__(
        self,
        url: str,
        executable_path: str = None
    ) -> "Driver":
        self.url = url
        self.executable_path=executable_path
        if not executable_path:
            self.executable_path = self.find_webdriver_path()

    def __call__(self):
        """Shortcut to HTML source method"""
        return self.html_source()

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

    def html_source(self) -> str:
        """Retrieves a HTML page source as a string"""
        with webdriver.Firefox(
            executable_path=self.executable_path
        ) as driver:
            driver.get(self.url)
            html = driver.page_source
        return html
