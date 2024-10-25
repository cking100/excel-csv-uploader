from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm
import pandas as pd
from django.core.files.storage import FileSystemStorage
from PIL import Image
import mimetypes

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            mime_type, _ = mimetypes.guess_type(file.name)

            # Check if the file is an image
            if mime_type and mime_type.startswith('image'):
                # Save and display the image
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                file_url = fs.url(filename)
                return render(request, 'upload.html', {'form': form, 'image_url': file_url})

            # Check if the file is a CSV or Excel file
            elif file.name.endswith('.csv'):
                data = pd.read_csv(file)
            elif file.name.endswith(('.xls', '.xlsx')):
                data = pd.read_excel(file)
            else:
                return render(request, 'upload.html', {'form': form, 'error': 'Unsupported file type'})

            # Process CSV/Excel data
            try:
                extracted_data = data[['Cust State', 'Cust Pin', 'DPD']]
                return render(request, 'upload.html', {'form': form, 'data': extracted_data.to_html()})
            except KeyError as e:
                return render(request, 'upload.html', {'form': form, 'error': f'Missing column: {e}'})
    else:
        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form})
