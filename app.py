from flask import Flask, request, render_template, redirect, url_for, Response
import boto3
from config import S3_BUCKET

app = Flask(__name__)


@app.route("/")
def home():
    S3_resource = boto3.resource("s3")
    bucket = S3_resource.Bucket(S3_BUCKET)
    summaries = bucket.objects.all()
    return render_template("index.html", bucket=bucket, files=summaries)


@app.route("/upload", methods=["POST"])
def upload_files():
    file = request.files["file"]

    S3_resource = boto3.resource("s3")
    bucket = S3_resource.Bucket(S3_BUCKET)
    bucket.Object(file.filename).put(Body=file)

    return redirect(url_for("home"))


@app.route("/retrieve", methods=["POST"])
def get_file():
    key = request.form["key"]

    S3_resource = boto3.resource("s3")
    bucket = S3_resource.Bucket(S3_BUCKET)

    file_object = bucket.Object(key).get()
    return render_template("file.html",
                           file_text=file_object["Body"].read(),
                           key=key
                           )


@app.route("/download", methods=["POST"])
def download():
    key = request.form["key"]

    S3_resource = boto3.resource("s3")
    bucket = S3_resource.Bucket(S3_BUCKET)

    file_object = bucket.Object(key).get()
    return Response(
        file_object["Body"].read(),
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment;filename={}".format(key)},
    )


@app.route("/update", methods=["POST"])
def update():
    file = request.files["file"]
    key = request.form["key"]

    S3_resource = boto3.resource("s3")
    bucket = S3_resource.Bucket(S3_BUCKET)
    bucket.Object(key).put(Body=file)

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
