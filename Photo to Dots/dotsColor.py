'''
Justine Serdoncillo
September 26, 2023
ARTS 3890 - 3D Modeling and Fabrication
'''

"""
Transform an input image into colored dots to represent an image
"""

"""
Feedback
- varying sizes of circles per channel
- choose an image that has a higer contrast
- find one that has 3 sliding things already
- maybe 3d print a container 
"""

import numpy as np
import cv2
import random
import matplotlib.pyplot as plt
import matplotlib.image as img


def showImage(imageName):
    if np.shape(imageName) == ():
        print("Empty Image")
        return 0
    else:
        while (True):
            cv2.imshow("Display", imageName)
            if cv2.waitKey(20) & 0xFF == 27: # ASCII character = 27 which is 'escape'
                break  
        cv2.destroyWindow("Display")
        
def saveImage(imageName, filename):
    showImage(imageName)
    name = "images/saved/" + filename + ".png"
    cv2.imwrite(name, imageName)


# %%
if __name__ == "__main__":
    # Import and view the image
    name = "test2"
    file = "images/" + name + ".jpg"
    image = cv2.imread(file)    
    raw = np.asarray(image)

    # Creating the image into a square
    print(raw.shape)
    lowIndex = np.argmin(raw.shape[:-1])
    low = raw.shape[lowIndex]
    if lowIndex == 0:
        g = raw.shape[1]
        p = int(round(0.5*(g-low)))
        centered = raw[:,p:-p,:]
        print(centered.shape)
    else:
        g = raw.shape[0]
        p = int(round(0.5*(g-low)))
        if p % 2 == 0:
            centered = raw[p:-p-1,:,:]
        else:
            centered = raw[p:-p,:,:]
        print(centered.shape)    
    #showImage(centered)
    #saveImage(centered, "center"+name)
       
    # Pad image
    thick = int(round(low*(0.4)))
    newImage = np.ones((low+2*thick, low+2*thick, 3), np.uint8) * 127
    newImage[thick:thick+low, thick:thick+low, :] = centered
    centered = np.copy(newImage)
    #saveImage(centered, "padded"+name)
    
    # Create a new array of new size
    numCirc = 49 # should be an odd number
    scale = [1/5, 1/6, 1/7]
    d = int(round(centered.shape[0]/(numCirc+1))*0.75)
    mid = int(round(0.5*low))
    
    colors = np.zeros((numCirc,numCirc,3))
    th = np.array([np.pi*2/3,0,np.pi*4/3])
    xx = np.zeros((numCirc,numCirc,3),dtype=int) + mid #+ int(round(mid/2))
    yy = np.zeros((numCirc,numCirc,3),dtype=int) + mid #+ int(round(mid/2))
    lowest  = -int(np.floor(0.5*numCirc))
    highest =  int(np.floor(0.5*numCirc))
    
    # Sample the color value of each channel across the image
    for y in np.arange(lowest, highest+1):
        for x in np.arange(lowest, highest+1):
            for k in range(3):
                yy[y,x,k] += d*y*np.cos(th[k]) - d*x*np.sin(th[k])
                xx[y,x,k] += d*y*np.sin(th[k]) + d*x*np.cos(th[k])
    
    # Determine the size of the circle based on the color channel value
    for y in np.arange(lowest, highest+1):
        for x in np.arange(lowest, highest+1):
            for k in range(3):
                colors[y,x,k] = centered[yy[y,x,k]+thick,xx[y,x,k]+thick,k]*scale[k]
    
    # Add a slight shift so not fully centered
    #for k in range(3):
    #    xx[:,:,k] += k-1
    #    yy[:,:,k] += k-1
    
    # Plot the photo  
    cs = 'bgr'
    fig, ax = plt.subplots(figsize=(4,4), dpi=int(low/2))
    ax.set_axis_off()
    ax.set_xlim([0   , low])
    ax.set_ylim([-low,   0])
    for C in range(3): 
        ax.scatter(xx[:,:,C].flatten(), -yy[:,:,C].flatten(), s=colors[:,:,C].flatten(), color=cs[C], alpha=0.1)
        
    for C in range(3): 
        fig, ax = plt.subplots(figsize=(4,4), dpi=int(low/2))
        ax.set_axis_off()
        ax.set_xlim([0   , low])
        ax.set_ylim([-low,   0])
        ax.scatter(xx[:,:,C].flatten(), -yy[:,:,C].flatten(), s=colors[:,:,C].flatten(), color="k", alpha=0.1)

         
       
    