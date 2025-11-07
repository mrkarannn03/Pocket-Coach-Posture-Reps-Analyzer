import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, WebRtcMode
import cv2
import mediapipe as mp
import numpy as np
import time
import random

# --- Standard Angle Configuration ---
CONFIG = {
    "Push-up": {"down": 70.0, "up": 160.0, "desc": "Elbows"},
    "Squat": {"down": 90.0, "up": 170.0, "desc": "Knees"},
    "Plank": {"down": 10.0, "up": 10.0, "desc": "Time"},
}

# --- Quotes for positive feedback ---
POSITIVE_QUOTES = [
    "Great work! Consistency is the key to lasting change.",
    "Every rep counts! You're building a stronger foundation.",
    "The hardest lift is lifting your foot off the couch. Well done!",
    "Your body can stand almost anything. It’s your mind that you have to convince.",
    "Keep pushing your limits. You are stronger than you think!",
]

# --- Helper Functions ---
def calculate_angle(a, b, c):
    """Calculates the angle between three points (A, B, C) with B as the vertex."""
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b
    
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
    angle = np.arccos(cosine_angle)
    
    return np.degrees(angle)

def format_time(seconds):
    """Formats seconds into H:MM:SS."""
    if seconds < 0:
        seconds = 0
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02}:{m:02}:{s:02}"

# --- Base Exercise Tracking Class ---
class BaseExerciseTracker(VideoTransformerBase):
    def __init__(self, exercise_name, down_angle, up_angle):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False, model_complexity=1,
            min_detection_confidence=0.5, min_tracking_confidence=0.5
        )
        self.drawer = mp.solutions.drawing_utils
        self.styles = mp.solutions.drawing_styles
        
        self.exercise = exercise_name
        self.down_angle_threshold = down_angle
        self.up_angle_threshold = up_angle
        self.counter = 0.0 # Use float for plank time
        self.form_ok = False
        self.display_message = "Waiting to start..."
        self.session_data = [] # List to store data after each rep
        
        self.start_time = time.time()
        self.frame_count = 0
        self.fps = 0
        # Store initial session start time from Streamlit state
        self.session_start_time = st.session_state.get('session_start_time', time.time())

    def save_session_data(self):
        """
        Explicitly saves final data to Streamlit session state. 
        This is called reliably by the 'Stop Stream' button callback.
        """
        st.session_state['rep_data'] = self.session_data
        st.session_state['final_count'] = self.counter # Reps or total time held
        # Calculate the total session time elapsed
        st.session_state['final_time'] = time.time() - self.session_start_time 
        st.session_state['exercise_type'] = self.exercise

    def calculate_metrics(self, landmarks):
        """Placeholder method to be overridden by specific exercise logic."""
        return 0.0, False 

    def update_state(self, main_angle, form_ok):
        """Placeholder method to be overridden by specific exercise logic."""
        pass 

    def draw_data(self, frame, width):
        """Draws common data (FPS, Reps/Time)."""
        session_duration = time.time() - self.session_start_time
        
        # Display Reps or Time based on exercise type
        metric_label = "Reps" if self.exercise != "Plank" else "Time"
        metric_value = f"{int(self.counter)}" if self.exercise != "Plank" else f"{self.counter:.1f}s"
        
        cv2.putText(frame, f"Exercise: {self.exercise}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"{metric_label}: {metric_value}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), 2)
        cv2.putText(frame, f"Session: {format_time(session_duration)}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 165, 0), 2)
        cv2.putText(frame, f"FPS: {self.fps:.1f}", (width - 120, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        form_color = (0, 255, 0) if self.form_ok else (0, 0, 255)
        cv2.putText(frame, f"Form: {'OK' if self.form_ok else 'BAD'}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, form_color, 2)
        cv2.putText(frame, self.display_message, (10, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)


    def transform(self, frame):
        frame = frame.to_ndarray(format="bgr24")
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = self.pose.process(frame_rgb)
        height, width, _ = frame.shape

        # FPS calculation
        self.frame_count += 1
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= 1.0:
            self.fps = self.frame_count / elapsed_time
            self.frame_count = 0
            self.start_time = time.time()

        if results.pose_landmarks:
            self.drawer.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                                       landmark_drawing_spec=self.styles.get_default_pose_landmarks_style())

            landmarks = results.pose_landmarks.landmark
            try:
                main_angle, self.form_ok = self.calculate_metrics(landmarks)
                self.update_state(main_angle, self.form_ok)
            except Exception:
                self.display_message = "Landmarks missing or error in calculation."
                self.form_ok = False
                
        else:
            cv2.putText(frame, "No body detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        self.draw_data(frame, width)
        return frame


# --------------------------------------------------------------------------
# --- 1. PUSH-UP TRACKER (Repetition Counting) ---
# --------------------------------------------------------------------------
class PushupTracker(BaseExerciseTracker):
    def __init__(self):
        super().__init__("Push-up", CONFIG["Push-up"]["down"], CONFIG["Push-up"]["up"])
        self.state = "waiting_down"
        self.current_angle = 0.0
        self.current_rep_min_angle = 180.0
        self.rep_start_time = None

    def check_form(self, landmarks):
        """Checks for plank-like form (hip alignment)."""
        try:
            shoulder_y = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y
            hip_y = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y
            ankle_y = landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].y
            mid_y = (shoulder_y + ankle_y) / 2
            # Check if hip is too far up or down (poor plank form)
            return abs(hip_y - mid_y) < 0.15 
        except IndexError:
            return False

    def get_elbow_angle(self, landmarks):
        """Calculates the elbow angle for the left arm."""
        try:
            shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            elbow = landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value]
            wrist = landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value]

            coords = [[l.x, l.y] for l in [shoulder, elbow, wrist]]
            return calculate_angle(coords[0], coords[1], coords[2])
        except Exception:
            return 180.0

    def calculate_metrics(self, landmarks):
        angle = self.get_elbow_angle(landmarks)
        self.current_angle = angle
        form_ok = self.check_form(landmarks)
        
        # Track minimum angle for form feedback
        if self.state == "waiting_up":
            self.current_rep_min_angle = min(self.current_rep_min_angle, angle)
            
        return angle, form_ok

    def update_state(self, main_angle, form_ok):
        if not form_ok:
            self.display_message = "Adjust Form! (Hips/Back)"
            # Don't reset state, but don't count reps
        
        if form_ok:
            if self.state == "waiting_down":
                if main_angle < self.down_angle_threshold:
                    self.state = "waiting_up"
                    self.display_message = "Down! Now Push Up"
                    self.rep_start_time = time.time()
            
            elif self.state == "waiting_up":
                if main_angle > self.up_angle_threshold:
                    self.counter += 1
                    rep_duration = time.time() - self.rep_start_time if self.rep_start_time else 0.0
                    self.state = "waiting_down"
                    self.display_message = "Nice Rep!"
                    
                    # Store data after successful rep
                    self.session_data.append({
                        "rep": int(self.counter), 
                        "form_ok": form_ok, 
                        "min_angle": self.current_rep_min_angle,
                        "duration": rep_duration
                    })
                    self.current_rep_min_angle = 180.0 # Reset min angle for next rep
                    self.rep_start_time = None
                else:
                    self.display_message = "Extend Arms Fully"
            
    def draw_data(self, frame, width):
        super().draw_data(frame, width)
        cv2.putText(frame, f"Elbow Angle: {self.current_angle:.1f} deg", (10, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)


# --------------------------------------------------------------------------
# --- 2. SQUAT TRACKER (Repetition Counting) ---
# --------------------------------------------------------------------------
class SquatTracker(BaseExerciseTracker):
    def __init__(self):
        super().__init__("Squat", CONFIG["Squat"]["down"], CONFIG["Squat"]["up"])
        self.state = "waiting_down"
        self.current_angle = 180.0
        self.current_rep_min_angle = 180.0
        self.rep_start_time = None

    def get_knee_angle(self, landmarks):
        """Calculates the hip-knee-ankle angle for the left side."""
        try:
            hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
            knee = landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value]
            ankle = landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value]
            
            coords = [[l.x, l.y] for l in [hip, knee, ankle]]
            return calculate_angle(coords[0], coords[1], coords[2])
        except Exception:
            return 180.0

    def check_form(self, landmarks):
        """Checks for depth and back straightness (simplified)."""
        # Simple check for depth: Hip should not drop below the knee line horizontally
        try:
            return landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y < landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].y
        except IndexError:
            return False

    def calculate_metrics(self, landmarks):
        angle = self.get_knee_angle(landmarks)
        self.current_angle = angle
        form_ok = self.check_form(landmarks)
        
        # Track minimum angle for form feedback
        if self.state == "waiting_up":
            self.current_rep_min_angle = min(self.current_rep_min_angle, angle)
            
        return angle, form_ok

    def update_state(self, main_angle, form_ok):
        if self.state == "waiting_down":
            if main_angle < self.down_angle_threshold:
                self.state = "waiting_up"
                self.display_message = "Deep Squat! Push Up"
                self.rep_start_time = time.time()
            else:
                self.display_message = "Squat Deeper (Knee Angle)"
        
        elif self.state == "waiting_up":
            if main_angle > self.up_angle_threshold:
                self.counter += 1
                rep_duration = time.time() - self.rep_start_time if self.rep_start_time else 0.0
                self.state = "waiting_down"
                self.display_message = "Nice Rep!"
                
                # Store data after successful rep
                self.session_data.append({
                    "rep": int(self.counter), 
                    "form_ok": form_ok, 
                    "min_angle": self.current_rep_min_angle,
                    "duration": rep_duration
                })
                self.current_rep_min_angle = 180.0 # Reset min angle for next rep
                self.rep_start_time = None
            else:
                self.display_message = "Stand Up Fully"
                
    def draw_data(self, frame, width):
        super().draw_data(frame, width)
        cv2.putText(frame, f"Knee Angle: {self.current_angle:.1f} deg", (10, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

# --------------------------------------------------------------------------
# --- 3. PLANK TRACKER (Time-based/Hold) ---
# --------------------------------------------------------------------------
class PlankTracker(BaseExerciseTracker):
    def __init__(self):
        super().__init__("Plank", CONFIG["Plank"]["down"], CONFIG["Plank"]["up"])
        self.is_holding = False
        self.hold_start_time = None
        self.elapsed_time = 0.0

    def check_form(self, landmarks):
        """Checks for near-straight line alignment (shoulder, hip, ankle)."""
        try:
            shoulder_y = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y
            hip_y = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y
            ankle_y = landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].y
            
            mid_y = (shoulder_y + ankle_y) / 2
            # Check for straight line alignment with tighter tolerance
            return abs(hip_y - mid_y) < 0.05 
        except IndexError:
            return False

    def calculate_metrics(self, landmarks):
        # Angle is irrelevant for plank, focus on form check
        return 0.0, self.check_form(landmarks)

    def update_state(self, main_angle, form_ok):
        current_time = time.time()
        
        if form_ok:
            if not self.is_holding:
                # Start new hold
                self.is_holding = True
                self.hold_start_time = current_time - self.elapsed_time # Continue from last time
                self.display_message = "Form OK! HOLD"
            else:
                # Update time held
                self.counter = current_time - self.hold_start_time
                self.display_message = f"HOLDING: {int(self.counter)}s"
                
        else:
            if self.is_holding:
                # Form broken - stop holding, update final count
                self.elapsed_time = self.counter 
                self.session_data.append({"time_held": self.elapsed_time, "form_ok": False}) 
                
            self.is_holding = False
            self.hold_start_time = None
            self.display_message = "BAD FORM! Adjust Hips/Back"
            self.counter = self.elapsed_time # Keep displaying the total time held so far


# --- Mapping Exercise Names to Tracker Classes ---
TRACKER_MAPPING = {
    "Push-up": PushupTracker,
    "Squat": SquatTracker,
    "Plank": PlankTracker,
}

# --------------------------------------------------------------------------
# --- Streamlit UI (Global Scope) ---
# --------------------------------------------------------------------------

st.set_page_config(page_title="💪 AI Pocket Coach", layout="wide")
st.title("💪 AI Powered Pocket Coach")

# --- Sidebar Exercise Selector ---
st.sidebar.header("Select Exercise")
selected_exercise = st.sidebar.radio(
    "Choose your workout:",
    list(TRACKER_MAPPING.keys()),
    key="exercise_selector"
)

# --- Session State Initialization ---
if 'is_started' not in st.session_state:
    st.session_state['is_started'] = False
if 'show_summary' not in st.session_state:
    st.session_state['show_summary'] = False
if 'rep_data' not in st.session_state:
    st.session_state['rep_data'] = []
if 'session_start_time' not in st.session_state:
    st.session_state['session_start_time'] = time.time()
if 'final_count' not in st.session_state:
    st.session_state['final_count'] = 0.0
if 'final_time' not in st.session_state:
    st.session_state['final_time'] = 0.0
if 'exercise_type' not in st.session_state:
    st.session_state['exercise_type'] = selected_exercise
    
# --- CSS Injection ---
st.markdown(
    """
    <style>
        .stVideo video {
            width: 100% !important;
            height: auto !important;
        }
        /* Styling for the red stop button */
        .stButton button[kind="secondary"] {
            background-color: #dc3545;
            color: white;
            font-weight: bold;
            border: none;
        }
        .stButton button[kind="secondary"]:hover {
            background-color: #c82333;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Start/Stop Button Callbacks ---
def start_button_callback():
    # Reset state and start time for a new session
    st.session_state['is_started'] = True
    st.session_state['show_summary'] = False
    st.session_state['rep_data'] = []
    st.session_state['session_start_time'] = time.time()
    st.session_state['exercise_type'] = st.session_state['exercise_selector']
    # Clear old results
    st.session_state['final_count'] = 0.0
    st.session_state['final_time'] = 0.0


def stop_button_callback():
    """
    FIX: Retrieves the active context from session state directly for reliable data saving.
    """
    if 'active_tracker_stream' in st.session_state:
        webrtc_ctx = st.session_state['active_tracker_stream']
        if webrtc_ctx and webrtc_ctx.video_transformer:
            # Explicitly call the save method on the live tracker instance
            webrtc_ctx.video_transformer.save_session_data() 
        else:
            print("Warning: Could not access live video transformer for final data save.")
    
    st.session_state['is_started'] = False
    st.session_state['show_summary'] = True
    
def new_session_callback():
    st.session_state['show_summary'] = False


# --- Main Content Display ---

if not st.session_state['is_started'] and not st.session_state['show_summary']:
    # Initial screen content
    st.markdown(f"### Ready to start your **{selected_exercise}** workout?")
    st.button("Start Camera Stream", on_click=start_button_callback, type="primary")
    
    # Display current calibration in the main body
    st.markdown("---")
    st.subheader("Current Calibration")
    st.markdown(
        f"**{CONFIG[selected_exercise]['desc']}** angle for Down/Bottom = **${CONFIG.get(selected_exercise, {}).get('down', 0)}^\circ$**,"
        f" Up/Top = **${CONFIG.get(selected_exercise, {}).get('up', 0)}^\circ$**."
    )

elif st.session_state['is_started']:
    # Live Tracking Screen
    
    col_status, col_button = st.columns([4, 1])

    with col_button:
        # FIX: Call the callback without arguments. The callback now retrieves the context internally.
        st.button("🔴 Stop Stream", on_click=stop_button_callback, type="secondary")


    with col_status:
        st.info(f"Camera stream active for **{st.session_state['exercise_type']}**. Begin your exercise!") 
        
    # --- Instructions (Dynamic based on selection) ---
    st.markdown("---")
    st.subheader("🏋️ Instructions")
    if selected_exercise == "Push-up":
            st.markdown(
                """
                * Ensure **full body** is visible (side view recommended).
                * Maintain **plank form** (straight hips/back).
                * Rep counts when **elbow angle** drops below **$70^\circ$** and returns above **$160^\circ$**.
                """
            )
    elif selected_exercise == "Squat":
            st.markdown(
                """
                * Ensure **full body** is visible (side view recommended).
                * Rep counts when **knee angle** drops below **$90^\circ$** and returns above **$170^\circ$**.
                * Focus on knee tracking and depth.
                """
            )
    elif selected_exercise == "Plank":
            st.markdown(
                """
                * Hold a straight **shoulder-hip-ankle line** (side view).
                * The timer only runs when your form is **OK**.
                """
            )
        
    # --- Dynamic Tracker Instance Creation ---
    TrackerClass = TRACKER_MAPPING[st.session_state['exercise_type']]
    
    webrtc_streamer(
            key="active_tracker_stream", # Unique key for the active stream
            mode=WebRtcMode.SENDRECV,
            video_transformer_factory=lambda: TrackerClass(),
            media_stream_constraints={"video": True, "audio": False},
            async_transform=True,
    )
    
    # Quote of the day placeholder
    st.markdown("---")
    st.info(f"**Motivation:** {random.choice(POSITIVE_QUOTES)}")

elif st.session_state['show_summary']:
    # --------------------------------------------------------------------------
    # --- POST-WORKOUT SUMMARY METRICS ---
    # --------------------------------------------------------------------------
    
    exercise_type = st.session_state.get('exercise_type', 'N/A')
    
    st.header(f"🎉 Workout Summary: {exercise_type}")
    
    # Initialize values
    final_count = st.session_state.get('final_count', 0.0)
    total_session_time = st.session_state.get('final_time', 0.0)
    rep_data = st.session_state.get('rep_data', [])
    
    # --- Metric Calculation Logic ---
    rating = 0.0
    
    if exercise_type in ["Push-up", "Squat"]:
        total_reps = int(final_count)
        # Check form_ok and rep existence for accurate count
        valid_reps = sum(1 for data in rep_data if data.get('form_ok') and data.get('rep') is not None)
        
        if total_reps > 0:
            form_percentage = (valid_reps / total_reps) * 100
            # Simple rating: 50% = 5/10, 100% = 10/10
            rating = 4.0 + (form_percentage / 100) * 6.0 
        else:
            form_percentage = 0.0
            rating = 0.0
            
        # Display Repetition Metrics
        col_summary_1, col_summary_2, col_summary_3 = st.columns(3)
        with col_summary_1:
            st.metric("Total Reps Attempted", f"{total_reps}")
        with col_summary_2:
            st.metric("Reps with OK Form", f"{valid_reps}")
        with col_summary_3:
            st.metric("Form Quality", f"{form_percentage:.1f}%")
        
    elif exercise_type == "Plank":
        total_time_s = final_count
        
        # Simple rating based on time (Max 10 for 120s or more)
        if total_time_s > 0:
            rating = min(10.0, 4.0 + (total_time_s / 120.0) * 6.0) 
        else:
            rating = 0.0
            
        # Display Time Metrics
        col_time_1, col_time_2 = st.columns(2)
        with col_time_1:
            st.metric("Total Time Held (s)", f"{total_time_s:.1f}s")
        with col_time_2:
            st.metric("Total Session Time", format_time(total_session_time))
        
    # --- Overall Rating ---
    st.markdown("---")
    st.subheader("🌟 Overall Performance")
    
    final_rating = min(10.0, max(0.0, rating))
    
    st.metric("Workout Rating (0-10)", f"{final_rating:.1f}")
    
    # --- Form Details (Rep-by-Rep for Repetition Exercises) ---
    if exercise_type in ["Push-up", "Squat"] and rep_data:
        st.markdown("---")
        st.subheader("🔍 Repetition Analysis")
        
        rep_data_display = [
            {
                "Rep #": data['rep'],
                "Form Status": "✅ OK" if data.get('form_ok') else "❌ BAD FORM",
                "Min Angle": f"{data.get('min_angle', 0):.1f} deg",
                "Duration": f"{data.get('duration', 0):.1f} s"
            } for data in rep_data
        ]
        st.dataframe(rep_data_display, use_container_width=True)

    # --- Restart Button and Quote ---
    st.markdown("---")
    st.info(f"**Quote of the day:** {random.choice(POSITIVE_QUOTES)}")

    st.button("Start New Session", on_click=new_session_callback, type="primary")