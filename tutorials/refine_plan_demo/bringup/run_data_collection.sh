#!/bin/bash
# Runs the simulation 100 times with proper clean up for data collection

MONGO_CONNECTION_STRING=$1

for RUN in {0..99..1};
do
    echo "STARTING DATA COLLECTION RUN $(($RUN + 1))/100"
    source ./start_sim.sh data $MONGO_CONNECTION_STRING
    sleep 20s # Wait for everything to be properly setup before waiting
    sh ./termination_checker.sh
done
