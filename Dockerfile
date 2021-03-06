#FROM gcr.io/google.com/cloudsdktool/cloud-sdk:alpine
FROM openjdk:8

RUN curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-373.0.0-linux-x86_64.tar.gz &&\
        tar -xf google-cloud-sdk-373.0.0-linux-x86_64.tar.gz && ./google-cloud-sdk/install.sh

#default values
ARG GCP_REGION=asia-southeast1
ARG GCP_PROJECT
ARG APP_QUERY
ARG APP_SERVER
ARG APP_TOPIC
ARG BIGQUERY_TEMPLATE_LOCATION
ARG AUTOSCALING_ALGORITHM
ARG STAGING_LOCATION
ARG TEMPLATE_LOCATION
ARG SUBNETWORK
ARG NETWORK

ENV GCP_REGION $GCP_REGION
ENV GCP_PROJECT $GCP_PROJECT
ENV APP_QUERY $APP_QUERY
ENV APP_SERVER $APP_SERVER
ENV APP_TOPIC $APP_TOPIC
ENV BIGQUERY_TEMPLATE_LOCATION $BIGQUERY_TEMPLATE_LOCATION
ENV AUTOSCALING_ALGORITHM $AUTOSCALING_ALGORITHM
ENV STAGING_LOCATION $STAGING_LOCATION
ENV TEMPLATE_LOCATION $TEMPLATE_LOCATION
ENV SUBNETWORK $SUBNETWORK
ENV NETWORK $NETWORK

ENV GOOGLE_CLOUD_CREDENTIALS /.google-credentials

ENTRYPOINT chmod +x /app/entrypoint.sh && /app/entrypoint.sh
