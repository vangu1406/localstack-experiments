import boto3
from flask import Flask, request, render_template
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

ENDPOINT_URL_ = 'http://localstack:4566'
AWS_ACCESS_KEY = "test"
AWS_SECRET_KEY = "test"
S3_BUCKET_NAME = "my-bucket"

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('frontend.html')


@app.route('/upload', methods=["POST"])
def upload_file():
    try:
        f = request.files["file"]
        file_path = os.path.join("/tmp", f.filename)
        f.save(file_path)

        s3client = boto3.client(
            "s3",
            region_name="us-east-1",
            endpoint_url=ENDPOINT_URL_,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )

        s3client.upload_file(file_path, S3_BUCKET_NAME, f.filename)
        logger.info(f"File {f.filename} successfully uploaded to S3")

        os.remove(file_path)

        return "File uploaded successfully"

    except Exception as e:
        logger.error(f"Error while uploading file: {str(e)}")
        return f"Error while uploading file: {str(e)}", 500


@app.route('/view')
def view():
    try:
        dbclient = boto3.client(
            "dynamodb",
            region_name="us-east-1",
            endpoint_url=ENDPOINT_URL_,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )

        jresponsearray = dbclient.scan(TableName="my-dynamotable")
        itemlist = jresponsearray.get("Items", [])

        jsonlist = [item["filename"]["S"] for item in itemlist]

        return render_template("view.html", jsonlist=jsonlist)

    except Exception as e:
        logger.error(f"Error while displaying items from DynamoDB: {str(e)}")
        return f"Error while displaying items: {str(e)}", 500


if __name__ == "__main__":
    app.run(debug=True)
