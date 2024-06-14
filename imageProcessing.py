import cv2
import numpy as np

# Clean image
# This function takes and image as input and reduces the noise resulting in strong definition of the edges especially between the text and the background.
# The function takes the following parameters:
# imgPath: The location to be processed
def cleanImage(imgPath):
    # Read image
    img = cv2.imread(imgPath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Increase size
    scaling_factor = 4.0  # TODO make this conditional - ie only if we are dealing with a small image
    new_width = int(img.shape[1] * scaling_factor)
    new_height = int(img.shape[0] * scaling_factor)
    img = cv2.resize(img, (new_width, new_height))

    # Apply dilation and erosion together in a process know as "opening"
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # Write image to disk
    cv2.imwrite("removed_noise.png", img)
    cv2.imshow("removed_noise.png", img)
    
    # Apply threshold to get image with only black and white 
    # Notes: Adaptive thresh is suposed to be more complex.  As is I'm getting better results from global but that may not be true with photos (esp w shadow)
    # https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html
    # adaptiveThresh = cv2.adaptiveThreshold(
    #     img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2
    # )
    # noise_removed = cv2.medianBlur(adaptiveThresh, 3)
    # _, multiThresh = cv2.threshold(noise_removed, 150, 255, cv2.THRESH_BINARY_INV)
    # multiThresh = cv2.medianBlur(multiThresh, 3)   
    # _, multiThresh = cv2.threshold(multiThresh, 150, 255, cv2.THRESH_BINARY_INV) 

    _, globalThresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV)   
    cv2.imwrite("globalThresh.png", globalThresh)
    cv2.imshow("globalThresh.png", globalThresh)
    #cv2.waitKey(0)

    # TESTING
    # noThresh = pytesseract.image_to_string(img)
    # adaptiveThresh = pytesseract.image_to_string(multiThresh)

    # globalThresh = pytesseract.image_to_string(globalThresh)
    # # Print the extracted text
    # print("Img:")
    # print(noThresh)

    # # print("adaptive/multiThresh:")
    # # print(multiThresh)
    
    # print("globalThresh:")
    # print(globalThresh)

    return img
