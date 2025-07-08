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
                    def authorEmail = sh(
                        script: "git log -1 --pretty=format:'%ae'",
                        returnStdout: true
                    ).trim()
                    currentBuild.description = "Last commit by: ${authorEmail}"
                    if (authorEmail != env.INSTRUCTOR_EMAIL) {
                        currentBuild.result = 'SUCCESS'
                        error("Not instructor's commit. Skipping pipeline.")
                    }
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
            mail to: "${env.INSTRUCTOR_EMAIL}",
                 subject: "Jenkins Test Success: To-Do App",
                 body: "All tests passed. See attached log.",
                 attachLog: true
        }
        failure {
            mail to: "${env.INSTRUCTOR_EMAIL}",
                 subject: "Jenkins Test Failure: To-Do App",
                 body: "Some tests failed. See attached log.",
                 attachLog: true
        }
    }
} 
