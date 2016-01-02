#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def organise_way_name(way_name):
    prob_names={'st':'street','st.':'street','ave':'avenue','ave.':'avenue','rd':'road','rd.':'road','center':'centre','':'N/A','None':'N/A'}
    if str(way_name) in prob_names.keys():
        way_name=prob_names[str(way_name)]
    return way_name

def organise_address(addr):
    return addr

def shape_element(element):
    dictionary = {}
    dictionary['created']={}
    dictionary['member']={}
    if element.tag == "node" or element.tag == "way" or element.tag=='relation':

        #organise second level key-value pairs
        for child in element:
            if child.tag=='tag':
                if 'description' not in dictionary.keys():
                    dictionary['description']={}
                child_key=child.attrib['k']
                if problemchars.search(child_key):
                    pass
                elif child_key=='name':
                    way_name=child.attrib['v'].lower().split('(')[0].split(' ')
                    way_last_name=organise_way_name(way_name[-1])
                    way_name[0:-1].append(way_last_name)
                    dictionary['description']['name']=' '.join(way_name)
                elif child_key.split(':')[0]=='addr' and len(child_key.split(':'))>1:
                    if 'address_detail' not in dictionary['description'].keys():
                        dictionary['description']['address_detail']={}
                    dictionary['description']['address_detail'][str(child_key.split(':')[1])]=child.attrib['v']
                else:
                    dictionary['description'][child_key]=child.attrib['v']
            elif child.tag=='nd':
                if 'member' not in dictionary.keys():
                    dictionary['member']={}
                dictionary['member']['type']='node' 
                if 'ref' not in dictionary['member'].keys():
                    dictionary['member']['ref']=[]
                dictionary['member']['ref'].append(int(child.attrib['ref']))   
            elif child.tag=='member':
                if 'member' not in dictionary.keys():
                    dictionary['member']={}
                dictionary['member']['type']=child.attrib['type']
                if 'role' in child.attrib.keys():
                    dictionary['member']['role']=child.attrib['role']
                if 'ref' not in dictionary['member'].keys():
                    dictionary['member']['ref']=[]
                dictionary['member']['ref'].append(int(child.attrib['ref']))
        # organise first level key-value pairs
        for key in element.attrib.keys():
            
            if key=='timestamp' or key=='user':
                dictionary['created'][key]=element.attrib[key]
            elif key=='changeset' or key=='uid':
                dictionary['created'][key]=int(element.attrib[key])
            elif key=='version':
                dictionary['created'][key]=float(element.attrib[key])
            elif key in ['lon','lat']:
                dictionary['pos']=[float(element.attrib['lat']),float(element.attrib['lon'])]
            else:
                dictionary[key]=element.attrib[key]
        dictionary['type']=element.tag
        return dictionary
    else:
        return None


def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                    # clear the element to save memory
                    element.clear()
                else:
                    fo.write(json.dumps(el) + "\n")
                    element.clear()



if __name__ == "__main__":
    process_map('london.osm')
