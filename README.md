# Smart-Traffic-Management
Smart Traffic Management is an AI based project which is used to automatically manage the Traffic in the cities 
by applying some Deep Learning Algorithms. This Project mainly performs 3 functions:
1)Traffic Violation Detections: Detects the vehicles when it is Crossing the Traffic Signal during Red Light and also
stores those vehicle images.
2)Traffic Density Calculation : Calculates the Total No. Of Vehicles in different regions of the video.It can be used
to dynamically manage Traffic Lights.
3)Automatic Traffic Analysis : Analyze the Traffic Automatically using Object Detection and Object Tracking.

Requirements

1.	Python is the basic requirement. Python should be installed on system and running. If you have GPU run the requirement file for GPU.
i.	TensorFlow CPU - pip install -r requirements.txt
ii.	TensorFlow GPU - pip install -r requirements-gpu.txt

2. For Running in Anaconda :
(i)Tensorflow CPU
conda env create -f conda-cpu.yml
conda activate tracker-cpu

(ii)Tensorflow GPU
conda env create -f conda-gpu.yml
conda activate tracker-gpu

3.	Nvidia Driver (For GPU, if you haven't set it up already)
(i)	Ubuntu 18.04
            sudo add-apt-repository ppa:graphics-drivers/ppa
            sudo apt install nvidia-driver-430
(ii)	Windows/Other - https://www.nvidia.com/Download/index.aspx

4. Downloading official pretrained weights (While the weights have already been added if you want to add any other model weighhts or your 
own model weights . Add them in the weights folder and remove already present weights.)
(i)	 For Linux: Let's download official yolov3 weights pretrained on COCO dataset. 
    wget https://pjreddie.com/media/files/yolov3.weights -O weights/yolov3.weights

(ii)For Windows: You can download the yolov3 weights here:    https://pjreddie.com/media/files/yolov3.weights then save them to the weights folder.

5. Saving your yolov3 weights as a TensorFlow model.Load the weights using `load_weights.py` script. This will convert the yolov3 weights into TensorFlow .tf model files. Execute python load_weights.py command on cmd in the folder containing load_weights.py file, you should see proper .tf files in your weights folder. You are now ready to run the application.

6. Change the paths of various files and folders in all the python files according to your system.
