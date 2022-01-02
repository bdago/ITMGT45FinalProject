import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

user_db = client["users"]

organizations_db = client["organizations"]

# User
def check_user(username):
    users_coll = user_db["users"]
    user = users_coll.find_one({"username":username})
    return user

def check_email(email):
    users_coll = user_db["users"]
    user = users_coll.find_one({"email":email})
    return user

def create_user(userinput):
    users_coll = user_db["users"]
    users_coll.insert_one(userinput)

def update_user(email,fullname,username,password):
    users_coll = user_db["users"]
    users_coll.update_one({'fullname': fullname}, {'$set':{'password':password, 'email': email, 'username': username}})
# Organizations
def get_orgs():
    org_list = []

    orgs_coll = organizations_db['organizations']
    
    for b in orgs_coll.find({}):
        org_list.append(b)

    return org_list
          
def get_org(code):
    orgs_coll = organizations_db['organizations'] 
    org = orgs_coll.find_one({"code": code})
    return org

# Update password
def update_password(username, password):
    user_db.update_one({'username':username}, {'$set':{'password':password}})





