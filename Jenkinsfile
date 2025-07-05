pipeline {
    agent any

    environment {
        EC2_IP = "http://54.197.18.201:3001"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/MemoonaIshfaq/todo-react-pipeline.git'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                sh '''
                    docker-compose -f docker-compose.yml up --build --abort-on-container-exit --exit-code-from test-runner test-runner
                '''
            }
        }

        stage('Cleanup Test Containers') {
            steps {
                sh 'docker-compose -f docker-compose.yml down'
            }
        }

        stage('Deploy React App') {
            steps {
                sh 'docker-compose -f docker-compose.yml up -d react-app'
            }
        }
    }

    post {
        always {
            script {
                def authorEmail = sh(script: "git log -1 --pretty=format:'%ae'", returnStdout: true).trim()
                if (authorEmail == "qasimalik@gmail.com") {
                    def log = currentBuild.rawBuild.getLog(999).join("\n")

                    emailext(
                        subject: "📋 Jenkins Test Results",
                        body: "${log}",
                        to: "qasimalik@gmail.com"
                    )
                } else {
                    echo "No email sent – commit not made by instructor."
                }
            }
        }
    }
}
