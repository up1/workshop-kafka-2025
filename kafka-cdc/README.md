# Workshop
* Source => MySQL
* Change Data Capture with Kafka-Connect
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

## 2. Start Kafka UI
```
$docker compose up -d kafka-ui
```

Access to web ui
* http://localhost:8080/
  * Add cluster
    * Bootstrap Servers=broker
    * Port=19092