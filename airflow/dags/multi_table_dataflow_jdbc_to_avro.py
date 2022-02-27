import os, datetime, time, json, pytz
from airflow import DAG
from airflow import models
from airflow.operators.dummy_operator import DummyOperator
#from hooks.custombigquery import CustomBigQueryHook
#from airflow.contrib.operators.dataflow_operator import DataflowTemplateOperator
#custom dataflow plugin
from dataflow_plugins.dataflow_operator import DataflowTemplateOperator
from common_functions.pagerduty_incident import dag_failure_on_callback
from airflow.utils.dates import days_ago
from operators.bq_logging.DagLogStatus import BQDagLog
from airflow.contrib.operators.ssh_operator import SSHOperator

JOB_NAME='dataflow'
TEMPLATE_PATH='gs://scg-udp-lake-dev/dataflow_temp/templates/JdbcToAvro'
REGION='australia-southeast1'
ZONE='australia-southeast1-b'
PROJECT='scg-udp-etl-dev'
BUCKET='scg-udp-lake-dev/dataflow_temp'
batch_start_task = "log_start"
yesterday = datetime.datetime.combine(
    datetime.datetime.today() - datetime.timedelta(1),
    datetime.datetime.min.time())

LOW="2021040400"
HIGH="2021040600"

default_args = {
    'start_date': yesterday,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=1),
    'dataflow_default_options': {
        'project': PROJECT,
        'region': REGION,
        'zone': ZONE,
        'tempLocation': 'gs://{}/develop'.format(BUCKET),
        'stagingLocation': 'gs://{}/develop/staging/'.format(BUCKET),
        #'serviceAccountEmail': 'composer@scg-udp-etl-dev.iam.gserviceaccount.com',
        'tempLocation': 'gs://scg-udp-lake-dev/develop/dataflow_temp',
        'subnetwork': 'https://www.googleapis.com/compute/v1/projects/scg-net-stg-0/regions/australia-southeast1/subnetworks/udp-etl-dev-0',
        'network': 'scg-net-stg-0',
        'ipConfiguration': 'WORKER_IP_UNSPECIFIED',
        'bypassTempDirValidation': False,
        'additionalExperiments': [],
        'numberOfWorkerHarnessThreads': 1000,
        'numWorkers': 4,
        'autoscalingAlgorithm': 'NONE',
        'machineType': 'n1-standard-16'
    }
}

dataflow_pipeline_param = [
    {
        "jobName": "miranda",
        "template": "gs://scg-udp-lake-dev/dataflow_temp/templates/multi_table_jdbc_to_avro_develop_latest",
        "parameters": {
            "connectionURL": "jdbc:sqlserver://10.32.9.95:1433;databaseName=Miranda_2017_Q4_PARK_DB;",
            "tableNames": "APMCashBalance,APMCurrentCashBalance,CCMovements,ContractParkerMovements," +
                          "Customers,EntriesExits,ExtCardSystemMovements,MonetaryMovements,OpenParkingTrans," +
                          "PaidExcessTimes,ParkingMovements,ParkingTransPartialRates,ParkingTransWithoutTurnover," +
                          "PaymentWithSkiDataValueCard,PaymentWithValidationProviders,PaystationCashBalance," +
                          "RevenueCashPayments,RevenueCCPayments,RevenueCreditEntriesIssued," +
                          "RevenueCreditEntriesRedeemed,RevenueInvoicePayments,RevenueParkingTrans,RevenueSales",
            "username": "dwdev",
            "password": "dwdev",
            "output": "gs://scg-udp-lake-parking-pi-dev/develop/miranda",
            "queryParallelism": "10",
            "splitColumn": "Time",
            "fetchSize": "10000",
            "lowWaterMark": LOW,
            "highWaterMark": HIGH,
            "tableNamesWithoutTime": "Customers,APMCurrentCashBalance,OpenParkingTrans",
            "driverClassName": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
        }
    },
    {
        "jobName": "belconnen",
        "template": "gs://scg-udp-lake-dev/dataflow_temp/templates/multi_table_jdbc_to_avro_develop_latest",
        "parameters": {
            "connectionURL": "jdbc:sqlserver://10.8.33.250:1433;databaseName=PARK_DB;",
            "tableNames": "APMCashBalance,APMCurrentCashBalance,CCMovements,ContractParkerMovements," +
                          "Customers,EntriesExits,ExtCardSystemMovements,MonetaryMovements,OpenParkingTrans," +
                          "PaidExcessTimes,ParkingMovements,ParkingTransPartialRates,ParkingTransWithoutTurnover," +
                          "PaymentWithSkiDataValueCard,PaymentWithValidationProviders,PaystationCashBalance," +
                          "RevenueCashPayments,RevenueCCPayments,RevenueCreditEntriesIssued," +
                          "RevenueCreditEntriesRedeemed,RevenueInvoicePayments,RevenueParkingTrans,RevenueSales",
            "username": "online",
            "password": "B3lc0nn3n",
            "output": "gs://scg-udp-lake-parking-pi-dev/develop/belconnen",
            "queryParallelism": "10",
            "splitColumn": "Time",
            "fetchSize": "10000",
            "lowWaterMark": LOW,
            "highWaterMark": HIGH,
            "tableNamesWithoutTime": "Customers,APMCurrentCashBalance,OpenParkingTrans",
            "driverClassName": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
        }
    },
    {
        "jobName": "bondi_junction",
        "template": "gs://scg-udp-lake-dev/dataflow_temp/templates/multi_table_jdbc_to_avro_develop_latest",
        "parameters": {
            "connectionURL": "jdbc:sqlserver://10.8.12.250:1433;databaseName=PARK_DB;",
            "tableNames": "APMCashBalance,APMCurrentCashBalance,CCMovements,ContractParkerMovements," +
                          "Customers,EntriesExits,ExtCardSystemMovements,MonetaryMovements,OpenParkingTrans," +
                          "PaidExcessTimes,ParkingMovements,ParkingTransPartialRates,ParkingTransWithoutTurnover," +
                          "PaymentWithSkiDataValueCard,PaymentWithValidationProviders,PaystationCashBalance," +
                          "RevenueCashPayments,RevenueCCPayments,RevenueCreditEntriesIssued," +
                          "RevenueCreditEntriesRedeemed,RevenueInvoicePayments,RevenueParkingTrans,RevenueSales",
            "username": "online",
            "password": "wfbondi123",
            "output": "gs://scg-udp-lake-parking-pi-dev/develop/bondi_junction",
            "queryParallelism": "10",
            "splitColumn": "Time",
            "fetchSize": "10000",
            "lowWaterMark": LOW,
            "highWaterMark": HIGH,
            "tableNamesWithoutTime": "Customers,APMCurrentCashBalance,OpenParkingTrans",
            "driverClassName": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
        }
    },
    {
        "jobName": "carousel",
        "template": "gs://scg-udp-lake-dev/dataflow_temp/templates/multi_table_jdbc_to_avro_develop_latest",
        "parameters": {
            "connectionURL": "jdbc:sqlserver://10.41.156.250:1433;databaseName=PARK_DB;",
            "tableNames": "APMCashBalance,APMCurrentCashBalance,CCMovements,ContractParkerMovements," +
                          "Customers,EntriesExits,ExtCardSystemMovements,MonetaryMovements,OpenParkingTrans," +
                          "PaidExcessTimes,ParkingMovements,ParkingTransPartialRates,ParkingTransWithoutTurnover," +
                          "PaymentWithSkiDataValueCard,PaymentWithValidationProviders,PaystationCashBalance," +
                          "RevenueCashPayments,RevenueCCPayments,RevenueCreditEntriesIssued," +
                          "RevenueCreditEntriesRedeemed,RevenueInvoicePayments,RevenueParkingTrans,RevenueSales",
            "username": "Online",
            "password": "yGoZxDY5X",
            "output": "gs://scg-udp-lake-parking-pi-dev/develop/carousel",
            "queryParallelism": "10",
            "splitColumn": "Time",
            "fetchSize": "10000",
            "lowWaterMark": LOW,
            "highWaterMark": HIGH,
            "tableNamesWithoutTime": "Customers,APMCurrentCashBalance,OpenParkingTrans",
            "driverClassName": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
        }
    },
    {
        "jobName": "chatswood",
        "template": "gs://scg-udp-lake-dev/dataflow_temp/templates/multi_table_jdbc_to_avro_develop_latest",
        "parameters": {
            "connectionURL": "jdbc:sqlserver://10.8.215.250:1433;databaseName=PARK_DB;",
            "tableNames": "APMCashBalance,APMCurrentCashBalance,CCMovements,ContractParkerMovements," +
                          "Customers,EntriesExits,ExtCardSystemMovements,MonetaryMovements,OpenParkingTrans," +
                          "PaidExcessTimes,ParkingMovements,ParkingTransPartialRates,ParkingTransWithoutTurnover," +
                          "PaymentWithSkiDataValueCard,PaymentWithValidationProviders,PaystationCashBalance," +
                          "RevenueCashPayments,RevenueCCPayments,RevenueCreditEntriesIssued," +
                          "RevenueCreditEntriesRedeemed,RevenueInvoicePayments,RevenueParkingTrans,RevenueSales",
            "username": "Parkuser",
            "password": "dZ44UHQ2",
            "output": "gs://scg-udp-lake-parking-pi-dev/develop/chatswood",
            "queryParallelism": "10",
            "splitColumn": "Time",
            "fetchSize": "10000",
            "lowWaterMark": LOW,
            "highWaterMark": HIGH,
            "tableNamesWithoutTime": "Customers,APMCurrentCashBalance,OpenParkingTrans",
            "driverClassName": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
        }
    },
    {
        "jobName": "chermside",
        "template": "gs://scg-udp-lake-dev/dataflow_temp/templates/multi_table_jdbc_to_avro_develop_latest",
        "parameters": {
            "connectionURL": "jdbc:sqlserver://10.8.106.250:1433;databaseName=PARK_DB;",
            "tableNames": "APMCashBalance,APMCurrentCashBalance,CCMovements,ContractParkerMovements," +
                          "Customers,EntriesExits,ExtCardSystemMovements,MonetaryMovements,OpenParkingTrans," +
                          "PaidExcessTimes,ParkingMovements,ParkingTransPartialRates,ParkingTransWithoutTurnover," +
                          "PaymentWithSkiDataValueCard,PaymentWithValidationProviders,PaystationCashBalance," +
                          "RevenueCashPayments,RevenueCCPayments,RevenueCreditEntriesIssued," +
                          "RevenueCreditEntriesRedeemed,RevenueInvoicePayments,RevenueParkingTrans,RevenueSales",
            "username": "Online",
            "password": "NZ6zwUF4",
            "output": "gs://scg-udp-lake-parking-pi-dev/develop/chermside",
            "queryParallelism": "10",
            "splitColumn": "Time",
            "fetchSize": "10000",
            "lowWaterMark": LOW,
            "highWaterMark": HIGH,
            "tableNamesWithoutTime": "Customers,APMCurrentCashBalance,OpenParkingTrans",
            "driverClassName": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
        }
    },
    {
        "jobName": "coomera",
        "template": "gs://scg-udp-lake-dev/dataflow_temp/templates/multi_table_jdbc_to_avro_develop_latest",
        "parameters": {
            "connectionURL": "jdbc:sqlserver://10.41.172.250:1433;databaseName=PARK_DB;",
            "tableNames": "APMCashBalance,APMCurrentCashBalance,CCMovements,ContractParkerMovements," +
                          "Customers,EntriesExits,ExtCardSystemMovements,MonetaryMovements,OpenParkingTrans," +
                          "PaidExcessTimes,ParkingMovements,ParkingTransPartialRates,ParkingTransWithoutTurnover," +
                          "PaymentWithSkiDataValueCard,PaymentWithValidationProviders,PaystationCashBalance," +
                          "RevenueCashPayments,RevenueCCPayments,RevenueCreditEntriesIssued," +
                          "RevenueCreditEntriesRedeemed,RevenueInvoicePayments,RevenueParkingTrans,RevenueSales",
            "username": "Online",
            "password": "fi0g2l398snZ",
            "output": "gs://scg-udp-lake-parking-pi-dev/develop/coomera",
            "queryParallelism": "10",
            "splitColumn": "Time",
            "fetchSize": "10000",
            "lowWaterMark": LOW,
            "highWaterMark": HIGH,
            "tableNamesWithoutTime": "Customers,APMCurrentCashBalance,OpenParkingTrans",
            "driverClassName": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
        }
    },
    {
        "jobName": "doncaster",
        "template": "gs://scg-udp-lake-dev/dataflow_temp/templates/multi_table_jdbc_to_avro_develop_latest",
        "parameters": {
            "connectionURL": "jdbc:sqlserver://10.8.160.250:1433;databaseName=PARK_DB;",
            "tableNames": "APMCashBalance,APMCurrentCashBalance,CCMovements,ContractParkerMovements," +
                          "Customers,EntriesExits,ExtCardSystemMovements,MonetaryMovements,OpenParkingTrans," +
                          "PaidExcessTimes,ParkingMovements,ParkingTransPartialRates,ParkingTransWithoutTurnover," +
                          "PaymentWithSkiDataValueCard,PaymentWithValidationProviders,PaystationCashBalance," +
                          "RevenueCashPayments,RevenueCCPayments,RevenueCreditEntriesIssued," +
                          "RevenueCreditEntriesRedeemed,RevenueInvoicePayments,RevenueParkingTrans,RevenueSales",
            "username": "online",
            "password": "Sc3ntr3DBAcc$ss",
            "output": "gs://scg-udp-lake-parking-pi-dev/develop/doncaster",
            "queryParallelism": "10",
            "splitColumn": "Time",
            "fetchSize": "10000",
            "lowWaterMark": LOW,
            "highWaterMark": HIGH,
            "tableNamesWithoutTime": "Customers,APMCurrentCashBalance,OpenParkingTrans",
            "driverClassName": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
        }
    },
    {
        "jobName": "eastgardens",
        "template": "gs://scg-udp-lake-dev/dataflow_temp/templates/multi_table_jdbc_to_avro_develop_latest",
        "parameters": {
            "connectionURL": "jdbc:sqlserver://10.40.76.250:1433;databaseName=PARK_DB;",
            "tableNames": "APMCashBalance,APMCurrentCashBalance,CCMovements,ContractParkerMovements," +
                          "Customers,EntriesExits,ExtCardSystemMovements,MonetaryMovements,OpenParkingTrans," +
                          "PaidExcessTimes,ParkingMovements,ParkingTransPartialRates,ParkingTransWithoutTurnover," +
                          "PaymentWithSkiDataValueCard,PaymentWithValidationProviders,PaystationCashBalance," +
                          "RevenueCashPayments,RevenueCCPayments,RevenueCreditEntriesIssued," +
                          "RevenueCreditEntriesRedeemed,RevenueInvoicePayments,RevenueParkingTrans,RevenueSales",
            "username": "online",
            "password": "07OhRUA+",
            "output": "gs://scg-udp-lake-parking-pi-dev/develop/eastgardens",
            "queryParallelism": "10",
            "splitColumn": "Time",
            "fetchSize": "10000",
            "lowWaterMark": LOW,
            "highWaterMark": HIGH,
            "tableNamesWithoutTime": "Customers,APMCurrentCashBalance,OpenParkingTrans",
            "driverClassName": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
        }
    },
    {
        "jobName": "geelong",
        "template": "gs://scg-udp-lake-dev/dataflow_temp/templates/multi_table_jdbc_to_avro_develop_latest",
        "parameters": {
            "connectionURL": "jdbc:sqlserver://10.32.9.232:52513;databaseName=master;",
            "tableNames": "APMCashBalance,APMCurrentCashBalance,CCMovements,ContractParkerMovements," +
                          "Customers,EntriesExits,ExtCardSystemMovements,MonetaryMovements,OpenParkingTrans," +
                          "PaidExcessTimes,ParkingMovements,ParkingTransPartialRates,ParkingTransWithoutTurnover," +
                          "PaymentWithSkiDataValueCard,PaymentWithValidationProviders,PaystationCashBalance," +
                          "RevenueCashPayments,RevenueCCPayments,RevenueCreditEntriesIssued," +
                          "RevenueCreditEntriesRedeemed,RevenueInvoicePayments,RevenueParkingTrans,RevenueSales",
            "username": "dwdev",
            "password": "dwbeteam",
            "output": "gs://scg-udp-lake-parking-pi-dev/develop/geelong",
            "queryParallelism": "10",
            "splitColumn": "Time",
            "fetchSize": "10000",
            "lowWaterMark": LOW,
            "highWaterMark": HIGH,
            "tableNamesWithoutTime": "Customers,APMCurrentCashBalance,OpenParkingTrans",
            "driverClassName": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
        }
    },
    {
        "jobName": "hurstville",
        "template": "gs://scg-udp-lake-dev/dataflow_temp/templates/multi_table_jdbc_to_avro_develop_latest",
        "parameters": {
            "connectionURL": "jdbc:sqlserver://10.40.52.250:1433;databaseName=PARK_DB;",
            "tableNames": "APMCashBalance,APMCurrentCashBalance,CCMovements,ContractParkerMovements," +
                          "Customers,EntriesExits,ExtCardSystemMovements,MonetaryMovements,OpenParkingTrans," +
                          "PaidExcessTimes,ParkingMovements,ParkingTransPartialRates,ParkingTransWithoutTurnover," +
                          "PaymentWithSkiDataValueCard,PaymentWithValidationProviders,PaystationCashBalance," +
                          "RevenueCashPayments,RevenueCCPayments,RevenueCreditEntriesIssued," +
                          "RevenueCreditEntriesRedeemed,RevenueInvoicePayments,RevenueParkingTrans,RevenueSales",
            "username": "online",
            "password": "3ox5Z2IGib",
            "output": "gs://scg-udp-lake-parking-pi-dev/develop/hurstville",
            "queryParallelism": "10",
            "splitColumn": "Time",
            "fetchSize": "10000",
            "lowWaterMark": LOW,
            "highWaterMark": HIGH,
            "tableNamesWithoutTime": "Customers,APMCurrentCashBalance,OpenParkingTrans",
            "driverClassName": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
        }
    },
    {
        "jobName": "kotara",
        "template": "gs://scg-udp-lake-dev/dataflow_temp/templates/multi_table_jdbc_to_avro_develop_latest",
        "parameters": {
            "connectionURL": "jdbc:sqlserver://10.32.9.232:52513;databaseName=master;",
            "tableNames": "APMCashBalance,APMCurrentCashBalance,CCMovements,ContractParkerMovements," +
                          "Customers,EntriesExits,ExtCardSystemMovements,MonetaryMovements,OpenParkingTrans," +
                          "PaidExcessTimes,ParkingMovements,ParkingTransPartialRates,ParkingTransWithoutTurnover," +
                          "PaymentWithSkiDataValueCard,PaymentWithValidationProviders,PaystationCashBalance," +
                          "RevenueCashPayments,RevenueCCPayments,RevenueCreditEntriesIssued," +
                          "RevenueCreditEntriesRedeemed,RevenueInvoicePayments,RevenueParkingTrans,RevenueSales",
            "username": "dwdev",
            "password": "dwbeteam",
            "output": "gs://scg-udp-lake-parking-pi-dev/develop/kotara",
            "queryParallelism": "10",
            "splitColumn": "Time",
            "fetchSize": "10000",
            "lowWaterMark": LOW,
            "highWaterMark": HIGH,
            "tableNamesWithoutTime": "Customers,APMCurrentCashBalance,OpenParkingTrans",
            "driverClassName": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
        }
    },
    {
        "jobName": "liverpool",
        "template": "gs://scg-udp-lake-dev/dataflow_temp/templates/multi_table_jdbc_to_avro_develop_latest",
        "parameters": {
            "connectionURL": "jdbc:sqlserver://10.32.9.232:52513;databaseName=master;",
            "tableNames": "APMCashBalance,APMCurrentCashBalance,CCMovements,ContractParkerMovements," +
                          "Customers,EntriesExits,ExtCardSystemMovements,MonetaryMovements,OpenParkingTrans," +
                          "PaidExcessTimes,ParkingMovements,ParkingTransPartialRates,ParkingTransWithoutTurnover," +
                          "PaymentWithSkiDataValueCard,PaymentWithValidationProviders,PaystationCashBalance," +
                          "RevenueCashPayments,RevenueCCPayments,RevenueCreditEntriesIssued," +
                          "RevenueCreditEntriesRedeemed,RevenueInvoicePayments,RevenueParkingTrans,RevenueSales",
            "username": "dwdev",
            "password": "dwbeteam",
            "output": "gs://scg-udp-lake-parking-pi-dev/develop/liverpool",
            "queryParallelism": "10",
            "splitColumn": "Time",
            "fetchSize": "10000",
            "lowWaterMark": LOW,
            "highWaterMark": HIGH,
            "tableNamesWithoutTime": "Customers,APMCurrentCashBalance,OpenParkingTrans",
            "driverClassName": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
        }
    },
    {
        "jobName": "miranda_master",
        "template": "gs://scg-udp-lake-dev/dataflow_temp/templates/multi_table_jdbc_to_avro_develop_latest",
        "parameters": {
            "connectionURL": "jdbc:sqlserver://10.8.72.250:1433;databaseName=PARK_DB;",
            "tableNames": "APMCashBalance,APMCurrentCashBalance,CCMovements,ContractParkerMovements," +
                          "Customers,EntriesExits,ExtCardSystemMovements,MonetaryMovements,OpenParkingTrans," +
                          "PaidExcessTimes,ParkingMovements,ParkingTransPartialRates,ParkingTransWithoutTurnover," +
                          "PaymentWithSkiDataValueCard,PaymentWithValidationProviders,PaystationCashBalance," +
                          "RevenueCashPayments,RevenueCCPayments,RevenueCreditEntriesIssued," +
                          "RevenueCreditEntriesRedeemed,RevenueInvoicePayments,RevenueParkingTrans,RevenueSales",
            "username": "ONLINE",
            "password": "$centr3gr0up",
            "output": "gs://scg-udp-lake-parking-pi-dev/develop/miranda-master",
            "queryParallelism": "10",
            "splitColumn": "Time",
            "fetchSize": "10000",
            "lowWaterMark": LOW,
            "highWaterMark": HIGH,
            "tableNamesWithoutTime": "Customers,APMCurrentCashBalance,OpenParkingTrans",
            "driverClassName": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
        }
    },
    {
        "jobName": "north_lakes",
        "template": "gs://scg-udp-lake-dev/dataflow_temp/templates/multi_table_jdbc_to_avro_develop_latest",
        "parameters": {
            "connectionURL": "jdbc:sqlserver://10.40.180.250:1433;databaseName=PARK_DB;",
            "tableNames": "APMCashBalance,APMCurrentCashBalance,CCMovements,ContractParkerMovements," +
                          "Customers,EntriesExits,ExtCardSystemMovements,MonetaryMovements,OpenParkingTrans," +
                          "PaidExcessTimes,ParkingMovements,ParkingTransPartialRates,ParkingTransWithoutTurnover," +
                          "PaymentWithSkiDataValueCard,PaymentWithValidationProviders,PaystationCashBalance," +
                          "RevenueCashPayments,RevenueCCPayments,RevenueCreditEntriesIssued," +
                          "RevenueCreditEntriesRedeemed,RevenueInvoicePayments,RevenueParkingTrans,RevenueSales",
            "username": "online",
            "password": "KcT1u0R9s9",
            "output": "gs://scg-udp-lake-parking-pi-dev/develop/north-lakes",
            "queryParallelism": "10",
            "splitColumn": "Time",
            "fetchSize": "10000",
            "lowWaterMark": LOW,
            "highWaterMark": HIGH,
            "tableNamesWithoutTime": "Customers,APMCurrentCashBalance,OpenParkingTrans",
            "driverClassName": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
        }
    },
    {
        "jobName": "parramatta",
        "template": "gs://scg-udp-lake-dev/dataflow_temp/templates/multi_table_jdbc_to_avro_develop_latest",
        "parameters": {
            "connectionURL": "jdbc:sqlserver://10.40.140.250:1433;databaseName=PARK_DB;",
            "tableNames": "APMCashBalance,APMCurrentCashBalance,CCMovements,ContractParkerMovements," +
                          "Customers,EntriesExits,ExtCardSystemMovements,MonetaryMovements,OpenParkingTrans," +
                          "PaidExcessTimes,ParkingMovements,ParkingTransPartialRates,ParkingTransWithoutTurnover," +
                          "PaymentWithSkiDataValueCard,PaymentWithValidationProviders,PaystationCashBalance," +
                          "RevenueCashPayments,RevenueCCPayments,RevenueCreditEntriesIssued," +
                          "RevenueCreditEntriesRedeemed,RevenueInvoicePayments,RevenueParkingTrans,RevenueSales",
            "username": "online",
            "password": "r^B6B$8qVy",
            "output": "gs://scg-udp-lake-parking-pi-dev/develop/parramatta",
            "queryParallelism": "10",
            "splitColumn": "Time",
            "fetchSize": "10000",
            "lowWaterMark": LOW,
            "highWaterMark": HIGH,
            "tableNamesWithoutTime": "Customers,APMCurrentCashBalance,OpenParkingTrans",
            "driverClassName": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
        }
    },
    {
        "jobName": "penrith",
        "template": "gs://scg-udp-lake-dev/dataflow_temp/templates/multi_table_jdbc_to_avro_develop_latest",
        "parameters": {
            "connectionURL": "jdbc:sqlserver://10.40.148.250:1433;databaseName=PARK_DB;",
            "tableNames": "APMCashBalance,APMCurrentCashBalance,CCMovements,ContractParkerMovements," +
                          "Customers,EntriesExits,ExtCardSystemMovements,MonetaryMovements,OpenParkingTrans," +
                          "PaidExcessTimes,ParkingMovements,ParkingTransPartialRates,ParkingTransWithoutTurnover," +
                          "PaymentWithSkiDataValueCard,PaymentWithValidationProviders,PaystationCashBalance," +
                          "RevenueCashPayments,RevenueCCPayments,RevenueCreditEntriesIssued," +
                          "RevenueCreditEntriesRedeemed,RevenueInvoicePayments,RevenueParkingTrans,RevenueSales",
            "username": "Parkuser",
            "password": "KDCrGdR3ya",
            "output": "gs://scg-udp-lake-parking-pi-dev/develop/penrith",
            "queryParallelism": "10",
            "splitColumn": "Time",
            "fetchSize": "10000",
            "lowWaterMark": LOW,
            "highWaterMark": HIGH,
            "tableNamesWithoutTime": "Customers,APMCurrentCashBalance,OpenParkingTrans",
            "driverClassName": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
        }
    },
    {
        "jobName": "southland",
        "template": "gs://scg-udp-lake-dev/dataflow_temp/templates/multi_table_jdbc_to_avro_develop_latest",
        "parameters": {
            "connectionURL": "jdbc:sqlserver://10.40.35.250:1433;databaseName=PARK_DB;",
            "tableNames": "APMCashBalance,APMCurrentCashBalance,CCMovements,ContractParkerMovements," +
                          "Customers,EntriesExits,ExtCardSystemMovements,MonetaryMovements,OpenParkingTrans," +
                          "PaidExcessTimes,ParkingMovements,ParkingTransPartialRates,ParkingTransWithoutTurnover," +
                          "PaymentWithSkiDataValueCard,PaymentWithValidationProviders,PaystationCashBalance," +
                          "RevenueCashPayments,RevenueCCPayments,RevenueCreditEntriesIssued," +
                          "RevenueCreditEntriesRedeemed,RevenueInvoicePayments,RevenueParkingTrans,RevenueSales",
            "username": "Parkuser",
            "password": "Cxu5Rtqw",
            "output": "gs://scg-udp-lake-parking-pi-dev/develop/penrith",
            "queryParallelism": "10",
            "splitColumn": "Time",
            "fetchSize": "10000",
            "lowWaterMark": LOW,
            "highWaterMark": HIGH,
            "tableNamesWithoutTime": "Customers,APMCurrentCashBalance,OpenParkingTrans",
            "driverClassName": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
        }
    },
    {
        "jobName": "sydney",
        "template": "gs://scg-udp-lake-dev/dataflow_temp/templates/multi_table_jdbc_to_avro_develop_latest",
        "parameters": {
            "connectionURL": "jdbc:sqlserver://10.77.254.200:1433;databaseName=PARK_DB;",
            "tableNames": "APMCashBalance,APMCurrentCashBalance,CCMovements,ContractParkerMovements," +
                          "Customers,EntriesExits,ExtCardSystemMovements,MonetaryMovements,OpenParkingTrans," +
                          "PaidExcessTimes,ParkingMovements,ParkingTransPartialRates,ParkingTransWithoutTurnover," +
                          "PaymentWithSkiDataValueCard,PaymentWithValidationProviders,PaystationCashBalance," +
                          "RevenueCashPayments,RevenueCCPayments,RevenueCreditEntriesIssued," +
                          "RevenueCreditEntriesRedeemed,RevenueInvoicePayments,RevenueParkingTrans,RevenueSales",
            "username": "Onlineuser",
            "password": "XyeUgP2mvA",
            "output": "gs://scg-udp-lake-parking-pi-dev/develop/sydney",
            "queryParallelism": "10",
            "splitColumn": "Time",
            "fetchSize": "10000",
            "lowWaterMark": LOW,
            "highWaterMark": HIGH,
            "tableNamesWithoutTime": "Customers,APMCurrentCashBalance,OpenParkingTrans",
            "driverClassName": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
        }
    },
    {
        "jobName": "newmarket",
        "template": "gs://scg-udp-lake-dev/dataflow_temp/templates/multi_table_jdbc_to_avro_develop_latest",
        "parameters": {
            "connectionURL": "jdbc:sqlserver://10.48.137.201:1433;databaseName=PARK_DB;",
            "tableNames": "APMCashBalance,APMCurrentCashBalance,CCMovements,ContractParkerMovements," +
                          "Customers,EntriesExits,ExtCardSystemMovements,MonetaryMovements,OpenParkingTrans," +
                          "PaidExcessTimes,ParkingMovements,ParkingTransPartialRates,ParkingTransWithoutTurnover," +
                          "PaymentWithSkiDataValueCard,PaymentWithValidationProviders,PaystationCashBalance," +
                          "RevenueCashPayments,RevenueCCPayments,RevenueCreditEntriesIssued," +
                          "RevenueCreditEntriesRedeemed,RevenueInvoicePayments,RevenueParkingTrans,RevenueSales",
            "username": "Onlineuser",
            "password": "Qm06W2JXaf",
            "output": "gs://scg-udp-lake-parking-pi-dev/develop/newmarket",
            "queryParallelism": "10",
            "splitColumn": "Time",
            "fetchSize": "10000",
            "lowWaterMark": LOW,
            "highWaterMark": HIGH,
            "tableNamesWithoutTime": "Customers,APMCurrentCashBalance,OpenParkingTrans",
            "driverClassName": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
        }
    },
    {
        "jobName": "woden",
        "template": "gs://scg-udp-lake-dev/dataflow_temp/templates/multi_table_jdbc_to_avro_develop_latest",
        "parameters": {
            "connectionURL": "jdbc:sqlserver://10.32.9.232:52513;database=master;",
            "tableNames": "APMCashBalance,APMCurrentCashBalance,CCMovements,ContractParkerMovements,Customers,EntriesExits,ExtCardSystemMovements,MonetaryMovements,OpenParkingTrans,PaidExcessTimes,ParkingMovements,ParkingTransPartialRates,ParkingTransWithoutTurnover,PaymentWithSkiDataValueCard,PaymentWithValidationProviders,PaystationCashBalance,RevenueCashPayments,RevenueCCPayments,RevenueCreditEntriesIssued,RevenueCreditEntriesRedeemed,RevenueInvoicePayments,RevenueParkingTrans,RevenueSales,SystemEvents,Customers_PI,ContractParkerMovements_PI",
            "username": "dwdev",
            "password": "dwbeteam",
            "output": "gs://scg-udp-lake-parking-pi-dev/develop/woden",
            "queryParallelism": "10",
            "splitColumn": "Time",
            "fetchSize": "10000",
            "lowWaterMark": LOW,
            "highWaterMark": HIGH,
            "tableNamesWithoutTime": "Customers,APMCurrentCashBalance,OpenParkingTrans",
            "driverClassName": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
        }
    }
]

# Define a DAG (directed acyclic graph) of tasks.
# Any task you create within the context manager is automatically added to the
# DAG object.
with models.DAG(
    # The id you will see in the DAG airflow page
    "datalake_multitable_jdbc_to_avro_develop",
    default_args=default_args,
    # The interval with which to schedule the DAG
    schedule_interval=None,  # Override to match your needs
) as dag:

    log_start = BQDagLog(
        task_id=batch_start_task,
        default_args=default_args,
        dag=dag,
        mode="START"
    )

    log_end = BQDagLog(
        task_id="log_end",
        default_args=default_args,
        dag=dag,
        trigger_rule="all_done",
        mode="END",
        batch_start_task="log_start"
    )

    # Split lists
    def split_list(input_list, size):
        return (input_list[i::size] for i in range(size))

    # Generate Centre Task List
    def generate_centre_tasks():
        task_list = []
        for centres in dataflow_pipeline_param:
            data_dict = dict(centres)
            center_start_task = "start_job_" + str(data_dict["jobName"])

            df_task = DataflowTemplateOperator(
                task_id=center_start_task,
                jobName=data_dict["jobName"],
                template=data_dict["template"],
                parameters=data_dict["parameters"],
                batch_start_task="log_start",
                dag=dag,
                external_params=[]
            )

            task_list.append([df_task])
        return(task_list)

    task_list = generate_centre_tasks()
    task_list_split = []
    # Spit tasks based on concurrency
    if len(task_list) > 0:
        task_list_split = list(split_list(task_list, 20))
    else:
        raise AirflowException("No tasks were created")

    log_start
    for each_list in task_list_split:
        prev = log_start
        for tasks in each_list:
            prev >> tasks[0]
            tasks[0] >> log_end
