# import numpy as np
# import pandas as pd
# import cv2
# import matplotlib.pyplot as plt
# import os


# path = 'C:/Users/lenovo/Pictures/Disease_dataset/app/src'
# img1 = cv2.imread(os.path.join(path, 'ME9a119499f199bba787f40a2be65e0908.jpg'))

# img_building = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)  # Convert from cv's BRG default color order to RGB

# orb = cv2.ORB_create()  # OpenCV 3 backward incompatibility: Do not create a detector with `cv2.ORB()`.

# key_points, description = orb.detectAndCompute(img_building, None)
# img_building_keypoints = cv2.drawKeypoints(img_building, 
#                                            key_points, 
#                                            img_building, 
#                                            flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# final_img = cv2.resize(img_building_keypoints, (1000,650))
# cv2.imwrite('C:/Users/lenovo/Pictures/Disease_dataset/app/cv/test.jpg', final_img) 
# print('done')

# plt.figure(figsize=(16, 16))
# plt.title('ORB Interest Points')
# plt.imshow(img_building_keypoints); 
# plt.show()
# cv2.waitKey()
# cv2.destroyAllWindows()

# import threading
# import time

# def sleepy_man(secs):
#     print('Starting to sleep inside')
#     time.sleep(secs)
#     print('Woke up inside')

# x = threading.Thread(target = sleepy_man, args = (1,))
# x.start()
# print(threading.activeCount())
# time.sleep(1.2)
# print('Done')

import json
import os

# with open("data.json", encoding='utf-8', errors='ignore') as f:
#     data = json.load(f)
#     data["id"] = "greet"
#     json.dump(data, open("data.json", "w"), indent = 4)
#     print(data["id"])

print(os.getcwd()+'\src')