import cv2
import numpy as np
import pyvirtualcam
import os
import mediapipe as mp

# Menggunakan modul solutions melalui objek mp
mp_hands = mp.solutions.hands
mp_face = mp.solutions.face_mesh
mp_draw = mp.solutions.drawing_utils

# Inisialisasi MediaPipe Hands & Face Mesh
hands = mp_hands.Hands(
    min_detection_confidence=0.7, 
    min_tracking_confidence=0.7, 
    max_num_hands=2
)

face_mesh = mp_face.FaceMesh(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Muat gambar dari folder assets
assets_dir = 'assets'
memes = {
    'call_sign_tongue': cv2.imread(os.path.join(assets_dir, 'plenger-cat.jpg')),
    'heart_hands': cv2.imread(os.path.join(assets_dir, 'love-sign.jpg')),
    'index_head': cv2.imread(os.path.join(assets_dir, 'nerd-pose.jpg')),
    'hold_head': cv2.imread(os.path.join(assets_dir, 'kaget.jpg')),
    'ok_sign': cv2.imread(os.path.join(assets_dir, 'sigma-amba.jpg')),
    'shh_pose': cv2.imread(os.path.join(assets_dir, 'indian-men.jpg'))
}

cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

def overlay_image(background, foreground, x, y, size=(250, 250)):
    if foreground is None:
        return background
    fg_resized = cv2.resize(foreground, size)
    h, w = fg_resized.shape[:2]
    if y + h > background.shape[0] or x + w > background.shape[1] or x < 0 or y < 0:
        return background
    if fg_resized.shape[2] == 4:
        alpha = fg_resized[:, :, 3] / 255.0
        for c in range(0, 3):
            background[y:y+h, x:x+w, c] = (alpha * fg_resized[:, :, c] + (1.0 - alpha) * background[y:y+h, x:x+w, c])
    else:
        background[y:y+h, x:x+w] = fg_resized
    return background

def get_finger_status(lm):
    fingers = []
    # Jempol
    fingers.append(1 if lm[4].x < lm[3].x else 0)
    # 4 Jari lain
    tips, pip = [8, 12, 16, 20], [6, 10, 14, 18]
    for i in range(4):
        fingers.append(1 if lm[tips[i]].y < lm[pip[i]].y else 0)
    return fingers

def dist(p1, p2):
    return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def detect_gestures(hand_results, face_results):
    if not hand_results.multi_hand_landmarks:
        return None

    hands_lm = hand_results.multi_hand_landmarks
    num_hands = len(hands_lm)
    
    # Ambil data wajah jika terdeteksi
    face_lm = face_results.multi_face_landmarks[0].landmark if face_results.multi_face_landmarks else None

    # --- DETEKSI 2 TANGAN ---
    if num_hands == 2:
        h1, h2 = hands_lm[0].landmark, hands_lm[1].landmark
        
        # Gesture 2: Dua tangan bentuk hati
        if dist(h1[4], h2[4]) < 0.1 and dist(h1[8], h2[8]) < 0.1:
            return 'heart_hands'
            
        # Gesture 5: Kedua tangan pegang kepala
        if face_lm:
            head_top_y = face_lm[10].y
            if h1[8].y < head_top_y + 0.1 and h2[8].y < head_top_y + 0.1:
                return 'hold_head'

    # --- DETEKSI 1 TANGAN ---
    for lm in hands_lm:
        pts = lm.landmark
        f = get_finger_status(pts)
        
        # Gesture 6: Tangan bentuk "O" (OK sign)
        if dist(pts[4], pts[8]) < 0.05 and f[2] == 1 and f[3] == 1 and f[4] == 1:
            return 'ok_sign'

        if face_lm:
            lips_y = face_lm[13].y
            ear_r_x, ear_l_x = face_lm[234].x, face_lm[454].x
            
            # Gesture 1: Call sign "🤙" + Melet
            is_call_sign = (f[0] == 1 and f[1] == 0 and f[2] == 0 and f[3] == 0 and f[4] == 1)
            is_tongue_out = dist(face_lm[13], face_lm[14]) > 0.04
            if is_call_sign and is_tongue_out:
                return 'call_sign_tongue'
                
            # Gesture 4: Suruh diam (Shh pose)
            if f[1] == 1 and f[2] == 0 and f[3] == 0 and f[4] == 0:
                if dist(pts[8], face_lm[13]) < 0.08:
                    return 'shh_pose'

            # Gesture 3: Telunjuk ke atas di samping kepala
            if f[1] == 1 and f[2] == 0 and f[3] == 0 and f[4] == 0:
                is_near_side_head = (abs(pts[8].x - ear_r_x) < 0.1 or abs(pts[8].x - ear_l_x) < 0.1)
                if is_near_side_head and pts[8].y < lips_y:
                    return 'index_head'

    return None

# Jalankan kamera virtual dan loop pemrosesan video
with pyvirtualcam.Camera(width=width, height=height, fps=30, fmt=pyvirtualcam.PixelFormat.BGR) as cam:
    print(f'Kamera virtual aktif: {cam.device}')
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Mirror frame agar tampilan seperti cermin
        #frame = cv2.flip(frame, 1)

        # Ubah BGR ke RGB untuk pemrosesan MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Deteksi tangan dan wajah
        hand_results = hands.process(rgb_frame)
        face_results = face_mesh.process(rgb_frame)

        # Deteksi gestur berdasarkan landmark
        gesture = detect_gestures(hand_results, face_results)

        # Jika gestur terdeteksi dan gambar meme ada, tempelkan gambar di pojok kanan atas
        if gesture and gesture in memes and memes[gesture] is not None:
            frame = overlay_image(frame, memes[gesture], x=width - 270, y=20, size=(250, 250))

        # Kirim frame ke kamera virtual (OBS / Zoom / Meet)
        cam.send(frame)
        cam.sleep_until_next_frame()

        # Tampilkan juga di jendela lokal
        cv2.imshow("Meme Overlay Webcam", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()