node('small') {
    checkout scm
    stage('build') {
        sh 'docker build . -t test'
    }

}
