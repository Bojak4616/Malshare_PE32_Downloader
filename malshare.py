#!/usr/bin/python

import requests
import argparse
from os import listdir, chdir, getcwd, environ
from sys import exit


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--dry_run', required=False, dest='dry_run', action='store_true',
                        help='See hashes that would be downloaded')
	parser.add_argument('-dir', '--directory', required=False, dest='directory', default=getcwd(),
                        help='Directory to place malware. Default is CWD')
	parser.add_argument('-c', '--count', required=False, dest='count', default=0,
                        help='Number of malware to download')
	
	return parser.parse_args()


def get_hashes():
	hashes = []
	for month in xrange(1,13):
		print '[*] On month: {}'.format(month)
		for day in xrange(1,29):
			url = 'http://www.malshare.com/daily/2016-{:02d}-{:02d}/malshare_fileList.2016-{:02d}-{:02d}.txt'.format(month, day, month, day)
			try:
				r = requests.get(url)
				hashes += r.content.split('\n')
				hashes.pop()
			except KeyboardInterrupt:
				print '\n'.join(hashes)
				print "[!] Interrupted"
				print "[*] Current scraped hashes"
				exit(0)
			except requests.RequestException as e:
				print e
				pass
			
	return hashes

def dl_mal(directory, hashes, count_max):
	print "[*] Starting to download malware"
	count = 0
	chdir(directory)
	files = [_file.rstrip('.exe') for _file in listdir(directory)]
	for _hash in hashes:
		if _hash in files: continue
		try:
			r = requests.get('http://malshare.com/api.php?api_key={}&action=details&hash={}'.format(environ['MAL_KEY'], _hash))
			_json = r.json()

			if _json['F_TYPE'] == 'PE32':
				r = requests.get('http://malshare.com/api.php?api_key={}&action=getfile&hash={}'.format(environ['MAL_KEY'], _hash))
				if r.content.find('ERROR!') >= 0:
					print "[!] Error: API limit reached for downloads"
					return True
				with open('{}.exe'.format(_hash), 'wb') as FILE:
					FILE.write(r.content)
				count += 1
				#print count
				if count == count_max: return True

		except KeyboardInterrupt:
			print "[!] Interrupted"
			print "[!] Last file: {}.exe MAY be currupted".format(_hash)
			exit(0)
		except requests.RequestException as e:
                        print e
                        pass	 

def main():
	args = parse_args()
	hashes = get_hashes()
	if not args.dry_run: dl_mal(args.directory, hashes, args.count) 
	print "[*] All done!"
	exit(0)

if __name__ == '__main__':
	main()

