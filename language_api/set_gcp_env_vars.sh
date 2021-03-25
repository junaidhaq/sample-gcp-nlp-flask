#!/bin/bash
export PROJECT_ID=$(gcloud config get-value core/project)

# Check if populated
if [[ -z "$PROJECT_ID" ]]
then
        export PROJECT_ID="sample-gcp-nlp-flask"
fi
echo PROJECT_ID = $PROJECT_ID

# This should have been done manual already (one off)
# gcloud iam service-accounts keys create ~/key.json --iam-account example@${PROJECT_ID}.iam.gserviceaccount.com

export GOOGLE_APPLICATION_CREDENTIALS="/home/${USER}/key.json"
echo GOOGLE_APPLICATION_CREDENTIALS = $GOOGLE_APPLICATION_CREDENTIALS

echo "Finished"
