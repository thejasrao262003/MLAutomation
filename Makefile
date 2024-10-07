# DockerHub Variables
DOCKER_REGISTRY=thejasrao2003
IMAGE_TAG=latest

# Services
SERVICES=datapreprocessing modeltraining visualisation frontend hyperparametertuning nginx

# Kubernetes manifests directory
K8S_DIR=k8s

# Build Docker Images
build:
	@for service in $(SERVICES); do \
		echo "Building Docker image for $$service"; \
		docker build -t $(DOCKER_REGISTRY)/modeltraining-$$service:$(IMAGE_TAG) ./$$service; \
	done

# Push Docker Images to DockerHub
push:
	@for service in $(SERVICES); do \
		echo "Pushing Docker image for $$service"; \
		docker push $(DOCKER_REGISTRY)/modeltraining-$$service:$(IMAGE_TAG); \
	done

# Deploy to Kubernetes
deploy:
	@for service in $(SERVICES); do \
		echo "Deploying $$service to Kubernetes"; \
		kubectl apply -f $(K8S_DIR)/$$service-deployment.yaml; \
	done

# Clean Docker Images
clean:
	@for service in $(SERVICES); do \
		echo "Removing Docker image for $$service"; \
		docker rmi $(DOCKER_REGISTRY)/modeltraining-$$service:$(IMAGE_TAG) || true; \
	done

# Full pipeline: Build, Push, Deploy
all: build push deploy

# Build and Push Docker Images
docker: build push
