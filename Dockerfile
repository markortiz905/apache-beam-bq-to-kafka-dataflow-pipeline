#FROM gcr.io/google.com/cloudsdktool/cloud-sdk:alpine
FROM openjdk:8

RUN curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-373.0.0-linux-x86_64.tar.gz &&\
        tar -xf google-cloud-sdk-373.0.0-linux-x86_64.tar.gz && ./google-cloud-sdk/install.sh

#default values
ARG GCP_REGION=asia-southeast1
ARG GCP_PROJECT
ARG JDBC_TO_AVRO_LOCATION
ARG JDBC_TO_BQ_LOCATION
ARG GCP_STAGING_LOCATION
ARG KMS_ENC_KEY
ENV GCP_REGION $GCP_REGION
ENV GCP_PROJECT $GCP_PROJECT
ENV JDBC_TO_AVRO_LOCATION $JDBC_TO_AVRO_LOCATION
ENV JDBC_TO_BQ_LOCATION $JDBC_TO_BQ_LOCATION
ENV GCP_STAGING_LOCATION $GCP_STAGING_LOCATION
ENV KMS_ENC_KEY $KMS_ENC_KEY
ENV GOOGLE_CLOUD_CREDENTIALS /.google-credentials

ENTRYPOINT chmod +x /app/entrypoint.sh && /app/entrypoint.sh
