package com.scentregroup.beam;

import lombok.extern.slf4j.Slf4j;
import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.coders.SerializableCoder;
import org.apache.beam.sdk.io.gcp.bigquery.BigQueryIO;
import org.apache.beam.sdk.io.kafka.KafkaIO;
import org.apache.beam.sdk.options.PipelineOptionsFactory;
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.transforms.MapElements;
import org.apache.beam.sdk.transforms.ParDo;
import org.apache.beam.sdk.values.TypeDescriptor;
import org.apache.kafka.clients.CommonClientConfigs;
import org.apache.kafka.common.config.SaslConfigs;
import org.apache.kafka.common.config.SslConfigs;
import org.apache.kafka.common.serialization.StringSerializer;

import java.util.HashMap;
import java.util.Map;

/**
 * @author mortiz
 */
@Slf4j
public class BigQueryToKafkaPipeline {

    public static void main(String[] args) {
        Pipeline pipeline = Pipeline.create(PipelineOptionsFactory.fromArgs(args).withValidation().create());
        log.info("starting...");

        String query = System.getenv("APP_QUERY");
        String server = System.getenv("APP_SERVER");
        String topic = System.getenv("APP_TOPIC");
        String jass = System.getenv("APP_KAFKA_JAAS_SECRET");
        log.info("query: {}", query);

        Map<String, Object> kafkaProp = new HashMap();
        kafkaProp.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, "SASL_SSL");
        kafkaProp.put(CommonClientConfigs.BOOTSTRAP_SERVERS_CONFIG, server);
        kafkaProp.put(SaslConfigs.SASL_MECHANISM, "PLAIN");
        kafkaProp.put(SaslConfigs.SASL_JAAS_CONFIG, jass);
        kafkaProp.put(SslConfigs.SSL_ENDPOINT_IDENTIFICATION_ALGORITHM_CONFIG, "https");

        pipeline
                .apply("Read events from BQ",
                        BigQueryIO.readTableRows().fromQuery(query).usingStandardSql())
                .apply("TableRows to Message",
                        MapElements.into(TypeDescriptor.of(Message.class)).via(Message::fromTableRow))
                .setCoder(SerializableCoder.of(Message.class))
                .apply("Map from events",
                        ParDo.of(new DoFn<Message, String>() {
                            @ProcessElement
                            public void processElement(@Element Message input, OutputReceiver<String> outputReceiver) {
                                String message = input.getMessage();
                                //List<String> events = JsonPath.read(message, "*");
                                //events.forEach(event -> outputReceiver.output(event));
                                outputReceiver.output(message);
                            }
                        }))
                .apply(KafkaIO.<Void, String>write()
                        .withBootstrapServers(server)
                        .withTopic(topic)
                        .withValueSerializer(StringSerializer.class)
                        .withProducerConfigUpdates(kafkaProp)
                        .values())
                .getPipeline()
                .run();
    }
}
