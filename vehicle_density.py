import numpy as np
import imutils
import time
import cv2
import datetime
classname = []
#list_of_vehicles = ["bicycle","car","motorbike","bus","truck"]
def get_vehicle_count(boxes, class_names):
    
    total_vehicle_count = 0 # total vechiles present in the image
    dict_vehicle_count = {}
    # dictionary with count of each distinct vehicles detected
    list_of_vehicles = ["bicycle","car","motorbike","bus","truck"]

    for i in range(len(boxes)):
        class_name = class_names[i]
		# print(i,".",class_name)
        if(class_name in list_of_vehicles):
            total_vehicle_count += 1
            dict_vehicle_count[class_name] = dict_vehicle_count.get(class_name,0) + 1

    return total_vehicle_count, dict_vehicle_count


def mainfunc(area_list,video_file):
    
    writer = None
    (W, H) = (None, None)
    print(area_list)
    labelsPath = "./data/labels/coco.names"
    LABELS = open(labelsPath).read().strip().split("\n")
    
    list_of_vehicles = ["car","bus","motorbike","truck","bicycle"]
    
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),dtype="uint8")
    
    weightsPath = "./weights/yolov3.weights"
    configPath = "./weights/yolov3.cfg"
    
    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    
    video_path = video_file
    vs = cv2.VideoCapture(video_path)

    while True:
        counter=[0 for i in range(10)]
    	# read the next frame from the file
        (grabbed, frame) = vs.read()

        if not grabbed:
            break
    
        if W is None or H is None:
            (H, W) = frame.shape[:2]
    
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),swapRB=True, crop=False)
        net.setInput(blob)
        layerOutputs = net.forward(ln)

        boxes = []
        confidences = []
        classIDs = []
    
    	# loop over each of the layer outputs
        for output in layerOutputs:
    		# loop over each of the detections
            for detection in output:

                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                if confidence > 0.6:
                    
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX,centerY, width, height) = box.astype("int")
    

                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
    

                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)
                    classname.append(LABELS[classID])
    
    	# apply non-maxima suppression to suppress weak, overlapping
    	# bounding boxes
        idxs = cv2.dnn.NMSBoxes(boxes, confidences,0.6,0.3)
        
        box_list=[]
        class_list=[]
        if len(idxs) > 0:
            for i in idxs.flatten():
                box_list.append(boxes[i])
                class_list.append(LABELS[classIDs[i]])
    			# extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                
                x1=x
                y1=y
                x2=x+w
                y2=y+h
                
                xc= x1 + (x2-x1)//2
                yc = y1 +((y2-y1)//2)
                
                rcount=0
                for ar in area_list:
                    x1crop = ar[0][0]
                    y1crop = ar[0][1]
                    x2crop = ar[1][0]
                    y2crop = ar[1][1]
                    print(x1crop)
                    print(x2crop)
                    print(y1crop)
                    color1 = (0, 0, 255)
                    cv2.rectangle(frame, (x1crop, y1crop), (x2crop, y2crop), color1, 1)
                    
                    if(xc>x1crop and xc<x2crop  and yc>y1crop  and yc<y2crop ):
                        if(LABELS[classIDs[i]] in list_of_vehicles ):
                            print(LABELS[classIDs[i]])
                            counter[rcount]+=1
                            color = [int(c) for c in COLORS[classIDs[i]]]
                            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                            text = "{}".format(LABELS[classIDs[i]])
                            cv2.putText(frame, text, (x, y - 5),cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                            
                    rcount+=1

        #total_vehicles, each_vehicle = get_vehicle_count(box_list, class_list)
        
        for i in range(len(area_list)):
            color = (0, 0, 255) 
            txt1 = "Region{}:{}".format(i+1,counter[i])
            xi = area_list[i][0][0]
            yi = area_list[i][0][1]
            cv2.putText(frame, txt1, (xi,yi-10),cv2.FONT_HERSHEY_SIMPLEX, 1,color , 2)

        if writer is None:
            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
            filename = "Traffic_Density_%s.avi" % (datetime.datetime.now().strftime('%d%m%Y%H%M'))
            writer = cv2.VideoWriter("./data/output/Traffic Density/"+filename, fourcc, 30,
			                 (frame.shape[1], frame.shape[0]), True)
        writer.write(frame)
    
        if cv2.waitKey(1) == ord('q'):
            break
    print("[INFO] cleaning up...")
    writer.release()
    vs.release()
