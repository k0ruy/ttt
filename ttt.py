
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the PNG image
image_path = 'shapes/vecteezy_doodle-freehand-drawing-of-bali-island-map_21454377.png'
image_png = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

# Extract the alpha channel as the border should be clear on it
alpha_channel = image_png[:, :, 3]

# Invert the alpha channel so the border is white and the background is black
_, binary_alpha = cv2.threshold(alpha_channel, 0, 255, cv2.THRESH_BINARY)

# Find contours on the binary alpha channel
contours_png, _ = cv2.findContours(binary_alpha, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Again, assuming the largest contour is the border of Bali
largest_contour_png = max(contours_png, key=cv2.contourArea)

# Simplify the contour to reduce the number of points
epsilon_png = 1/(10**10) * cv2.arcLength(largest_contour_png, True)
approx_border_png = cv2.approxPolyDP(largest_contour_png, epsilon_png, True)

# Extract the border coordinates
border_coordinates_png = approx_border_png.squeeze()
border_coordinates_png[:,1] = -border_coordinates_png[:,1]


# Calculate the centroid
centroid = np.mean(border_coordinates_png, axis=0)

# Calculate the angles and distances for each point
angles = np.arctan2(border_coordinates_png[:, 1] - centroid[1], border_coordinates_png[:, 0] - centroid[0])
distances = np.sqrt((border_coordinates_png[:, 0] - centroid[0])**2 + (border_coordinates_png[:, 1] - centroid[1])**2)

# Choose a new starting point (by index or coordinates)
new_start_index = 5000  # for example, you can set this to any index you want

# Calculate the angle offset
angle_offset = angles[new_start_index]

# Adjust the angles by the angle offset
adjusted_angles = angles - angle_offset

# Ensure the angles are within the range (-π, π)
adjusted_angles = (adjusted_angles + np.pi) % (2 * np.pi) - np.pi

# Sort the points by the adjusted angle
sorted_indices = np.argsort(adjusted_angles)
sorted_angles = adjusted_angles[sorted_indices]
sorted_distances = distances[sorted_indices]

# Create the plot
fig, ax = plt.subplots(figsize=(30, 10))
ax.scatter(np.degrees(sorted_angles), -sorted_distances, s=1)  # Convert angles to degrees for better readability
# ax.set_xlabel('Angle (degrees)')
# ax.set_ylabel('Distance from Centroid')
# ax.set_title('Radial Unfolding of Bali Border with New Starting Point')
ax.set_aspect(1/30)
ax.axis('off')

# plot bali contour
#ax.plot(border_coordinates_png[:,0], border_coordinates_png[:,1])
plt.show()
