# get tags from gce metadata and put them into grains store

import socket
import httplib
import json

TIMEOUT = 1

def gce_ext_ip():

    try:
        h = httplib.HTTPConnection('metadata', timeout=TIMEOUT)
        h.request('GET',
            '/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip',
            ' ', {'X-Google-Metadata-Request': 'True'})
        rsp = h.getresponse()
        #h.close()
        return {'pub_fqdn_ipv4': rsp.read()}
    except (httplib.HTTPException, socket.error) as err:
         return dict()

def gce_tags():
    try:
        h = httplib.HTTPConnection('metadata', timeout=TIMEOUT)
        h.request('GET',
            '/computeMetadata/v1/instance/tags', ' ', {'X-Google-Metadata-Request': 'True'})
        rsp = h.getresponse()
        tags = json.loads(rsp.read())
        #h.close()
        return {'tags': tags, 'roles': tags}
    except (httplib.HTTPException, socket.error) as err:
         return dict()

if __name__ == '__main__':
    print gce_ext_ip()
    print gce_tags()
