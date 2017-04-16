#!/usr/bin/python

from os import listdir, chdir, getcwd, environ
import sys
import argparse
from datetime import date, timedelta
from random import shuffle
import requests

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dry_run', required=False, dest='dry_run', action='store_true',
                        help='See hashes that would be downloaded')
    parser.add_argument('-dir', '--directory', required=False, dest='directory', default=getcwd(),
                        help='Directory to place malware. Default is CWD')
    parser.add_argument('-c', '--count', required=False, dest='count', default=0,
                        help='Number of malware to download')
    
    return parser.parse_args()

def datespan(startDate, endDate, delta=timedelta(days=1)):
    currentDate = startDate
    while currentDate < endDate:
        yield currentDate
        currentDate += delta

def get_hashes():
    hashes = []
    for day in datespan(date(2016, 1, 1), date(2017, 1, 1)):
        url = 'http://www.malshare.com/daily/{0}/malshare_fileList.{0}.txt'.format(day.strftime('%Y-%m-%d'))
        try:
            r = requests.get(url)
            hashes += r.content.splitlines()
        except KeyboardInterrupt:
            print '\n'.join(hashes)
            print "[!] Interrupted"
            print "[*] Current scraped hashes"
            sys.exit(0)
        except requests.RequestException as e:
            print e

    # Shuffling is not optimal, but gets downloading new stuff sooner		
    return shuffle(hashes)

def dl_mal(directory, hashes, count_max):
    print "[*] Starting to download malware"

    chdir(directory)    
    files = [_file.rstrip('.exe') for _file in listdir(directory)]
    
    count = 0
    params = {
        'api_key': environ['MAL_KEY']
    }
    
    for _hash in hashes:
        if _hash in files:
            continue

        try:
            params.update({'action': 'details', 'hash': _hash})
            r = requests.get('http://malshare.com/api.php', params=params)
            _json = r.json()

            if _json['F_TYPE'] == 'PE32':
                params.update({'action': 'getfile'})
                r = requests.get('http://malshare.com/api.php', params=params)
                if 'ERROR!' in r.content:
                    print "[!] Error: API limit reached for downloads"
                    break
                with open('{}.exe'.format(_hash), 'wb') as f:
                    f.write(r.content)
                
                count += 1
                #print count
                if count == count_max:
                    break
        except KeyboardInterrupt:
            print "[!] Interrupted"
            print "[!] Last file: {}.exe MAY be currupted".format(_hash)
            sys.exit(0)
        except requests.RequestException as e:
            print e

def main():
    args = parse_args()
    hashes = get_hashes()
    if not args.dry_run:
        dl_mal(args.directory, hashes, args.count) 

    print "[*] All done!"
    sys.exit(0)

if __name__ == '__main__':
    main()
