from abc import ABC, abstractmethod


class BaseParserCompany(ABC):
    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def get_company_name(self):
        pass

    @abstractmethod
    def get_company_description(self):
        pass

    @abstractmethod
    def get_company_address(self):
        pass

    @abstractmethod
    def get_company_phones(self):
        pass

    @abstractmethod
    def get_company_site_link(self):
        pass

    @abstractmethod
    def get_company_social_networks_links(self):
        pass

    @abstractmethod
    def get_reviews(self):
        pass


class BaseParser(ABC):
    @abstractmethod
    def get(self, url: str):
        pass

    @abstractmethod
    def find_element_by_xpath(self, path: str):
        pass

    @abstractmethod
    def get_list_elements_by_xpath(self, path: str):
        pass

    @abstractmethod
    def get_attribute(self, path: str, attribute: str):
        pass

    @abstractmethod
    def click_element(self, path: str):
        pass
