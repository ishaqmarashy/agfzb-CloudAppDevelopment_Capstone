from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
import requests, sys

# Connects to the cloudant instance and runs the appropriate function related to the request
def main(dict):
    try:
        client = Cloudant.iam(
            account_name=dict["COUCH_USERNAME"],
            api_key=dict["IAM_API_KEY"],
            connect=True,
        )
        databaseName = "reviews"
        mydatabase = client.create_database(databaseName)
        selector=make_selector(dict)
        if valid_review:
            return push_record(mydatabase,review)
        if len(selector)>0:
            return get_matching_records(mydatabase,selector)
        else:
            return get_all_records(mydatabase)
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}
    
# Extracts the selector parameters
def make_selector(dict):
    selector={}
    if dict:
        for key, value in dict.items(): 
            if key!='IAM_API_KEY' and key!='COUCH_URL' and key!='COUCH_USERNAME':
                if key=='dealerId':
                    selector['dealership']=value
                else:
                    selector[key]=value
    return selector

# Checks for a review and validates its formatting
def valid_review(review):
    required_keys = ["id","name", "dealership", "review", "purchase", "purchase_date", "car_make", "car_model", "car_year"]
    for key in required_keys:
        if key not in review["review"]:
            return False
    return True

# Gets all the records in the database
def get_all_records(mydatabase):
    results = []
    for document in mydatabase:
        results.append(document)
    return {"result":results}

#  Gets all the records in the database matching the selector query
def get_matching_records(mydatabase,selector):
    res=mydatabase.get_query_result(selector)
    results = []
    for document in res:
        results.append(document)
    return {"result":results}

#  inserts a record in the database using parameters given through the post request
def push_record(mydatabase, review):
    res=mydatabase.create_document(review)
    return {"result": res.exists()}

# Made these variables for testing purposes 
review={
        "id": 1114,
        "name": "Upkar Lidder",
        "dealership": 15,
        "review": "Great service!",
        "purchase": False,
        "another": "field",
        "purchase_date": "02/16/2021",
        "car_make": "Audi",
        "car_model": "Car",
        "car_year": 2021 
        }
dict = {
  "IAM_API_KEY": "s9C8uG0zYUsRweN1laUVgoZgB2lWrTdGAdd3gBt3rPHS",
  "COUCH_USERNAME":"7ecbbb4a-e98c-4727-9e2a-7385639134c0-bluemix",
  "COUCH_URL": "https://7ecbbb4a-e98c-4727-9e2a-7385639134c0-bluemix.cloudantnosqldb.appdomain.cloud",
  "dealerId": 15,
  "review":review
}