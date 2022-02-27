#!/bin/sh

echoerr() { echo "$@" 1>&2; }

deploy_dataflow_template() {
    echo "--- Building... $3"

    ./gradlew clean execute -Pdataflow-runner \
    	-DmainClass=com.scentregroup.beam.JsonPropJdbcToAvroPipeline \
    	-Dexec.args=" --autoscalingAlgorithm=THROUGHPUT_BASED \
    		--runner=DataflowRunner \
    		--project=$1 \
    		--stagingLocation=$2 \
    		--templateLocation=$3 \
    		--region=$4 \
    		--subnetwork=https://www.googleapis.com/compute/v1/projects/scg-net-stg-0/regions/australia-southeast1/subnetworks/udp-etl-dev-0 \
    		--network=scg-net-stg-0 \
    		--jsonSourcePath=gs://sample-project/parking-test/parking36.json \
    		--lowWaterMark=2017-10-01T00:55:29 \
    		--highWaterMark=2017-10-03T00:55:29 \
    		--batchId=test-batch-id \
    		--kmsEncryptionKey=$5 \
    		--attemptNumber=1"

    ret=$?
    echo "status - $ret"
    if [ $ret -ne 0 ]; then
        echoerr "Failed to Build [$3]"
        exit 1
    else
        echo "Build Success [$3]"
    fi
}

deploy_dataflow_template $GCP_PROJECT $GCP_STAGING_LOCATION $JDBC_TO_AVRO_LOCATION $GCP_REGION $KMS_ENC_KEY
deploy_dataflow_template $GCP_PROJECT $GCP_STAGING_LOCATION $JDBC_TO_BQ_LOCATION $GCP_REGION $KMS_ENC_KEY
