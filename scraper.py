import requests
import lxml.html as html
import os  # Ayuda a crear la carpeta por dia 
import datetime

from requests import status_codes

HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//text-fill[not (@class)]/a/@href'
XPATH_TITLE = '//div[@class="mb-auto"]/text-fill/span/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not (@class)]/text()'


def parse_notice(link, today):
    
    try:
        response = requests.get(link) # Get link notice
        
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                # Si en caso de que encuentre un titulo con comillas, esto lo replazará con un espacio
                title = title.replace('\"','')
                title = title.replace('¿','')
                title = title.replace('?', '')
                print(title)
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                print(summary)
                body = parsed.xpath(XPATH_BODY)
                print(body)
            except IndexError:
                return 
            
            # manejador contextual de python
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def parse_home():
    # try catch to work safe
    try:
        response = requests.get(HOME_URL) # Extract HTML from page
        if response.status_code == 200:
            home = response.content.decode('utf-8') #Ayuda a transformar todos los caracteres a UTF-8
            parsed = html.fromstring(home) # Toma el contenido de HTML y tranforma en un documento especial al partir del cual se puede realziar XPATH
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            # print(len(links_to_notices))
            # print(links_to_notices)
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today): # Devuelve un resultado booleano si ya existe la carpeta o no
                os.mkdir(today) # Si no eciste la carpeta, la crea
            
            for link in links_to_notices:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}') # Eleva el error
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == '__main__':
    run()