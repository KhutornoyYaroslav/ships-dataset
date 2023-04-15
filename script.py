import numpy as np
import cv2
import _utils
from pathlib import Path
from PIL import Image

folder_name = r"C:\Users\RMC\Desktop\start"
folder = Path(folder_name)
if folder.is_dir():
    folder_count = len([1 for file in folder.iterdir()])


for i in range(folder_count):
    image = folder_name+'\ship_'+str(i)+'.jpeg'
    print(image)
    smallestSideSize = 500
    # real would be thicker because of masking process
    mainRectSize = .04
    fgSize = .15

    img = cv2.imread(image)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    height, width = img.shape[:2]
    new_w, new_h = _utils.new_image_size(width, height, smallestSideSize)

    # resize image to lower resources usage
    # if you need masked image in original size, do not resize it
    img_small = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # quantify colors
    img_small = _utils.quantify_colors(img_small, 32, 10)

    # create mask tpl
    mask = np.zeros(img_small.shape[:2], np.uint8)

    # create BG rect
    bg_w = round(new_w * mainRectSize)
    bg_h = round(new_h * mainRectSize)
    bg_rect = (bg_w, bg_h, new_w - bg_w, new_h - bg_h)

    # create FG rect
    fg_w = round(new_w * (1 - fgSize) / 2)
    fg_h = round(new_h * (1 - fgSize) / 2)
    fg_rect = (fg_w, fg_h, new_w - fg_w, new_h - fg_h)

    # color: 0 - bg, 1 - fg, 2 - probable bg, 3 - probable fg
    cv2.rectangle(mask, fg_rect[:2], fg_rect[2:4], color=cv2.GC_FGD, thickness=-1)

    mask_preset = mask.copy()

    bgdModel1 = np.zeros((1, 65), np.float64)
    fgdModel1 = np.zeros((1, 65), np.float64)

    cv2.grabCut(img_small, mask, bg_rect, bgdModel1,
                fgdModel1, 3, cv2.GC_INIT_WITH_RECT)
    mask_rect = mask.copy()

    cv2.rectangle(mask, bg_rect[:2], bg_rect[2:4],
                color=cv2.GC_PR_BGD, thickness=bg_w * 3)

    cv2.grabCut(img_small, mask, bg_rect, bgdModel1,
                fgdModel1, 10, cv2.GC_INIT_WITH_MASK)

    mask_mask = mask.copy()

    # mask to remove background
    mask_result = np.where((mask == 1) + (mask == 3), 255, 0).astype('uint8')

    # if we are removing too much, assume there is no background
    unique, counts = np.unique(mask_result, return_counts=True)
    mask_dict = dict(zip(unique, counts))

    if mask_dict[0] > mask_dict[255] * 1.6:
        mask_result = np.where((mask == 0) + (mask != 1) +
                            (mask != 3), 255, 0).astype('uint8')

    # apply mask to image
    masked = cv2.bitwise_and(img_small, img_small, mask=mask_result)
    masked[mask_result < 2] = [0, 0, 255]  # change black bg to blue

    mask_mask = mask_mask*70
    # draw rect on original image
    cv2.rectangle(img_small, bg_rect[:2], bg_rect[2:4], (255, 0, 0), 2)
    cv2.rectangle(img_small, fg_rect[:2], fg_rect[2:4], (0, 255, 0), 2, cv2.FILLED)


    _, mask_mask = cv2.threshold(mask_mask, 141, 255, cv2.THRESH_BINARY)

    
    im2 = Image.fromarray(mask_mask)
    # сохраняем новое изображение
    im2.save(r"C:\Users\RMC\Desktop\ready\s_"+str(i)+".jpeg")
