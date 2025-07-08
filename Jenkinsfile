pipeline {
    agent any

    environment {
        APP_IMAGE = 'memoona2/todo-react-app:latest'
        TEST_IMAGE = 'python:3.10-slim'
        INSTRUCTOR_EMAIL = 'qasimalik@gmail.com'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Commit Author') {
            steps {
                script {
                    env.AUTHOR_EMAIL = sh(
                        script: "git log -1 --pretty=format:'%ae'",
                        returnStdout: true
                    ).trim()
                    currentBuild.description = "Last commit by: ${env.AUTHOR_EMAIL}"
                }
            }
        }

        stage('Build App Image') {
            steps {
                sh 'docker build -t $APP_IMAGE .'
            }
        }

        stage('Run App Container') {
            steps {
                sh 'docker run -d --rm -p 3000:3000 --name todo-app $APP_IMAGE'
                sh 'sleep 10'
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                docker run --rm --network host \
                    -v $PWD/tests:/tests \
                    -v $PWD/requirements.txt:/requirements.txt \
                    $TEST_IMAGE /bin/bash -c "
                        pip install --no-cache-dir selenium webdriver-manager && \
                        pip install -r /requirements.txt || true && \
                        python /tests/test_todo_app.py > result.log 2>&1
                    "
                '''
            }
        }
    }

    post {
        always {
            sh 'docker stop todo-app || true'
        }

        success {
            script {
                if (env.AUTHOR_EMAIL == env.INSTRUCTOR_EMAIL) {
                    mail to: "${env.INSTRUCTOR_EMAIL}",
                         subject: "✅ Jenkins Test Success: To-Do App",
                         body: "All tests passed successfully."
                }
            }
        }

        failure {
            script {
                if (env.AUTHOR_EMAIL == env.INSTRUCTOR_EMAIL) {
                    mail to: "${env.INSTRUCTOR_EMAIL}",
                         subject: "❌ Jenkins Test Failure: To-Do App",
                         body: "Some tests failed. Please check the Jenkins logs for details."
                }
            }
        }
    }
}
