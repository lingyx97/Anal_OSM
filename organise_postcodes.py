from pymongo import MongoClient
import re

def formatting_postcodes(problem_postcode):
	problem_postcode=''.join(problem_postcode.split())
	chars=list(problem_postcode)
	digits=[]
	for i in range(len(chars)):
		try:
			int(chars[i])
			digits.append(i)
		except ValueError:
			pass
	if digits!=[]:
		chars.insert(digits[-1],' ')
		formatted_postcode=''.join(chars)
	else:
		formatted_postcode=problem_postcode
	return formatted_postcode


def find_problem_postcodes(data,db=None):
	normal_district_code='^[A-Z]{1,2}\d{1,2}[A-Z]?$'
	problem_elem=[]
	for elem in data:
		#solve the lower case problem
		if elem['postcode']!=elem['postcode'].upper():
			elem['postcode']=elem['postcode'].upper()
			if db:
				db.london.update({'id':elem['_id']},{'$set':{'description.address_detail.postcode':elem['postcode']}})
		#check the format of postcodes
		parts=elem['postcode'].split(' ')
		if len(parts)>0 and re.compile(normal_district_code).match(parts[0]):
			if (len(parts)==2 and re.compile('^\d[A-Z]{2}$').match(parts[1])) or len(parts)==1:
				pass
		else:
			problem_elem.append(elem)
	return problem_elem
#query for all postcodes
client = MongoClient()
db=client.osm
data=db.london.aggregate([{'$match':{'description.address_detail':{'$exists':1}}},{'$project':{'_id':'$id','type':'$type','address':'$description.address_detail'}},{'$match':{'address.postcode':{'$exists':1}}},{'$project':{'_id':'$_id',"postcode":'$address.postcode'}}])

problem_elem=find_problem_postcodes(data,db)

for elem in problem_elem:
	elem['postcode']=formatting_postcodes(elem['postcode'])

final_problem_elems=find_problem_postcodes(problem_elem)

print(len(final_problem_elems))
print(final_problem_elems)
