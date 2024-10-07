# DockerHub Variables
DOCKER_REGISTRY=thejasrao2003
IMAGE_TAG=latest

# Services
SERVICES=datapreprocessing modeltraining visualisation frontend hyperparametertuning
NGINX_SERVICE=nginx

# Kubernetes manifests directory
K8S_DIR=k8s

# Build Docker Images
build:
	@for service in $(SERVICES); do \
		echo "Building Docker image for $$service"; \
		docker build -t $(DOCKER_REGISTRY)/modeltraining-$$service:$(IMAGE_TAG) ./$$service; \
	done
	# Build nginx image separately
	@echo "Building Docker image for nginx"; \
	docker build -t $(DOCKER_REGISTRY)/nginx:$(IMAGE_TAG) ./nginx

# Push Docker Images to DockerHub
push:
	@for service in $(SERVICES); do \
		echo "Pushing Docker image for $$service"; \
		docker push $(DOCKER_REGISTRY)/modeltraining-$$service:$(IMAGE_TAG); \
	done
	# Push nginx image separately
	@echo "Pushing Docker image for nginx"; \
	docker push $(DOCKER_REGISTRY)/nginx:$(IMAGE_TAG)

# Deploy to Kubernetes
deploy:
	@for service in $(SERVICES); do \
		echo "Deploying $$service to Kubernetes"; \
		kubectl apply -f $(K8S_DIR)/$$service-deployment.yaml; \
	done
	# Deploy nginx configmap and nginx
	@echo "Applying nginx ConfigMap to Kubernetes"; \
	kubectl apply -f $(K8S_DIR)/nginx-configmap.yaml
	@echo "Deploying nginx to Kubernetes"; \
	kubectl apply -f $(K8S_DIR)/nginx-deployment.yaml

# Clean Docker Images
clean:
	@for service in $(SERVICES); do \
		echo "Removing Docker image for $$service"; \
		docker rmi $(DOCKER_REGISTRY)/modeltraining-$$service:$(IMAGE_TAG) || true; \
	done
	# Remove nginx image separately
	@echo "Removing Docker image for nginx"; \
	docker rmi $(DOCKER_REGISTRY)/nginx:$(IMAGE_TAG) || true

# Full pipeline: Build, Push, Deploy
all: build push deploy

# Build and Push Docker Images
docker: build push
