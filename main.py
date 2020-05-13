# -*- coding: utf-8 -*-


'''
USER VARIABLES
'''
# AWS Programatic Credentials: Access key id, secret and region
AWS_ACCESS_KEY_ID = 'xxxxxxxxxxxxx'
AWS_ACCESS_KEY_SECRET = 'xxxxxxxxxxxxxxxxxxxxxx'
# Region name: eu-west-1 (Ireland), eu-west-3 (Paris), etc...
AWS_REGION_NAME = 'eu-west-3'

# Filter on specified namespace/image list
# AWS ECR Namespace/Image dictionary: {'<namespaceName>': ['imageName']}
#   Example: {'germainlefebvre4': ['hello-world']}
REGISTRIES_DICT = {
    'germainlefebvre4': [
        'hello-world'
    ]
}

# Maximum number of tags retrieved from AWS ECR: <integer>
#   Example: 1, 20, 50
RELEASES_MAX = 50

# Debug mode
DEBUG_MODE = True


'''
Main function
'''
# Load dependencies
from flask import Flask, jsonify
from flask_api import status
import logging
import sys
import os
import boto3
import json

# Configure logging
root = logging.getLogger()
root.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
root.addHandler(handler)
# Override boto3 logging
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('nose').setLevel(logging.CRITICAL)

# Initialize flask
app = Flask(__name__)
app.url_map.strict_slashes = False



'''
Technical routes
'''
# Remove trailing slash from URLs
@app.before_request
def clear_trailing():
    from flask import redirect, request

    rp = request.path
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])

'''
Applicative routes
'''
@app.route('/', methods=['GET'])
def getNamespaces():
    return jsonify(
        msg="Please select an authorized registry namespace name.",
        registries=list(REGISTRIES_DICT.keys())
    ), status.HTTP_404_NOT_FOUND

@app.route('/<string:namespaceName>', methods=['GET'])
def getNamespaceImages(namespaceName):
    return jsonify(
        msg="Please select a image name into the namespace.",
        images=REGISTRIES_DICT.get(namespaceName)
    ), status.HTTP_404_NOT_FOUND

@app.route('/<string:namespaceName>/<string:imageName>')
def getNamespaceImageReleases(namespaceName, imageName):
    if imageName not in REGISTRIES_DICT.get(namespaceName):
        return jsonify(
            msg="Please provide a authorized image name.",
            images=REGISTRIES_DICT.get(namespaceName)
        ), status.HTTP_404_NOT_FOUND
    try:
        releases = awsEcrListImages(namespaceName, imageName)
        return jsonify(
            name=imageName,
            releases=releases
        ), status.HTTP_200_OK
    except:
        return jsonify(
            msg="Please provide a authorized image name.",
            images=REGISTRIES_DICT.get(namespaceName)
        ), status.HTTP_404_NOT_FOUND

'''
AWS functions
'''
def awsClientConnect():
    try:
        client = boto3.client(
            'ecr',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_ACCESS_KEY_SECRET,
            region_name=AWS_REGION_NAME,
        )

        return client
    except:
        return jsonify(
            error="An error occured on connecting to aws."
        ), HTTP_500_INTERNAL_SERVER_ERROR

def awsEcrListImages(namespaceName, imageName):
    try:
        client = awsClientConnect()
        response = client.list_images(
            repositoryName=f"{namespaceName}/{imageName}",
            maxResults=RELEASES_MAX,
            filter={
                'tagStatus': 'TAGGED'
            }
        )

        # Filter on image tag pattern
        # This will exclude all tags begging with 'commit-'
        # result = [x.get('imageTag') for x in response.get('imageIds') if 'commit-' not in x.get('imageTag')]
        
        result = response.get('imageIds')

        return sorted(result)
    except:
        return jsonify(
            error="An error occured on retrieving image list.",
        ), HTTP_500_INTERNAL_SERVER_ERROR


'''
Standalone python execution
'''
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=DEBUG_MODE)
