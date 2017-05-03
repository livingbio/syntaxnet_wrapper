library 'common'

node('large'){
    def project='syntaxnet'
    base_build{
        name=project
        test_script = {->
            sh 'python test.py'
        }
        release = {->
            dockerhub.push_image(project, base_build.release_version())
        }
    }
}
