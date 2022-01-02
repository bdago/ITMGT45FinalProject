import database as db

def login(email, password):

    temp_user = db.check_email(email)
    if (temp_user == None):
        return False
    else:
        if(temp_user["password"]==password):
            return temp_user
        else:
            return False
            
