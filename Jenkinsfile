pipeline {
    agent any

    stages {

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t ci-demo .'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running tests inside container...'
                sh 'docker run ci-demo'
            }
        }
    }
}