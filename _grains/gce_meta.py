"""
get project and instance metadata from Google Compute Engine's metadata
service and put them into grains store
"""

import socket
import httplib

HEADERS = {'X-Google-Metadata-Request': 'True'}
BASEURL = '/computeMetadata/v1/'
TIMEOUT = 1

def __get_url(http, url, metad):
    """Recursive function to get all the nested metadata. Will walk recursively
    using the last character of the return data being / as an indication that
    it should descend
    """
    try:
        http.request('GET', url, headers=HEADERS, timeout=TIMEOUT)
        dirs = http.getresponse().read().split('\n')
        # print(url, dirs)
        for directory in dirs:
            if directory == '':
                continue
            if directory[-1] == "/":
                # print("recursing into", url, directory)
                __get_url(http, url + directory, metad)
            else:
                http.request('GET', url + directory, headers=HEADERS)
                furl = url.replace(BASEURL, '') + directory
                data = http.getresponse().read()
                # print('furl:data', furl, data)
                metad[furl] = data
    except (httplib.HTTPException, socket.error) as err:
         return dict()


def gce_metadata():
    """Setup some variables and call the recursive function with the BASEURL
    """
    try:
        http = httplib.HTTPConnection('metadata', timeout=TIMEOUT)
        metad = dict()
        __get_url(http, BASEURL, metad)
        return {'gce': metad}
    except (httplib.HTTPException, socket.error) as err:
         return dict()


if __name__ == '__main__':
    print gce_metadata()
