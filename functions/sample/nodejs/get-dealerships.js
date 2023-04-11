const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

// Connects to the cloudant instance and runs the appropriate function related to the request
function main(params) {
  return new Promise(function (resolve, reject) {
    const dbname = 'dealerships';
    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({ authenticator: authenticator });
    cloudant.setServiceUrl(params.COUCH_URL);
    const selector=makeSelector(params)
    const results =Object.keys(selector).length>0?getMatchingRecords(cloudant,dbname,selector):getAllRecords(cloudant,dbname)
    results.then((results) => {
    if (results.rows||results.docs){
      code=200
    }
    else{
      code=404
    }
    resolve({
        statusCode: code,
        headers: { "Content-Type": "application/json" },
        body: results,
      });
    });
  });
}

// Extracts the selector parameters
function makeSelector(params){
    const selector={}
    const exlusions=['IAM_API_KEY','COUCH_URL','COUCH_USERNAME','__ow_headers','__ow_method','__ow_path']
    if(params){
        for (const [key, value] of Object.entries(params)) {
            if(!exlusions.includes(key)){
                selector[key]=convertToNumber(value);
            }
        }
    }
    return selector;
}

// Gets all the records in the database
async function getAllRecords(cloudant,dbname){
    try {
        const result = await cloudant.postAllDocs({ db: dbname, includeDocs: true });
        const results = result.result;
        return results;  
      }
      catch (error) {
        const err = { error: error.message }
        return err;
      }
}

function convertToNumber(inputString) {
  const parsedInt = parseInt(inputString);
  const parsedFloat = parseFloat(inputString);

  if (!isNaN(parsedInt) && parsedInt.toString() === inputString) {
    return parsedInt;
  } else if (!isNaN(parsedFloat) && parsedFloat.toString() === inputString) {
    return parsedFloat;
  } else {
    return inputString;
  }
}

// Gets all the records in the database matching the selector query
async function getMatchingRecords(cloudant,dbname, selector) {
    try{
        const result = await cloudant.postFind({db:dbname,selector:selector})
        const results = result.result;
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
  "long": -106.3,
};

main(params).then((dealers) => console.log(dealers));