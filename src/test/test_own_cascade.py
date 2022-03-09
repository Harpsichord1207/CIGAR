import cv2


model_file = 'cascade.xml'
test_image = r'C:\Users\liutao3\Desktop\CigTemp\ARImages\pz1.jpg'

model = cv2.CascadeClassifier(model_file)
image = cv2.imread(test_image)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

minSizeWidth = int((image.shape[0] + image.shape[1]) / 20)
print(minSizeWidth)
targets = model.detectMultiScale(gray_image, 1.3, 5, 0, (minSizeWidth, minSizeWidth))

for x, y, w, h in targets:
    print(w, h)
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)


cv2.imwrite("res.jpg", image)
# cv2.imshow("CV2", cv2.resize(image, (960, 540)))
# cv2.waitKey(0)


if __name__ == '__main__':
    pass
