pipeline {
    agent any

    environment {
        AUTHOR_EMAIL = sh(script: "git log -1 --pretty=format:'%ae'", returnStdout: true).trim()
    }

    stages {
        stage('Clone') {
            steps {
                git branch: 'main', url: 'https://github.com/MemoonaIshfaq/todo-react-pipeline.git'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker-compose -f docker-compose.yml up --build --abort-on-container-exit test-runner'
            }
        }

        stage('Deploy App') {
            steps {
                sh 'docker-compose -f docker-compose.yml up -d react-app'
            }
        }
    }

    post {
        always {
            script {
                def authorEmail = sh(script: "git log -1 --pretty=format:'%ae'", returnStdout: true).trim()
                echo "Commit author email: ${authorEmail}"
                
                if (authorEmail == "qasimalik@gmail.com") {
                    emailext(
                        subject: "🧪 Jenkins Test Results for Instructor",
                        body: "Tests finished. View Jenkins Build: ${env.BUILD_URL}",
                        to: 'qasimalik@gmail.com'
                    )
                } else {
                    echo "No email sent. Commit not made by instructor."
                }
            }
        }
    }
}
