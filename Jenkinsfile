pipeline {
    agent any
    environment {
        APP_NAME = "test app name"
    } 
    stages {
        stage('Build Image' ) {
            steps {
        sh "echo ${env.APP_NAME}"
            }
        }
    }
}        