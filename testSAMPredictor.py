from ultralytics.models.sam import Predictor as SAMPredictor
import cv2


#open a file with yolo bounding box annotations and draw them on an image using CV
#bounding boxes are annotated as follows:
#<object-class> <x_center> <y_center> <width> <height>
#where x_center, y_center, width, and height are relative to image size, so they must be multiplied by image width and height to get pixel values
#this function reads in these values, draws them on the image, and shows the image
#it then 
def showSegmentAndBoxes(imagePath, annotationPath):
    #open image
    image = cv2.imread(imagePath)
    #get image dimensions
    imageHeight, imageWidth, channels = image.shape

    bboxes = [] 


    # Create SAMPredictor
    overrides = dict(conf=0.25, task='segment', mode='predict', imgsz=1024, model="mobile_sam.pt")
    predictor = SAMPredictor(overrides=overrides)
    predictor.set_image(cv2.imread(imagePath))

    #open annotation file
    with open(annotationPath, 'r') as f:
        #read each line
        for line in f:
            #split line into list of strings
            line = line.split()
            #convert strings to floats
            line = [float(i) for i in line]
            #convert relative values to pixel values
            x_center = int(line[1] * imageWidth)
            y_center = int(line[2] * imageHeight)
            width = int(line[3] * imageWidth)
            height = int(line[4] * imageHeight)
            #calculate bounding box corners
            x1 = int(x_center - width/2)
            y1 = int(y_center - height/2)
            x2 = int(x_center + width/2)
            y2 = int(y_center + height/2)

            #save bounding box coordinates
            # bboxes.append([x1, y1, x2, y2])

            results = predictor(bboxes=[x1, y1, x2, y2])
            

            #draw bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 1)
            #show image
            cv2.imshow('Box', image)
            #wait .5 seconds
            cv2.waitKey(500)

       



showSegmentAndBoxes('./poop.jpg', './test/Barley_103_D4_12Aug2020.txt')

