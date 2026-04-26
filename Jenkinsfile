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

        // 4. Build Docker Image
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
            }
        }

        // 5. Push Docker Image
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

        // 6. Apply Base Kubernetes
        stage('Deploy Base') {
            steps {
                sh '''
                export KUBECONFIG=${KUBECONFIG}
                kubectl apply -f k8s/base/
                '''
            }
        }

        // 7. Rolling Update + AUTO Rollback
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

        // 8. Blue-Green Deployment
        stage('Blue-Green Deploy') {
            steps {
                sh '''
                export KUBECONFIG=${KUBECONFIG}

                kubectl apply -f k8s/strategies/blue-green/

                echo "Switching traffic to GREEN..."
                kubectl patch svc aceest-service -n aceest \
                -p '{"spec":{"selector":{"app":"aceest","version":"green"}}}'
                '''
            }
        }

        // 9. Canary Deployment
        stage('Canary Deploy') {
            steps {
                sh '''
                export KUBECONFIG=${KUBECONFIG}
                kubectl apply -f k8s/strategies/canary/
                '''
            }
        }

        // 10. Shadow Deployment
        stage('Shadow Deploy') {
            steps {
                sh '''
                export KUBECONFIG=${KUBECONFIG}
                kubectl apply -f k8s/strategies/shadow/
                '''
            }
        }

        // 11. A/B Testing Deployment
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
            echo "Pipeline SUCCESS: All deployment strategies executed!"
        }
        failure {
            echo "Pipeline FAILED: Rollback executed where needed"
        }
    }
}
