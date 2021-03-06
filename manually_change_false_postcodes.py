from pymongo import MongoClient
client = MongoClient()
db=client.osm
# postcodes are from google map
db.london.update({'id':'648285107'},{'$set':{'description.address_detail.postcode':'SG11 1ET'}})
db.london.update({'id':'1271588141'},{'$set':{'description.address_detail.postcode':'WD17 2UB'}})
db.london.update({'id':'1513576709'},{'$set':{'description.address_detail.postcode':'RH6 7ES'}})
db.london.update({'id':'1520009478'},{'$set':{'description.address_detail.postcode':'KT20 7LF'}})
db.london.update({'id':'2466428733'},{'$set':{'description.address_detail.postcode':'SW1W'}})
db.london.update({'id':'2711482815'},{'$set':{'description.address_detail.postcode':'SW1P 2AF'}})
db.london.update({'id':'2874761450'},{'$set':{'description.address_detail.postcode':'SG1 4LJ'}})
db.london.update({'id':'3414744922'},{'$set':{'description.address_detail.postcode':'CM7 3YG'}})
db.london.update({'id':'3714045140'},{'$set':{'description.address_detail.postcode':'SW1P 1EP'}})
db.london.update({'id':'28875926'},{'$set':{'description.address_detail.postcode':'TN23 1PJ'}})
db.london.update({'id':'47201271'},{'$set':{'description.address_detail.postcode':'SL6 8LT'}})
db.london.update({'id':'62318890'},{'$set':{'description.address_detail.postcode':'AL2 2LX'}})
db.london.update({'id':'76969932'},{'$set':{'description.address_detail.postcode':'RG6 7HT'}})
db.london.update({'id':'98977077'},{'$set':{'description.address_detail.postcode':'WC1N 1AA'}})
db.london.update({'id':'105556113'},{'$set':{'description.address_detail.postcode':'EC2V 7PG'}})
db.london.update({'id':'112564610'},{'$set':{'description.address_detail.postcode':'WC1N 3LZ'}})
db.london.update({'id':'118720806'},{'$set':{'description.address_detail.postcode':'SW1P 2AF'}})
db.london.update({'id':'161825935'},{'$set':{'description.address_detail.postcode':'SW16 6HP'}})
db.london.update({'id':'168769172'},{'$set':{'description.address_detail.postcode':'AL1 1LN'}})
db.london.update({'id':'209204539'},{'$set':{'description.address_detail.postcode':'SW18 5TR'}})
db.london.update({'id':'257092300'},{'$set':{'description.address_detail.postcode':'WC1N 1AB'}})
db.london.update({'id':'262121100'},{'$set':{'description.address_detail.postcode':'SW11 5PZ'}})
db.london.update({'id':'290143856'},{'$set':{'description.address_detail.postcode':'SE3 2PB'}})
db.london.update({'id':'291682335'},{'$set':{'description.address_detail.postcode':'GU28 0QD'}})
