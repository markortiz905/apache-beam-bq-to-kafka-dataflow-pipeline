#!/bin/sh

echoerr() { echo "$@" 1>&2; }

deploy_dataflow_template() {
    echo "--- Building... $3"

    exec_args=" --autoscalingAlgorithm=$8 \
                   		--runner=DataflowRunner \
                   		--project=$1 \
                   		--stagingLocation=$2 \
                   		--templateLocation=$3 \
                   		--region=$4 \
                   		--subnetwork=$5 \
                   		--network=$6 \
                   		--tempLocation=$7 "

    echo "exec_args: $exec_args"
    ./gradlew clean execute -Pdataflow-runner \
    	-DmainClass=com.scentregroup.beam.BigQueryToKafkaPipeline \
    	-Dexec.args="$exec_args"

    ret=$?
    echo "status - $ret"
    if [ $ret -ne 0 ]; then
        echoerr "Failed to Build [$3]"
        exit 1
    else
        echo "Build Success [$3]"
    fi
}

deploy_dataflow_template $GCP_PROJECT $STAGING_LOCATION $TEMPLATE_LOCATION $GCP_REGION $SUBNETWORK $NETWORK $BIGQUERY_TEMPLATE_LOCATION $AUTOSCALING_ALGORITHM
