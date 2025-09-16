from kafka import KafkaConsumer
from elasticsearch import Elasticsearch, helpers
from datetime import datetime
import json

# es = Elasticsearch(["http://elasticsearch:9200"])

consumer = KafkaConsumer(
    "dbz.inventory.v2.inventory.orders",  # Topic name
    bootstrap_servers=["broker:19092"],
    auto_offset_reset="latest",  # Ensures reading from the latest offset if the group has no offset stored
    enable_auto_commit=True,  # Automatically commits the offset after processing
    group_id="log_consumer_group",  # Specifies the consumer group to manage offset tracking
    max_poll_records=10,  # Maximum number of messages per batch
    fetch_max_wait_ms=2000,  # Maximum wait time to form a batch (in ms)
)


def create_bulk_actions(orders):
    for order in orders:
        yield {
            "_index": "orders",
            "_source": {
                "order_number": order["payload"]["order_number"],
                "customer_id": order["payload"]["customer_id"],
                "order_date": order["payload"]["order_date"],
                "total_amount": order["payload"]["total_amount"],
            },
        }


if __name__ == "__main__":
    print("Start demo with python kafka consumer")
    try:
        print("Starting message consumption...")
        while True:

            messages = consumer.poll(timeout_ms=1000)

            # process each batch messages
            for _, records in messages.items():
                orders = [json.loads(record.value) for record in records]
                print(orders)
                # bulk_actions = create_bulk_actions(orders)
                # response = helpers.bulk(es, bulk_actions)
                # print(f"Indexed {response[0]} logs.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        consumer.close()
        print(f"Finish")