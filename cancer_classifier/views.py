from django.shortcuts import render
from .forms import ImageUploadForm
import os
from django.conf import settings
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Chat, Conversation, ImageUpload
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
import json
from .models import SkinCondition, HealthTopic


# Load your Keras model once
model_path = os.path.join(settings.BASE_DIR, 'skin_lesion_classifier.h5')
model = load_model(model_path)

# Sample data structure for storing results (you may want to use a database in the future)
image_results = []  # This will store the recent image uploads and their results

def preprocess_image(img_path):
    """
    Preprocess the image for prediction.
    Adjust resizing and normalization based on your model training.
    """
    image = Image.open(img_path).convert('RGB')
    image = image.resize((224, 224))  
    image_array = np.array(image) / 255.0 
    image_array = np.expand_dims(image_array, axis=0)  # Shape: (1, 224, 224, 3)
    return image_array

@login_required
def predict_cancer(request):
    result = None
    cancer_type = None
    uploaded_image_url = None  # To send the uploaded image URL to the template

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded image
            img = form.cleaned_data['image']
            img_path = os.path.join(settings.MEDIA_ROOT, img.name)

            try:
                # Save the uploaded image to the media directory
                with open(img_path, 'wb+') as f:
                    for chunk in img.chunks():
                        f.write(chunk)

                # Preprocess the image for prediction
                image_array = preprocess_image(img_path)

                # Get model prediction
                prediction = model.predict(image_array)

                # If model output is a probability distribution (for multi-class)
                if prediction.shape[-1] > 1:
                    predicted_class = np.argmax(prediction[0])
                else:
                    # If output is binary (cancer or not)
                    predicted_class = 1 if prediction[0][0] > 0.5 else 0

                # Map class index to cancer type
                cancer_classes = {
                    0: 'Benign',
                    1: 'Malignant',
                }

                # Get the cancer type based on predicted class
                cancer_type = cancer_classes.get(predicted_class, "Unknown Type")
                result = 'Cancer Detected' if predicted_class != 0 else 'No Cancer'

                # If cancer is detected, check if it is benign or malignant
                if predicted_class != 0:  # Not benign
                    result = 'Cancer Detected'
                else:  # Benign
                    result = 'No Cancer'

                # Save the image and result to the database
                image_upload = ImageUpload.objects.create(
                    user=request.user,  # Ensure the image is linked to the logged-in user
                    image=img,  # Save the image directly from the form
                    result=result,
                    cancer_type=cancer_type,
                    timestamp=datetime.now()
                )

                # After saving, get the URL of the saved image
                uploaded_image_url = image_upload.image.url  # This is the correct way to get the URL

            except Exception as e:
                result = f"Error in model prediction: {e}"

    else:
        form = ImageUploadForm()

    return render(request, 'index.html', {
        'form': form,
        'result': result,
        'cancer_type': cancer_type,
        'uploaded_image_url': uploaded_image_url,
    })

class UserImagesView(LoginRequiredMixin, ListView):
    model = ImageUpload
    template_name = 'user_images.html'
    context_object_name = 'user_uploaded_images'

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return ImageUpload.objects.all().order_by('-timestamp')  # Admins see all
        return ImageUpload.objects.filter(user=self.request.user).order_by('-timestamp') 


def dashboard(request):
    # Collect the required statistics
    cancer_count = sum(1 for result in image_results if result['result'] == 'Cancer Detected')
    no_cancer_count = len(image_results) - cancer_count
    recent_images = image_results[-5:]

    # Prepare statistics for the dashboard (you could replace this with database queries in the future)
    statistics = {
        'total_images': len(image_results),
        'cancer_count': cancer_count,
        'no_cancer_count': no_cancer_count,
    }

    # Prepare data for the chart (line or bar chart)
    timestamps = [entry['timestamp'] for entry in image_results]
    cancer_data = [entry['predicted_class'] for entry in image_results]  

    # Send the data to the template for rendering the charts
    return render(request, 'dashboard.html', {
        'statistics': statistics,
        'recent_images': recent_images,
        'timestamps': timestamps,
        'cancer_data': cancer_data,
    })


def AboutUs(request):

    return render(request, 'about-us.html')


class ChatListView(LoginRequiredMixin, ListView):
    model = Conversation
    template_name = 'bot.html'  # Update with your actual template name
    context_object_name = 'conversations'

    def get_queryset(self):
        """
        Fetch and return all conversations for the current logged-in user,
        ordered by creation date (most recent first).
        """
        return Conversation.objects.filter(user=self.request.user).order_by('-created_at')

    def post(self, request, *args, **kwargs):
        """
        Handle saving the user's message and bot response.
        """
        if request.is_ajax():
            user_message = request.POST.get('user_message')
            conversation_id = request.POST.get('conversation_id')

            if user_message and conversation_id:
                # Ensure the conversation exists and is owned by the user
                try:
                    conversation = Conversation.objects.get(id=conversation_id, user=request.user)
                except Conversation.DoesNotExist:
                    return JsonResponse({'error': 'Conversation not found or not owned by the user'}, status=404)

                # Save the user message to the Chat model
                user_chat = Chat.objects.create(
                    user=request.user,
                    conversation=conversation,
                    text=user_message,
                    message_type='outgoing',
                    created_at=timezone.now()
                )

                # Generate a bot response (for example, using AI or API integration)
                bot_response = f"This is a generated bot response to: {user_message}"

                # Save the bot response to the Chat model
                bot_chat = Chat.objects.create(
                    user=request.user,  # You can use a "bot" user if you'd like
                    conversation=conversation,
                    text=bot_response,
                    message_type='incoming',
                    created_at=timezone.now()
                )

                # Return the user message and bot response as JSON
                return JsonResponse({
                    'user_message': user_message,
                    'bot_response': bot_response
                })

        return JsonResponse({'error': 'Invalid request'}, status=400)
    


class SkinConditionListView(ListView):
    model = SkinCondition
    template_name = 'skin_conditions/list.html'
    context_object_name = 'conditions'

class SkinConditionDetailView(DetailView):
    model = SkinCondition
    template_name = 'skin_conditions/detail.html'
    context_object_name = 'condition'


class HealthTopicListView(ListView):
    model = HealthTopic
    template_name = 'health_topics/list.html'
    context_object_name = 'topics'

class HealthTopicDetailView(DetailView):
    model = HealthTopic
    template_name = 'health_topics/detail.html'
    context_object_name = 'topic'
    