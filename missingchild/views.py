from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.conf import settings
import os
import cv2
import numpy as np
import insightface

# import settings
from django.core.mail import send_mail
from .forms import ReportUploadForm, MissingChildReportForm
from .models import ReportUpload, MissingChildReport

# ✅ Global face model
face_model = None


def load_face_model():
    """Load InsightFace model only once, properly handling download."""
    global face_model
    if face_model is None:
        try:
            print("⏳ Loading InsightFace model (buffalo_l)...")
            face_model = insightface.app.FaceAnalysis(name="buffalo_l", providers=['CPUExecutionProvider'])
            face_model.prepare(ctx_id=0)  # CPU mode, automatically downloads if missing
            print("✅ InsightFace model loaded successfully.")
        except Exception as e:
            print("❌ Failed to load InsightFace model:", e)
            face_model = None
    return face_model


def get_embedding(image_path):
    """Extract embedding from an image path."""
    model = load_face_model()
    if model is None:
        return None, None

    img = cv2.imread(image_path)
    if img is None:
        return None, None

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faces = model.get(img_rgb)
    if not faces:
        return None, None

    embedding = faces[0].normed_embedding.astype(np.float32)
    age = getattr(faces[0], "age", None)
    return embedding, age


def compare_faces(embedding1, embedding2, threshold=0.35):
    """Compare two embeddings using cosine similarity."""
    if embedding1 is None or embedding2 is None:
        return False, None
    similarity = float(np.dot(embedding1, embedding2))
    return similarity > threshold, similarity


from django.core.mail import EmailMessage
from django.conf import settings
import os

def report_upload(request):
    """Handle missing child report uploads and perform face matching with location tracking."""
    result = None
    matched_child = None
    uploaded_image_url = None
    matched_image_url = None

    if request.method == 'POST':
        form = ReportUploadForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            # Capture location data
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            address = request.POST.get('address')

            report.latitude = latitude
            report.longitude = longitude
            report.address = address
            report.save()

            image_path = report.image.path
            uploaded_image_url = report.image.url

            # Extract face embedding
            embedding, age = get_embedding(image_path)
            if embedding is not None:
                report.embedding = embedding.tobytes()
                report.save()

                # Iterate through missing child reports to find match
                for child in MissingChildReport.objects.all():
                    if child.child_photo and os.path.exists(child.child_photo.path):
                        child_embedding, _ = get_embedding(child.child_photo.path)
                        if child_embedding is not None:
                            match, score = compare_faces(embedding, child_embedding)
                            if match:
                                matched_child = child
                                matched_image_url = child.child_photo.url
                                result = f"✅ Match Found! (Similarity: {score:.2f})"

                                # --- ADMIN EMAIL ---
                                admin_email = "prabhunandan016@gmail.com"
                                admin_subject = "🚨 Match Found in Missing Child Database"
                                admin_message = (
                                    f"A possible match has been found!\n\n"
                                    f"Child Name: {child.child_name}\n"
                                    f"Age: {child.age}\n"
                                    f"Last Seen Area: {child.last_area}\n\n"
                                    f"📍 Upload Location Details:\n"
                                    f"Address: {address}\n"
                                    f"Latitude: {latitude}\n"
                                    f"Longitude: {longitude}\n\n"
                                    f"Please verify the details in the admin dashboard.\n\n"
                                    f"— Missing Child Detection System"
                                )

                                admin_mail = EmailMessage(
                                    admin_subject,
                                    admin_message,
                                    settings.DEFAULT_FROM_EMAIL,
                                    [admin_email],
                                )

                                # Attach both photos (if available)
                                if os.path.exists(image_path):
                                    admin_mail.attach_file(image_path)
                                if child.child_photo and os.path.exists(child.child_photo.path):
                                    admin_mail.attach_file(child.child_photo.path)

                                admin_mail.send(fail_silently=False)
                                print(f"📧 Admin notification sent to {admin_email}")

                                # --- REPORTER EMAIL ---
                                reporter_email = child.email.strip() if child.email else None
                                if reporter_email:
                                    reporter_subject = "✅ Possible Match Found for Missing Child"
                                    reporter_message = (
                                        f"Dear {child.reporter_name},\n\n"
                                        f"Our system has found a possible match related to the missing child you reported.\n\n"
                                        f"Child Name: {child.child_name}\n"
                                        f"Approx. Age: {child.age}\n"
                                        f"Last Seen Area: {child.last_area}\n\n"
                                        f"📍 Upload Location:\n"
                                        f"Address: {address}\n"
                                        f"Latitude: {latitude}\n"
                                        f"Longitude: {longitude}\n\n"
                                        f"Our team has been notified and will review the match shortly.\n"
                                        f"Thank you for helping us in the search for missing children.\n\n"
                                        f"— Missing Child Detection System"
                                    )

                                    reporter_mail = EmailMessage(
                                        reporter_subject,
                                        reporter_message,
                                        settings.DEFAULT_FROM_EMAIL,
                                        [reporter_email],
                                    )

                                    # Attach both photos for reporter as well
                                    if os.path.exists(image_path):
                                        reporter_mail.attach_file(image_path)
                                    if child.child_photo and os.path.exists(child.child_photo.path):
                                        reporter_mail.attach_file(child.child_photo.path)

                                    reporter_mail.send(fail_silently=False)
                                    print(f"📧 Email sent to reporter: {reporter_email}")
                                else:
                                    print("⚠️ Reporter email missing. Skipping reporter email.")

                                break  # Stop after the first match

                if not matched_child:
                    result = "❌ No match found in database."
            else:
                result = "⚠️ No face detected in uploaded image."
        else:
            result = "⚠️ Invalid form submission."
    else:
        form = ReportUploadForm()

    return render(
        request,
        'report_upload.html',
        {
            'form': form,
            'result': result,
            'matched_child': matched_child,
            'uploaded_image_url': uploaded_image_url,
            'matched_image_url': matched_image_url
        }
    )

def report_success(request):
    return render(request, 'report_success.html')


def homepage(request):
    return render(request, 'home.html')


from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
# ... other imports (os, cv2, numpy, etc.)

def missingchildreport(request):
    """Handle Missing Child Report form submission."""
    if request.method == "POST":
        form_data = request.POST
        files = request.FILES

        child_photo = files.get('child_photo')
        if not child_photo:
            message = "⚠️ Please upload the child's photo."
            return render(request, 'missingchildreport.html', {'message': message})

        # --- FIX: Read the file content once for OpenCV, then reset the pointer ---
        
        # 1. Read the file content for OpenCV/face detection processing
        file_bytes = child_photo.read()
        
        # 2. CRITICAL: Reset the file pointer to the beginning (0)
        # This allows the model field to read the file contents later.
        child_photo.seek(0)
        
        # 3. Decode the file bytes for potential OpenCV use (face detection/validation)
        np_arr = np.frombuffer(file_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Save record
        new_record = MissingChildReport(
            child_name=form_data.get('child_name'),
            age=form_data.get('age'),
            last_area=form_data.get('last_area'),
            moles=form_data.get('moles'),
            dress_color=form_data.get('dress_color'),
            
            # --- CRITICAL CHANGE: Assign the uploaded File object directly ---
            child_photo=child_photo, # Assign the file object here
            
            reporter_name=form_data.get('reporter_name'),
            relation=form_data.get('relation'),
            phone=form_data.get('phone'),
            email=form_data.get('email'),
            
            # Assign other files directly
            aadhaar_photo=files.get('aadhaar_photo'),
            fir_copy=files.get('fir_copy')
        )

        # 4. Save the record and its files
        # Django automatically saves 'child_photo' since the file object was assigned above.
        # Removed the problematic line: new_record.child_photo.save(child_photo.name, ContentFile(child_photo.read())) 
        new_record.save() 

        return render(request, 'report_success.html')

    return render(request, 'missingchildreport.html')


def missingdata(request):
    """Display all missing child reports with optional status filter."""
    status_filter = request.GET.get('status', 'all')
    if status_filter == 'missing':
        reports = MissingChildReport.objects.filter(status='missing').order_by('-submitted_at')
    elif status_filter == 'found':
        reports = MissingChildReport.objects.filter(status='found').order_by('-submitted_at')
    else:
        reports = MissingChildReport.objects.all().order_by('-submitted_at')

    return render(request, 'missingdata.html', {
        'children': reports,
        'status_filter': status_filter
    })
