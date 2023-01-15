import yadisk
import json
import os

app = yadisk.YaDisk(token="y0_AgAAAABVMeAeAAkABAAAAADZoPpcdW_KymU6SwyKRxaGwRznNyOtKDQ")

app.upload('js.json', 'data.json')
app.download('data.json', 'js.json')
number = int(input())
num1, num2, num3 = input().split('.')
new_data = {"id": number, "coords": [int(num1), int(num2), int(num3)]}
with open('js.json', encoding='utf-8') as file:
    data = json.load(file)
    data['data'].append(new_data)
    with open('js.json', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=2)
try:
    app.upload('js.json', 'data.json')
except yadisk.exceptions.PathExistsError:
    app.remove('data.json', permanently=True)
    app.upload('js.json', 'data.json')
    # os.remove('js.json')

