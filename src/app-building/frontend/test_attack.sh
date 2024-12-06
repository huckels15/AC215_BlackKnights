curl \
-X POST \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
https://us-east1-aiplatform.googleapis.com/ui/projects/secret-cipher-399620/locations/us-east1/endpoints/3829946445218185216:predict \
-d '{
  "instances": [
    {
      "model": "resnet",
      "attack": "fgsm",
      "epsilon": 0.2
    }
  ]
}'