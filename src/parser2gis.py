import itertools
from time import sleep
from dataclasses import dataclass
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from src.constants import COMPANY_ELEM_XPATHS
from src.base import BaseParser, BaseParserCompany


@dataclass
class Parser(BaseParser):
    driver: webdriver

    def get(self, url: str) -> None:
        """Открываем браузер и переходим по заданному URl
        Args:
            url (str): URL ресурса
        """
        self.driver.get(url=url)

    def find_element_by_xpath(self, path: str) -> WebElement | str:
        """Ищет элемент по XPATH и Возвращает WebElement или пустую строку, если елемент не найден
        Args:
            path (str): XPATH элемента
        """
        try:
            return self.driver.find_element(By.XPATH, path)
        except NoSuchElementException:
            return ""

    def get_list_elements_by_xpath(self, path: str) -> list[WebElement | None]:
        """Ищет все элементы по XPATH и возвращает список элементов. Иначе возвращает пустой список
        Args:
            path (str): XPATH элемента
        """
        return self.driver.find_elements(By.XPATH, path)

    def click_element(self, path: str) -> bool:
        """Кликает по элементу, если он найден, и возвращает True. В противном случае возвращает False
        Args:
            path (str): XPATH элемента
        """
        elem = self.find_element_by_xpath(path)
        if elem:
            elem.click()
            return True
        else:
            return False

    def get_attribute(self, path: str, attribute: str) -> str | None:
        """Возвращает заданный атрибут элемента.
        Args:
            path (str): XPATH элемента
            attribute (str): атрибут элемента
        """
        elem = self.find_element_by_xpath(path)
        return elem.get_attribute(attribute)


@dataclass
class ParserCompany2Gis(BaseParserCompany):
    parser: Parser

    def get(self, url: str) -> None:
        self.parser.get(url=url)

    def get_company_name(self) -> str:
        return self.parser.find_element_by_xpath(COMPANY_ELEM_XPATHS["name"]).text

    def get_company_description(self) -> str:
        return self.parser.find_element_by_xpath(COMPANY_ELEM_XPATHS["description"]).text

    def get_company_address(self) -> str:
        street = self.parser.find_element_by_xpath(
            COMPANY_ELEM_XPATHS["street"]).text
        city = self.parser.find_element_by_xpath(
            COMPANY_ELEM_XPATHS["city"]).text.split(", ")
        city.reverse()
        city.append(street)
        address = ", ".join(city)
        return address

    def get_company_phones(self) -> list[str | None]:
        if self.parser.click_element(COMPANY_ELEM_XPATHS["show_phones_btn"]):
            list_elems = self.parser.get_list_elements_by_xpath(
                COMPANY_ELEM_XPATHS["phones"])
            return [''.join(itertools.filterfalse(str.isalpha, item.text.replace('\n', ''))) for item in list_elems]
        else:
            return []

    def get_company_site_link(self) -> str | None:
        return self.parser.get_attribute(COMPANY_ELEM_XPATHS["link"], attribute="href")

    def get_company_social_networks_links(self) -> dict[str: str]:
        path = COMPANY_ELEM_XPATHS["social_links"]
        dict_links = {}
        list_elems = self.parser.get_list_elements_by_xpath(path)
        for elem in list_elems:
            title = elem.find_element(By.XPATH, "span/a/div/span").text
            link = elem.find_element(By.TAG_NAME, "a").get_attribute("href")
            dict_links.setdefault(title, link)
        return dict_links

    def get_reviews(self) -> list[str | None]:
        if self.parser.click_element(COMPANY_ELEM_XPATHS["review_link_btn"]):
            reviews = []
            sleep(3)
            list_elems = self.parser.get_list_elements_by_xpath(
                COMPANY_ELEM_XPATHS["review_text"])
            for elem in list_elems:
                try:
                    reviews.append(elem.find_element(
                        By.XPATH, "div[4]/div[1]/a").text)
                except NoSuchElementException:
                    continue
            return reviews
        else:
            return []

