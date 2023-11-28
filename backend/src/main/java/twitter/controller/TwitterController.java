/*
Author: Wei Ge - 1074198
        Han Wang - 1041260 
        YanBei Jiang - 1087029
        Yiwen Zhang - 1002781
        Zening Zhang - 1078374
*/
package twitter.controller;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import org.springframework.context.annotation.PropertySource;
import org.springframework.core.io.ClassPathResource;
import org.springframework.scheduling.annotation.Async;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.*;
import java.util.*;
import java.util.concurrent.*;

import com.alibaba.fastjson.JSONObject;

import javax.sql.rowset.spi.SyncResolver;

@RestController
public class TwitterController {

    // database configuration
    String dbConfiguration = "db_config.properties";
    String username;
    String password;
    String node0;
    String node1;
    String node2;
    String[] nodeLists;
    String port;
    String oldDBName;
    String newDBName;
    String proDBName;
    String cacheTweetsDBName;
    String cacheAurinDBName;

    /**
     * The initialzier which set up the database configuration
     */
    public TwitterController() {
        try {
            // read the configuration file .properties
            ClassPathResource source = new ClassPathResource(dbConfiguration);
            InputStream file = source.getInputStream();
            Properties properties = new Properties();
            properties.load(new BufferedReader(new InputStreamReader(file, "UTF-8")));

            // assign configuration
            username = (String)properties.get("username");
            password = (String)properties.get("password");
            node0 = (String)properties.get("node0");
            node1 = (String)properties.get("node1");
            node2 = (String)properties.get("node2");
            nodeLists = new String[]{node0, node1, node2};
            port = (String)properties.get("port");
            oldDBName = (String)properties.get("old_db_name");
            newDBName = (String)properties.get("new_db_name");
            proDBName = (String)properties.get("pro_db_name");
            cacheTweetsDBName = (String)properties.get("cache_tweets_db_name");
            cacheAurinDBName = (String)properties.get("cache_aurin_db_name");
        } catch (IOException e){
            System.out.println("DB Configuration does not exist");
        }
    }

    /**
     * Get the aurin dataset from the couchdb
     */
    @Async
    @RequestMapping("/data/get_aurin")
    public JSONObject getAurinData(){

        // the response body
        JSONObject respJson = new JSONObject();

        try {

            // communicate with couchdb to get all document's information
            JSONObject dataSummaryJson = communicateWithCouchDB("/_all_docs", cacheAurinDBName);

            // get the data summary
            List<JSONObject> rows = JSONArray.parseArray(JSON.toJSONString(dataSummaryJson.get("rows")), JSONObject.class);

            // get each rows according to their id
            for (int i = 0; i < rows.size(); i++) {
                // extract id from thw data summary
                String id = JSON.toJSONString(rows.get(i).get("id"));

                // get each id's detailed document
                JSONObject dataRow = communicateWithCouchDB("/" + id.replaceAll("\"", ""), cacheAurinDBName);

                // extract informations from each rows
                for (Map.Entry<String, Object> entry : dataRow.entrySet()) {
                    // filter out the default value in couchdb: _id and _rev
                    if (entry.getKey().equals("_id") || entry.getKey().equals("_rev")) {
                        continue;
                    }
                    respJson.put(entry.getKey(), entry.getValue());
                }
            }

            respJson.put("status", 200);
            return respJson;
        }

        // no available database source
        catch (Exception e){
            // re-initialize the response because 'respJson = (JSONObject) dataRow.get("data");' may cause the response to be null
            respJson = new JSONObject();
            respJson.put("status", 403);
            respJson.put("error", "No available databases");
            return respJson;
        }
    }

    /**
     * Get the tweets dataset from the couchdb
     * @return
     */
    @Async
    @RequestMapping("/data/get_tweets")
    public JSONObject getTweetsData(){
        // the response body
        JSONObject respJson = new JSONObject();

        try {
            // communicate with couchdb to get all document's information
            JSONObject dataSummaryJson = communicateWithCouchDB("/_all_docs", cacheTweetsDBName);

            // get the data summary
            List<JSONObject> rows = JSONArray.parseArray(JSON.toJSONString(dataSummaryJson.get("rows")), JSONObject.class);

            // get the newest document
            String newestId = "000000";
            // get each rows according to their id
            for (int i = 0; i < rows.size(); i++) {
                // extract id from thw data summary
                String currId = JSON.toJSONString(rows.get(i).get("id")).replaceAll("_design/", "").replaceAll("\"", "");
                // compare the newest document id
                if (Integer.valueOf(newestId) < Integer.valueOf(currId)) {
                    newestId = currId;
                }
            }

            // get the detailed content of the newest document
            JSONObject dataRow = communicateWithCouchDB("/_design/" + newestId, cacheTweetsDBName);
            // return the data
            respJson = (JSONObject) dataRow.get("data");
            respJson.put("status", 200);
            return respJson;
        }
        // no available database source
        catch (Exception e){
            // re-initialize the response because 'respJson = (JSONObject) dataRow.get("data");' may cause the response to be null
            respJson = new JSONObject();
            respJson.put("status", 403);
            respJson.put("error", "No available databases");
            return respJson;
        }
    }


    /**
     * Send request to the couchdb followed by receiving response
     * @param urlTail the url tail of request
     * @param dbName the db name be sent the request
     * @return the json format response from the couchdb
     */
    private JSONObject communicateWithCouchDB(String urlTail, String dbName){
        // response
        JSONObject respJson = null;

        // candidate node
        List<String> candidateNodes = new ArrayList<>();
        candidateNodes.add(nodeLists[0]);
        candidateNodes.add(nodeLists[1]);
        candidateNodes.add(nodeLists[2]);

        // to balance the server's load, the back-end will randomly select a node to visit
        Random random = new Random();
        int nodeIndex = random.nextInt(3);
        // get the node
        String node = candidateNodes.get(nodeIndex);
        // remove the node be used from the candidate
        candidateNodes.remove(nodeIndex);

        // try to connect the couchdb
        // if the request time exceeds the limit, change another node to try
        while (true) {

            // end the loop if getting response
            if (respJson != null){
                break;
            }
            // end the loop if there is no more nodes can be used
            if (candidateNodes.size() == 0){
                break;
            }

            // establish the task to communicate with couchdb
            String finalNode = node;
            Callable<String> task = new Callable<String>() {
                @Override
                public String call() throws Exception {
                    // generate the request
                    String url = "http://" + username + ":" + password + "@" + finalNode + ":" + port + "/" + dbName + urlTail;
                    String[] cmds = {"curl", "-X", "GET", url};
                    // send request to couchdb and get the response
                    String resp = execCurl(cmds);
                    return resp;
                }
            };

            // try to run the curl task
            ExecutorService exeservices = Executors.newSingleThreadExecutor();
            Future<String> future = exeservices.submit(task);
            try {
                // run the method
                String result = future.get(3, TimeUnit.SECONDS);
                // transfer response from String to Json
                respJson = JSON.parseObject(result);
            }
            // time exceeds, change another node to try
            catch (Exception e) {
                node = candidateNodes.get(0);
                candidateNodes.remove(node);
            }
        }

        return respJson;
    }

    /**
     * Send curl request and get response
     * @param cmds the curl request
     * @return response from server
     */
    private String execCurl(String[] cmds) {
        ProcessBuilder process = new ProcessBuilder(cmds);
        Process p;
        try {
            p = process.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));
            StringBuilder builder = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                builder.append(line);
                builder.append(System.getProperty("line.separator"));
            }
            return builder.toString();

        } catch (IOException e) {
            System.out.print("error");
            e.printStackTrace();
        }
        return null;
    }
}