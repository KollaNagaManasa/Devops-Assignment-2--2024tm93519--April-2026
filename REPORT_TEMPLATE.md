# Assignment 2 Report - ACEest Fitness & Gym

## CI/CD Architecture Overview
The repository uses GitHub for version control and Jenkins for CI/CD orchestration.  
On each commit, Jenkins pulls the latest code, installs dependencies, runs Pytest tests, triggers SonarQube analysis with quality gate checks, builds Docker images, pushes versioned images to Docker Hub, and performs deployment updates in Kubernetes.

### Toolchain
- Git + GitHub
- Jenkins
- Pytest
- SonarQube
- Docker
- Docker Hub
- Kubernetes / Minikube

## Challenges and Mitigation
- **Version consolidation challenge:** multiple historical code versions had inconsistent structures.  
  **Mitigation:** preserved all historical version files and exposed versions through a stable Flask service endpoint.

- **Quality assurance in automation:** builds can pass without quality standards.  
  **Mitigation:** enforced SonarQube analysis and quality gate in Jenkins.

- **Release risk in production-like deployment:** direct full replacement can cause instability.  
  **Mitigation:** added manifests for rolling update, blue-green, canary, shadow, and A/B testing.

- **Rollback requirement:** failed deployments require fast recovery.  
  **Mitigation:** included rollout rollback script and Kubernetes rollback command flow.

## Key Automation Outcomes
- End-to-end CI/CD implemented from commit to deployment.
- Automated unit testing and quality validation integrated into pipeline.
- Containerized runtime ensures environment consistency.
- Progressive deployment strategy manifests prepared for safer releases.
- Rollback capability established for deployment failures.

## Evidence Attachments (Submission)
- GitHub repository link
- Jenkins successful run screenshots
- SonarQube quality gate screenshot
- Docker Hub image tags screenshot
- Kubernetes deployment and service endpoint screenshot
- Rollback demonstration screenshot
# Assignment 2 Report - ACEest Fitness & Gym CI/CD

## 1. CI/CD Architecture Overview
The project implements an automated CI/CD flow for a Flask-based fitness management application.  
The workflow starts from code commit in GitHub and continues through Jenkins-based build, testing, static analysis, image packaging, registry push, and Kubernetes deployment.

### Pipeline Flow
1. Developer pushes code to GitHub.
2. Jenkins triggers pipeline (`Jenkinsfile`).
3. Dependencies are installed and unit tests run using Pytest.
4. SonarQube static code analysis executes and quality gate is enforced.
5. Docker image is built and pushed to Docker Hub.
6. Kubernetes rollout updates the running application.
7. Rollback is available through Kubernetes rollout history.

### Tools Used
- Version Control: Git + GitHub
- CI/CD: Jenkins
- Test Automation: Pytest
- Code Quality: SonarQube
- Containerization: Docker
- Registry: Docker Hub
- Orchestration: Kubernetes (Minikube/cloud)

## 2. Challenges Faced and Mitigation

### Challenge 1: Pipeline consistency across environments
- **Issue:** Local environment and Jenkins environment differences caused build issues.
- **Mitigation:** Standardized dependencies with `requirements.txt`, used containerized runtime and reproducible build commands.

### Challenge 2: Deployment reliability
- **Issue:** Risk of downtime during updates.
- **Mitigation:** Added rolling update strategy with readiness probes and deployment status checks.

### Challenge 3: Safer production releases
- **Issue:** Immediate full rollout of new version can introduce production risk.
- **Mitigation:** Added strategy manifests for blue-green, canary, shadow, and A/B testing to progressively validate new releases.

### Challenge 4: Code quality enforcement
- **Issue:** Builds could pass with functional tests but poor quality code.
- **Mitigation:** Integrated SonarQube and quality gate stage in Jenkins.

## 3. Key Automation Outcomes
- Reduced manual deployment steps by automating build, test, scan, image push, and rollout.
- Improved software reliability through repeatable unit tests and health checks.
- Increased release confidence using progressive deployment strategy options.
- Enabled quick rollback to stable versions using Kubernetes rollout commands.

## 4. Evidence to Include in Submission
- GitHub repository link
- Screenshots of successful Jenkins runs
- SonarQube dashboard screenshot and quality gate status
- Docker Hub repository with version-tagged images
- `kubectl get all -n aceest` and service endpoint output
- Demonstration of at least one rollback execution
