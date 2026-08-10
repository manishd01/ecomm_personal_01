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
        stage('Clean Workspace') {
            steps {
                deleteDir()
            }
        }

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Fix Line Endings: CRLF/LF') {
            steps {
                sh '''
                    echo ===== CONFIGURE GIT =====
                    git config core.autocrlf false
                    git config core.eol lf

                    echo ===== CHECK EFFECTIVE CONFIG =====
                    git config --show-origin --get core.autocrlf
                    git config --show-origin --get core.eol

                    echo ===== CHECK ATTRIBUTES =====
                    git check-attr text eol -- order-service/entrypoint.sh

                    echo ===== RESTORE FILES =====
                    git checkout -- .

                    echo ===== VERIFY ENTRYPOINTS =====
                    git ls-files --eol order-service/entrypoint.sh
                    git ls-files --eol inventory-service/entrypoint.sh
                    git ls-files --eol customer-service/entrypoint.sh
                    git ls-files --eol payment-service/entrypoint.sh
                    git ls-files --eol notification-service/entrypoint.sh
                    git ls-files --eol shipping-service/entrypoint.sh
                '''
            }
        }

        stage('Verify CRLF/LF : for entrypoint file') {
            steps {
                sh '''
                    echo ===== ORDER =====
                    git ls-files --eol order-service/entrypoint.sh

                    echo ===== INVENTORY =====
                    git ls-files --eol inventory-service/entrypoint.sh

                    echo ===== CUSTOMER =====
                    git ls-files --eol customer-service/entrypoint.sh

                    echo ===== PAYMENT =====
                    git ls-files --eol payment-service/entrypoint.sh

                    echo ===== NOTIFICATION =====
                    git ls-files --eol notification-service/entrypoint.sh

                    echo ===== SHIPPING =====
                    git ls-files --eol shipping-service/entrypoint.sh
                '''
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker compose -f docker-compose.yml -f docker-compose.prod.yml build'
            }
        }

        // stage('Verify Docker Image') {
        //     steps {
        //         sh '''
        //         echo ===== CHECKING ORDER IMAGE =====
        //         docker run --rm manishhd01/order-service:latest cat -v /app/entrypoint.sh
        //         '''
        //     }
        // }

        stage('Docker Hub Login') {
            steps {
                sh '''
                    echo "$DOCKER_HUB_PSW" | docker login -u "$DOCKER_HUB_USR" --password-stdin
                '''
            }
        }

        stage('Push Docker Images') {
            steps {
                sh 'docker push manishhd01/order-service:latest'
                sh 'docker push manishhd01/inventory-service:latest'
                sh 'docker push manishhd01/customer-service:latest'
                sh 'docker push manishhd01/payment-service:latest'
                sh 'docker push manishhd01/notification-service:latest'
                sh 'docker push manishhd01/shipping-service:latest'
                sh 'docker push manishhd01/frontend:latest'
            }
        }

        // stage('Deploy to EC2') {
        //     steps {
        //         sshagent(credentials: ['ec2-ssh-key']) {
        //             sh """
        //             ssh -o StrictHostKeyChecking=no %EC2_USER%@%EC2_HOST% ^
        //             "cd ~/ecommerce-microservices && docker compose pull && docker compose up -d"
        //             """
        //         }
        //     }
        // }  //// not using ssh as of now;


        // stage('Deploy to EC2') {
        //     steps {
        //         withCredentials([file(credentialsId: 'ec2-pem-file_Secret_file', variable: 'PEM_FILE')]) {

        //             sh """
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
                    sh '''
                        chmod 600 "$EC2_KEY"

                        ssh -i "$EC2_KEY" \
                            -o StrictHostKeyChecking=no \
                            "$EC2_USER@$EC2_HOST" \
                            "cd /home/ubuntu/ecomm_personal_01 && \
                            git pull && \
                            docker compose -f docker-compose.yml -f docker-compose.prod.yml pull && \
                            docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d"
                    '''
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