
from django import forms
from .models import ReportUpload

class ReportUploadForm(forms.ModelForm):
    class Meta:
        model = ReportUpload
        fields = ['image', 'uploader_name', 'uploader_contact']

from .models import MissingChildReport

class MissingChildReportForm(forms.ModelForm):
    class Meta:
        model = MissingChildReport
        fields = '__all__'
