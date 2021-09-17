import json
import requests
import argparse
import pprint
import time


def get_json(name):
    # GET /tlds/ajax.php?cmd=search&columns=id,name,zoneid,length,idn,thedate,&ecf=name&ecv=~%25vtb%25&days=2&mode=added&_search=false&nd=1631880373670&rows=500&page=1&sidx=length&sord=asc HTTP/1.1
    headers = dict()
    with open("headers", "r") as f:
        for line in f.readlines():
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
            print("oops 503 Service Unavailable")
            print('Wait 5 seconds!')
            time.sleep(5)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--domain", help="add domain here")
    args = vars(ap.parse_args())

    if args['domain']:
        get_json(name=args["domain"])
