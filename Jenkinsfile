
pipeline {
    agent any

    stages {
        stage('Hello World') {
            steps {
                echo 'Pipeline berhasil dijalankan dari GitHub!'
            }
        }

        stage('Checkout') {
            steps {
                echo 'Kode sumber berhasil diambil dari repository.'
            }
        }

        stage('Check Docker') {
            steps {
                bat 'docker --version'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t project-jenkins:latest .'
            }
        }
    }
}
