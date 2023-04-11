import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **params):
    try:
        if not 'api_key' in params:
            response = requests.get(url,params=params,  headers={'Content-Type': 'application/json'})
        else:
            api_key=params['api_key']
            del params['api_key']
            response = requests.get(url,params=params,  headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', api_key))
        status_code = response.status_code
        # print(f"{url} with status {status_code}")
        json_data = json.loads(response.text)
        # print("res: ", json_data, response, params,status_code)
        return json_data
    except requests.exceptions.RequestException as e:
        print("Network exception occurred: {}".format(str(e)))
        return None

# Create a `post_request` to make HTTP POST requests
def post_request(url, json_payload, **params): 
    response = requests.post(url, params=params, json=json_payload)
    return response


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **params):
    results = []
    json_result = get_request(url, **params)
    
    if json_result:
        if 'rows' in json_result:
            dealers = json_result["rows"]
        elif 'docs' in json_result:
            dealers = json_result["docs"]
        else:
            return results

        for dealer in dealers:
            if 'doc' in dealer:
                dealer_doc = dealer["doc"]
            else :
                dealer_doc=dealer
            dealer_obj = CarDealer(
                address=dealer_doc.get("address"),
                city=dealer_doc.get("city"),
                full_name=dealer_doc.get("full_name"),
                id=dealer_doc.get("id"),
                lat=dealer_doc.get("lat"),
                long=dealer_doc.get("long"),
                short_name=dealer_doc.get("short_name"),
                st=dealer_doc.get("st"),
                state=dealer_doc.get("state"),
                zip=dealer_doc.get("zip")
            )
            results.append(dealer_obj)
            
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf (url, **params):
    results = []
    reviews = get_request(url,**params)
    if len(reviews)>0:
        for dealer_review_doc in reviews:
            sentiment = analyze_review_sentiments(dealer_review_doc.get("review"))
            dealer_review = DealerReview(
                dealership=dealer_review_doc.get("dealership"),
                name=dealer_review_doc.get("name"),
                purchase=dealer_review_doc.get("purchase"),
                review=dealer_review_doc.get("review"),
                purchase_date=dealer_review_doc.get("purchase_date"),
                car_make=dealer_review_doc.get("car_make"),
                car_model=dealer_review_doc.get("car_model"),
                car_year=dealer_review_doc.get("car_year"),
                sentiment=sentiment,
                id=dealer_review_doc.get("id")
            )
            results.append(dealer_review)
    return results

def get_dealer_by_id_from_cf(url, dealerId):
    params={'id':dealerId }
    dealership = get_dealers_from_cf(url,**params)
    return dealership
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealerreview):
    url=''
    version='2022-04-07'
    api_key=''
    authenticator = IAMAuthenticator(api_key) 
    natural_language_understanding = NaturalLanguageUnderstandingV1(
    version=version,
    authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response=''
    try:
        response = natural_language_understanding.analyze(text=dealerreview, features=Features(sentiment={})).get_result()
        sentiment=response['sentiment']['document']['label']
    except:
        sentiment='Neutral'
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
    return sentiment.capitalize()



