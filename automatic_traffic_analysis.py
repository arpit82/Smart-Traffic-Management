import time, random
import numpy as np
import datetime
import cv2
import matplotlib.pyplot as plt
import tensorflow as tf
from yolov3_tf2.models import (YoloV3, YoloV3Tiny)
from yolov3_tf2.dataset import transform_images
from yolov3_tf2.utils import draw_outputs, convert_boxes

from deep_sort import preprocessing
from deep_sort import nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from tools import generate_detections as gdet
from PIL import Image


def mainfunc(file_name):
    max_cosine_distance = 0.5
    nn_budget = None
    nms_max_overlap = 1.0
    num_classes = 80
    classes_path = './data/labels/coco.names'
    weights_path = './weights/yolov3.tf'
    output_format = 'XVID'
    video = file_name
    output_filename = "Traffic_Analysis_%s.avi" % (datetime.datetime.now().strftime('%d%m%Y%H%M'))
    output = './data/output/Automatic Traffic Analysis/'+output_filename
    size = 416
    
    
    #initialize deep sort
    model_filename = 'model_data/mars-small128.pb'
    encoder = gdet.create_box_encoder(model_filename, batch_size=1)
    metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
    tracker = Tracker(metric)

    physical_devices = tf.config.experimental.list_physical_devices('GPU')
    if len(physical_devices) > 0:
        tf.config.experimental.set_memory_growth(physical_devices[0], True)

    yolo = YoloV3(classes=num_classes)

    yolo.load_weights(weights_path)
    print('weights loaded')

    class_names = [c.strip() for c in open(classes_path).readlines()]
    print('classes loaded')

    try:
        vid = cv2.VideoCapture(int(video))
    except:
        vid = cv2.VideoCapture(video)

    out = None

    if output:
        # by default VideoCapture returns float instead of int
        width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(vid.get(cv2.CAP_PROP_FPS))
        codec = cv2.VideoWriter_fourcc(*output_format)
        out = cv2.VideoWriter(output, codec, fps, (width, height))
        list_file = open('detection.txt', 'w')
        frame_index = -1 
    
    fps = 0.0
    count = 0 
    centroidsy=[[] for i in range(700)]
    centroidsx=[0 for i in range(700)]
    idCounter=[0 for i in range(700)]
    downCount = 0
    upCount = 0 
    
    while True:
        _, img = vid.read()
        

        if img is None:
            print("Empty Frame")
            time.sleep(0.1)
            count+=1
            if count < 2:
                continue
            else: 
                break

        img_in = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
        img_in = tf.expand_dims(img_in, 0)
        img_in = transform_images(img_in, size)

        t1 = time.time()
        boxes, scores, classes, nums = yolo.predict(img_in)
        classes = classes[0]
        
        names = []
        for i in range(len(classes)):
            names.append(class_names[int(classes[i])])
        names = np.array(names)
        converted_boxes = convert_boxes(img, boxes[0])
        features = encoder(img, converted_boxes)    
        detections = [Detection(bbox, score, class_name, feature) for bbox, score, class_name, feature in zip(converted_boxes, scores[0], names, features)]
        
        #initialize color map
        cmap = plt.get_cmap('tab20b')
        colors = [cmap(i)[:3] for i in np.linspace(0, 1, 20)]

        # run non-maxima suppresion
        boxs = np.array([d.tlwh for d in detections])
        scores = np.array([d.confidence for d in detections])
        classes = np.array([d.class_name for d in detections])
        indices = preprocessing.non_max_suppression(boxs, classes, nms_max_overlap, scores)
        detections = [detections[i] for i in indices]  

        print(classes)
        vehicles=["bicycle","car","motorbike","bus","truck"]
        #ind_list=[]
        class_list=list(classes)
        count_bicycle=0
        count_car=0
        count_motorbike=0
        count_bus=0
        count_truck=0
        for cl in class_list:
            if cl in vehicles:
                if cl =="bicycle":
                    count_bicycle += 1
                elif cl == "car":
                    count_car += 1
                elif cl == "motorbike":
                    count_motorbike += 1
                elif cl == "bus":
                    count_bus += 1
                elif cl == "truck":
                    count_truck += 1
                    
        width_image = img.shape[1]
        height_image = img.shape[0]
        cv2.putText(img,"Cars: "+str(count_car),(width_image-200,30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0),2)
        cv2.putText(img,"Truck: "+str(count_truck),(width_image-200, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50,255,0),2)
        cv2.putText(img,"Bus: "+str(count_bus),(width_image-200, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (55,55,55),2)
        cv2.putText(img,"Motorbike: "+str(count_motorbike),(width_image-200, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255),2)
        cv2.putText(img,"Bicycle: "+str(count_bicycle),(width_image-200, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0),2)
        
        xcord = width_image
        ycord = height_image//2
        
        cv2.line(img, (0,ycord),(xcord,ycord), (0, 0, 255), 2)
        
        #detections = [detections[j] for j in ind_list] 
        # Call the tracker
        tracker.predict()
        tracker.update(detections)
         
        
        for track in tracker.tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                continue 
            bbox = track.to_tlbr()
            class_name = track.get_class()
            color = colors[int(track.track_id) % len(colors)]
            color = [i * 255 for i in color]
            
            obj_id = track.track_id
            
            x1=int(bbox[0])
            y1=int(bbox[1])
            x2=int(bbox[2])
            y2=int(bbox[3])
            
            xc= x1+ (x2-x1)//2
            yc = y1+((y2-y1)//2)
            
            print("id=",obj_id)
            

            centroidsy[obj_id].append(yc)
            centroidsx[obj_id]=xc
            
            new = centroidsy[obj_id][-1]
            olds= centroidsy[obj_id][1:len(centroidsy[obj_id])-1]
            prev_mean = np.mean(olds)
            
            direction = new - prev_mean
            
            if(direction>0 and new > ycord and olds[0] < ycord and centroidsx[obj_id] >= 0 and centroidsx[obj_id] < xcord):
                if(idCounter[obj_id]!=1):
                    downCount += 1
                    #id_list.append(obj_id)
                idCounter[obj_id]=1
                
            elif(direction<0 and new < ycord and olds[0] > ycord and centroidsx[obj_id] >= 0 and centroidsx[obj_id] <= xcord):
                if(idCounter[obj_id]!=1):
                    upCount += 1
                   # id_list.append(obj_id)
                idCounter[obj_id]=1
                
                
            cv2.putText(img,"Down Count: "+str(downCount),(width_image-200,130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255),2)
            cv2.putText(img,"Up Count: "+str(upCount),(width_image-200,150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255),2)
            
            
            cv2.rectangle(img, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color, 2)
            cv2.rectangle(img, (int(bbox[0]), int(bbox[1]-30)), (int(bbox[0])+(len(class_name)+len(str(track.track_id)))*17, int(bbox[1])), color, -1)
            cv2.putText(img, class_name + "-" + str(track.track_id),(int(bbox[0]), int(bbox[1]-10)),0, 0.75, (255,255,255),2)
        
        fps  = ( fps + (1./(time.time()-t1)) ) / 2
        cv2.putText(img, "FPS: {:.2f}".format(fps), (0, 30),
                          cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)
        cv2.imshow('output', img)
        if output:
            out.write(img)
            frame_index = frame_index + 1
            list_file.write(str(frame_index)+' ')
            if len(converted_boxes) != 0:
                for i in range(0,len(converted_boxes)):
                    list_file.write(str(converted_boxes[i][0]) + ' '+str(converted_boxes[i][1]) + ' '+str(converted_boxes[i][2]) + ' '+str(converted_boxes[i][3]) + ' ')
            list_file.write('\n')
        
                # press q to quit
        if cv2.waitKey(1) == ord('q'):
                    break
        
            
    vid.release()
    if output:
        out.release()
        list_file.close()
    cv2.destroyAllWindows()