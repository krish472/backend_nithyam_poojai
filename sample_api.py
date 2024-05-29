from flask import Flask , jsonify, logging, request
from flask_cors import CORS
# from pymongo import MongoClient
import pymongo
from bson import ObjectId
from bson.json_util import dumps

client = pymongo.MongoClient('mongodb://localhost:27017/')
# client = pymongo.MongoClient('mongodb+srv://krishnaveni472:Arjun_123@nithyampoojai.eeo5jdt.mongodb.net/')

db = client['vaathiyaarList']

collection=db["vaathiyaarContacts"]
poojaList = db['poojaList']
poojaDesc = db['poojaDesc']


app = Flask(__name__)
CORS(app)

@app.route('/getDetails', methods = ['GET'])
def get_data():
    listall = collection.find({})
    eachitem = list(listall)
    for item in eachitem:
        item['_id'] = str(item['_id'])
        data ={
            "code" : 100,
            "message" : "Successful",
            "allitem" : eachitem
        }
    return jsonify(data)




@app.route('/signup', methods=['POST'])
def post_data():
    signInDetails = request.get_json()
    name = signInDetails.get('name')
    age = signInDetails.get('age')
    address = signInDetails.get('address')
    contact = signInDetails.get('contact')
    area = signInDetails.get('area')
    
    if not all([name, age, address, contact, area]):
        return jsonify({"error": "Missing data"}), 400
    
    # db = mongo.db.signin_details
    finalData = {
        "name": name,
        "age": age,
        "address": address,
        "contact": contact,
        "area": area
    }
    duplicate = len(list(collection.find({"name" : finalData['name']})))
    print (duplicate)
    if  duplicate == 0:
        collection.insert_one(finalData)
        
        allData = list(collection.find({}, {'_id': 0}))  # Exclude _id field from the response
        
        data = {
            "code" : 100,
            "message": "Added to the list",
            "data": allData
        }
    
        return jsonify(data)
    else:
        return 'Duplicate found'

@app.route('/agentId' , methods=['GET'])
def agentDetail():
  agentId = request.args.get('agentId')
  agent = collection.find_one({"name": agentId})
  if agent:
        agent['_id'] = str(agent['_id'])
        return jsonify(agent)
  else:
        return jsonify({"error": "Agent not found"})

@app.route('/signin', methods=['POST'])
def signin():
    requestdata = request.get_json()
    name = requestdata.get('email')
    print (requestdata)
    item = collection.find_one({"name": name})
    print (item)
    if item:
        return get_data()
    else:
        data = {
            "code" : 101,
            "message" : 'You are not a registered member'
        }
        return jsonify(data)

@app.route('/getPoojaList' , methods=['GET'])
def get_poojaList():
    allpooja = poojaList.find()
    ind_Pooja = list(allpooja)
    for pooja in ind_Pooja:
        pooja['_id'] = str(pooja['_id'])
    data ={
        "code" : 100,
        "message" : "successful",
        "poojalist" : ind_Pooja
    }
    return jsonify(data)

@app.route('/searchPooja' , methods=['POST'])
def searchPooja():
    requestdata = request.get_json()
    print (requestdata)
    name = requestdata.get('name')    
    item = poojaList.find_one({"name" : name})
    item['_id'] = str(item['_id'])
    return jsonify(item)

@app.route('/poojaDescription', methods=['GET'])
def get_pooja_description():
    # Assuming poojaDesc is a collection object obtained from MongoDB
    pooja_description_cursor = poojaDesc.find()

    # Convert the cursor to a list of dictionaries
    ind_pooja_desc = list(pooja_description_cursor)

    # Convert ObjectId to strings if needed
    for pooja in ind_pooja_desc:
        pooja['_id'] = str(pooja['_id'])

    # Construct response data
    data = {
        "code": 100,
        "message": "successful",
        "poojaDesc": ind_pooja_desc
    }

    return jsonify(data)
@app.route('/poojaStory', methods=['GET'])
def get_poojaStory():
    poojadetailId = request.args.get('poojaId')
    print("Received request for poojaId:", poojadetailId)

    # Convert the provided poojaId to ObjectId
    try:
        poojadetailId = ObjectId(poojadetailId)
    except:
        return 'Invalid poojaId', 400

    # Query the poojaDesc collection for the specified poojaId
    poojaDetails = poojaDesc.find_one({"_id": poojadetailId})

    if poojaDetails:
        # Convert ObjectId to string
        poojaDetails['_id'] = str(poojaDetails['_id'])
        # Construct response data
        data = {
            "code": 100,
            "message": "successful",
            "poojaDesc": poojaDetails
        }
        return jsonify(data)
    else:
        return 'Pooja does not exist', 404
    
@app.route('/booking' , methods = ['POST'])
def booking():
    requestdata = request.get_json()
    print(requestdata)
    pname = requestdata['poojaName'],
    date = requestdata['bookingDate']
    time = requestdata['time']
    bookingdata = {
        "name" : pname,
        "date" : date,
        "time" : time
    }
    data = {
        "code" : 100,
        "message" :"booking Sucessful",
        "details": bookingdata
    }
    return jsonify(data)
        
if __name__ == '__main__':
    app.run(debug=True)
