import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Function to detect shapes and return detected shapes as a list
def detect_shapes(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    shape_info = []

    for contour in contours:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) == 3:
            shape = "Triangle"
        elif len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = w / float(h)
            shape = "Square" if 0.95 <= aspect_ratio <= 1.05 else "Rectangle"
        elif len(approx) == 5:
            shape = "Pentagon"
        elif len(approx) == 6:
            shape = "Hexagon"
        else:
            shape = "Circle"

        cv2.drawContours(image, [approx], 0, (0, 255, 0), 2)
        cv2.putText(image, shape, (approx[0][0][0], approx[0][0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Append the shape information for display
        shape_info.append(shape)

    return image, shape_info

# Function to detect symmetry
def find_symmetry(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        contour = contour[:, 0, :]
        M = cv2.moments(contour)
        if M["m00"] == 0:
            continue
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)
        cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)

        # Check for symmetry (basic approach)
        symmetry = True
        for i in range(len(contour)):
            x1, y1 = contour[i]
            x2, y2 = contour[-i % len(contour)]
            if abs(x1 - x2) > 10 or abs(y1 - y2) > 10:
                symmetry = False
                break

        if symmetry:
            cv2.putText(image, "Symmetric", (cX - 30, cY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    return image

# Function to complete curves
def complete_curves(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    dilated = cv2.dilate(edges, None, iterations=2)

    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        if len(approx) > 3:
            cv2.polylines(image, [approx], True, (0, 255, 255), 2)

    return image

# Tkinter interface
class ShapeDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shape Detection Application")

        # Buttons and Canvases
        self.upload_button = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=20)

        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack()

        self.canvas1 = tk.Canvas(self.canvas_frame, width=300, height=300)
        self.canvas1.grid(row=0, column=0, padx=10)
        self.label1 = tk.Label(self.canvas_frame, text="Detected Shapes:")
        self.label1.grid(row=1, column=0)

        self.canvas2 = tk.Canvas(self.canvas_frame, width=300, height=300)
        self.canvas2.grid(row=0, column=1, padx=10)
        self.label2 = tk.Label(self.canvas_frame, text="Symmetry Detection")
        self.label2.grid(row=1, column=1)

        self.canvas3 = tk.Canvas(self.canvas_frame, width=300, height=300)
        self.canvas3.grid(row=0, column=2, padx=10)
        self.label3 = tk.Label(self.canvas_frame, text="Curve Completion")
        self.label3.grid(row=1, column=2)

        # Labels to display text information
        self.text_label1 = tk.Label(root, text="")
        self.text_label1.pack(pady=5)

        self.text_label2 = tk.Label(root, text="")
        self.text_label2.pack(pady=5)

        self.text_label3 = tk.Label(root, text="")
        self.text_label3.pack(pady=5)

        self.image_path = None

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if self.image_path:
            shapes_image, shape_info = detect_shapes(self.image_path)
            symmetry_image = find_symmetry(self.image_path)
            completed_curves_image = complete_curves(self.image_path)

            # Display the images
            self.show_image(shapes_image, self.canvas1)
            self.show_image(symmetry_image, self.canvas2)
            self.show_image(completed_curves_image, self.canvas3)

            # Update text labels with relevant information
            self.text_label1.config(text="Detected Shapes: " + ", ".join(set(shape_info)))
            self.text_label2.config(text="Symmetry Detection: Check image for 'Symmetric' label")
            self.text_label3.config(text="Curve Completion: Check image for completed curves")

    def show_image(self, image, canvas):
        # Convert image to RGB (Tkinter requires RGB format)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        tk_image = ImageTk.PhotoImage(image_pil)
        canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
        canvas.image = tk_image  # Keep a reference to avoid garbage collection

if __name__ == "__main__":
    root = tk.Tk()
    app = ShapeDetectionApp(root)
    root.mainloop()
