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
                    & "C:\\nvm4w\\nodejs\\cdxgen.ps1" -o bom.json
                    
                    Write-Host "Sending to Dependency Track..."
                    $apiUrl = "http://your-dependency-track/api/v1/bom"
                    $apiKey = $DEPENDENCY_TRACK_API_KEY
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                powershell '''
                    $BuildDir = "lambda_build"
                    
                    if (Test-Path $BuildDir) {
                        Remove-Item $BuildDir -Recurse -Force
                    }
                    New-Item -ItemType Directory -Force -Path $BuildDir | Out-Null
                    
                    if (Test-Path "requirements.txt") {
                        Write-Host "Installing dependencies from requirements.txt into $BuildDir..."
                        pip install -r requirements.txt -t $BuildDir
                    } else {
                        Write-Host "No requirements.txt found. Skipping dependency installation."
                    }
                '''
            }
        }

        stage('Packaging (Build)') {
            steps {
                powershell '''
                    $SourceFile = "app.py"
                    $PackageName = "app.zip"
                    $BuildDir = "lambda_build"
                    
                    if (Test-Path $PackageName) {
                        Remove-Item $PackageName -Force
                    }
                    
                    Write-Host "Copying source code to build directory..."
                    Copy-Item -Path $SourceFile -Destination $BuildDir\
                    
                    Write-Host "Packaging everything for AWS Lambda..."
                    Compress-Archive -Path "$BuildDir\\*" -DestinationPath $PackageName -Force
                    
                    Write-Host "Package $PackageName successfully generated."
                '''
            }
        }

        stage('Deploy (Terraform)') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'aws-keys', passwordVariable: 'AWS_SECRET_ACCESS_KEY', usernameVariable: 'AWS_ACCESS_KEY_ID')]) {
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