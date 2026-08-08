
pipeline {
    agent any

    environment {
        DOCKER_HUB = credentials('dockerhub-creds')

        EC2_HOST = "3.226.15.198"
        EC2_USER = "ubuntu"
        // EC2_KEY = "M:\\projects\\Resum_project\\ecomm\\ecomm_Server_key.pem" /// for now hardcode, will change laterL

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
                bat 'docker compose -f docker-compose.yml -f docker-compose.prod.yml build'
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


        // stage('Deploy to EC2') {
        //     steps {
        //         withCredentials([file(credentialsId: 'ec2-pem-file_Secret_file', variable: 'PEM_FILE')]) {

        //             bat """
        //             ssh -i "%PEM_FILE%" ^
        //             -o StrictHostKeyChecking=no ^
        //             ubuntu@3.226.15.198 ^
        //             "cd ~/ecommerce-microservices && docker compose pull && docker compose up -d"
        //             """

        //         }
        //     }
        // }  //////not working, telling Load key "C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\ecomm-pipeline@tmp\\secretFiles\\5a542122-34db-4bff-8b53-848edf2e7034\\file9551972910908143207.tmp": bad permissions


        stage('Deploy to EC2') {
            steps {
                withCredentials([file(credentialsId: 'ec2-pem-file_Secret_file', variable: 'EC2_KEY')]) {
                bat """
                echo Using key: %EC2_KEY%
                echo ===== WHOAMI =====
                whoami

                echo ===== USERNAME =====
                echo %USERNAME%

                echo ===== FILE PERMISSIONS BEFORE =====
                icacls "%EC2_KEY%"

                icacls "%EC2_KEY%" /inheritance:r
                icacls "%EC2_KEY%" /remove:g "BUILTIN\\Users"
                icacls "%EC2_KEY%" /grant:r "SYSTEM:(R)"

                ssh -i "%EC2_KEY%" ^
                -o StrictHostKeyChecking=no ^
                %EC2_USER%@%EC2_HOST% ^
                "cd /home/ubuntu/ecomm_personal_01 && git pull && docker compose -f docker-compose.yml -f docker-compose.prod.yml pull && docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d"
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

