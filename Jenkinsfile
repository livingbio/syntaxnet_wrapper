node('small') {
    checkout scm
    stage('build') {
        docker.build('test')
    }
    stage('push') {
    	docker.withRegistry("https://565110903685.dkr.ecr.us-west-2.amazonaws.com/jenkins", "ecr:a-credential-id") {
  			docker.image("test").push()
		}
    }

}
