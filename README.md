<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Powered Pocket Coach Documentation</title>
    <!-- Load Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Custom styles for readability */
        .markdown-body a {
            color: #34d399; /* Emerald 400 */
            text-decoration: none;
            transition: color 0.2s;
        }
        .markdown-body a:hover {
            color: #10b981; /* Emerald 500 */
        }
        /* Style list labels for better differentiation */
        .markdown-body ul li::marker {
            color: #34d399;
        }
    </style>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                    },
                    colors: {
                        'primary-dark': '#1f2937', /* Gray 800 */
                        'secondary-light': '#34d399', /* Emerald 400 */
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-gray-900 text-gray-100 font-sans min-h-screen p-4 sm:p-8">

    <div class="max-w-4xl mx-auto bg-primary-dark p-6 sm:p-10 rounded-xl shadow-2xl">
        
        <!-- Header -->
        <header class="pb-6 border-b border-gray-700 mb-8">
            <h1 class="text-4xl sm:text-5xl font-extrabold text-white flex items-center">
                <span class="mr-3 text-secondary-light">💪</span> AI Powered Pocket Coach
            </h1>
            <p class="text-lg text-gray-400 mt-2">Real-time Exercise Tracker Documentation</p>
        </header>

        <div class="markdown-body space-y-8">
            <!-- Project Description -->
            <p class="text-gray-300 leading-relaxed text-lg">
                The <strong class="text-secondary-light">AI Powered Pocket Coach</strong> is a real-time workout tracking application built with Streamlit and MediaPipe. It uses pose estimation to monitor user form, count repetitions, and track holding time for various exercises, providing instant visual feedback and a summary of performance metrics after the session.
            </p>

            <!-- Features -->
            <section class="space-y-4">
                <h2 class="text-3xl font-bold border-l-4 border-secondary-light pl-3 text-white">✨ Features</h2>
                <ul class="list-disc list-inside space-y-3 text-gray-300 ml-4">
                    <li>
                        <strong class="text-secondary-light">Real-time Pose Estimation:</strong> Utilizes Google's MediaPipe Pose to accurately detect 33 body landmarks.
                    </li>
                    <li>
                        <strong class="text-secondary-light">Repetition Tracking:</strong> Counts reps for movement-based exercises like **Push-ups** and **Squats**.
                    </li>
                    <li>
                        <strong class="text-secondary-light">Time Tracking:</strong> Measures the duration of hold exercises like **Plank**, only counting time when form is correct.
                    </li>
                    <li>
                        <strong class="text-secondary-light">Instant Form Feedback:</strong> Provides visual cues and on-screen messages when the user's form deviates from optimal angles (e.g., knee depth, hip alignment).
                    </li>
                    <li>
                        <strong class="text-secondary-light">Post-Workout Summary:</strong> Generates a summary dashboard showing total reps/time, form quality percentage, and a session rating.
                    </li>
                    <li>
                        <strong class="text-secondary-light">Customizable Angle Thresholds:</strong> Uses predefined angle configurations for accurate tracking of elbow and knee movements.
                    </li>
                </ul>
            </section>

            <!-- Getting Started -->
            <section class="space-y-4 pt-4 border-t border-gray-700">
                <h2 class="text-3xl font-bold border-l-4 border-secondary-light pl-3 text-white">🚀 Getting Started</h2>
                <p class="text-gray-300">Follow these steps to set up and run the application locally.</p>

                <h3 class="text-2xl font-semibold text-gray-200">Prerequisites</h3>
                <p class="text-gray-300">
                    You need <strong class="text-secondary-light">Python 3.8+</strong> installed on your system.
                </p>

                <h3 class="text-2xl font-semibold text-gray-200">Installation</h3>
                
                <ol class="list-decimal list-inside space-y-4 text-gray-300 ml-4">
                    <li>
                        <p><strong>Clone the repository:</strong></p>
                        <pre class="bg-gray-800 p-3 rounded-lg overflow-x-auto text-sm text-green-400 mt-1"><code>git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME</code></pre>
                    </li>
                    <li>
                        <p><strong>Create and activate a virtual environment (Recommended):</strong></p>
                        <pre class="bg-gray-800 p-3 rounded-lg overflow-x-auto text-sm text-green-400 mt-1"><code>python -m venv venv
# On Linux/macOS
source venv/bin/activate
# On Windows
venv\Scripts\activate</code></pre>
                    </li>
                    <li>
                        <p><strong>Install the required dependencies:</strong></p>
                        <pre class="bg-gray-800 p-3 rounded-lg overflow-x-auto text-sm text-green-400 mt-1"><code>pip install -r requirements.txt</code></pre>
                    </li>
                </ol>

                <h3 class="text-2xl font-semibold text-gray-200 mt-6">`requirements.txt` Content</h3>
                <p class="text-gray-300">
                    This file should be created in the root directory to list all necessary dependencies:
                </p>
                <pre class="bg-gray-800 p-3 rounded-lg overflow-x-auto text-sm text-yellow-300"><code>streamlit
opencv-python
mediapipe
streamlit-webrtc
numpy</code></pre>

            </section>

            <!-- Usage -->
            <section class="space-y-4 pt-4 border-t border-gray-700">
                <h2 class="text-3xl font-bold border-l-4 border-secondary-light pl-3 text-white">🏃 Usage</h2>
                
                <ol class="list-decimal list-inside space-y-4 text-gray-300 ml-4">
                    <li>
                        <p><strong>Run the Streamlit application:</strong></p>
                        <pre class="bg-gray-800 p-3 rounded-lg overflow-x-auto text-sm text-green-400 mt-1"><code>streamlit run app.py</code></pre>
                    </li>
                    <li>
                        <p><strong>Open in Browser:</strong> The command will automatically open the application in your default web browser (usually at <span class="text-secondary-light">http://localhost:8501</span>).</p>
                    </li>
                    <li>
                        <p><strong>Start Workout:</strong></p>
                        <ul class="list-disc list-inside space-y-2 text-gray-400 ml-6">
                            <li>Select your exercise (**Push-up, Squat, or Plank**) from the sidebar.</li>
                            <li>Click **"Start Camera Stream"**. You will be prompted to grant camera access.</li>
                            <li>Position yourself so your full body is visible to the camera, ideally in a side profile view for most exercises.</li>
                            <li>Perform the exercise. The tracker will count your reps/time and provide real-time form feedback.</li>
                            <li>Click <strong class="text-red-500">"🔴 Stop Stream"</strong> to end the session and view your summary metrics.</li>
                        </ul>
                    </li>
                </ol>
            </section>
            
            <!-- Project Structure -->
            <section class="space-y-4 pt-4 border-t border-gray-700">
                <h2 class="text-3xl font-bold border-l-4 border-secondary-light pl-3 text-white">🛠️ Project Structure</h2>
                <ul class="list-disc list-inside space-y-3 text-gray-300 ml-4">
                    <li>
                        <strong class="text-secondary-light">app.py:</strong> The main Python file containing all Streamlit components, MediaPipe integration, exercise tracking classes, and the UI logic.
                    </li>
                    <li>
                        <strong class="text-secondary-light">README.md:</strong> This documentation file.
                    </li>
                    <li>
                        <strong class="text-secondary-light">requirements.txt:</strong> Lists the Python dependencies needed for setup.
                    </li>
                </ul>
            </section>
            
            <!-- Contributing -->
            <section class="space-y-4 pt-4 border-t border-gray-700">
                <h2 class="text-3xl font-bold border-l-4 border-secondary-light pl-3 text-white">🤝 Contributing</h2>
                <p class="text-gray-300">
                    Feel free to open issues or submit pull requests to improve the accuracy of the tracking, add new exercises, or enhance the user interface!
                </p>
            </section>

        </div>

    </div>

</body>
</html>