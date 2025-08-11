import cv2
import numpy as np

image = cv2.imread("opencv/shapes.jpg")

# ==== Step 1: convert the image to grayscale ==== 
image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# ==== Step 2: apply Canny edge detection ====
lower_threshold = 50
upper_threshold = 150

canny_edge = cv2.Canny(image_grayscale, lower_threshold, upper_threshold)

# ==== Step 3: find contours ====
contours, hierarchy = cv2.findContours(
    canny_edge.copy(), 
    cv2.RETR_EXTERNAL, 
    cv2.CHAIN_APPROX_NONE
)

# ==== Step 4: find the length of the contours ====
print(f"Number of contours found: {len(contours)}")
print(f"Hierarchy: {hierarchy}")
print(contours[0])

# ==== Display Images ====
cv2.imshow("Original Image", image)
cv2.imshow("Grayscale Image", image_grayscale)
cv2.imshow("Canny Edge Detection", canny_edge)

cv2.waitKey(0) 