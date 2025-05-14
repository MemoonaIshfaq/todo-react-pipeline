pipeline {
    agent any

    stages {
        stage('Checkout Repo') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build('todo-react-jenkins')
                }
            }
        }

        stage('Run with Docker Compose') {
            steps {
                sh 'docker-compose -p todojenkins -f docker-compose.yml up -d'
            }
        }
    }
}

