import json
from kafka import KafkaConsumer
import psycopg2
import logging

consumer = KafkaConsumer(
    "cdc-using-debezium-topic.public.User",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

conn = psycopg2.connect(
    dbname="cdc-using-debezium",
    user="postgres",
    password="123",
    host="localhost",
    port="5443",
)


def execute_merge(cursor, id, name):
    merge_query = """
        MERGE INTO scd2_user AS target
        USING (
            SELECT %(id)s AS id, %(name)s AS name
        ) AS source
        ON target.id = source.id
        WHEN MATCHED THEN
            UPDATE SET 
                end_date = current_timestamp - interval '1 second',
                current_flag = FALSE
    """
    insert_query = """
        INSERT INTO scd2_user (id, name, start_date, end_date, current_flag)
        VALUES (%(id)s, %(name)s, current_timestamp, NULL, TRUE);
    """

    cursor.execute(merge_query, {"id": id, "name": name})
    cursor.execute(insert_query, {"id": id, "name": name})


try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            print("Waiting...")
        else:
            cursor = conn.cursor()
            for msg in consumer:
                # Extract relevant data from the Kafka message
                payload = msg.value["payload"]
                id = payload["after"]["id"]
                name = payload["after"]["name"]
                logging.info(f"Processing message: id={id}, name={name}")
                # Execute the MERGE SQL statement
                execute_merge(cursor, id, name)
                logging.info("Transaction committed successfully.")
                # Commit the transaction
                conn.commit()
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
