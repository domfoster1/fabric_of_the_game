from django.shortcuts import render

"""Display the user's shirt collection."""

def my_collection(request):
  
    return render(request, 'my_collection/collection.html')