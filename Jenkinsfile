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

        stage('Run Selenium Tests') {
            steps {
                script {
                    sh '''
                        docker run --rm \
                        --network=host \
                        -v "$PWD:/tests" \
                        -w /tests \
                        python:3.10-slim bash -c "
                            apt-get update && apt-get install -y wget unzip curl gnupg && \
                            curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
                            echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' > /etc/apt/sources.list.d/google-chrome.list && \
                            apt-get update && apt-get install -y google-chrome-stable && \
                            pip install selenium webdriver-manager && \
                            python test_cases.py
                        "
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            mail to: 'qasimalik@gmail.com',
                 subject: "✅ Jenkins Pipeline Success - Todo App",
                 body: "Build + Test completed successfully.\n\nRegards,\nJenkins"
        }
        failure {
            mail to: 'qasimalik@gmail.com',
                 subject: "❌ Jenkins Pipeline Failed - Todo App",
                 body: "Pipeline failed. Please check Jenkins console for errors.\n\nRegards,\nJenkins"
        }
    }
}
