import cv2
import time
import win32gui, win32con
import tkinter as tk
from tkinter import messagebox, filedialog
import os
import threading

class CCTVSoftware:
    def __init__(self, root):
        self.root = root
        self.root.title("CCTV Software")
        self.root.geometry("400x300")
        self.video_recording = False
        self.video_paused = False
        self.video_capture = None
        self.video_writer = None

        # Create GUI elements
        self.label = tk.Label(root, text="Welcome to CCTV Software", font=("Arial", 16))
        self.label.pack(pady=20)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=20)

        self.start_button = tk.Button(self.button_frame, text="Start Recording", command=self.start_recording)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(self.button_frame, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.pause_button = tk.Button(self.button_frame, text="Pause Recording", command=self.pause_recording, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=10)

        self.minimize_button = tk.Button(self.button_frame, text="Minimize", command=self.minimize_window)
        self.minimize_button.pack(side=tk.LEFT, padx=10)

        self.view_button = tk.Button(self.button_frame, text="View Saved Videos", command=self.view_saved_videos)
        self.view_button.pack(side=tk.LEFT, padx=10)

        self.status_label = tk.Label(root, text="Status: Not Recording", font=("Arial", 12))
        self.status_label.pack(pady=10)

    def start_recording(self):
        self.video_recording = True
        self.video_paused = False
        self.stop_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Recording...")
        self.video_capture = cv2.VideoCapture(0)
        self.video_writer = cv2.VideoWriter('footages/recording.mp4', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))
        self.video_thread = threading.Thread(target=self.capture_video)
        self.video_thread.start()

    def stop_recording(self):
        self.video_recording = False
        self.stop_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Not Recording")
        if self.video_capture:
            self.video_capture.release()
            self.video_capture = None
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None

    def pause_recording(self):
        if self.video_paused:
            self.video_paused = False
            self.pause_button.config(text="Pause Recording")
            self.status_label.config(text="Status: Recording...")
        else:
            self.video_paused = True
            self.pause_button.config(text="Resume Recording")
            self.status_label.config(text="Status: Paused")

    def minimize_window(self):
        window = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(window, win32con.SW_MINIMIZE)

    def capture_video(self):
        while self.video_recording:
            if not self.video_paused:
                check, frame = self.video_capture.read()
                if check:
                    frame = cv2.flip(frame, 1)
                    t = time.ctime()
                    cv2.rectangle(frame, (5, 5, 100, 20), (255, 255, 255), cv2.FILLED)
                    cv2.putText(frame, "Camera 1", (20, 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
                    cv2.imshow('CCTV Camera', frame)
                    self.video_writer.write(frame)
                    if cv2.waitKey(1) == 27:
                        self.stop_recording()
                    elif cv2.waitKey(1) == ord('m'):
                        self.minimize_window()
                else:
                    print("Error: Unable to read frame from camera.")
                    self.stop_recording()
            else:
                cv2.waitKey(0)
        cv2.destroyAllWindows()

    def view_saved_videos(self):
        video_dir = 'footages/'
        video_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
        if not video_files:
            messagebox.showinfo("No Videos Found", "No saved videos found in the 'footages' directory.")
            return
        video_file = filedialog.askopenfilename(initialdir= video_dir, title ="Select a video file", filetypes=[("MP4 files", "*.mp4")])

root = tk.Tk()
cctv_software = CCTVSoftware(root)
root.mainloop()
