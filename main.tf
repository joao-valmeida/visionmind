provider "aws" {
  region = "us-east-1"
}

# 1. Banco de Dados (DynamoDB)
resource "aws_dynamodb_table" "metadata" {
  name         = "ImageMetadata"
  billing_mode = "PAY_PER_REQUEST" # FinOps: Paga apenas pelo que usar
  hash_key     = "imageId"

  attribute {
    name = "imageId"
    type = "S"
  }
}

# 2. Storage (S3 Bucket)
resource "aws_s3_bucket" "images" {
  bucket_prefix = "visionmind-raw-images-"
  force_destroy = true
}

# 3. Segurança: IAM Role (Least Privilege)
resource "aws_iam_role" "lambda_exec" {
  name = "visionmind_lambda_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

resource "aws_iam_policy" "lambda_policy" {
  name        = "visionmind_lambda_least_privilege"
  description = "IAM policy for VisionMind Lambda"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        # Permissão restrita apenas ao bucket do projeto
        Effect   = "Allow"
        Action   = ["s3:GetObject"]
        Resource = "${aws_s3_bucket.images.arn}/*"
      },
      {
        # O Rekognition não tem "resource specific ARN", então o '*' é obrigatório aqui
        Effect   = "Allow"
        Action   = ["rekognition:DetectLabels"]
        Resource = "*"
      },
      {
        # Permissão de escrita restrita apenas à tabela criada
        Effect   = "Allow"
        Action   = ["dynamodb:PutItem"]
        Resource = aws_dynamodb_table.metadata.arn
      },
      {
        # Permissão básica para gerar logs de observabilidade
        Effect   = "Allow"
        Action   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_attach" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

# 4. Computação (AWS Lambda)
resource "aws_lambda_function" "analyzer" {
  filename         = "app.zip" # O arquivo compactado gerado na esteira
  function_name    = "VisionMindAnalyzer"
  role             = aws_iam_role.lambda_exec.arn
  handler          = "app.lambda_handler"
  runtime          = "python3.10"
  timeout          = 30

  environment {
    variables = {
      DYNAMODB_TABLE = aws_dynamodb_table.metadata.name
    }
  }
}

# 5. Gatilho Orientado a Eventos (S3 -> Lambda)
resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.analyzer.arn
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.images.arn
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.images.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.analyzer.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_lambda_permission.allow_s3]
}