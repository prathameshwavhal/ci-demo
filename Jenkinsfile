pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/prathameshwavhal/ci-demo'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ci-demo .'
            }
        }

        stage('Run Tests with Retry') {
            steps {
                script {
                    try {
                        sh 'docker run ci-demo'
                    } catch (err) {
                        echo "Test failed. Retrying..."
                        sh 'docker run ci-demo'
                    }
                }
            }
        }
    }
}