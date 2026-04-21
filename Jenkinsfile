// pipeline {
//     agent any

//     stages {

//         stage('Build Docker Image') {
//             steps {
//                 sh 'docker build -t ci-demo .'
//             }
//         }

//         stage('Run Tests with Retry') {
//             steps {
//                 script {
//                     try {
//                         sh 'docker run ci-demo'
//                     } catch (err) {
//                         echo "Test failed. Retrying..."
//                         sh 'docker run ci-demo'
//                     }
//                 }
//             }
//         }
//     }
// }

pipeline {
    agent any

    stages {

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ci-demo .'
            }
        }

        stage('Run Tests with Decision System') {
            steps {
                script {

                    def maxAttempts = 3
                    def attempt = 1
                    def success = false
                    def triedActions = []

                    while (attempt <= maxAttempts && !success) {

                        echo "Attempt ${attempt}"

                        sh 'docker build -t ci-demo .'
                        def status = sh(script: 'docker run ci-demo', returnStatus: true)

                        if (status == 0) {
                            echo "Pipeline succeeded"
                            success = true
                            break
                        }

                        echo "Pipeline failed"

                        def failure_type = "test_failure"

                        def action = sh(
                            script: "python decision.py ${failure_type} ${triedActions.join(',')}",
                            returnStdout: true
                        ).trim()

                        echo "Chosen action: ${action}"

                        triedActions.add(action)

                        if (action == "retry") {
                            echo "Retrying..."
                        }
                        else if (action == "reinstall") {
                            sh 'pip install -r requirements.txt || true'
                        }
                        else if (action == "clean") {
                            sh 'docker system prune -f'
                        }

                        writeFile file: "data_${attempt}.txt",
                        text: "${failure_type},${action},${status}"

                        attempt++
                    }

                    if (!success) {
                        error "Pipeline failed after ${maxAttempts} attempts"
                    }
                }
            }
        }
    }
}