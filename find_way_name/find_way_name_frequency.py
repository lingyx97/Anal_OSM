import operator
import xml.etree.cElementTree as ET

data={}
with open('way_name.txt','r',encoding='utf_8') as f:
	for line in f:
		data[line.strip()]=0
context=ET.iterparse('london.osm',events=('start','end'))
context=iter(context)
event, root=next(context)
for event, element in context:
	if event=='end':
		if element.tag=='way':
			for child in element:
				if 'k' in child.attrib.keys():
					if child.attrib['k']=='name':
						data[child.attrib['v'].split('(')[0].split(' ')[-1].lower()]+=1
		root.clear()
mydict = sorted(data.items(), key=operator.itemgetter(1), reverse=True)
with open('way_name_with_frequency.txt','w',encoding='utf_8') as f:
	for k, v in mydict:
		row='{0}:{1}'.format(k,v)
		f.write(row)
		f.write('\n')
	f.close()