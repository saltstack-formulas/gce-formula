# get tags from gce metadata and put them into grains store

import httplib
import json

def gce_ext_ip():

    h = httplib.HTTPConnection('metadata')
    h.request('GET',
        '/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip',
        ' ', {'X-Google-Metadata-Request': 'True'})
    rsp = h.getresponse()
    #h.close()
    return {'pub_fqdn_ipv4': rsp.read()}

def gce_tags():
    h = httplib.HTTPConnection('metadata')
    h.request('GET',
        '/computeMetadata/v1/instance/tags', ' ', {'X-Google-Metadata-Request': 'True'})
    rsp = h.getresponse()
    tags = json.loads(rsp.read())
    #h.close()
    return {'tags': tags, 'roles': tags}

if __name__ == '__main__':
    print gce_ext_ip()
    print gce_tags()
