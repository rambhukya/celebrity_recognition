from flask import Flask, render_template, request
import boto3
import json
app = Flask(__name__)
from werkzeug.utils import secure_filename

ak="ASIA4RW7ZWQXLZRAQJU6"
ask="zorBl98PMnCL3M3rqBPpgrT5gJoySDB1y85QJJgO"
at="FwoGZXIvYXdzEM///////////wEaDCKF2GE4+Btdth3HsSLFAX17QWdeoyf8cv70J935yMoYjn6Edd2pNdXhjFIBcjghblggBN4lLqXxA24miWlxv2zoeojZW98Ud6W6ACOQJpj+6NvFHFuspP7QMJ3dUxwUOJ6VwhOHF+Gln2NXODpp4dUSBm8CBjzkroxXjLOg/Xp4LaeG8J/tI0i/vwCJcq+jibEuPDXucyVsp9nYTn2cK0yQdo2G7RwghD9JqTsRWXXoU/ngtEo1wtP+Dt9OlrNEWmWaayprQ37zzTSPKP9x5612gfv8KNb94JkGMi0neyoxHUyfRrdxwzF63YjTOSs2bee4USPXAc3lfLB2vI6+B51xeDSKTm2xxoA="

s3 = boto3.client(
    's3',
    aws_access_key_id=ak,
    aws_secret_access_key=ask,
    aws_session_token=at
)
rek = boto3.client('rekognition',
    aws_access_key_id=ak,
    aws_secret_access_key=ask,
    aws_session_token=at
)
BUCKET_NAME='test300922'

@app.route('/')  
def home():
    return render_template("index.html")

@app.route('/upload',methods=['post'])
def upload():
    if request.method == 'POST':
        img = request.files['file']
        if img:
                filename = secure_filename(img.filename)
                img.save(filename)
                s3.upload_file(
                    Bucket = BUCKET_NAME,
                    Filename=filename,
                    Key = filename
                )
                response = rek.recognize_celebrities(
                 Image={
                    'S3Object': {
                    'Bucket': BUCKET_NAME,
                    'Name': filename,
                }
                })
                msg = "Upload Done ! "
                test = response
                s1=json.dumps(test)
                object=json.loads(s1)
                s2=(object['CelebrityFaces'])
                s4=s2[0]
                s5=s4['Name']

    return render_template("index.html",msg =s5 )




if __name__ == "__main__":
    
    app.run(debug=True)

