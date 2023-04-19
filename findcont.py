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

    contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    '''
    max = 0
    sel_countour = None
    for countour in contours:
        if countour.shape[0] > max:
            sel_countour = countour
            max = countour.shape[0]
    '''

    cv2.drawContours(black_image, contours, -1, (255, 255, 255), 47)
    im2 = Image.fromarray(black_image)
    # сохраняем новое изображение
    im2.save(r"C:\Users\RMC\Desktop\ready\s_"+str(i)+".jpeg")
    