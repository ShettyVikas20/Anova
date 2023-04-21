from django.shortcuts import render
import json
import requests
from google.oauth2.credentials import Credentials
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django import forms
from googleapiclient.errors import HttpError
import io
import google_auth_oauthlib
from fund import settings

class FileUploadForm(forms.Form):
    file = forms.FileField()

def file_upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the uploaded file
            file = request.FILES['file']
            # Call a function to upload the file to Google Drive
            upload_file_to_drive(file)
            return HttpResponseRedirect(reverse('file_upload_success'))
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})

def file_upload_success(request):
    return render(request, 'file_upload_success.html')

def upload_file_to_drive(file):
    # Load the client ID and client secret from a file or environment variables
    # These should not be hard-coded in your code
    #client_id = client_id 
    #client_secret = client_secret

    # Build the credentials object using the OAuth2 flow
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_config(
        {'client_id': settings.client_id, 'client_secret': settings.client_secret},
        scopes=['https://www.googleapis.com/auth/drive.file'])
    creds = flow.run_local_server(port=0)

    # Create a Drive API client
    service = build('drive', 'v3', credentials=creds)

    # Define the metadata for the new file
    file_metadata = {
        'name': file.name,
        'parents': ['1SradRZBBp_cFiBxf6MOmZmV9U-glj54_']
    }

    # Create the new file and upload the contents
    try:
        media = io.BytesIO(file.read())
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print('File ID: %s' % file.get('id'))
    except HttpError as error:
        print('An error occurred: %s' % error)
        file = None

    return file.get('id')