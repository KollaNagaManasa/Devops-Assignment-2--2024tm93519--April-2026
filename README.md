# ACEest Fitness & Gym - Assignment 2 (DevOps CI/CD)

This repository completes the CI/CD assignment requirements for ACEest Fitness & Gym.

## Included Deliverables
- Uploaded ACEest version files from Assignment 1 (`Aceestver*.py`)
- Flask service entry file: `ACEest_Fitness.py`
- Unit tests: `tests/test_aceest.py`
- Jenkins pipeline: `Jenkinsfile`
- Docker build file: `Dockerfile`
- SonarQube scanner config: `sonar-project.properties`
- Kubernetes base manifests and strategy manifests under `k8s/`
- Deployment and rollback scripts under `scripts/`

## Run Locally
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python ACEest_Fitness.py
```

## Run Tests
```powershell
pytest -q --junitxml=junit.xml
```

## Docker
```powershell
docker build -t your-dockerhub-username/aceest-fitness:v1 .
docker push your-dockerhub-username/aceest-fitness:v1
docker tag your-dockerhub-username/aceest-fitness:v1 your-dockerhub-username/aceest-fitness:latest
docker push your-dockerhub-username/aceest-fitness:latest
```

## Kubernetes Base Deploy
```powershell
kubectl apply -f k8s/base/namespace.yaml
kubectl apply -f k8s/base/deployment.yaml
kubectl apply -f k8s/base/service.yaml
kubectl get all -n aceest
```

## Deployment Strategies
- Rolling Update: `k8s/strategies/rolling-update/deployment-rolling.yaml`
- Blue-Green: `k8s/strategies/blue-green/deployment-blue-green.yaml`
- Canary: `k8s/strategies/canary/deployment-canary.yaml`
- Shadow: `k8s/strategies/shadow/deployment-shadow.yaml`
- A/B Testing: `k8s/strategies/ab-testing/deployment-ab-testing.yaml`

## Rollback
```powershell
.\scripts\rollback.ps1 -Namespace aceest -Deployment aceest-fitness
```

## Important Setup
- Replace `your-dockerhub-username` in `Jenkinsfile` and all `k8s` manifests.
- Create Jenkins credentials:
  - `dockerhub-creds`
  - SonarQube server configured as `sonarqube-server`
# ACEest Fitness & Gym - DevOps CI/CD Assignment 2

This project demonstrates an end-to-end DevOps CI/CD workflow for a Flask application.

## Tech Stack
- Git and GitHub
- Jenkins pipeline
- Pytest for unit tests
- SonarQube for static code analysis
- Docker containerization
- Kubernetes (Minikube or cloud)

## Project Structure
- `ACEest_Fitness.py` - main application entry point
- `ACEest_Fitness_v1.py` to `ACEest_Fitness_v5.py` - versioned app entry points
- `app/` - Flask app package
- `tests/` - Pytest test suite
- `Dockerfile` - container build definition
- `Jenkinsfile` - CI/CD pipeline
- `k8s/` - Kubernetes manifests and deployment strategy examples
- `sonar-project.properties` - SonarQube scanner configuration

## Local Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python ACEest_Fitness.py
```

Run a specific version:
```bash
python ACEest_Fitness_v1.py
python ACEest_Fitness_v2.py
python ACEest_Fitness_v3.py
python ACEest_Fitness_v4.py
python ACEest_Fitness_v5.py
```

## Run Tests
```bash
pytest -q --junitxml=junit.xml
```

## Docker Build
```bash
docker build -t your-dockerhub-username/aceest-fitness:v1 .
docker push your-dockerhub-username/aceest-fitness:v1
```

## Kubernetes Base Deployment
```bash
kubectl apply -f k8s/base/namespace.yaml
kubectl apply -f k8s/base/deployment.yaml
kubectl apply -f k8s/base/service.yaml
kubectl get all -n aceest
```

## Deployment Strategy Manifests
- Blue-Green: `k8s/strategies/blue-green/deployment-blue-green.yaml`
- Canary: `k8s/strategies/canary/deployment-canary.yaml`
- Shadow: `k8s/strategies/shadow/deployment-shadow.yaml`
- A/B Testing: `k8s/strategies/ab-testing/deployment-ab-testing.yaml`
- Rolling Update: `k8s/strategies/rolling-update/deployment-rolling.yaml`

## Notes
Replace `your-dockerhub-username` in manifests and Jenkinsfile before running the pipeline.
