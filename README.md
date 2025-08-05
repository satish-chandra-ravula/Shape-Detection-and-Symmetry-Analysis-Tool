# Shape-Detection-and-Symmetry-Analysis-Tool
Shape Detection and Symmetry Analysis Tool

This project is a Python GUI application that allows users to upload an image and visualize the following outputs:

Shape Detection including Triangles Squares Rectangles Circles and more

Symmetry Detection by identifying reflection symmetries in objects

Curve Completion to complete broken curves using edge detection and contour approximation

The graphical interface is built using Tkinter and all image processing functionalities are implemented using OpenCV and NumPy.

Features

Upload an image and detect geometric shapes with labels on the image

Identify reflection symmetry in objects and visualize center points

Complete broken curves and visualize bounding boxes and polylines

Display all three outputs simultaneously in a single interface

Shape names and process details are displayed below each panel in the GUI

Technologies Used

Python 3

OpenCV cv2 for image processing

NumPy for array operations

Tkinter for building the graphical user interface

Pillow PIL for displaying images in Tkinter

Project Structure

shape_detection_app.py which is the main Python script

README.md which contains project documentation

requirements.txt for listing required Python packages

Installation and Setup Instructions
1 Clone the repository using git clone and navigate to the project directory
2 Optionally create a Python virtual environment and activate it
3 Install the required Python packages using pip install -r requirements.txt
4 Run the application by executing python shape_detection_app.py

How to Use the Application
1 Launch the application by running the Python script
2 Click the Upload Image button in the interface
3 Select an image file with png jpg or jpeg extension
4 The application will process and display three outputs
a Detected Shapes with shape labels on the image
b Symmetry Detection showing symmetric contours and center points
c Curve Completion displaying completed curves and bounding boxes
5 The names of detected shapes and additional information will be displayed below the images

Limitations

Symmetry detection uses a basic reflection symmetry check and works best with simple symmetric shapes

Curve completion is implemented using Canny Edge Detection and contour approximation techniques not deep learning methods

The accuracy of detection depends on the quality and clarity of input images

Future Enhancements

Improve symmetry detection to handle rotated and scaled shapes
Add Bezier curve fitting for precise curve completions
Provide an option to save the processed output images
Integrate deep learning based models for better shape and symmetry detection

License
This project is open source and available under the MIT License

Contributing
You are welcome to contribute to this project by forking the repository and submitting pull requests For major changes it is recommended to open an issue first to discuss the proposed improvements
