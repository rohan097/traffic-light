import cv2
import argparse
import numpy as np
import imutils
import math
def setup(args):

    #clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize = (8,8))

    avg = None
    kernel1 = np.ones((3,3), np.uint8)

    if 'video1.avi' in args['video']:
        kernel2 = np.ones((21,21), np.uint8)
        kernel3 = np.ones((3,3), np.uint8)
        weight = 0.805
        dil_iter = 1
        er_iter = 5

    else:
        kernel2 = np.ones((7,7),np.uint8) # 21,21
        kernel3 = np.ones((1,1),np.uint8) # 3,3
        weight = 0.47
        dil_iter = 2
        er_iter = 30
    return avg, kernel1, kernel2, kernel3, weight, dil_iter, er_iter

def processing(args, frame, avg, kernel1, kernel2, kernel3, weight, dil_iter, er_iter, initial_frame):

    if  'video1.avi' in args['video']:
        frame = frame[5:,75:]

    frame = frame[30:,:]
    frame = imutils.resize(frame, width = 500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21),0)

    if initial_frame:
        if 'video1.avi' not in args['video']:
            avg = gray.copy().astype("float")
        else:
            avg = cv2.imread('/home/rohan/GDG/Ba1.jpg')
            avg = avg[35:,75:]
            avg = imutils.resize(avg, width = 500)
            avg = cv2.cvtColor(avg, cv2.COLOR_BGR2GRAY)
            avg = cv2.GaussianBlur(avg, (21,21), 0)
            avg = avg.astype(float)
    cv2.accumulateWeighted(gray, avg, weight) # Last value was actually 0.5, but the best value is 0.805
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

    blob = cv2.threshold(frameDelta,5,255,cv2.THRESH_BINARY_INV)[1]
    thresh = cv2.threshold(frameDelta,5,255,cv2.THRESH_BINARY)[1]
    thresh = cv2.erode(thresh, kernel3, iterations = 6)
    thresh = cv2.dilate(thresh, kernel1, iterations = dil_iter)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel2, iterations = 1)# Originally this is not there
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return avg, frame, cnts

def track(frame, cnts, count_i, count_o):

    cnts = cnts[1]
    counter = 0
    incoming = 0
    outgoing = 0
    for c in cnts:
        if not( 200 < cv2.contourArea(c) < 16000 ):
            continue
        (x,y, w,h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255),2)
        M = cv2.moments(c)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        # outgoing traffic is blue
        if (cy - 250 + 0.714*cx > 0):
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
            outgoing +=1
        # incoming traffic is green
        else:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
            incoming +=1

        counter += 1
    count_i = count_i + incoming
    count_o = count_o + outgoing
    return count_i, count_o

def counts(count_i, count_o):
    count_i = count_i/3.0
    count_o = count_o/3.0
    print (math.ceil(count_i), math.ceil(count_o))

def main():

    ap = argparse.ArgumentParser()
    ap.add_argument("video", help = "path to the video file")
    ap.add_argument("feed")
    args = vars(ap.parse_args())
    count_i = 0
    count_o = 0
    iter_value = 0
    avg, kernel1, kernel2, kernel3, weight, dil_iter, er_iter = setup(args)
    camera = cv2.VideoCapture(args['video'])

    initial_frame = True
    while True:

        grabbed, frame = camera.read()
        if grabbed == False:
            break
        avg, frame, cnts = processing(args, frame, avg, kernel1, kernel2, kernel3, weight, dil_iter, er_iter, initial_frame)
        count_i, count_o = track(frame, cnts, count_i, count_o )
        if iter_value % 3 == 0:
            counts(count_i, count_o)
            count_i = 0
            count_o = 0

        cv2.imshow('Traffic_Cam', frame)
        key = cv2.waitKey(100) & 0xFF
        if key == ord("q"):
            break
        iter_value += 1
        initial_frame = False

    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
