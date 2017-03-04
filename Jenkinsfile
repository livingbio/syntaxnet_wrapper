node('small') {
    checkout scm
    stage('Build') {
        docker.build('jenkins:syntaxnet')
    }

    stage('Test'){
        withDockerContainer('jenkins:syntaxnet') {
            sh 'python test.py'
        }
    }

    stage('Deploy') {
        
		withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'dockerhub', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD']]) {
			sh "docker login --password=${PASSWORD} --username=${USERNAME}"
			sh "docker pull gliacloud/syntaxnet"
			def now = new Date()
			def key = now.format("yyyyMMdd-HH", TimeZone.getTimeZone('UTC'))
			sh "docker tag gliacloud/syntaxnet gliacloud/syntaxnet:" + key
			sh "docker tag jenkins:syntaxnet gliacloud/base_images:syntaxnet"
			sh "docker push gliacloud/syntaxnet"
			sh "docker push gliacloud/syntaxnet:" + key
		}
    }
}
