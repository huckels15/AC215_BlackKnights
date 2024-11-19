curl -X POST http://35.221.41.10:8000/resnet-attack/ \
-H "Content-Type: application/json" \
-d '{"model": "resnetl0l", "attack": "fgsm", "epsilon": 0.2}'