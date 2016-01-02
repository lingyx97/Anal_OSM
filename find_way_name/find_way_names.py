import xml.etree.cElementTree as ET
data=set()
count=0
def find_way_name(element,data):
	if element.tag=='way':
		for child in element:
			if 'k' in child.attrib.keys():
				if child.attrib['k']=='name':
					data.add(child.attrib['v'].split('(')[0].split(' ')[-1].lower())
	return data
# some process to avoid memoryError
context=ET.iterparse('london.osm',events=('start','end'))
context=iter(context)
event, root=next(context)
for event, element in context:
	if event=='end':
		data=find_way_name(element,data)
		root.clear()
#save to file to avoid too much memory consumption
with open('way_name.txt','w',encoding='utf_8') as f:
	f.write(str(len(data)))
	f.write('\n')
	for elem in data:
		f.write(elem)
		f.write('\n')
	f.close()
