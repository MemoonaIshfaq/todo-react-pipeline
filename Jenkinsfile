pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/MemoonaIshfaq/todo-react-pipeline.git'
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
