from django.db import models


class MissingChildReport(models.Model):
    STATUS_CHOICES = [
        ('missing', 'Missing'),
        ('found', 'Found'),
    ]

    # Child Details
    child_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    last_area = models.CharField(max_length=200)
    moles = models.CharField(max_length=200)
    dress_color = models.CharField(max_length=50)
    child_photo = models.ImageField(upload_to='child_photos/')
    aadhaar_photo = models.ImageField(upload_to='aadhaar_photos/')
    fir_copy = models.FileField(upload_to='fir_copies/', blank=True, null=True)

    # Reporting Person Details
    reporter_name = models.CharField(max_length=100)
    relation = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=False)

    # New field to track status
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='missing')

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.child_name} reported by {self.reporter_name}"



class ReportUpload(models.Model):
    image = models.ImageField(upload_to='report_uploads/')
    uploader_name = models.CharField(max_length=100)
    uploader_contact = models.CharField(max_length=20)
    latitude = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    embedding = models.BinaryField(blank=True, null=True)  # store face embedding as bytes
    matched_child = models.ForeignKey(MissingChildReport, blank=True, null=True, on_delete=models.SET_NULL)
    reporter_email = models.EmailField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.uploader_name} uploaded on {self.uploaded_at}"

    
    
