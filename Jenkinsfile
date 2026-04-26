pipeline {
    agent any

    environment {
        IMAGE_NAME = "kollanagamanasa/aceest-fitness"
        IMAGE_TAG = "${BUILD_NUMBER}"
        KUBE_CONFIG = "/var/lib/jenkins/config"
    }

    stages {

        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m pip install --upgrade pip --user
                pip3 install --user -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                export PATH=$PATH:/var/lib/jenkins/.local/bin
                export PYTHONPATH=$PYTHONPATH:$(pwd)
                pytest -q --junitxml=junit.xml
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
            }
        }

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

        // Apply base configs
        stage('Apply Base') {
            steps {
                sh '''
                export KUBECONFIG=${KUBE_CONFIG}
                kubectl apply -f k8s/base/
                '''
            }
        }

        // Rolling update with rollback
        stage('Rolling Update + Rollback') {
            steps {
                sh '''
                export KUBECONFIG=${KUBE_CONFIG}

                kubectl set image deployment/aceest-fitness \
                aceest-fitness=${IMAGE_NAME}:${IMAGE_TAG} -n aceest

                if ! kubectl rollout status deployment/aceest-fitness -n aceest --timeout=60s; then
                    echo "Rollback triggered"
                    kubectl rollout undo deployment/aceest-fitness -n aceest
                    exit 1
                fi
                '''
            }
        }

        // Blue-Green
        stage('Blue-Green Deploy') {
            steps {
                sh '''
                export KUBECONFIG=${KUBE_CONFIG}

                kubectl apply -f k8s/blue-green/

                # switch traffic to green
                kubectl patch svc aceest-service -n aceest \
                -p '{"spec":{"selector":{"app":"aceest","version":"green"}}}'
                '''
            }
        }

        // Canary
        stage('Canary Deploy') {
            steps {
                sh '''
                export KUBECONFIG=${KUBE_CONFIG}
                kubectl apply -f k8s/canary/
                '''
            }
        }

        // Shadow
        stage('Shadow Deploy') {
            steps {
                sh '''
                export KUBECONFIG=${KUBE_CONFIG}
                kubectl apply -f k8s/shadow/
                '''
            }
        }

        // A/B Testing (basic)
        stage('A/B Deployment') {
            steps {
                sh '''
                export KUBECONFIG=${KUBE_CONFIG}
                kubectl apply -f k8s/ab-testing/
                '''
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: '**/junit.xml'
        }
        success {
            echo "All deployment strategies executed successfully"
        }
        failure {
            echo "Pipeline failed - rollback handled"
        }
    }
}
