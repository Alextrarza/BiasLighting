from PIL import Image
from pixels_on_vector import *
import numpy as np
import cv2
import pandas 

# Open the image
im = Image.open('image.jpg')

vector_mean = []
width, height = im.size
frame = np.zeros((height,width,3), np.uint8)
# Define the starting and ending coordinates of the vector
end = (round(width/2),round(height/2))

def createLineIterator(P1, P2, img):
    #Produces and array that consists of the coordinates and intensities of each pixel in a line between two points

    #Parameters:
    #    -P1: a numpy array that consists of the coordinate of the first point (x,y)
    #    -P2: a numpy array that consists of the coordinate of the second point (x,y)
    #    -img: the image being processed

    #Returns:
    #    -it: a numpy array that consists of the coordinates and intensities of each pixel in the radii (shape: [numPixels, 3], row = [x,y,intensity])     
    
    #define local variables for readability
    imageH = height
    imageW = width
    P1X = P1[0]
    P1Y = P1[1]
    P2X = P2[0]
    P2Y = P2[1]

    #difference and absolute difference between points
    #used to calculate slope and relative location between points
    dX = P2X - P1X
    dX = np.intc(dX)
    dY = P2Y - P1Y
    dY = np.intc(dY)
    dXa = np.abs(dX)
    dYa = np.abs(dY)

    #predefine numpy array for output based on distance between points
    itbuffer = np.empty(shape=(np.maximum(dYa,dXa),3),dtype=np.float32).astype(np.float32)
    itbuffer.fill(np.nan)
    px = im.load()
    
    #Obtain coordinates along the line using a form of Bresenham's algorithm
    negY = P1Y > P2Y
    negX = P1X > P2X
    if P1X == P2X: #vertical line segment
        itbuffer[:,0] = P1X
        if negY:
            itbuffer[:,1] = np.arange(P1Y - 1,P1Y - dYa - 1,-1)
        else:
            itbuffer[:,1] = np.arange(P1Y+1,P1Y+dYa+1)              
    elif P1Y == P2Y: #horizontal line segment
        itbuffer[:,1] = P1Y
        if negX:
            itbuffer[:,0] = np.arange(P1X-1,P1X-dXa-1,-1)
        else:
            itbuffer[:,0] = np.arange(P1X+1,P1X+dXa+1)
    else: #diagonal line segment
        steepSlope = dYa > dXa
        if steepSlope:
            slope = dX.astype(np.float32)/dY.astype(np.float32)
            if negY:
                itbuffer[:,1] = np.arange(P1Y-1,P1Y-dYa-1,-1)
            else:
                itbuffer[:,1] = np.arange(P1Y+1,P1Y+dYa+1)
            itbuffer[:,0] = (slope*(itbuffer[:,1]-P1Y)).astype(np.intc) + P1X
        else:
            slope = dY.astype(np.float32)/dX.astype(np.float32)
            if negX:
                itbuffer[:,0] = np.arange(P1X-1,P1X-dXa-1,-1)
            else:
                itbuffer[:,0] = np.arange(P1X+1,P1X+dXa+1)
            itbuffer[:,1] = (slope*(itbuffer[:,0]-P1X)).astype(np.intc) + P1Y

    #Remove points outside of image
    colX = itbuffer[:,0]
    colY = itbuffer[:,1]
    itbuffer = itbuffer[(colX >= 0) & (colY >=0) & (colX<imageW) & (colY<imageH)]
   
    #Get intensities from img ndarray
    return itbuffer

for szerokosc in range(width):
    for wysokosc in range(height):
        if szerokosc==0 or szerokosc==width-1 or wysokosc==0 or wysokosc==height-1:
            # Calculate the x,y coordinates of each point along the vector
            points = createLineIterator((szerokosc, wysokosc), end , im)
            
            # Get the color of each pixel along the vector
            colors = []
            for point in points:
                x, y, z = point
                color = im.getpixel((int(x), int(y)))
                frame[int(y), int(x)] = color
                colors.append(color)
            
            vector_mean.append(colors)
            
            

# Print the colors of the pixels along the vector
print(vector_mean)
frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
cv2.imshow("Preview",frame)
cv2.waitKey()
cv2.destroyAllWindows()

