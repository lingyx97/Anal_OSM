A. A brief overview of the dataset:
	
a. description:
--1. filename: london.osm
--2. source: https://mapzen.com/data/metro-extracts
--3. position: London (lat=50.941~51.984, lon=-1.115~0.895)
--4. reason for choice: London is the largest city in the UK
--5. size of the osm file: 2,406,119,448 bytes

b. first 10 lines:
--1. code:
			count=0
			with open('london.osm','r') as a:
				for line in a:
					count+=1
					print(line)
					if count==10:
						break
--2. output: 'first 10 lines.txt'
--3. comment: first 3 lines in the osm file are useless for the analysis, and will be ignored in the future.

B. Consider each tag separately:

a. nodes:
--1. sample lines: 'first 10 lines.txt'
--2. find possible keys in the nodes:
----i. Code:
import xml.etree.cElementTree as ET
data=set()
count=0
for _, element in ET.iterparse('london.osm'):
	if element.tag=='node':
		count+=1
		for k in element.attrib.keys():
			if k=='k':
				data.add(element.attrib['k'])
			elif k!='v':
				data.add(k)
		if count==100:
			break
print(data)
----ii. Output: {'changeset', 'timestamp', 'version', 'id', 'user', 'lat', 'lon', 'uid'}

b. ways:
--1. sample lines: 'sample ways.txt'
--2. find possible keys in the nodes:
----i. Code:
import xml.etree.cElementTree as ET
data=set()
count=0
for _, element in ET.iterparse('london.osm'):
	if element.tag=='way':
		count+=1
		for k in element.attrib.keys():
			if k=='k':
				data.add(element.attrib['k'])
			elif k!='v':
				data.add(k)
		if count==100:
			break
	else:
		element.clear()
----ii. Output: {'changeset', 'user', 'timestamp', 'id', 'version', 'uid'}

c. relations:
--1. sample lines: 'sample relations.txt'
--2. possible keys in the relations: {'user', 'version', 'id', 'uid', 'changeset', 'timestamp'}

d. comment: all three tags contain similar keys, the only major differences are about their sub-elements. Therefore a format like below will be used in the output json file:
{
	'id': int (id),
	'type': str('node'/'way'/'relation'),
	(if 'type'=='node') 'pos':[float (lat), float (lon)],
	'created':{
		"changeset": int (changeset),
            	"user": str (user),
           	"version": float (version),
            	"uid": int (uid),
            	"timestamp": str (timestamp)
	},
	description:{
		2nd-level-tag['k']:2nd-level-tag['v']
	},
	member:{
		'type':str ('node' if 2nd-level-elem.tag=='nd', 2nd-level-elem['type'] if 2nd-level-elem.tag=='member')
		'ref'=list ([int (ref)])
		(if 2nd-level-elem.tag=='member') 'role':str (role)
	},
	other keys: str (values)
}

C. Check way names:
a. get the list of all way names and their count: './find_way_name'
b. comment: some way names are repeated in different names (e.g. 'road' and 'rd'), and some need special cares (e.g. those ways with 'name' field empty). Other non-standard road names are too complicated to be organised, and therefore left as they were.
c. solution: 'organise_way_name' function in 'produce_json.py'


D. Check address:
a. postcodes:
--1. find all abnormal postcodes:
----i. Code: (after importing 'london.osm.json' into mongodb)
from pymongo import MongoClient
import re
normal_district_code='^(EC|WC|E|N|NW|SE|SW|W|BR|CR|DA|EN|HA|IG|KT|RM|SM|TW|UB|WD)\d{1,2}[A-Z]?$'
problem_code=[]
client = MongoClient()
db=client.osm
data=db.london.aggregate([{'$match':{'description.address_detail':{'$exists':1}}},{'$project':{'_id':'$id','type':'$type','address':'$description.address_detail'}},{'$match':{'address.postcode':{'$exists':1}}},{'$project':{'_id':'$_id',"postcode":'$address.postcode'}}])
for elem in data:
	parts=elem['postcode'].split(' ')
	if len(parts)==2 and re.compile(normal_district_code).match(parts[0]) and re.compile('^\d[A-Z]{2}$').match(parts[1]):
		pass
	else:
		problem_code.append(elem)
print(len(problem_code))
print(problem_code)
----ii. Comment: Firstly notice that there are 26710 out of 50709 problematic results, most of which are postcodes outside the London City. Therefore the map may include a large area around however outside London. Secondly notice that there are also many postcodes which only have the first half (e.g. E1, a valid postcode should be E1 8GP or something similar). Thirdly, some postcodes are in lower case. The first two problems are unnecessary to be solved, and the third one is easy to be solved. Therefore my codes have been changed a bit to produce a new list.
There are 177 elements in the new list, and almost all of them have spacing issue. e.g. N5 1AN has been saved as N51AN. A new function called formatting_postcodes has been introduced to solve the problem.
All 24 remaining problematic postcodes have been updated manually.
--2. solution: 'organise_postcodes.py', 'manually_change_false_postcodes.py'

b. Housenumber:
--1. find abnormal housenumbers:
----i. Code:
from pymongo import MongoClient
import re
client = MongoClient()
db=client.osm
data=db.london.aggregate([{'$match':{'description.address_detail.housenumber':{'$exists':1}}},{"$project":{'_id':'$id','housenumber':'$description.address_detail.housenumber'}}])
problem_elem=[]
count=0
for elem in data:
	count+=1
	if not re.compile('^\d+\w?').match(elem['housenumber']):
		problem_elem.append(elem)
print(count)
print(len(problem_elem))
----ii. Comment: 1229 out of 208480 housenumbers are not in the common format (some integer+one english character). Some major uncommon housenumbers are:
Ranges of housenumber (e.g. 11-28). (keep)
Single characters. (keep)
Those including prefix (e.g. Unit 3). (keep)
Housenumbers separated by ';', '/', and '&'. (will all be replaced by ',')
Random words (delete)
638 are left unformatted. (too many to be changed one by one)

E. some more details about the dataset:
a. amenity:
--1. total: 109708
--2. pipeline to count each type: aggregate([{'$match':{'description.amenity':{'$exists':1}}},{'$group':{'_id':'$description.amenity','count':{'$sum':1}}},{'$sort':{'count':-1}}])
(all other unmentioned pipelines are similar to the one above)
--3. comment on output:
about 16.4% are parking area
about 12.0% are post box
all other are below 10%
	There are 3821 restaurants with tag 'cuisine', among which Indian accounts for 20.9%, Italian accounts for 15.6%, and Chinese accounts for 9.0%. However, there are some values like 'Asian', which could be counted as Chinese, Indian or some other Asian cuisine depending on case. There are also some cuisine like: 'vegetarian_indian' which contains the word 'indian' but could not be recognised properly.
	There are 5167 places of worship with field 'religion', among which 93.6% are Christian and 2.8% are Muslim. There are 15 different kinds of religion in total, but all religions are minor compared to christian if only look at number of places of worship.
	There are 1521 banks with names in London. Three most common banks are (in descending order):　 Barclays (18.7% or more), Natwest (15.2% or more), and HSBC (12.5% or more). If consider the fact that Natwest belongs to RBS, and Lloyds Bank, TSB, Halifax, and Band of Scotland are all subsidiaries of Lloyds Banking Group, then RBS (18.0% or more) is the third most commonly seen bank in London, and Lloyds Banking Group (20.7% or more) is the largest banking group in London. Barclay becomes the second most commonly seen bank in London.

If only consider nodes:

	There are 2476 restaurants with tag 'cuisine'. 20.2% are Indian foods, 16.0% are Italian foods, and 9.1% are Chinese foods.
	There are 2181 places of worship with tag 'religion'. 93.7% are Christian, and 3.2% are Muslim. There are 11 different religions in total.
	There are 1038 banks with names in London. 20.0% are Barclays, 15.6% are Natwest, and 12.9% are HSBC. RBS and Natwest accounts for 18.8% in total, and Lloyds Banking Group accounts for 20.2%.
	There are 1534 schools, 87 colleges, 233 kindergartens, 162 hospitals, and 190 police.

If take [51.44~51.58 N, -0.23~-0.03 E] (which is London city center) instead of the Greater London, then:
	There are 1175 restaurants with tag 'cuisine'. Italian food becomes the most popular cuisine, which takes 15.5%. Indian foods drop to the second most popular, and is responsible for 12.8% of the total. Chinese foods are still third most popular, and takes a percentage of 6.8%. Notices all three percentages drop in value. Obviously cuisines are more averagely distributed in London city center.
	There are 223 places of worship with tag 'religion'. The number seems to be much less than 2181, but the area chosen is also much less (about 10% on map, but not sure without calculation). 82% are Christian, and 9.0% Muslim. Christian becomes less dominated in London city center but is still major. Number of religions decreases to 9.
	There are 301 banks with names in London city center (obviously more banks per unit area in city center than on the outskirts). 17.6% are Barclays, 16.3% are Natwest, and 14.0% are HSBC. RBS and Natwest takes 21.6% (which exceeds Barclays), and 15.9% are Lloyds Banking Group. Lloyds Banking Group seems to be much less influential in the city center than on the outskirts.
	There are 121 schools, 33 colleges, 54 kindergartens, 19 hospitals, and 23 police. Hospitals and police seem to be independent (but cannot be proved) on whether it is in city center or not, while kindergartens and colleges are more concentrated in city center and schools seem to be more concentrated on the outskirts.

b. users:
There are 12256088 documents with attribute 'created.user', among which 10705246 are nodes, 1519005 are ways, and 30921 are relations.
There are 8251 users in total. 11.3% of 12256088 documents are contributed by top 3 users, 50.0% of documents are contributed by top 32 users.
[{'$match':{'created.user':{'$exists':1}}},{'$group':{'_id':'$created.user','count':{'$sum':1}}},{'$group':{'_id':'$count','c':{'$sum':1}}},{'$sort':{'_id':-1}}]
20.8% of all users only appear once, and 50.8% of all users appear 10 times or less.
Obviously most of documents are contributed by few users. If looking at the timestamps of top contributing users, it is easy to notice that most of the documents they contribute were created in a short period of time (lots of documents produced each second). Therefore it is reasonable to guess that they have used some software to improve the map. That also explains why most users only contribute a few lines (because it is time consuming to modify the map manually).

F. ways to improve the dataset:
a. the website could add some restrictions on the format of postcodes in some major countries.
--benefits: postcodes become more likely to be correct
--drawbacks: false postcodes become more similar to correct ones, and thus more difficult to distinguish from the correct ones.
b. the map could ask for help from game players of Ingress.
--benefits: more users will participate
--drawbacks: needs permission from google
c. could develop mobile apps:
--benefits: users could add points easily whenever they see something new
--drawbacks: developing a mobile app will cost lots of money (may not be worthy)
d. whenever a new element has been added. The element could be compared with other elements of the same type. If the detail of the element is very similar (e.g. 'Lloyds Bank' and 'lloyds bank') to details of some other elements but with only a little bit difference, then send them to other users for double check.
--benefits: increase the uniformity of dataset
--drawbacks: the level of similarity is hard to decide, and thus the suggestion is difficult to fulfill.

G. other resources:
a. Google Map
b. http://deerchao.net/tutorials/regex/regex.htm
c. https://docs.mongodb.org/getting-started/python/client/
d. https://docs.mongodb.org/manual/
e. https://docs.python.org/3/
f. http://effbot.org/zone/element-iterparse.htm
