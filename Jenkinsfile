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

stage('Run Tests with Decision') {
    steps {
        script {

            def maxAttempts = 3
            def triedActions = []

            for (int attempt = 1; attempt <= maxAttempts; attempt++) {

                echo "======== Attempt ${attempt} ========"

                sh 'docker build -t ci-demo .'

                def status = sh(script: 'docker run ci-demo', returnStatus: true)

                if (status == 0) {
                    echo "✅ Success on attempt ${attempt}"
                    return
                }

                echo "❌ Failed on attempt ${attempt}"

                // call python decision system
                def action = sh(
                    script: "python3 decision.py test_failure ${triedActions.join(',')}",
                    returnStdout: true
                ).trim()

                echo "👉 Action chosen: ${action}"

                triedActions.add(action)

                // execute action
                if (action == "retry") {
                    echo "Retrying..."
                }
                else if (action == "reinstall") {
                    echo "Reinstalling..."
                    sh 'pip install -r requirements.txt || true'
                }
                else if (action == "clean") {
                    echo "Cleaning..."
                    sh 'docker system prune -f'
                }
            }

            error "🚨 Failed after ${maxAttempts} attempts"
        }
    }
}