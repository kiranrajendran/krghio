import java.util.*;

import com.amazonaws.client.builder.AwsClientBuilder;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDB;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDBClientBuilder;
import com.amazonaws.services.dynamodbv2.document.DynamoDB;
import com.amazonaws.services.dynamodbv2.document.Item;
import com.amazonaws.services.dynamodbv2.document.PutItemOutcome;
import com.amazonaws.services.dynamodbv2.document.Table;
import com.amazonaws.services.dynamodbv2.document.spec.QuerySpec;
import com.amazonaws.services.dynamodbv2.document.ItemCollection;
import com.amazonaws.services.dynamodbv2.document.utils.ValueMap;
import com.amazonaws.regions.*;



public boolean processRow(StepMetaInterface smi, StepDataInterface sdi) throws KettleException 
{


	Object[] r = getRow();
	if (r == null) {
		setOutputDone();
		return false;
	}


  AmazonDynamoDB client = AmazonDynamoDBClientBuilder.defaultClient(); //.build;
	// .withRegion(Regions.US_WEST_2).build();
  DynamoDB dynamoDB = new DynamoDB(client);

  Table table = dynamoDB.getTable("servers");

  String server_name = getInputRowMeta().getString(r, getParameter("SERVERNAME"), null );
    
  QuerySpec spec = new QuerySpec()
    .withKeyConditionExpression("server_name = :v_server_name")
    .withValueMap(new ValueMap()
      .withString(":v_server_name", server_name));

  ItemCollection<QueryOutcome> items = table.query(spec);

  Iterator<Item> iterator = items.iterator();
  Item item = null;
  while (iterator.hasNext()) {
      item = (Item) iterator.next();
      logBasic(item.toJSONPretty());
    }

  
  r = createOutputRow(r, data.outputRowMeta.size());

  int index = getInputRowMeta().size();
  
  r[index++] = item == null ? null : item.getStringSet("server_name");
  r[index++] = item == null ? null : item.getStringSet("DB_HOST");
  r[index++] = item == null ? null : item.getStringSet("DB_PORT");
  r[index++] = item == null ? null : item.getStringSet("DB_SCHEMA");
  r[index++] = item == null ? null : item.getStringSet("DB_USER");
  r[index++] = item == null ? null : item.getStringSet("DB_PASS");
  
  putRow(data.outputRowMeta, r); 

   return true;
}

public boolean init(StepMetaInterface stepMetaInterface, StepDataInterface stepDataInterface) {
   if (super.init(stepMetaInterface, stepDataInterface)) {

     return true;
   }
   return false;
}
