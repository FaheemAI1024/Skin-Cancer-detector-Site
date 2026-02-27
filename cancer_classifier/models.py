from django.db import models
from django.contrib.auth.models import User

class ImageUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/')
    result = models.CharField(max_length=255)
    cancer_type = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image: {self.image.name} - {self.result}"

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, related_name='chats', on_delete=models.CASCADE)
    text = models.TextField()
    message_type = models.CharField(max_length=10, choices=[('incoming', 'Incoming'), ('outgoing', 'Outgoing')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.user.username} in {self.conversation.name} on {self.created_at}"
    


class SkinCondition(models.Model):
    CONDITION_TYPES = [
        ('benign', 'Benign'),
        ('malignant', 'Malignant'),
        ('precancerous', 'Precancerous'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    condition_type = models.CharField(max_length=20, choices=CONDITION_TYPES)
    image = models.ImageField(upload_to='skin_conditions/', blank=True, null=True)
    detected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class HealthTopic(models.Model):
    CATEGORY_CHOICES = [
        ('cancer', 'Cancer'),
        ('nutrition', 'Nutrition'),
        ('mental_health', 'Mental Health'),
        ('fitness', 'Fitness'),
        ('skin_health', 'Skin Health'),
        ('general', 'General'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='health_topics/', blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class HealthArticle(models.Model):
    CATEGORIES = [
        ('cancer', 'Cancer'),
        ('mental_health', 'Mental Health'),
        ('fitness', 'Fitness'),
        ('nutrition', 'Nutrition'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORIES)
    content = models.TextField()
    image = models.ImageField(upload_to='health_articles/', blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title