import cv2
from gui_buttons import Buttons

#Initialize buttons
button = Buttons()
button.add_button("person",20,20)
button.add_button("cell phone",20,80)
button.add_button("book",20,140)
button.add_button("bottle",20,200)
button.add_button("cat",20,260)

#OpenCV DNN
net=cv2.dnn.readNet("dnn_model\dnn_model\yolov4-tiny.weights","dnn_model\dnn_model\yolov4-tiny.cfg")
model=cv2.dnn_DetectionModel(net)
model.setInputParams(size=(320,320),scale=1/255)

class_list=[]
with open("dnn_model\dnn_model\classes.txt", "r") as file_obj:
    for item in file_obj.readlines():
        obj=item.strip()
        class_list.append(obj)

# print(class_list)

#Initialize camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

# button_person=False

def click_button(event,x,y,flags,params):
    global button_person
    if event==cv2.EVENT_LBUTTONDOWN:
        # print(x,y)
        # polygon=np.array([[(20,20),(220,20),(220,70),(20,70)]])

        # is_inside=cv2.pointPolygonTest(polygon, (x,y), False)
        # if is_inside>0:
            
        #     if button_person is False:
        #         button_person=True
        #     else:
        #         button_person=False
        button.button_click(x,y)


# Create Window
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame",click_button)

while True:
    # Get frames
    ret, frame=cap.read()

    #Get active buttons
    active_buttons=button.active_buttons_list()


    # Object detection
    (class_ids, scores, boundingBoxes)=model.detect(frame)

    # #Draw button
    # polygon=np.array([[(20,20),(220,20),(220,70),(20,70)]])
    # cv2.fillPoly(frame, polygon, (0,0,100))
    # cv2.putText(frame, "Person", (30,60), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,255), 3)
    
    
    #Writing object class
    for class_id,score,bbox in zip(class_ids,scores,boundingBoxes):
        (x,y,w,h)=bbox
        #Draw a class
        className=class_list[class_id]

        if className in active_buttons:
            cv2.putText(frame, className,(x,y-5), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,255), 3)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)

    #Display button
    button.display_buttons(frame)
    
    
    cv2.imshow("Frame",frame)
    if cv2.waitKey(1)==ord('a'):
        break

cap.release()
cv2.destroyAllWindows()