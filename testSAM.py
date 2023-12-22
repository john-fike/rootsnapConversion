from ultralytics import SAM
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
            bboxes.append([x1, y1, x2, y2])

            #draw bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 1)

        model = SAM('sam_b.pt')  # load semgmentation model
        for box in bboxes:
            #feed sam model the image and bounding boxes (bbox) to annotate image
            results = model(imagePath, bboxes= box)
            annotated_image = results[0].plot()

            # Check if the image was loaded successfully
            if annotated_image is not None:
                # Display the image
                cv2.imshow('Image', annotated_image)
                #wait for keystroke to close window
                cv2.waitKey(0) 
            else:
                print("Failed to load the image or the file does not exist.")


    #show image
    cv2.imshow('Image', image)
    #wait for keystroke to close window
    cv2.waitKey(0)


showSegmentAndBoxes('./poop.jpg', './test/Barley_103_D4_12Aug2020.txt')

