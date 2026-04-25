pipeline {
    agent any

    environment {
        IMAGE_NAME = "kollanagamanasa/aceest-fitness"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        // 🔹 1. Checkout Code
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // 🔹 2. Install Dependencies
        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m pip install --upgrade pip --user
                pip3 install --user -r requirements.txt
                '''
            }
        }

        // 🔹 3. Run Unit Tests
        stage('Run Unit Tests') {
            steps {
                sh '''
                export PATH=$PATH:/var/lib/jenkins/.local/bin
                pip3 install --user pytest
                pytest -q --junitxml=junit.xml
                '''
            }
        }

        // 🔹 4. SonarQube Analysis
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube-server') {
                    sh '''
                    export PATH=$PATH:/opt/sonar-scanner/bin

                    sonar-scanner \
                    -Dsonar.projectKey=aceest-fitness \
                    -Dsonar.sources=. \
                    -Dsonar.host.url=http://localhost:9000 \
                    -Dsonar.login=$SONAR_AUTH_TOKEN
                    '''
                }
            }
        }

        // 🔹 5. Build Docker Image
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
            }
        }

        // 🔹 6. Push Docker Image
        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                    docker push ${IMAGE_NAME}:latest
                    '''
                }
            }
        }

        // 🔹 7. Apply Kubernetes Config
        stage('Apply Kubernetes Config') {
            steps {
                sh '''
                export KUBECONFIG=/var/lib/jenkins/config
                kubectl apply -f k8s/base/
                '''
            }
        }

        // 🔹 8. Rolling Deployment
        stage('Deploy Rolling Update') {
            steps {
                sh '''
                export KUBECONFIG=/var/lib/jenkins/config
                kubectl set image deployment/aceest-fitness \
                aceest-fitness=${IMAGE_NAME}:${IMAGE_TAG} -n aceest || true

                kubectl rollout status deployment/aceest-fitness -n aceest
                '''
            }
        }

        // 🔹 9. Canary Deployment
        stage('Canary Deployment') {
            steps {
                sh '''
                export KUBECONFIG=/var/lib/jenkins/config
                kubectl apply -f k8s/canary/
                '''
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: '**/junit.xml'
        }
    }
}
