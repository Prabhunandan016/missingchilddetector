🧒 Missing Child Detection System


🎥 Web Page Demo

The web application's functionality is demonstrated in this video: 
Google drive link : https://drive.google.com/drive/folders/1v45TMd8243Y7kd-F_pBOJjWs6QP8SNEp 


This web application, developed using the Django framework, facilitates the reporting and detection of missing children.

🚀 Key Features

Missing Child Reporting: Users can submit detailed reports via a dedicated form.

Data Management: A backend interface for administrators to manage and track reports.

Web Page Demo: A video demonstration of the web application is available via the link below.



📁 Code Structure

The project follows a standard Django project layout:

missingchild/       # Main Django project configuration (settings, URLs)
└── missingchild/   # Core Django application
    ├── models.py          # Database schema (MissingChildReport, ReportUpload)
    ├── views.py           # Logic for rendering pages & handling forms
    ├── urls.py            # URL mappings
    ├── forms.py           # Form input validation
    ├── admin.py           # Registers models with Django Admin
    └── migrations/        # Database schema history

templates/                  # HTML files for front-end pages
├── home.html               # Main landing page
├── missingchildreport.html # Form for filing missing child reports
├── navbar.html, footer.html # Reusable page components

static/                      # CSS, JS, and images
media/                       # User-uploaded files (photos, reports)
manage.py                     # Django management script
.gitignore                    # Files/folders ignored by Git (venv/, media/, db.sqlite3)
venv/                         # Python virtual environment (ignored by Git)

📧 Email Templates

The system sends automated emails in two scenarios:

1️⃣ Reporter Confirmation

Sent to the person filing the report to confirm successful submission.

Recipient: Reporter's Email (MissingChildReport.email)

Subject: Report Received: Missing Child Report Confirmation

Content:

Dear [Reporter Name],

Thank you for submitting a report on the missing child, [Child Name].
Your report has been successfully received and our team is currently reviewing the details.

Your Report ID is: [Report ID]

We will contact you immediately if any further information is needed or if there is an update on the case.

Thank you for your cooperation.

2️⃣ Admin Notification

Alerts administrators about a new report submission.

Recipient: Admin/Support Email

Subject: NEW Missing Child Report Awaiting Review

Content:

A new Missing Child Report has been submitted on the system.

Report ID: [Report ID]
Reported Child Name: [Child Name]
Submitted By: [Reporter Name] ([Reporter Email])

Please log in to the admin panel to review the submission and update its status.

💻 Getting Started
1️⃣ Clone the Repository
git clone [Your Repository URL]
cd missingchilddetection

2️⃣ Set up the Virtual Environment
python -m venv venv
.\venv\Scripts\activate    # On Windows PowerShell
# source venv/bin/activate  # On Linux/macOS

3️⃣ Install Dependencies
pip install -r requirements.txt
pip install django
pip install opencv-python
pip install insightface onnxruntime
python -m pip install --upgrade pip
pip install insightface onnxruntime --no-cache-dir
# (You may need to create this file first: pip freeze > requirements.txt)

4️⃣ Run Migrations
python manage.py makemigrations
python manage.py migrate

5️⃣ Run the Server
python manage.py runserver


The application will now be running at http://127.0.0.1:8000/

👤 Author

Prabhu Nandan
📧 Email: prabhunandan016@gmail.com


