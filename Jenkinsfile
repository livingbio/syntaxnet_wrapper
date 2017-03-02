node('small') {
    checkout scm
    stage('build') {
        docker.build('jenkins:syntaxnet')
    }

    stage('check'){
        withDockerContainer('jenkins:syntaxnet') {
            sh 'python test.py'
        }
    }

    stage('push') {
    	docker.withRegistry("https://565110903685.dkr.ecr.us-west-2.amazonaws.com/jenkins", "ecr:us-west-2:aws") {
  			docker.image("jenkins:syntaxnet").push()
		}
    }
}
