import cv2
from Editor import ImageEditor
from typing import Type

def scale_sticker(image1, image2):
    # Get the width of image2
    width_img2 = image2.shape[1]

    # Calculate the new width of image1
    new_width_img1 = int(width_img2 * 0.2)

    # Calculate the scale ratio
    ratio = new_width_img1 / image1.shape[1]

    # Calculate the new height of image1 while maintaining the aspect ratio
    new_height_img1 = int(image1.shape[0] * ratio)

    # Resize image1 with the new width and height
    resized_img1 = cv2.resize(image1, (new_width_img1, new_height_img1))

    return resized_img1

def add_sticker_to_photo(photo, sticker, x, y):
    # Calculate the start and end coordinates to position the sticker
    sticker_height, sticker_width, _ = sticker.shape
    x_start = x - int(sticker_width / 2)
    y_start = y - int(sticker_height / 2)
    x_end = x_start + sticker_width
    y_end = y_start + sticker_height
    
    # Check if the coordinates are within the photo boundaries
    if x_start >= 0 and y_start >= 0 and x_end <= photo.shape[1] and y_end <= photo.shape[0]:
        # Get the region of interest (ROI) in the photo to add the sticker
        roi = photo[y_start:y_end, x_start:x_end]
        
        # Get the alpha channel of the sticker
        sticker_alpha = sticker[:, :, 3] / 255.0
        
        # Apply the sticker to the ROI using the alpha channel
        for c in range(3):
            roi[:, :, c] = sticker_alpha * sticker[:, :, c] + (1 - sticker_alpha) * roi[:, :, c]
    
    return photo

# Function to handle mouse events
def add_sticker(event, x, y, flags, param):
    # Check if the left mouse button is pressed
    if event == cv2.EVENT_LBUTTONDOWN:
        # Scale the sticker image
        sticker = scale_sticker(param.get("sticker"), param.get("photo"))
        photo = add_sticker_to_photo(param.get("photo"), sticker, x, y)
        # Display the photo with the added sticker
        cv2.imshow('Photo with Sticker', photo)
        cv2.imwrite("atualizado.jpg", photo)

def load_images(editor: Type[ImageEditor], param):
    # Create a window to display the photo
    cv2.namedWindow('Photo with Sticker')

    # Initially display the photo
    cv2.imshow('Photo with Sticker', param.get("photo"))

    # Associate the mouse event handling function with the window
    cv2.setMouseCallback('Photo with Sticker', add_sticker, param)

    # Wait until the 'q' key is pressed to close the window
    while True:
        if cv2.waitKey(1) & 0xFF == ord('m'):
            # Close all opened windows
            cv2.destroyAllWindows()
            break
        if cv2.waitKey(1) & 0xFF == ord('s'):
            editor.new_current_image(cv2.imread("atualizado.jpg"))
            editor.display_image(editor.get_current_image())
            cv2.destroyAllWindows()
            break