pipeline {
    agent any

    environment {
        IMAGE_NAME = "kollanagamanasa/aceest-fitness"
        IMAGE_TAG = "${BUILD_NUMBER}"
        KUBECONFIG = "/etc/rancher/k3s/k3s.yaml"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/KollaNagaManasa/Devops-Assignment-2--2024tm93519--April-2026'
            }
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
                export PYTHONPATH=$(pwd)
                pytest -q --junitxml=junit.xml
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
                    sh '''
                    export PATH=$PATH:/opt/sonar-scanner/bin

                    sonar-scanner \
                      -Dsonar.projectKey=aceest-fitness \
                      -Dsonar.sources=. \
                      -Dsonar.host.url=http://localhost:9000 \
                      -Dsonar.login=$SONAR_TOKEN || true
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    echo $DOCKER_PASS | docker login -u "$DOCKER_USER" --password-stdin
                    docker push $IMAGE_NAME:$IMAGE_TAG
                    '''
                }
            }
        }

        stage('Deploy Base') {
            steps {
                sh 'kubectl apply -f k8s/base/'
            }
        }

        stage('Rolling Update + Rollback') {
            steps {
                sh '''
                kubectl set image deployment/aceest-deployment aceest=$IMAGE_NAME:$IMAGE_TAG
                sleep 20
                kubectl rollout status deployment/aceest-deployment || \
                kubectl rollout undo deployment/aceest-deployment
                '''
            }
        }

        stage('Blue-Green Deployment') {
            steps {
                sh 'kubectl apply -f k8s/strategies/blue-green/'
            }
        }

        stage('Canary Deployment') {
            steps {
                sh 'kubectl apply -f k8s/strategies/canary/'
            }
        }

        stage('Shadow Deployment') {
            steps {
                sh 'kubectl apply -f k8s/strategies/shadow/'
            }
        }

        stage('A/B Deployment') {
            steps {
                sh 'kubectl apply -f k8s/strategies/ab-testing/'
            }
        }
    }

    post {
        always {
            junit 'junit.xml'
        }
        success {
            echo "PIPELINE SUCCESSFULL"
        }
        failure {
            echo "PIPELINE FAILED"
        }
    }
}
