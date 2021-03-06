import requests
import json

name = raw_input("Name: ")

headers = {
    'Pragma': 'no-cache',
    'Origin': 'http://127.0.0.1:5000',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,es-US;q=0.8,es;q=0.6,ru-BY;q=0.4,ru;q=0.2,en;q=0.2',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Mobile Safari/537.36',
    'Content-type': 'application/json',
    'Accept': '*/*',
    'Cache-Control': 'no-cache',
    'Referer': 'http://127.0.0.1:5000/',
    'Connection': 'keep-alive',
}

data = {
"userName": "thomais",
"lessons": [
    {
        "title": "string",
        "color1": "string",
        "color2": "string",
        "steps": [
            {
                "step_description":"list",
                "step_img":"string",
                "example_img":"list",
                "ex_description":"string"
            },
            {
                "step_description":"list",
                "step_img":"string",
                "example_img":"list",
                "ex_description":"string"
            },
            {
                "step_description":"list",
                "step_img":"string",
                "example_img":"list",
                "ex_description":"string"
            }

        ]

    }
]}

response = requests.post('http://127.0.0.1:5000/addLesson', headers=headers, data=json.dumps(data))
