import org.jenkinsci.plugins.workflow.steps.FlowInterruptedException
pipeline {
    agent any
    environment {
       tgBot_id = credentials('kin_of_memes_bot_id')
       my_chat_id = credentials('my_chat_id')
    }
    stages {
        try{
       stage('get dependencies'){
            steps {
                sh 'python3 -m venv ./venv'
                sh '. venv/bin/activate'
                sh 'pip install -r requirements.txt'
                   }
        }
       stage('runBot'){
            steps {
                sh 'python3 main.py'
                   }
        }
        }
        catch(e){
        currentBuild.result = "FAILURE"
        println("catch exeption. currentBuild.result: ${currentBuild.result}")
        }
    }

    post {
    failure {
    sh  ("""
        curl -s -X POST https://api.telegram.org/bot${tgBot_id}/sendMessage -d chat_id=${my_chat_id} -d parse_mode=markdown -d text="*${env.JOB_NAME}* FAILED ${env.BUILD_URL}"
    """)
    }
    aborted {
    sh  ("""
        curl -s -X POST https://api.telegram.org/bot${tgBot_id}/sendMessage -d chat_id=${my_chat_id} -d parse_mode=markdown -d text="*${env.JOB_NAME}* ABORTED ${env.BUILD_URL}"
    """)
    }

        }
    }
