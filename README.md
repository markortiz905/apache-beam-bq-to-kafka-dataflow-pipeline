[![Build status](https://badge.buildkite.com/b5e100ec73a04a809861da57daba7834e7cc6a29f34ed1181c.svg)](https://buildkite.com/scentregroup/sg-cp-kafka-mqtt)

## 🍀 Apache Beam Bigquery To Kafka Pipeline

This pipeline provides integration from bigquery to kafka. 

### Stack
![Java](https://img.shields.io/badge/java-%2357A143.svg?style=for-the-badge&logo=java&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%2357A143.svg?style=for-the-badge&logo=docker&logoColor=white) ![kafka](https://img.shields.io/badge/kafka-%2357A143.svg?style=for-the-badge&logo=kafka&logoColor=white) ![MQTT](https://img.shields.io/badge/mqtt-%2357A143.svg?style=for-the-badge&logo=mqtt&logoColor=white) ![Shell](https://img.shields.io/badge/shell-%2357A143.svg?style=for-the-badge&logo=shell&logoColor=white)

### Configs
```
KAFKA_MQTT_BOOTSTRAP_SERVERS: ***.australia-southeast1.gcp.confluent.cloud:9092
KAFKA_MQTT_PRODUCER_SECURITY_PROTOCOL: SASL_SSL
KAFKA_MQTT_PRODUCER_SASL_MECHANISM: PLAIN
KAFKA_MQTT_PRODUCER_SASL_JAAS_CONFIG: org.apache.kafka.common.security.plain.PlainLoginModule required username="**" password="**";
```

### Vault for secrets
- ??
### Service Account
- ??
### Deployments/CICD
- This can be deployed to Google Dataflow
- Buildkite will take care of building the template.

