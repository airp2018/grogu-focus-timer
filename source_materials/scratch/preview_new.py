import shutil, os

artifacts_dir = r"C:\Users\YANQIAO\.gemini\antigravity-ide\brain\71bd9e19-837b-4572-81e1-4c753dba50f4"

import cv2
cap1 = cv2.VideoCapture("饼干.mp4")
cap1.set(cv2.CAP_PROP_POS_FRAMES, 20)
ret, f1 = cap1.read()
cv2.imwrite(os.path.join(artifacts_dir, "cookie1_new.png"), f1)

cap2 = cv2.VideoCapture("饼干2.mp4")
cap2.set(cv2.CAP_PROP_POS_FRAMES, 60)
ret, f2 = cap2.read()
cv2.imwrite(os.path.join(artifacts_dir, "cookie2_new.png"), f2)

cap1.release(); cap2.release()
print("Done")
