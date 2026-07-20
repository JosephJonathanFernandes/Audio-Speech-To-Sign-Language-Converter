from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from src.core.services.nlp_service import NLPService

# Initialize the NLP service
nlp_service = NLPService()

@login_required(login_url="login")
def animation_view(request):
    if request.method == 'POST':
        text = request.POST.get('sen', '')
        
        # Process text using the NLP service
        words = nlp_service.process_text(text)
        
        if not words and text:
            messages.error(request, "Error processing text. Please try again with different words.")
        
        return render(request, 'animation.html', {'words': words, 'text': text})
    else:
        return render(request, 'animation.html')
