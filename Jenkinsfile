pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "your-dockerhub-username/aceest-fitness"
        TAG = "${BUILD_NUMBER}"
    }

    triggers {
        pollSCM('H/2 * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install') {
            steps {
                sh 'python3 -m pip install --upgrade pip'
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh 'pytest -q --junitxml=junit.xml'
            }
        }

        stage('SonarQube Scan') {
            steps {
                withSonarQubeEnv('sonarqube-server') {
                    sh 'sonar-scanner'
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t ${DOCKER_IMAGE}:${TAG} .'
                sh 'docker tag ${DOCKER_IMAGE}:${TAG} ${DOCKER_IMAGE}:latest'
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin'
                    sh 'docker push ${DOCKER_IMAGE}:${TAG}'
                    sh 'docker push ${DOCKER_IMAGE}:latest'
                }
            }
        }

        stage('Deploy Rolling Update') {
            steps {
                sh 'kubectl set image deployment/aceest-fitness aceest-fitness=${DOCKER_IMAGE}:${TAG} -n aceest'
                sh 'kubectl rollout status deployment/aceest-fitness -n aceest'
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'junit.xml'
        }
    }
}
pipeline {
    agent any

    environment {
        IMAGE_NAME = "your-dockerhub-username/aceest-fitness"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m pip install --upgrade pip'
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh 'pytest -q --junitxml=junit.xml'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube-server') {
                    sh 'sonar-scanner'
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin'
                    sh 'docker push ${IMAGE_NAME}:${IMAGE_TAG}'
                    sh 'docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest'
                    sh 'docker push ${IMAGE_NAME}:latest'
                }
            }
        }

        stage('Deploy Rolling Update') {
            steps {
                sh 'kubectl set image deployment/aceest-fitness aceest-fitness=${IMAGE_NAME}:${IMAGE_TAG} -n aceest'
                sh 'kubectl rollout status deployment/aceest-fitness -n aceest'
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: '**/junit.xml'
        }
    }
}
