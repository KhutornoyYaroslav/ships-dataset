import cv2
import numpy as np
from pathlib import Path
from PIL import Image
  
# Let's load a simple image with 3 black squares
folder_name = r"C:\Users\RMC\Desktop\start"
folder = Path(folder_name)
if folder.is_dir():
    folder_count = len([1 for file in folder.iterdir()])

for i in range(folder_count):
    img = folder_name+'\ship_'+str(i)+'.jpeg'
    print(img)

    image = cv2.imread(img)
 
    # Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Find Canny edges
    
    edged = cv2.Canny(gray, 30, 200)
    



    black_image = image//255

    # Finding Contours
    # Use a copy of the image e.g. edged.copy()
    # since findContours alters the image

    cv2.imshow('image', edged)
    cv2.waitKey(0)

    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    print()

    cv2.drawContours(black_image, contours, -1, (255, 255, 255), -1)
    cv2.imshow('image', black_image)
    cv2.waitKey(0)

    im2 = Image.fromarray(black_image)
    # сохраняем новое изображение
    im2.save(r"C:\Users\RMC\Desktop\ready\s_"+str(i)+".jpeg")
