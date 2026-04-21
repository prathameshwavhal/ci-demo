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

stage('Run Tests with Decision System') {
    steps {
        script {

            def maxAttempts = 3
            def attempt = 1
            def success = false
            def triedActions = []

            while (attempt <= maxAttempts && !success) {

                echo "Attempt ${attempt}"

                // Run container and capture status
                def status = sh(script: 'docker run ci-demo', returnStatus: true)

                if (status == 0) {
                    echo "Pipeline succeeded"
                    success = true
                    break
                }

                echo "Pipeline failed"

                // 🔥 STEP 1: Detect failure
                def failure_type = "test_failure"  // (we'll improve later)

                // 🔥 STEP 2: Get action from decision system
                def action = sh(
                    script: "python decision.py ${failure_type} ${triedActions.join(',')}",
                    returnStdout: true
                ).trim()

                echo "Chosen action: ${action}"

                // Track actions
                triedActions.add(action)

                // 🔥 STEP 3: Execute action
                if (action == "retry") {
                    echo "Retrying..."
                }
                else if (action == "reinstall") {
                    echo "Reinstalling dependencies..."
                    sh 'pip install -r requirements.txt || true'
                }
                else if (action == "clean") {
                    echo "Cleaning build..."
                    sh 'docker system prune -f'
                }

                // 🔥 STEP 4: Log data
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