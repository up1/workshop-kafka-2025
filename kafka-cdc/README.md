# Workshop
* Source => MySQL
* Change Data Capture with [Debezium](https://debezium.io/)
* Event store with apache Kafka 4.0
  * Single node
* Destination => Standard Output
* Working with Docker
  * [Kafka image](https://github.com/apache/kafka/tree/trunk/docker/examples/docker-compose-files)

## 1. Start Kafka broker
* Single node

```
$docker compose up -d broker

$docker compose ps
NAME      IMAGE                COMMAND                  SERVICE   CREATED         STATUS         PORTS
broker    apache/kafka:4.0.0   "/__cacert_entrypoin…"   broker    5 seconds ago   Up 5 seconds   0.0.0.0:9092->9092/tcp
```

## 2. Start [Kafka UI](https://github.com/provectus/kafka-ui)
```
$docker compose up -d kafka-ui
```

Access to web ui
* http://localhost:8080/
  * Add cluster
    * Bootstrap Servers=broker
    * Port=19092

## 3. Start MySQL server
* Data source for Debezium
```
$docker compose up -d mysql

$docker compose ps
NAME                IMAGE                           COMMAND                  SERVICE    CREATED              STATUS              PORTS
broker              apache/kafka:4.0.0              "/__cacert_entrypoin…"   broker     About a minute ago   Up About a minute   0.0.0.0:9092->9092/tcp
kafka-cdc-mysql-1   mysql:9                         "docker-entrypoint.s…"   mysql      About a minute ago   Up About a minute   0.0.0.0:3306->3306/tcp, 33060/tcp
kafka-ui            provectuslabs/kafka-ui:latest   "/bin/sh -c 'java --…"   kafka-ui   About a minute ago   Up About a minute   0.0.0.0:8080->8080/tcp
```

## 4. Start CDC with Debezium
```
$docker compose up -d connect

$docker compose ps
NAME                  IMAGE                           COMMAND                  SERVICE    CREATED          STATUS          PORTS
broker                apache/kafka:4.0.0              "/__cacert_entrypoin…"   broker     3 minutes ago    Up 3 minutes    0.0.0.0:9092->9092/tcp
kafka-cdc-connect-1   quay.io/debezium/connect:3.1    "/docker-entrypoint.…"   connect    32 seconds ago   Up 31 seconds   8778/tcp, 0.0.0.0:8083->8083/tcp, 9092/tcp
kafka-cdc-mysql-1     mysql:9                         "docker-entrypoint.s…"   mysql      3 minutes ago    Up 3 minutes    0.0.0.0:3306->3306/tcp, 33060/tcp
kafka-ui              provectuslabs/kafka-ui:latest   "/bin/sh -c 'java --…"   kafka-ui   3 minutes ago    Up 3 minutes    0.0.0.0:8080->8080/tcp
```

## 5. Deploy Debezium connector
* Use postman collection in folder `/postman`

Configuration of connector
```
{
    "name": "mysql-connector",
    "config": {
    "tasks.max": "1",
    "connector.class": "io.debezium.connector.mysql.MySqlConnector",
    "database.hostname": "mysql",
    "database.port": "3306",
    "database.user": "root",
    "database.password": "debezium",
    "database.include.list": "inventory",
    "table.include.list": "inventory.orders",
    "database.server.id": "1",
    "message.key.columns": "inventory.orders:order_number",
    "schema.history.internal.kafka.bootstrap.servers": "broker:19092",
    "schema.history.internal.kafka.topic": "dbz.inventory.history",
    "snapshot.mode": "schema_only",
    "topic.prefix": "dbz.inventory.v2",
    "transforms": "unwrap",
    "transforms.unwrap.delete.handling.mode": "rewrite",
    "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState"
  }
}
```

See result in Kafka UI
* http://localhost:8080/

## 6. Try to produce data into MySQL database
```
$docker compose exec -it mysql bash

$mysql -umysqluser -pmysqlpw
$show databases;
$use inventory;
$show tables;
$select * from orders;

# Insert new data
$INSERT INTO `inventory`.`orders`(`customer_id`,`order_date`,`total_amount`)VALUES(100,'2025-04-28',100);

```

## 7. Try to consume data from Kafka
```
$docker compose exec -it broker bash

# List all topics
$/opt/kafka/bin/kafka-topics.sh --bootstrap-server broker:9092 --list
```

New topic
* dbz.inventory.v2.inventory.orders


Consumer data from topic
```
$/opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server broker:9092 --topic dbz.inventory.v2.inventory.orders --from-beginning

```

## 8. Start Elastic search 8
```
$docker compose up -d elasticsearch
```

Check status of server
* http://localhost:9200/

## 9. Start consumer with Python
* [Kakfa python](https://github.com/dpkp/kafka-python)
```
$docker compose build consumer
$docker compose up -d consumer
```

## 10. Try to produce data into MySQL database
* Check result in elasticsearch
  * http://localhost:9200/
  * List of indices
    * http://localhost:9200/_cat/indices
  * Search data in index=orders
    * http://localhost:9200/orders/_search

## Delete all resources
```
$docker compose down
$docker volume prune
```

## Reference websites
* [Examples for running Debezium](https://github.com/debezium/debezium-examples)