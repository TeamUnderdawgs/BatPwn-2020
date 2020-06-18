const { Client } = require("@elastic/elasticsearch");
                   require("dotenv").config();
const elasticUrl = process.env.ELASTIC_URL || "http://206.189.137.227:9200/";
const esclient   = new Client({ node: elasticUrl });
const index      = "flag";
const type       = "flag";

async function createIndex(index) {
  try {
    await esclient.indices.create({ index });
    console.log(`Created index ${index}`);
  } catch (err) {
    console.error(`An error occurred while creating the index ${index}:`);
    console.error(err);
  }
}

async function setFlagMapping () {
  try {
    const schema = {
      flag: {
        type: "text" 
      }
    };
  
    await esclient.indices.putMapping({ 
      index, 
      type,
      include_type_name: true,
      body: { 
        properties: schema 
      } 
    })
    
    console.log("Quotes mapping created successfully");
  
  } catch (err) {
    console.error("An error occurred while setting the quotes mapping:");
    console.error(err);
  }
}

async function checkConnection() {
  return new Promise(async (resolve) => {
    console.log("Checking connection to ElasticSearch...");
    let isConnected = false;
    while (!isConnected) {
      try {
        await esclient.cluster.health({});
        console.log("Successfully connected to ElasticSearch");
        isConnected = true;

      } catch (_) {
      }
    }
    resolve(true);
  });
}
module.exports = {
  esclient,
  setFlagMapping,
  checkConnection,
  createIndex,
  index,
  type
};