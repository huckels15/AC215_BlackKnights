# curl -X POST http://127.0.0.1:8000/resnet-attack/ \
# -H "Content-Type: application/json" \
# -d '{"model": "resnet", "attack": "fgsm", "epsilon": 0.2}'

# curl -X POST http://34.57.140.84:8000/resnet-attack/ \
# -H "Content-Type: application/json" \
# -d '{"model": "resnet", "attack": "pgd", "epsilon": 0.2, "eps_step": 0.01, "max_iter": 1}'

# curl -X POST http://34.57.140.84:8000/resnet-attack/ \
# -H "Content-Type: application/json" \
# -d '{"model": "resnet", "attack": "deepfool", "max_iter": 1}'

# curl -X POST http://127.0.0.1:8000/resnet-attack/ \
# -H "Content-Type: application/json" \
# -d '{"model": "resnet", "attack": "square", "epsilon": 0.2, "max_iter": 10}'

# curl -X POST http://127.0.0.1:8000/resnet-attack/ \
# -H "Content-Type: application/json" \
# -d '{"model": "resnet", "attack": "fgsm", "epsilon": 0.2}'

########################## ALEXNET ############################

# curl -X POST http://127.0.0.1:8000/predict \
# -H "Content-Type: application/json" \
# -d '{"model": "resnet", "attack": "fgsm", "epsilon": 0.2}'

# curl -X POST http://34.57.140.84:8000/resnet-attack/ \
# -H "Content-Type: application/json" \
# -d '{"model": "resnet", "attack": "pgd", "epsilon": 0.2, "eps_step": 0.01, "max_iter": 1}'
# curl -o example.png "http://34.57.140.84:8000/get-file/?file_path=figures/example_1_original_vs_adversarial.png"


# curl -X POST http://34.57.140.84:8000/resnet-attack/ \
# -H "Content-Type: application/json" \
# -d '{"model": "resnet", "attack": "deepfool", "max_iter": 1}'

# curl -X POST http://127.0.0.1:8000/predict \
# -H "Content-Type: application/json" \
-d '{
  "instances": [
    {
      "model": "resnet",
      "attack": "fgsm",
      "epsilon": 0.2
    }
  ]
}'

## CUSTOM EXAMPLE:
# curl -X POST http://127.0.0.1:8000/predict \
# -H "Content-Type: application/json" \
# -d '{
#   "instances": [
#     {
#       "model": "custom",
#       "model_path": "gs://custom-attacks-multi/test/example.h5",
#       "data_path": "gs://custom-attacks-multi/test/data",
#       "width": 28,
#       "height": 28,
#       "channels": 1,
#       "attack": "fgsm",
#       "epsilon": 0.2
#     }
#   ]
# }'

## LIVE CUSTOM EXAMPLE:
# curl \
# -X POST \
# -H "Authorization: Bearer $(gcloud auth print-access-token)" \
# -H "Content-Type: application/json" \
# https://us-central1-aiplatform.googleapis.com/ui/projects/secret-cipher-399620/locations/us-central1/endpoints/6918735191896752128:predict \
# -d '{
#   "instances": [
#     {
#       "model": "custom",
#       "model_path": "gs://custom-attacks-multi/test/example.h5",
#       "data_path": "gs://custom-attacks-multi/test/data",
#       "width": 28,
#       "height": 28,
#       "channels": 1,
#       "attack": "fgsm",
#       "epsilon": 0.2
#     }
#   ]
# }'

## REGULAR EXAMPLE
# curl \
# -X POST \
# -H "Authorization: Bearer $(gcloud auth print-access-token)" \
# -H "Content-Type: application/json" \
# https://us-east1-aiplatform.googleapis.com/ui/projects/secret-cipher-399620/locations/us-east1/endpoints/3829946445218185216:predict \
# -d '{
#   "instances": [
#     {
#       "model": "resnet",
#       "attack": "fgsm",
#       "epsilon": 0.2
#     }
#   ]
# }'

