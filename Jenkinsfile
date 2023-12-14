// Define an empty map for storing remote SSH connection parameters
def remote = [:]

pipeline {

    agent any

    environment {
        server_name = credentials('melisa_name')
        server_host = credentials('melisa_host')
        ssh_key = credentials('melisa_devops')
    }

    stages {
        stage('Ssh to connect bigelow server') {
            steps {
                script {
                    // Set up remote SSH connection parameters
                    remote.allowAnyHosts = true
                    remote.identityFile = ssh_key
                    remote.user = ssh_key_USR
                    remote.name = server_name
                    remote.host = server_host
                    
                }
            }
        }
        stage('Download latest release and create enviroment') {
            steps {
                script {
                    sshCommand remote: remote, command: """
                        cd /var/www/melisa
                        if [ ! -d admin ]; then
                            mkdir ./admin
                        fi
                        cd /var/www/melisa/admin
                        rm -rf env
                        rm -rf src
                        kill -9 \$(lsof -t -i:5003)
                        curl -LOk https://github.com/CIAT-DAPA/melisa_forms/releases/latest/download/release_melisa_admin.zip
                        unzip -o release_melisa_admin.zip
                        rm -fr release_melisa_admin.zip
                        python3 -m venv env
                    """
                }
            }
        }
        stage(' activate enviroment and install requirements') {
            steps {
                script {
                    sshCommand remote: remote, command: """
                        cd /var/www/melisa/admin
                        source env/bin/activate
                        cd src
                        pip install -r requirements.txt
                    """
                }
            }
        }
        stage('Init admin') {
            steps {
                script {
                    sshCommand remote: remote, command: """
                        cd /var/www/melisa/admin
                        source env/bin/activate
                        cd src
                        export DEBUG=False
                        export MELISA_ADMIN_PORT=5003
                        export CONNECTION_DB=mongodb://localhost:27017/melisa
                        export CONNECTION_DB2=mongodb://localhost:27017/aclimate_db
                        export HOST=0.0.0.0
                        nohup python3 app.py > log.txt 2>&1 &
                    """
                }
            }
        }       
    }
    
    post {
        failure {
            script {
                echo 'fail'
            }
        }

        success {
            script {
                echo 'everything went very well, admin in production'
            }
        }
    }
 
}