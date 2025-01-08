# PNG to OBJ

<p style="text-align: justify;">
  <strong>Input PNG</strong>
  <br/><br/>
  <img src="https://github.com/user-attachments/assets/95b306a2-70f1-4b07-a64e-2e3aff7fd5ed"/>
</p>

<p style="text-align: justify;">
  <strong>Output OBJ</strong>
  <br/><br/>
  <img src="https://github.com/user-attachments/assets/8c65d2f0-8680-42e8-a9e1-5db6f524911b"/>
</p>

<p style="text-align: justify;">
  The program begins by loading the image from the specified path and converting it into a pixel matrix for processing. The dimensions of the image (height and width) are obtained, and an empty list is initialized to store the coordinates of the detected objects. Additionally, a 3x3 iterator square (9 positions) is created to examine the neighboring pixels around the central pixel during processing.
</p>

<p style="text-align: justify;">
  The program iterates through the image pixel by pixel using a nested loop. In each iteration, the iterator square is updated, normalizing the coordinates to avoid segmentation errors when accessing pixels outside the image boundaries. If the central pixel of the iterator square is non-null (i.e., not empty) and has not been previously registered in the coordinates list, the contour tracking of the object begins.
</p>

<p style="text-align: justify;">
  During contour tracking, an empty list is created to store the coordinates of the detected object. The program follows a clockwise rotation order, starting from the pixel above the central pixel, to examine the neighboring pixels. At each step, it searches for a group of two adjacent pixels where one is non-null and the other is empty. When such a group is found, the non-null pixel is selected as the next pixel on the object's edge. The iterator square is updated to this new pixel, and the coordinate is recorded in the current object's list.
</p>

<p style="text-align: justify;">
  This process continues until the program returns to the initial pixel, indicating that the object's contour has been closed. At this point, the object's coordinate list is added to the main list of detected objects. Once the contour tracking ends, the iterator square resumes its traversal of the image from where it left off. If it encounters a non-null pixel that has already been registered, it is ignored, as it belongs to a previously captured object. If it finds a non-null pixel that has not been registered, it initiates the tracking of a new object.
</p>

<p style="text-align: justify;">
  Finally, the coordinates of all detected objects are stored sequentially in the main list, ready for use in retopology. This retopology can be performed by evaluating groups of three consecutive pixels to detect straight lines and simplify the object's representation in a 3D model.
</p>
