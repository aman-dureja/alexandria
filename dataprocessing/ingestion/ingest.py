import urllib2
import urllib
from BeautifulSoup import BeautifulSoup
import re
import subprocess

second_layer = []

def get_dirs(endpoint, dirs):
    page_source = urllib2.urlopen("http://gutenberg.readingroo.ms/" + endpoint)
    soup = BeautifulSoup(page_source)
    for link in soup.findAll('a'):
        try:
            new_dir = link.get('href')[:-1]
            int(new_dir)
            dirs.append(link.get('href'))
            # if check_leaf(endpoint) == 404:
            #     get_dirs(endpoint + new_dir + "/", dirs[dirs.index(link.get('href'))])
        except:
            pass

def check_leaf(endpoint):

    endpoint_list = endpoint.split('/')
    file_name = endpoint_list[-1] + ".txt"
    a = urllib.urlopen('http://gutenberg.readingroo.ms/' + endpoint + file_name)
    return a.getcode()

def ingest_txt(endpoint):
    top_dir = endpoint[0]
    endpoint_list = endpoint.split('/')
    second_dir = endpoint_list[4]
    file_name = second_dir + ".txt"

    subprocess.call(['./ingest.sh', top_dir, second_dir, file_name])

# specify which top level dir to ingest
dir_to_ingest = '1/0/0/0/'

get_dirs(dir_to_ingest, second_layer)

for endpoint in second_layer:
    ingest_txt(dir_to_ingest + endpoint)
