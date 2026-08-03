pipeline {
    agent any

    environment {
        DOCKER_HUB = credentials('dockerhub-creds')

        EC2_HOST = "3.226.15.198"
        EC2_USER = "ubuntu"
    }

    triggers {
        githubPush()
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                bat 'docker compose build'
            }
        }

        stage('Docker Hub Login') {
            steps {
                bat '''
                echo %DOCKER_HUB_PSW% | docker login -u %DOCKER_HUB_USR% --password-stdin
                '''
            }
        }

        stage('Push Docker Images') {
            steps {
                bat 'docker push manishhd01/order-service:latest'
                bat 'docker push manishhd01/inventory-service:latest'
                bat 'docker push manishhd01/customer-service:latest'
                bat 'docker push manishhd01/payment-service:latest'
                bat 'docker push manishhd01/notification-service:latest'
                bat 'docker push manishhd01/shipping-service:latest'
                bat 'docker push manishhd01/frontend:latest'
            }
        }

        // stage('Deploy to EC2') {
        //     steps {
        //         sshagent(credentials: ['ec2-ssh-key']) {
        //             bat """
        //             ssh -o StrictHostKeyChecking=no %EC2_USER%@%EC2_HOST% ^
        //             "cd ~/ecommerce-microservices && docker compose pull && docker compose up -d"
        //             """
        //         }
        //     }
        // }  //// not using ssh as of now;


        stage('Deploy to EC2') {
            steps {
                withCredentials([file(credentialsId: 'ec2-pem-file_Secret_file', variable: 'PEM_FILE')]) {

                    bat """
                    ssh -i "%PEM_FILE%" ^
                    -o StrictHostKeyChecking=no ^
                    ubuntu@3.226.15.198 ^
                    "cd ~/ecommerce-microservices && docker compose pull && docker compose up -d"
                    """

                }
            }
        }
    }

    post {

        success {
            echo "Deployment Successful!"
        }

        failure {
            echo "Deployment Failed!"
        }

    }
}   
