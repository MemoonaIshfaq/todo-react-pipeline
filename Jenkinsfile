pipeline {
    agent any

    environment {
        DOCKER_BUILDKIT = 1
    }

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main', url: 'https://github.com/MemoonaIshfaq/todo-react-pipeline.git'
            }
        }

        stage('Run Tests using Docker Compose') {
            steps {
                sh 'docker-compose up --build --abort-on-container-exit'
            }
        }
    }

    post {
        success {
            emailext (
                subject: "✅ Test Passed: ${env.JOB_NAME} [${env.BUILD_NUMBER}]",
                body: "All Selenium tests passed successfully!\n${env.BUILD_URL}",
                recipientProviders: [[$class: 'CulpritsRecipientProvider']]
            )
        }

        failure {
            emailext (
                subject: "❌ Test Failed: ${env.JOB_NAME} [${env.BUILD_NUMBER}]",
                body: "Some Selenium tests failed.\n${env.BUILD_URL}",
                recipientProviders: [[$class: 'CulpritsRecipientProvider']]
            )
        }
    }
}
