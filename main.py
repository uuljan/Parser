import requests
import csv
from datetime import datetime
from bs4 import BeautifulSoup
from multiprocessing import Pool


def get_html(url):
    r = requests.get(url)
    return r.text

def get_all_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    tds = soup.find('table', class_='table').find_all('td')
    links = []
    for td in tds:
        a = td.find('a').get('href')
        link = 'http://kenesh.kg' + a
        links.append(link)

    return links

def get_page_date(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        name = soup.find('h3', class_='deputy-name').text.strip()
    except:
        name = ''
    try:
        number = soup.find('p', class_='mb-10').text.strip()
    except:
        number = ''
    try:
        bio = soup.find('div', id='biography').text.strip()
    except:
        bio = ''

    data = {'name': name, 'number': number, 'bio': bio}

    return data

def write_csv(data):
    with open('deputy.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow((data['name'], data['number'], data['bio']))
        print(data['name'], data['number'], data['bio'],'parsed')

def make_all(url):
        html = get_html(url)
        data = get_page_date(html)
        write_csv(data)

def main():
    start = datetime.now()
    url = "http://www.kenesh.kg/ru/deputy/list/35"
    all_links = get_all_links(get_html(url))

    end = datetime.now()
    result = end - start
    print(str(result))


    with Pool(40) as p:
        p.map(make_all, all_links)
    end = datetime.now()

    total = end - start
    print(str(total))


if __name__=='__main__':
    main()