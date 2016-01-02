from pymongo import MongoClient
import re
client = MongoClient()
db=client.osm
data=db.london.aggregate([{'$match':{'description.address_detail.housenumber':{'$exists':1}}},{"$project":{'_id':'$id','housenumber':'$description.address_detail.housenumber'}}])

def valid_housenumber(housenumber,db):
	if re.compile('^(Unit|Flat)?\d*\w?((-|,)(Unit|Flat)?\d*\w?)*$').match(housenumber):
		return True
	elif re.compile('^(Unit|Flat)?\d*\w?((;|\/|&)(Unit|Flat)?\d*\w?)+$').match(housenumber):
		db.london.update({'description.address_detail.housenumber':housenumber},{'$set':{'description.address_detail.housenumber':housenumber.replace(';',',').replace('/',',').replace('&',',')}})
		return True
	elif re.compile('^[A-Za-z]{5,}$').match(housenumber):
		db.london.update({'description.address_detail.housenumber':housenumber},{'$set':{'description.address_detail.housenumber':''}})
		return True
	else:
		return False

count=0
problem_elem=[]
for elem in data:
	count+=1
	if elem['housenumber']=='':
		pass
	else:
		housenumber=''.join(elem['housenumber'].split())
		if elem['housenumber']!=housenumber:
			db.london.update({'id':elem['_id']},{'$set':{'description.address_detail.housenumber':housenumber}})	
		if not valid_housenumber(housenumber,db):
			problem_elem.append(elem)
print(count)
print(len(problem_elem))
i=0
for elem in problem_elem:
	i+=1
	print(elem)
	if i==40:
		break
