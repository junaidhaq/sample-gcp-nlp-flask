#!/bin/bash

echo "NOTE: make sure that you use source for this file"

export PROJECT_ID=$(gcloud config get-value core/project)

# Check if populated
if [[ -z "$PROJECT_ID" ]]
then
        export PROJECT_ID="sample-gcp-nlp-flask"
fi
echo PROJECT_ID = $PROJECT_ID

# Enable the APIs: (You can also do these through Navigation Menu -> APIs & Services)

gcloud services enable language.googleapis.com
gcloud services enable datastore.googleapis.com

# Create a Service Account to access the Google Cloud APIs when testing locally:

gcloud iam service-accounts create example \
 --display-name "sukhbir_bassi"

# Give your newly created Service Account appropriate permissions:

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
--member serviceAccount:example@${PROJECT_ID}.iam.gserviceaccount.com \
--role roles/owner

# After creating your Service Account, create a Service Account key:

gcloud iam service-accounts keys create ~/key.json --iam-account \
example@${PROJECT_ID}.iam.gserviceaccount.com

#Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to point to where you just put your Service Account key:
export GOOGLE_APPLICATION_CREDENTIALS="/home/${USER}/key.json"

echo "Start Python Virtual Environment"
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt

echo "Finished"
