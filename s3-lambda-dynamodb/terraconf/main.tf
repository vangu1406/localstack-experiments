resource "aws_s3_bucket" "my_bucket" {
  bucket = "my-bucket"
}


resource "aws_lambda_function" "my_func" {
  filename      = "my-func.zip"
  role = aws_iam_role.lambda_role.arn
  function_name = "my-func"
  handler       = "my-func.handler"
  runtime = "python3.8"
}


resource "aws_dynamodb_table" "my_dynamotable" {
  name           = "my-dynamotable"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"
  range_key      = "filename"
  attribute {
    name = "id"
    type = "S"
  }

  attribute {
    name = "filename"
    type = "S"
  }

}

resource "aws_s3_bucket_notification" "aws_lambda_trigger" {
  bucket = "${aws_s3_bucket.my_bucket.id}"
  lambda_function {
    lambda_function_arn = "${aws_lambda_function.my_func.arn}"
    events              = ["s3:ObjectCreated:*"]

  }
  depends_on = [aws_lambda_permission.example]
}


resource "aws_lambda_permission" "example" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = "my-func"
  principal     = "s3.amazonaws.com"
  source_arn    = "arn:aws:s3:::${aws_s3_bucket.my_bucket.id}"
}


resource "aws_iam_role" "lambda_role" {
  name = "lambda-role-name"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "*"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "lambda_iam_policy" {
  name = "lambda-iam-policy-name"
  role = "${aws_iam_role.lambda_role.id}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Stmt1687200984534",
      "Action": "*",
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}
