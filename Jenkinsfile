pipeline {
    agent any

    stages {
        stage('Static Security Analysis (SAST)') {
            steps {
                powershell '& "C:\\Program Files\\Python314\\Scripts\\semgrep.exe" scan --config auto'
            }
        }

        stage('Software Composition Analysis (SCA)') {
            steps {
                powershell '''
                    Write-Host "Generating SBOM with cdxgen..."
                    cdxgen -o bom.json
                    
                    Write-Host "Sending to Dependency Track..."
                    $apiUrl = "http://your-dependency-track/api/v1/bom"
                    $apiKey = $DEPENDENCY_TRACK_API_KEY
                '''
            }
        }

        stage('Packaging (Build)') {
            steps {
                powershell '''
                    $SourceFile = "app.py"
                    $PackageName = "app.zip"
                    
                    if (Test-Path $PackageName) {
                        Remove-Item $PackageName -Force
                    }
                    
                    Compress-Archive -Path $SourceFile -DestinationPath $PackageName -Force
                    Write-Host "Package $PackageName successfully generated."
                '''
            }
        }

        stage('Deploy (Terraform)') {
            steps {
                withCredentials([aws(credentialsId: 'aws-deploy-key', accessKeyVariable: 'AWS_ACCESS_KEY_ID', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    powershell '''
                        terraform init
                        terraform apply -auto-approve
                    '''
                }
            }
        }
    }
    
    post {
        always {
            powershell 'Write-Host "DevSecOps pipeline finished."'
        }
    }
}