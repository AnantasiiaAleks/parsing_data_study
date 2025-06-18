import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
from pprint import pprint

# url = "https://www.boxofficemojo.com/intl/?ref_=bo_nb_hm_tab"
url = "https://www.boxofficemojo.com"

ua = UserAgent()

headers = {"User-Agent": ua.chrome}     # рандомный User-Agent (рандомный chrome)
params = {"ref_": "=bo_nb_hm_tab"}

session = requests.session()        # открытие сессии (нужно, чтобы прога вела себя как человек)

response = session.get(url+"/intl", params=params, headers=headers)
# print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")
print()
# test_link = soup.find("a", {"class":"a-link-normal"})
# print(test_link)

rows = soup.find_all('tr')

films = []

for row in rows[1:]:
    film = {}

    try:
        area_info = row.find("td", {"class": "mojo-field-type-area_id"}).find("a")
        # можно оставить просто find(), так как внутри только один тег
        # если нужен первый тег внутри, можно поставить find_all()[0]
        film['area'] = [area_info.getText(), url + area_info.get("href")]

        weekend_info = row.find("td", {"class": "mojo-field-type-date_interval"}).find()
        film['weekend'] = [weekend_info.getText(), url + weekend_info.get("href")]

        film['releases'] = int(row.find("td", {"class": "mojo-field-type-positive_integer"}).getText())

        try:
            fst_release_info = row.find("td", {"class": "mojo-field-type-release"}).find()
            film['fst_release'] = [fst_release_info.getText(), url + fst_release_info.get("href")]
        except:
            film['fst_release'] = None
            print("Exception with fst_release, object = ", film['fst_release'])

        try:
            distributor_info = row.find("td", {"class": "mojo-field-type-studio"}).find()
            film['distributor'] = [distributor_info.getText(), url + distributor_info.get("href")]
        except:
            film['distributor'] = None
            print("Exception with distributor, object = ", film['distributor'])

        try:
            weekend_gross_info = row.find("td", {"class": "mojo-field-type-money"}).getText()
            if weekend_gross_info != '-':
                film['weekend_gross'] = int(re.sub(r'\D+', '', weekend_gross_info))
            else:
                film['weekend_gross'] = None
        except:
            film['weekend_gross'] = None
            print("Exception with weekend_gross, object = ", film['weekend_gross'])

    except:
        print("Exception with table, tag = <th>")


    if film:
        films.append(film)

print(len(films))
pprint(films)
