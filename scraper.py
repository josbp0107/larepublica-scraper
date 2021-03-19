import requests
import lxml.html as html

HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//text-fill[not (@class)]/a/@href'
XPATH_TITLE = '//div[@class="mb-auto"]/h2/span/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not (@class)]/text()'

def parse_home():
    # try catch to work safe
    try:
        response = requests.get(HOME_URL) # Extract HTML from page
        if response.status_code == 200:
            home = response.content.decode('utf-8') #Ayuda a transformar todos los caracteres a UTF-8
            parsed = html.fromstring(home) # Toma el contenido de HTML y tranforma en un documento especial al partir del cual se puede realziar XPATH
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            print(len(links_to_notices))
            print(links_to_notices)
        else:
            raise ValueError(f'Eror: {response.status_code}') # Eleva el error
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == '__main__':
    run()