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
        stage("Build Stahe (Docker)"){
            agent { label "build-server" }
            steps {
                sh "docker build -t ghcr.io/brovonthep/bj ."
            }
        }
    }
}        
