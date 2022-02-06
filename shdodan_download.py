# -*- coding: utf8 -*-
import requests, json
from datetime import datetime

time_sleep = 10

apikey = 'put your apikey here'
shodan_api = 'https://api.shodan.io'

max_result = 211600 # max count result to download
num_result = 0

query = 'put your query here'

def search_shodan(query, page):
    try:
        request = requests.get(shodan_api + '/shodan/host/search?query="laravel_session"', params={'key': apikey, 'page': page, 'minify': True}, timeout=60)
        resp = request.text
        return resp.encode('utf8')
    except Exception as err:
        try:
            ask_retry = input(f'hit enter to retry with query {query} page {page}')
            search_shodan(query, page)
        except KeyboardInterrupt:
            return False
        except EOFError:
            exit('Bye')
        

def save_result(json_data):
    global num_result
    ip_str = json_data['ip_str']
    port   = json_data['port']
    hostname = json_data['hostnames']
    real_protocol = json_data['_shodan']['module']

    # priv data
    if 'hostname' in json_data['_shodan']['options']:
        real_url = json_data['_shodan']['options']['hostname']
        final_data = real_protocol + '://' + str(real_url)
        num_result += 1
        open('site_result.txt', 'a').write(final_data + '\n')
    else:
        final_data = real_protocol + '://' + ip_str + ':' + str(port)
        num_result += 1
        open('ip_result.txt', 'a').write(final_data + '\n')

min_page = 80
while True:
    if num_result > max_result:
        break
    else:
        results = search_shodan(query, page=min_page)
        if results:
            try:
                loadjs = json.loads(results)

                # debug info
                now = datetime.now().strftime('%H:%M:%S')
                result_in_page = len(loadjs['matches'])
                print(f'[{now}][{result_in_page}][{num_result}/{max_result}] {query} - {min_page}')
                for json_data in loadjs['matches']:
                    save_result(json_data)
            except Exception as err:
                print(str(results))
                print(str(err) + ' - ERROR CANT LOADS JSON RESPON')
                x = input('input R for reload')
                if x == 'R' or x == 'r':
                    continue
    min_page += 1
