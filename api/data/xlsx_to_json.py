import json
import pandas


excel_data_fragment = pandas.read_excel('data.xlsx', sheet_name='Blatt1')
data = excel_data_fragment.to_json()
data = json.loads(data)

items = []

for p in data['Ort / Ville / Città']:
    zip_code = data['Postleitzahl / Code Postal / Codice Postale'][p]
    city = data['Ort / Ville / Città'][p]
    canton = data['Abkürzung / Abréviation / Abbreviazione'][p]

    items.append({
    	'zip': zip_code,
    	'city': city,
    	'canton': canton
    })

with open('data.json', 'w') as outfile:
    json.dump(items, outfile)
