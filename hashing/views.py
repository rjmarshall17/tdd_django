from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import HashForm
from .models import Hash
import hashlib


def home(request):
    if request.method == 'POST':
        filled_form = HashForm(request.POST)
        if filled_form.is_valid():
            text = filled_form.cleaned_data.get('text')
            text_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
            try:
                Hash.objects.get(hash=text_hash)
            except Hash.DoesNotExist:
                hash = Hash()
                hash.text = text
                hash.hash = text_hash
                hash.save()
            return redirect('hash', hash=text_hash)
    form = HashForm()
    return render(request, 'hashing/home.html', {'form': form})

def hash(request, hash):
    my_hash = Hash.objects.get(hash=hash)
    return render(request, 'hashing/hash.html', {'hash': my_hash})

def quickhash(request):
    text = request.GET['text']
    return JsonResponse({'hash': hashlib.sha256(text.encode('utf-8')).hexdigest()})
