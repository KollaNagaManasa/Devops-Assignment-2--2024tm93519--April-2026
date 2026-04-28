# ACEest Fitness & Gym – DevOps CI/CD Pipeline (Assignment 2)

## Overview

This project implements a complete **end-to-end CI/CD pipeline** for the ACEest Fitness & Gym application.

It demonstrates:

* Automated build and test pipeline
* Static code analysis using SonarCloud
* Docker-based containerization
* Kubernetes (K3s) deployment on AWS EC2
* Multiple deployment strategies

---

# Architecture

```
GitHub → Jenkins → Pytest → SonarCloud → Docker → DockerHub → Kubernetes (K3s) → NodePort → Browser
```

---

# Infrastructure (AWS EC2)

The entire pipeline is deployed on an EC2 instance.

## Instance Details

* OS: Amazon Linux 2023
* Instance Type: t2.small

## Installed Tools

* Java (for Jenkins)
* Jenkins
* Docker
* K3s (Lightweight Kubernetes)
* Sonar Scanner

---

# Security Group Configuration

| Port        | Purpose             |
| ----------- | ------------------- |
| 22          | SSH                 |
| 8080        | Jenkins UI          |
| 30000–32767 | Kubernetes NodePort |
| 80          | Optional web access |

---

# Project Structure

```
.
├── ACEest_Fitness.py
├── ACEest_Fitness_v1.py ... v5.py
├── tests/
│   └── test_aceest.py
├── Dockerfile
├── Jenkinsfile
├── sonar-project.properties
├── k8s/
│   ├── base/
│   │   ├── namespace.yaml
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   └── strategies/
│       ├── rolling/
│       ├── blue-green/
│       ├── canary/
│       ├── shadow/
│       └── ab-testing/
├── scripts/
│   └── rollback.ps1
└── requirements.txt
```

---

# CI/CD Pipeline (Jenkins)

Pipeline stages:

1. Checkout Code (GitHub)
2. Setup Python Environment
3. Run Tests (pytest)
4. SonarCloud Analysis
5. Build Docker Image
6. Push to DockerHub
7. Deploy to Kubernetes

---

# Testing

Run locally:

```bash
pytest -q --junitxml=junit.xml
```

---

# Code Quality

Integrated with SonarCloud for:

* Bugs detection
* Code smells
* Security vulnerabilities

---

# Docker

## Build Image

```bash
docker build -t kollanagamanasa/aceest-fitness:v1 .
```

## Push Image

```bash
docker push kollanagamanasa/aceest-fitness:v1
docker tag kollanagamanasa/aceest-fitness:v1 kollanagamanasa/aceest-fitness:latest
docker push kollanagamanasa/aceest-fitness:latest
```

---

# Kubernetes Deployment (K3s)

## Base Deployment

```bash
kubectl apply -f k8s/base/
```

## Verify

```bash
kubectl get pods -n aceest
kubectl get svc -n aceest
```

---

# Application Access

Application is exposed using NodePort:

```
http://<EC2-PUBLIC-IP>:<NodePort>
```

### Example:

```
http://98.130.128.175:31272
```

---

# Deployment Strategies

Implemented using Kubernetes manifests:

* Rolling Deployment
* Blue-Green Deployment
* Canary Deployment
* Shadow Deployment
* A/B Testing

Note: Strategies are applied **one at a time** due to resource constraints.

---

# Rollback

```bash
.\scripts\rollback.ps1 -Namespace aceest -Deployment aceest-fitness
```

---

# Jenkins Credentials

Configured in Jenkins:

| ID                 | Purpose                   |
| ------------------ | ------------------------- |
| docker-credentials | DockerHub login           |
| sonar-token        | SonarCloud authentication |

---

# Challenges Faced

* Low disk space on EC2 → caused pod eviction
* SonarQube server heavy → replaced with SonarCloud
* Kubernetes TLS errors → fixed kubeconfig
* External access issues → fixed security group

---

# Solutions

* Cleaned `/var/lib` and Jenkins builds
* Used lightweight K3s
* Configured NodePort correctly
* Allowed port range in AWS

---

# Results

* CI/CD pipeline executed successfully
* Docker image built and pushed
* Kubernetes deployment successful
* Application accessible via browser

---

# Project Links

## GitHub Repository

https://github.com/KollaNagaManasa/Devops-Assignment-2--2024tm93519--April-2026

## Jenkins Dashboard

http://98.130.128.175:8080

## Jenkins Pipeline Job

http://98.130.128.175:8080/job/Aceest-Fitness-Devops-Pipeline/

## SonarCloud Dashboard

https://sonarcloud.io/project/overview?id=kollanagamanasa_Devops-Assignment-2--2024tm93519--April-2026

## DockerHub Repository

https://hub.docker.com/r/kollanagamanasa/aceest-fitness

## Live Application

http://98.130.128.175:31272

---

# Conclusion

This project successfully demonstrates a **real-world DevOps pipeline** integrating CI/CD, testing, code quality analysis, containerization, and Kubernetes deployment.

It highlights practical problem-solving in constrained environments and follows industry best practices.

---
