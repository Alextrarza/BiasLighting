import cv2
import tkinter as tk
import serial
import dxcam

def main():
    # open the default camera
    cap = cv2.VideoCapture(0)
    # create camera object to capture screen
    #camera = dxcam.create(output_color="BGR")
    flaga_serial = True
    if not cap.isOpened():
        print("Error opening camera")
        return
    
    # Open the serial port
    try:
        serial_port = serial.Serial('COM11', baudrate=155200, timeout=1)
    except serial.SerialException as e:
        flaga_serial = False
    
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    while True:
        # Capture frame
        ret, frame = cap.read() # capture from camera
        #frame = camera.grab()  # capture full screen screenshot
        if not ret:
            print("Error capturing frame")
            break   
        # Convert colorspace from BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_width = frame.shape[1]
        frame_height = frame.shape[0]
        # Define regions of interest on the four edges of the screen
        roi_left = frame[0:frame_height, 0:10]
        roi_right = frame[0:frame_height, frame_width-10:frame_width]
        roi_top = frame[0:10, 0:frame_width]
        roi_bottom = frame[frame_height-10:frame_height, 0:frame_width]
        # Calculate mean color of edges
        color_left = cv2.mean(roi_left)
        color_right = cv2.mean(roi_right)
        color_top = cv2.mean(roi_top)
        color_bottom = cv2.mean(roi_bottom)
        # Print the average color of the pixels on each edge
        print("Left edge color:", color_left)
        print("Right edge color:", color_right)
        print("Top edge color:", color_top)
        print("Bottom edge color:", color_bottom)
        print()
        # send the color data over the serial port
        if flaga_serial == True:
            try:
                serial_port.write(color_left, color_right, color_top, color_bottom)
            except serial.SerialTimeoutException as e:
                print(f"Error sending data over serial port: {e}")
                return
        
        # show average color on left edge
        frame[0:frame_height, 0:10,:] = color_left[0:-1]
        # show average color on right edge
        frame[0:frame_height, frame_width-10:frame_width] = color_right[0:-1]
        # show average color on top edge
        frame[0:10, 0:frame_width] = color_top[0:-1]
        # show average color on bottom edge
        frame[frame_height-10:frame_height, 0:frame_width] = color_bottom[0:-1]

        # Convert back colorspace from RGB to BGR
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # create the window and show the image
        #cv2.namedWindow("Preview", cv2.WINDOW_NORMAL)
        cv2.imshow("Preview", frame)

        if cv2.waitKey(30) >= 0:
            break
        
    cap.release()
    cv2.destroyAllWindows()
    if flaga_serial == True:
        serial_port.close()
if __name__ == "__main__":
    main()
