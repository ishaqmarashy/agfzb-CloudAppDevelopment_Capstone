from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests

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
        if 'review' in dict:
            res=push_record(mydatabase,dict['review'])
            if res:
                code=200
            else:
                code=500
            return {
            'statusCode': code,
            'headers': { "Content-Type": "application/json" },
            'body': res,
            }
        else:
            selector=make_selector(dict)
            if len(selector)>0:
                res = get_matching_records(mydatabase,selector)
            else:
                res = get_all_records(mydatabase)
            if len(res)>0:
                code=200
            else:
                code=404
            return {
                'statusCode': code,
                'headers': { "Content-Type": "application/json" },
                'body': res,
            }
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

def convert_to_number(input_string):
    try:
        parsed_int = int(input_string)
        if str(parsed_int) == input_string:
            return parsed_int
    except ValueError:
        pass
    
    try:
        parsed_float = float(input_string)
        if str(parsed_float) == input_string:
            return parsed_float
    except ValueError:
        pass
    
    return input_string

# Extracts the selector parameters
def make_selector(dict):
    selector={}
    exlusions=['IAM_API_KEY','COUCH_URL','COUCH_USERNAME','__ow_headers','__ow_method','__ow_path']
    if dict:
        for key, value in dict.items(): 
            if key not in exlusions:
                selector[key]=convert_to_number(value)
    return selector


# Gets all the records in the database
def get_all_records(mydatabase):
    results = []
    for document in mydatabase:
        results.append(document)
    return results

#  Gets all the records in the database matching the selector query
def get_matching_records(mydatabase,selector):
    res=mydatabase.get_query_result(selector)
    results = []
    for document in res:
        results.append(document)
    return results

#  inserts a record in the database using parameters given through the post request
def push_record(mydatabase, review):
    res=mydatabase.create_document(review)
    return  res.exists()

# Made these variables for testing purposes 
review={
        "id": 1,
        "name": "Upkar Lidder",
        "dealership": 15,
        "review": "Great service!!",
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
}
print (main(dict))