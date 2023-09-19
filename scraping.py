import requests
from bs4 import BeautifulSoup

url= 'https://www.grandsgites.com'
response = requests.request('GET',url)
soup = BeautifulSoup (response.text,'html.parser')
options = soup.find("select",{"name":"choix_region"}).findAll("option")

region_links = []
for i in options:
  name = i.text
  link = i["value"];
  region_links.append({
      "region": name,
      "link": link
  })

import pandas as pd

# all gites info
houses = []

#iterate over regions and get each house main information (name and link)
for region_data in region_links:

  url_region = 'https://www.grandsgites.com/grand-gite-'+ region_data['link'] +'.htm'
  response_region = requests.request('GET',url_region)
  soup_region = BeautifulSoup (response_region.text,'html.parser')
  house_tag = soup_region.find_all('div', {'class':'t_donnees2'}) + soup_region.find_all('div', {'class':'t_donnees'})



  # iterate over each house collected
  for house in house_tag[0:2]:

      # to be completed
      # get info from main page
      house_info = {
          "region": region_data['region'],
          "house_name": house.a.text.strip(),
          "house_url": 'https://www.grandsgites.com/' + house.a.get('href')
      }

      #Get all house information from individual house page
      response_page = requests.request('GET',house_info['house_url'])
      soup_page = BeautifulSoup(response_page.text, 'html.parser')

      #Read Address
      address = soup_page.find('div', {'id':'bloc_pres_annonce'})
      house_info['address'] = list(address.children)[2].strip()

      #Read General information
      bloc = soup_page.find('div',{'id':'bloc_rubrique'})
      column = bloc.find_all('td',{'class':'col'})
      for col in column:
        house_info[col.text] = col.next_sibling.text

      #Read Prices information
      bloc_t = soup_page.find('div',{'id':'bloc_tarifs'})
      column_t = bloc_t.find_all('td',{'class':'col_t'})
      for col_t in column_t:
        house_info[col_t.text] = col_t.next_sibling.text

      #Read Equipment information
      bloc_e = soup_page.find('div',{'id':'bloc_equipements'})
      column_e = bloc_e.find_all('td',{'class':'col_eq'})
      for col_e in column_e:
        house_info[col_e.text] = col_e.next_sibling.text

      #Activities information
      bloc_act = soup_page.find('div',{'id':'bloc_activites'})
      column_act = bloc_act.find_all('td',{'class':'col_act'})
      for col_act in column_act:
        house_info[col_act.text] = col_act.next_sibling.text

      # append product_indo to products
      houses.append(house_info)

df = pd.DataFrame(houses)
df
