pipeline {
    agent any

    environment {
        IMAGE_NAME = "ashrith2727/ng-app"
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/brahmanyasudulagunta/Nginx-Application.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t $IMAGE_NAME:$IMAGE_TAG ./app"
            }
        }

        stage('Login to DockerHub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                }
            }
        }

        stage('Push Image') {
            steps {
                sh "docker push $IMAGE_NAME:$IMAGE_TAG"
            }
        }
    
        stage('Debug Kube') {
            steps {
                sh '''
                   kubectl config current-context
                   kubectl get deployments -A
                   '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh """
                kubectl set image deployment/python-app \
                python-app=$IMAGE_NAME:$IMAGE_TAG
                """
            }
        }

        stage('Verify Rollout') {
            steps {
                sh "kubectl rollout status deployment/python-app"
            }
        }
    }
}
