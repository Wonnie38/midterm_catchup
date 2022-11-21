#20210974 강채원
import numpy as np
import cv2
import random

def getline(canvas,x0,y0,x1,y1,color):
    # |기울기|<1 --> y =  (x-x0) * (y1-y0) / (x1-x0) +y0
    # |기울기|>1 --> x = (y-y0) * (x1-x0)/(y1-y0) +x0
    if(abs(x1-x0)<abs(y1-y0)): #|기울기|>1인 경우
        if(y1==y0):
            y = y0
            if(x0<x1):
                for x in range(x0,x1+1):
                    canvas[int(y),int(x)] = color
            else:
                for x in range(x0,x1-1,-1):
                    canvas[int(y),int(x)] = color
        else:
            if(y0<y1):
                for y in range(y0,y1+1):
                    x = (y-y0) * (x1-x0)/(y1-y0) +x0
                    canvas[int(y),int(x)] = color
            else:
                for y in range(y0,y1-1,-1):
                    x = (y-y0) * (x1-x0)/(y1-y0) +x0
                    canvas[int(y),int(x)] = color
   
    else:#|기울기|<=1인 경우
        if(x1==x0):
            x = x0
            if(y0<y1):
                for y in range(y0,y1+1):
                    canvas[int(y),int(x)] = color
            else:
                for y in range(y0,y1-1,-1):
                    canvas[int(y),int(x)] = color
        
        else:
            if(x0<x1):
                for x in range(x0,x1+1):
                    y =  (x-x0) * (y1-y0) / (x1-x0) +y0
                    canvas[int(y),int(x)] = color
                    
            else:
                for x in range(x0,x1-1,-1):
                    y =  (x-x0) * (y1-y0) / (x1-x0) +y0
                    canvas[int(y),int(x)] = color
                    
def deg2rad(deg):
    rad = deg*np.pi/180.0
    return rad
 
def makeTmat(a,b):
    Tmat = np.eye(3,3)
    Tmat[0,2] = a
    Tmat[1,2] = b
    return Tmat
    
def makeRmat(degree):
    rad = deg2rad(degree)
    c = np.cos(rad)
    s = np.sin(rad)
    Rmat = np.eye(3,3)
    Rmat[0,0] = c
    Rmat[0,1] = -s
    Rmat[1,0] = s
    Rmat[1,1] = c
      
    return Rmat

def drawPolygon(canvas,pts,color):
    num = pts.shape[0]
    for i in range(num-1):
        getline(canvas,pts[i,0],pts[i,1],pts[i+1,0],pts[i+1,1],color)   
    getline(canvas,pts[0,0],pts[0,1],pts[-1,0],pts[-1,1],color)   


def Next(p,theta):
    next = p @makeTmat(200,0)@makeTmat(0,35)@makeRmat(theta)@makeTmat(0,-35)
    return next

def Re_point(Q,point):
    Q = Q @ point
    Q = np.delete(Q,2,axis=0)
    Q = Q.T
    Q = Q.astype('int')
    return Q
   
def main():
    width,height = 1200,1200
    color = (255,255,255)
    canvas = np.zeros((height,width,3),dtype='uint8')
    rect=[]
    rect.append((0,0))
    rect.append((200,0))
    rect.append((200,70))
    rect.append((0,70))
    rect = np.array(rect)
    
    point = rect.copy()
    l = np.ones(4)
    point = point.T
    point = np.append(point,[l],axis=0)

    
    while True:
        canvas = np.zeros((height,width,3),dtype='uint8')
        theta = random.randint(-40,70)
        P = makeTmat(200,750)@makeRmat(-90)
        Q1 = Next(P,theta)
        Q2 = Next(Q1,random.randint(10,60))
        Q3 = Next(Q2,random.randint(20,60))
        Q4 = Next(Q3,random.randint(-30,50))
    
        P = Re_point(P,point)
        Q1 = Re_point(Q1,point)
        Q2 = Re_point(Q2,point)
        Q3 = Re_point(Q3,point)
        Q4 = Re_point(Q4,point)
        
        drawPolygon(canvas,P,color)
        drawPolygon(canvas,Q1,color)
        drawPolygon(canvas,Q2,color)
        drawPolygon(canvas,Q3,color)
        drawPolygon(canvas,Q4,color)
        
        cv2.imshow("dispWindow",canvas)
        if cv2.waitKey(100)==27:
            break
        
if __name__ =="__main__":
    main()