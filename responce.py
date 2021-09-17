import json
import requests
import argparse
import pprint
import time


def get_json(name):
    #GET /tlds/ajax.php?cmd=search&columns=id,name,zoneid,length,idn,thedate,&ecf=name&ecv=~%25vtb%25&days=2&mode=added&_search=false&nd=1631880373670&rows=500&page=1&sidx=length&sord=asc HTTP/1.1
    i = 5
    count = 0

    r = requests.get('https://dnpedia.com/tlds/search.php/')
    for c in r.cookies:
        new_session = (c.name+'='+c.value)

    headers = dict()
    with open("headers.txt", "r") as f:
        for line in f.readlines():
            if 'Cookie' in line:
                key, new_session = line.strip('\n').split(': ')
                headers[key] = new_session
            else:
                key, value = line.strip('\n').split(': ')
                headers[key] = value

    params = {
        'cmd': 'search',
        'columns': 'id,name,zoneid,length,idn,thedate,',
        'ecf': 'name',
        'ecv': '~%'+name+'%',
        'days': '2',
        'mode': 'added',
        '_search': 'false',
        'nd': '1631880373670',
        'rows': '500',
        'page': '1',
        'sidx': 'length',
        'sord': 'asc'
    }
    while True:
        try:
            r = requests.get('https://dnpedia.com/tlds/ajax.php', headers=headers, params=params)
            if r.status_code == 503:
                r.raise_for_status()
            else:
                pprint.pprint((json.dumps(r.json())))
                break
        except requests.exceptions.HTTPError:
            count += 1
            if count < 6:
                print("oops 503 Service Unavailable")
                print('Wait', i, 'seconds!')
                time.sleep(i)
            else:
                i = 10
                print("oops 503 Service Unavailable")
                print('Wait', i, 'seconds!')
                time.sleep(i)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--domain", help="add domain here")
    args = vars(ap.parse_args())

    if args['domain']:
        get_json(name=args["domain"])