"""
get project and instance metadata from Google Compute Engine's metadata
service and put them into grains store
"""

import httplib

HEADERS = {'X-Google-Metadata-Request': 'True'}
BASEURL = '/computeMetadata/v1/'

def __get_url(http, url, metad):
    """Recursive function to get all the nested metadata. Will walk recursively
    using the last character of the return data being / as an indication that
    it should descend
    """
    http.request('GET', url, headers=HEADERS)
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

def gce_metadata():
    """Setup some variables and call the recursive function with the BASEURL
    """
    http = httplib.HTTPConnection('metadata')
    metad = {}
    __get_url(http, BASEURL, metad)

    return {'gce': metad}

if __name__ == '__main__':
    print gce_metadata()
