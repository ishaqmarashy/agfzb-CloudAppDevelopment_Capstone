const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

// Connects to the cloudant instance and runs the appropriate function related to the request
async function main(params) {
  const dbname = 'dealerships';
  const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
  const cloudant = CloudantV1.newInstance({
    authenticator: authenticator
  });
  cloudant.setServiceUrl(params.COUCH_URL);
  const selector=makeSelector(params)
  if (Object.keys(selector).length>=1){
    return getMatchingRecords(cloudant,dbname,selector)
  }
  else{
    return getAllRecords(cloudant,dbname)
  }
}

// Extracts the selector parameters
function makeSelector(params){
    const selector={}
    if(params){
        for (const [key, value] of Object.entries(params)) {
            if(key!=='IAM_API_KEY' && key!=='COUCH_URL'&& key!=='COUCH_USERNAME'){
                selector[key]=value;
            }
        }
    }
    return selector;
}

// Gets all the records in the database
async function getAllRecords(cloudant,dbname){
    try {
        const result = await cloudant.postAllDocs({ db: dbname, includeDocs: true, limit: 2 });
        const results = { result: result.result.rows };
        return results;  
      }
      catch (error) {
        const err = { error: error.message }
        return err;
      }
}

// Gets all the records in the database matching the selector query
async function getMatchingRecords(cloudant,dbname, selector) {
    try{
        const result = await cloudant.postFind({db:dbname,selector:selector})
        const results = { result: result.result };
        return results;  
    }
    catch (error) {
    const err = { error: error.message }
    return err;
  }
 }
 
//  Made these variables for testing purposes 
const params = {
  "IAM_API_KEY": "s9C8uG0zYUsRweN1laUVgoZgB2lWrTdGAdd3gBt3rPHS",
  "COUCH_USERNAME":"7ecbbb4a-e98c-4727-9e2a-7385639134c0-bluemix",
  "COUCH_URL": "https://7ecbbb4a-e98c-4727-9e2a-7385639134c0-bluemix.cloudantnosqldb.appdomain.cloud",
  "state":"California"
};

