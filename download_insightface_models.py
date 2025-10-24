import os
import insightface
import cv2
import numpy as np

# ------------------------------
# Set InsightFace model directory
# ------------------------------
os.environ["INSIGHTFACE_MODEL_DIR"] = r"C:\Users\prabh\.insightface\models"

# ------------------------------
# Initialize face analysis model
# ------------------------------
face_model = insightface.app.FaceAnalysis(name="buffalo_l")
face_model.prepare(ctx_id=0)  # Use CPU; change to ctx_id=1 for GPU if available
print("✅ InsightFace model ready!")

# ------------------------------
# Load the image
# ------------------------------
image_path = r"C:\Users\prabh\missingchilddetection\missingchild\media\child_photos/jp.jpg"
img = cv2.imread(image_path)

if img is None:
    raise FileNotFoundError(f"⚠️ Could not read the image at path: {image_path}. Check path and file integrity.")

# ------------------------------
# Detect faces
# ------------------------------
faces = face_model.get(img)

if len(faces) == 0:
    print("⚠️ No face detected.")
else:
    print(f"Detected {len(faces)} face(s).")
    
    for i, face in enumerate(faces):
        embedding = face.normed_embedding.astype(np.float32)
        print(f"Face {i+1} embedding shape: {embedding.shape}")
        # Optional: draw bounding boxes and landmarks
        bbox = face.bbox.astype(int)
        cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
        if hasattr(face, "kps"):  # keypoints
            for (x, y) in face.kps.astype(int):
                cv2.circle(img, (x, y), 2, (0, 0, 255), -1)

    # Optional: show image with detections
    cv2.imshow("Faces", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
