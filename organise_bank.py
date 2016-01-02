from pymongo import MongoClient
client = MongoClient()
db=client.osm
data=db.london
data1=data.aggregate([{'$match':{'description.amenity':'bank','description.name':{'$exists':1}}},{'$project':{'_id':'$id','name':'$description.name'}}])
for elem in data1:
	name=elem['name'].strip()
	name=name.replace('royal bank of scotland','rbs').replace('the royal bank of scotland','rbs').replace('the rbs','rbs')
	name=name.replace('lloyds bank','lloyds').replace("lloyd's bank",'lloyds').replace("lloyd's",'lloyds')
	name=name.replace('barclays bank','barclays')
	name=name.replace('hsbc bank','hsbc')
	name=name.replace('nat west','natwest').replace('national westminster','natwest').replace('natwest bank','natwest')
	if elem['name']!=name:
		data.update({'id':elem['_id']},{'$set':{'description.name':name}})
