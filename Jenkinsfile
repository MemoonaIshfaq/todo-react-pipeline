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

        stage('Build and Run App using Docker Compose') {
            steps {
                script {
                    dir("${env.WORKSPACE}") {
                        sh 'docker-compose -p $COMPOSE_PROJECT_NAME -f docker-compose.yml up -d --build'
                        echo "Waiting for the app to fully start..."
                        sleep 15
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
                        -w /tests/tests \
                        python:3.10-slim bash -c "
                            apt-get update && apt-get install -y wget unzip curl gnupg && \
                            curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
                            echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' > /etc/apt/sources.list.d/google-chrome.list && \
                            apt-get update && apt-get install -y google-chrome-stable && \
                            pip install selenium webdriver-manager && \
                            python test_todo_app.py
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
                 subject: "✅ Jenkins Pipeline Success - Todo React App",
                 body: "Build and Selenium tests passed successfully. Review the Jenkins logs for more details."
        }
        failure {
            mail to: 'qasimalik@gmail.com',
                 subject: "❌ Jenkins Pipeline Failed - Todo React App",
                 body: "Pipeline failed during build or test. Please review logs for troubleshooting."
        }
    }
}
