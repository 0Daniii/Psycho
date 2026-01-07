import cv2
import mediapipe as mp
import time
import os
import sys

# --- CONFIGURARE CĂI ---
# Adăugăm folderul curent la calea Python
sys.path.append(os.getcwd())

from modules.data_logger import DatabaseManager
from modules.feature_extractor import FeatureExtractor

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

def main():
    print("\n\n--- PORNIRE SISTEM (VERSIUNEA FINALA) ---")
    
    # 1. CONECTARE LA BAZA DE DATE
    try:
        db = DatabaseManager()
        subject_id = db.create_subject("Nano Test User")
        session_id = db.create_session(subject_id, "Nano Session")
        print("✅ BAZA DE DATE ESTE CONECTATĂ!")
    except Exception as e:
        print(f"❌ EROARE CRITICĂ LA DB: {e}")
        return

    # 2. INITIALIZARE EXTRACTOR
    extractor = FeatureExtractor()

    # 3. PORNIRE CAMERĂ
    cap = cv2.VideoCapture(0)
    
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        print("📷 Camera a pornit. Colectez date... (Apasă ESC pentru a salva și ieși)")
        
        while cap.isOpened():
            success, image = cap.read()
            if not success: continue

            # Procesare MediaPipe
            image.flags.writeable = False
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = holistic.process(image_rgb)
            
            # Revenire la BGR pentru desenare
            image.flags.writeable = True
            image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
            h, w, _ = image.shape

            # Valori implicite
            mouth = 0.0
            hand_dist = 0.0
            redness = 0.0
            hand_det = 0

            # Calcule
            if results.face_landmarks:
                mouth = extractor.get_mouth_openness(results.face_landmarks, h, w)
                redness = extractor.get_cheek_redness(image, results.face_landmarks, h, w)
                mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION)

            if results.right_hand_landmarks:
                hand_det = 1
                if results.face_landmarks:
                    hand_dist = extractor.get_hand_face_distance(results.face_landmarks, results.right_hand_landmarks, h, w)
                mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

            # SALVARE ÎN DB (Aici e cheia!)
            db.save_frame(session_id, hand_det, hand_dist, mouth, 0.0, redness)

            # Afișare pe ecran
            cv2.putText(image, "SALVEZ DATE...", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(image, f"Mouth: {mouth:.1f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow('Thesis Recorder', image)

            # Ieșire cu ESC
            if cv2.waitKey(5) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()
    db.close()
    print("--- SESIUNE SALVATĂ CU SUCCES ---")

if __name__ == "__main__":
    main()
# verified.
