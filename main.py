import undetected_chromedriver as uc

from src.parser2gis import ParserCompany2Gis, Parser


def main():
    url = "https://2gis.ru/abakan/firm/70000001069066543"
    chrome_parser = Parser(uc.Chrome())

    parser = ParserCompany2Gis(parser=chrome_parser)
    parser.get(url=url)

    name = parser.get_company_name()
    description = parser.get_company_description()
    address = parser.get_company_address()
    list_phones = parser.get_company_phones()
    link = parser.get_company_site_link()
    soc_links = parser.get_company_social_networks_links()
    reviews = parser.get_reviews()

    print(
        name,
        description,
        address,
        list_phones,
        link,
        soc_links,
        reviews,
        sep="\n"
    )


if __name__ == "__main__":
    main()
