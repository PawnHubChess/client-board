import cv2
import numpy as np

class ImageRecognition:
    def __init__(self):
        self.move_from = None
        self.move_to = None

    def find_moved_piece(self):
        image1 = cv2.imread("image1.jpg")
        image2 = cv2.imread("image2.jpg")

        gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        
        diff = cv2.absdiff(gray1, gray2)
        
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return "Could not detect the moved piece."
        
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]
        
        def map_to_grid(x, y, board_size):
            letters = 'ABCDEFGH'
            grid_size = image1.shape[1] // board_size
            letter = letters[x // grid_size]
            number = board_size - (y // grid_size)
            return f"{letter}{number}"
        
        M = cv2.moments(contours[0])
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            self.move_to = map_to_grid(cX, cY, 8)
        else:
            self.move_to = None

        M = cv2.moments(contours[1])
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            self.move_from = map_to_grid(cX, cY, 8)
        else:
            self.move_from = None
        
# image_rec = ImageRecognition()
# image_rec.find_moved_piece()
# print(image_rec.move_from)
# print(image_rec.move_to)
