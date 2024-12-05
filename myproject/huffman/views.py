from django.shortcuts import render
from django.http import HttpResponse,FileResponse
from django.core.files.storage import default_storage
from .huffman import HuffmanCoding  # Updated import
import os
from django.conf import settings

def encode(request):
    download_url = None  # Initialize download URL variable
    
    if request.method == "POST":
        uploaded_file = request.FILES['file']
        
        # Save uploaded file to the location defined by MEDIA_ROOT
        input_path = os.path.join(settings.MEDIA_ROOT, 'uploads', uploaded_file.name)
        
        # Save the uploaded file
        with open(input_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        # Compress the file using Huffman coding
        compressed_file = "compressed.huff"
        huffman = HuffmanCoding()
        huffman.compress(input_path, compressed_file)

        # Provide a download link to the user
        download_url = os.path.join(settings.MEDIA_URL, "downloads", compressed_file)

    return render(request, 'html/encode.html', {'download_url': download_url})

def decode(request):
    download_url = None  # Initialize download URL variable
    
    if request.method == "POST":
        uploaded_file = request.FILES['file']
        
        # Ensure the uploads directory exists
        uploads_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
        os.makedirs(uploads_dir, exist_ok=True)  # Create the directory if it doesn't exist
        
        # Save uploaded file to the uploads directory
        input_path = os.path.join(uploads_dir, uploaded_file.name)
        with open(input_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        # Decompress the file using Huffman coding
        decompressed_file = "decompressed.txt"
        huffman = HuffmanCoding()
        output_path = os.path.join(settings.MEDIA_ROOT, "downloads", decompressed_file)
        huffman.decompress(input_path, decompressed_file)

        # Provide a download link to the user
        download_url = os.path.join(settings.MEDIA_URL, "downloads", decompressed_file)

    return render(request, 'html/decode.html', {'download_url': download_url})


def downloadEn(request):
    file = os.path.join(settings.BASE_DIR,'media/downloads/compressed.huff')
    fileOpen = open(file,'rb')

    return FileResponse(fileOpen)
    #myproject\media\downloads\compressed.huff

def downloadDe(request):
    file = os.path.join(settings.BASE_DIR,'downloads/decompressed.txt')
    fileOpen = open(file,'rb')
    #myproject\downloads\decompressed.txt
    return FileResponse(fileOpen)