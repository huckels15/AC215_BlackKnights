# ansible-playbook deploy-docker-images.yml -i inventory.yml
# # ansible-playbook deploy-model-reg.yml -i inventory.yml
# ansible-playbook deploy-containers.yml -i inventory.yml
ansible-playbook deploy-k8s-cluster.yml -i inventory.yml --extra-vars cluster_state=present