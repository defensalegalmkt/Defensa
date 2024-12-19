
# -*- coding: utf-8 -*-
import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import subprocess

class WebcamViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Defensa Legal")
        
        # Abrir la aplicación Iriun Webcam
        subprocess.Popen(["cmd", "/c", "start", r"C:\Program Files (x86)\Iriun Webcam\IriunWebcam.exe"])

        self.cap = cv2.VideoCapture(0)
        self.zoom_level = 1.0
        self.recording = False
        self.out = None

        self.canvas = tk.Canvas(root, width=640, height=480)
        self.canvas.pack()

        self.btn_zoom_in = tk.Button(root, text="Zoom In", command=self.zoom_in)
        self.btn_zoom_in.pack(side=tk.LEFT)

        self.btn_zoom_out = tk.Button(root, text="Zoom Out", command=self.zoom_out)
        self.btn_zoom_out.pack(side=tk.LEFT)

        self.btn_record = tk.Button(root, text="Record", command=self.toggle_recording)
        self.btn_record.pack(side=tk.LEFT)

        self.update_frame()

    def zoom_in(self):
        self.zoom_level = min(2.0, self.zoom_level + 0.1)

    def zoom_out(self):
        self.zoom_level = max(1.0, self.zoom_level - 0.1)

    def toggle_recording(self):
        if self.recording:
            self.recording = False
            if self.out:
                self.out.release()
            self.btn_record.config(text="Record")
        else:
            self.recording = True
            self.btn_record.config(text="Stop")
            filename = filedialog.asksaveasfilename(defaultextension=".avi", filetypes=[("AVI files", "*.avi")])
            if filename:
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                self.out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = self.apply_zoom(frame)
            if self.recording and self.out:
                self.out.write(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
            self.canvas.imgtk = imgtk
        self.root.after(10, self.update_frame)

    def apply_zoom(self, frame):
        h, w, _ = frame.shape
        new_h, new_w = int(h / self.zoom_level), int(w / self.zoom_level)
        y1, x1 = (h - new_h) // 2, (w - new_w) // 2
        y2, x2 = y1 + new_h, x1 + new_w
        return cv2.resize(frame[y1:y2, x1:x2], (w, h))

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()
        if self.recording and self.out:
            self.out.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = WebcamViewer(root)
    root.mainloop()