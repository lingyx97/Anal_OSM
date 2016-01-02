from pymongo import MongoClient
client = MongoClient()
db=client.osm
data=db.london.aggregate([{"$match":{'description.amenity':'restaurant','description.cuisine':{'$exists':1}}},{"$project":{'_id':'$id','cuisine':'$description.cuisine'}}])

for elem in data:
	if type(elem['cuisine'])==type(list()):
		cuisine=[]
		for i in range(len(elem['cuisine'])):
			cuisine.append(elem['cuisine'][i].replace(';',',').replace('&',',').replace('_',' ').strip().lower())
		if cuisine!=elem['cuisine']:
			db.london.update({'id':elem['_id']},{'$set':{'description.cuisine':cuisine}})
	else:
		elem['cuisine']=elem['cuisine'].replace(';',',').replace('&',',').replace('_',' ').lower()
		if len(elem['cuisine'].split(','))>1:
			elem['cuisine']=elem['cuisine'].split(',')
			for i in range(len(elem['cuisine'])):
				elem['cuisine'][i]=elem['cuisine'][i].strip()
			db.london.update({'id':elem['_id']},{'$set':{'description.cuisine':elem['cuisine']}})