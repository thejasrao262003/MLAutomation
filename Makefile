# DockerHub Variables
DOCKER_REGISTRY=thejasrao2003
IMAGE_TAG=latest

# Kubernetes manifests directory
K8S_DIR=k8s

# Build Docker Images using docker-compose
build:
	docker-compose build

# Push Docker Images to DockerHub
push:
	@for service in frontend datapreprocessing visualisation modeltraining hyperparametertuning; do \
		echo "Pushing Docker image for $$service"; \
		docker tag $$service $(DOCKER_REGISTRY)/modeltraining-$$service:$(IMAGE_TAG); \
		docker push $(DOCKER_REGISTRY)/modeltraining-$$service:$(IMAGE_TAG); \
	done

# Deploy to Kubernetes (for services + Nginx config and Nginx deployment)
deploy:
	@for service in frontend datapreprocessing visualisation modeltraining hyperparametertuning; do \
		echo "Deploying $$service to Kubernetes"; \
		kubectl apply -f $(K8S_DIR)/$$service-deployment.yaml; \
	done
	# Apply Nginx configmap
	@echo "Applying nginx-configmap.yaml to Kubernetes"; \
	kubectl apply -f $(K8S_DIR)/nginx-configmap.yaml
	# Deploy official Nginx image
	@echo "Deploying Nginx to Kubernetes"; \
	kubectl apply -f $(K8S_DIR)/nginx-deployment.yaml

# Clean Docker Images (for custom services only)
clean:
	@for service in frontend datapreprocessing visualisation modeltraining hyperparametertuning; do \
		echo "Removing Docker image for $$service"; \
		docker rmi $(DOCKER_REGISTRY)/modeltraining-$$service:$(IMAGE_TAG) || true; \
	done

# Full pipeline: Build, Push, Deploy
all: build push deploy

# Build and Push Docker Images
docker: build push
