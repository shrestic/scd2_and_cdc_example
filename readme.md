1. Run docker-compose up
2. Set up and create User table and SCD2 user table
3. Run curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" http://127.0.0.1:8083/connectors/ -d @debezium.json
4. Run to check
    - Run docker exec cdc-using-debezium-kafka /opt/bitnami/kafka/bin/kafka-console-consumer.sh --bootstrap-server cdc-using-debezium-kafka:29092 --topic cdc-using-debezium-topic.public.User --from-beginning | jq '.'
    or
    - Run docker run --tty \
  --network cdc-using-debezium-network \
  confluentinc/cp-kafkacat:7.0.14 \
  kafkacat -b cdc-using-debezium-kafka:29092 \
  -t cdc-using-debezium-topic.public.User
5. Run consumer script using python
6.Check data in the sdcd2 user table


##An important note: We might not get the previous data (within the before key) when executing an UPDATE or a DELETE query if PostgreSQL’s REPLICA IDENTITY is DEFAULT. So, we need to change it to FULL by executing the below query.