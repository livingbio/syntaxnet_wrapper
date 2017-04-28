library 'common'

node('large'){
    base_build{
        name='syntaxnet
        test_script = {->
            sh 'py.test pyknp'
        }
        release = {->
            sh 'echo release'
            dockerhub.push_image(name)
        }
    }
}
