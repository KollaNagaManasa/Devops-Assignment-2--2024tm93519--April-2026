pipeline {
    agent any

    environment {
        IMAGE_NAME = "kollanagamanasa/aceest-fitness"
        IMAGE_TAG = "${BUILD_NUMBER}"
        KUBECONFIG = "/var/lib/jenkins/config"
    }

    stages {

        // 1. Checkout
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // 2. Install Dependencies
        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m pip install --upgrade pip --user
                pip3 install --user -r requirements.txt
                '''
            }
        }

        // 3. Run Unit Tests
        stage('Run Unit Tests') {
            steps {
                sh '''
                export PATH=$PATH:/var/lib/jenkins/.local/bin
                export PYTHONPATH=$PYTHONPATH:$(pwd)

                pytest -q --junitxml=junit.xml
                '''
            }
        }

        // 4. SonarCloud Analysis (FIXED)
        stage('SonarCloud Analysis') {
            steps {
                withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
                    sh '''
                    export PATH=$PATH:/opt/sonar-scanner/bin

                    sonar-scanner \
                    -Dsonar.projectKey=kollanagamanasa_Devops-Assignment-2--2024tm93519--April-2026 \
                    -Dsonar.organization=kollanagamanasa \
                    -Dsonar.sources=. \
                    -Dsonar.tests=tests \
                    -Dsonar.exclusions=tests/** \
                    -Dsonar.host.url=https://sonarcloud.io \
                    -Dsonar.token=$SONAR_TOKEN
                    '''
                }
            }
        }

        // 5. Build Docker Image
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
            }
        }

        // 6. Push Docker Image
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

        // 7. Apply Base Kubernetes
        stage('Deploy Base') {
            steps {
                sh '''
                export KUBECONFIG=${KUBECONFIG}
                kubectl apply -f k8s/base/
                '''
            }
        }

        // 8. Rolling Update + Rollback
        stage('Rolling Update + Rollback') {
            steps {
                sh '''
                export KUBECONFIG=${KUBECONFIG}

                kubectl set image deployment/aceest-fitness \
                aceest-fitness=${IMAGE_NAME}:${IMAGE_TAG} -n aceest

                if ! kubectl rollout status deployment/aceest-fitness -n aceest --timeout=60s; then
                    echo "Deployment failed! Rolling back..."
                    kubectl rollout undo deployment/aceest-fitness -n aceest
                    kubectl rollout status deployment/aceest-fitness -n aceest
                    exit 1
                fi

                echo "Rolling update successful"
                '''
            }
        }

        // 9. Blue-Green Deployment
        stage('Blue-Green Deploy') {
            steps {
                sh '''
                export KUBECONFIG=${KUBECONFIG}

                kubectl apply -f k8s/strategies/blue-green/

                kubectl patch svc aceest-service -n aceest \
                -p '{"spec":{"selector":{"app":"aceest","version":"green"}}}'
                '''
            }
        }

        // 10. Canary Deployment
        stage('Canary Deploy') {
            steps {
                sh '''
                export KUBECONFIG=${KUBECONFIG}
                kubectl apply -f k8s/strategies/canary/
                '''
            }
        }

        // 11. Shadow Deployment
        stage('Shadow Deploy') {
            steps {
                sh '''
                export KUBECONFIG=${KUBECONFIG}
                kubectl apply -f k8s/strategies/shadow/
                '''
            }
        }

        // 12. A/B Testing Deployment
        stage('A/B Deployment') {
            steps {
                sh '''
                export KUBECONFIG=${KUBECONFIG}
                kubectl apply -f k8s/strategies/ab-testing/
                '''
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: '**/junit.xml'
        }
        success {
            echo "Pipeline SUCCESS: CI/CD + SonarCloud + All deployment strategies completed!"
        }
        failure {
            echo "Pipeline FAILED: Check logs"
        }
    }
}
