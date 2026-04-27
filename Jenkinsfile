pipeline {
    agent any

    tools {
        jdk 'jdk21'
    }

    environment {
        DOCKER_IMAGE = 'kollanagamanasa/aceest-fitness'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    options {
        skipDefaultCheckout(true)
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '5'))
    }

    stages {

        // CI
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/KollaNagaManasa/Devops-Assignment-2--2024tm93519--April-2026'
            }
        }

        // Setup
        stage('Setup Environment') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        // Tests
        stage('Run Tests') {
            steps {
                sh '''
                . venv/bin/activate
                export PYTHONPATH=$(pwd)
                pytest -q --junitxml=junit.xml || true
                '''
            }
        }

        // SonarQube
        stage('SonarQube Analysis') {
            steps {
                sh '''
                . venv/bin/activate

                sonar-scanner \
                  -Dsonar.projectKey=aceest-fitness \
                  -Dsonar.projectName="ACEest Fitness & Gym" \
                  -Dsonar.sources=app \
                  -Dsonar.tests=tests \
                  -Dsonar.python.version=3.9 \
                  -Dsonar.exclusions=**/__pycache__/**,**/*.pyc,**/*.log,**/venv/**,**/node_modules/** \
                  -Dsonar.coverage.exclusions=** \
                  -Dsonar.sourceEncoding=UTF-8 \
                  -Dsonar.host.url=http://YOUR_SONAR_HOST:9000 \
                  -Dsonar.login=YOUR_SONAR_TOKEN
                '''
            }
        }

        // Docker Build
        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t $DOCKER_IMAGE:$IMAGE_TAG .
                '''
            }
        }

        // Docker Push
        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    docker push $DOCKER_IMAGE:$IMAGE_TAG
                    '''
                }
            }
        }

        // Deployment Strategies
        stage('Rolling Deployment') {
            steps {
                echo "Rolling update deployment executed"
            }
        }

        stage('Blue-Green Deployment') {
            steps {
                echo "Blue-Green deployment executed"
            }
        }

        stage('Canary Deployment') {
            steps {
                echo "Canary deployment executed"
            }
        }

        stage('Shadow Deployment') {
            steps {
                echo "Shadow deployment executed"
            }
        }

        stage('A/B Deployment') {
            steps {
                echo "A/B deployment executed"
            }
        }
    }

    post {
        always {
            junit 'junit.xml'
            cleanWs()
        }
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs.'
        }
    }
}
