# 💪 AI Powered Pocket Coach: Real-time Exercise Tracker

The **AI Powered Pocket Coach** is a real-time workout tracking application built with **Streamlit** and **MediaPipe**.  
It uses advanced **pose estimation** to monitor user form, count repetitions, and track holding time for various exercises — providing **instant visual feedback** and a detailed **performance summary** after each session.

---

## ✨ Features

✅ **Real-time Pose Estimation**  
Uses Google’s **MediaPipe Pose** to accurately detect 33 body landmarks.

✅ **Repetition Tracking**  
Counts reps for movement-based exercises like **Push-ups** and **Squats**.

✅ **Time Tracking**  
Measures the duration of hold exercises like **Plank**, counting time only when form is correct.

✅ **Instant Form Feedback**  
Provides visual cues and on-screen messages when your posture deviates from optimal angles (e.g., knee depth, hip alignment).

✅ **Post-Workout Summary**  
Displays a summary dashboard showing total reps/time, form quality percentage, and a personalized session rating.

✅ **Customizable Angle Thresholds**  
Predefined configurations ensure accurate tracking of elbow, knee, and hip movements for different exercises.

---

## 🧠 Tech Stack

- **Frontend:** Streamlit  
- **Pose Estimation:** MediaPipe  
- **Video Processing:** OpenCV  
- **Realtime Communication:** streamlit-webrtc  
- **Computation & Angles:** NumPy  

---

## 🚀 Getting Started

Follow these steps to set up and run the application locally.

### 🔧 Prerequisites
- Python 3.8 or higher  
- A webcam for live tracking  

###⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/mrkarannn03/Pocket-Coach-Posture-Reps-Analyze
cd Pocket-Coach-Posture-Reps-Analyze
Create and activate a virtual environment (recommended):

bash
Copy code
python -m venv venv

# On Linux/macOS
source venv/bin/activate

# On Windows
venv\Scripts\activate
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
📦 requirements.txt
Create a requirements.txt file in the root directory with the following content:

plaintext
Copy code
streamlit
opencv-python
mediapipe
streamlit-webrtc
numpy
🏃 Usage
Run the Streamlit application:

bash
Copy code
streamlit run app.py
Once launched, open your browser to http://localhost:8501.

▶️ Start Your Workout
Select an exercise (Push-up, Squat, or Plank) from the sidebar.

Click “Start Camera Stream” and grant camera access.

Position yourself fully in frame (side profile works best).

Perform your exercise! The app will:

Track your reps/time

Provide live form feedback

Display metrics in real-time

Click “🔴 Stop Stream” to end your session and view the summary dashboard.

📊 Example Output
Metric	Example Value
Push-ups Completed	15
Average Form Accuracy	92%
Session Duration	3 min 40 sec
Rating	⭐⭐⭐⭐☆

🧾 Project Structure
bash
Copy code
AI-Powered-Pocket-Coach/
│
├── app.py                # Main Streamlit app (UI + logic)
├── requirements.txt      # Project dependencies
├── README.md             # Documentation
└── assets/               # (Optional) images, demo GIFs, etc.

markdown
Copy code
![Demo](assets/demo.gif)
If deployed online, include:


🚧 Future Enhancements
🏋️ Add more exercises (Lunges, Jumping Jacks, Yoga Poses)

🧍 Integrate AI-based form correction suggestions using angle analysis

📈 Create a progress dashboard to visualize improvement over time

🎵 Add optional sound feedback or voice guidance

📱 Make it mobile-friendly for on-the-go workouts

🤝 Contributing
Contributions are welcome!
To contribute:

Fork this repository

Create a new branch (feature/new-exercise)

Commit your changes

Submit a pull request

🙌 Acknowledgments
MediaPipe for pose estimation

Streamlit for the interactive app framework

OpenCV for video processing

💡 Stay fit with AI — your pocket coach is always ready!
