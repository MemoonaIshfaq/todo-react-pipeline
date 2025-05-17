pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = "jenkins_ci"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/MemoonaIshfaq/todo-react-pipeline.git'
            }
        }

        stage('Build and Run using Docker Compose') {
            steps {
                script {
                    dir("${env.WORKSPACE}") {
                        sh 'docker-compose -p $COMPOSE_PROJECT_NAME -f docker-compose.yml up -d --build'
                    }
                }
            }
        }
    }

    post {
        failure {
            echo 'Build failed. Please check the Jenkins logs for more details.'
        }
        success {
            echo 'Build and Docker Compose ran successfully!'
        }
    }
}
