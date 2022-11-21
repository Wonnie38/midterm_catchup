#20210974 강채원
import cv2
import numpy as np

def deg2rad(degree):
    rad = degree * np.pi / 180.0
    return rad

def getRegularNgon(ngon):
    vertices = []
    delta = 360.0/ngon
    for i in range(ngon):
        degree = delta * i
        radian = deg2rad(degree)
        x = np.cos(radian)
        y = np.sin(radian)
        vertices.append((x,y))
        
    vertices = np.array(vertices)    
    return vertices
    
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
                    
def drawPolygon(canvas,pts,color,axis=False):
    num = pts.shape[0]
    for i in range(num-1):
        getline(canvas,pts[i,0],pts[i,1],pts[i+1,0],pts[i+1,1],color)   
    getline(canvas,pts[0,0],pts[0,1],pts[-1,0],pts[-1,1],color)  
    
          
def makeTmat(a,b):
    T = np.eye(3,3)
    T[0,2] = a
    T[1,2] = b
    return T
    
def makeRmat(deg):
    R = np.eye(3,3)
    radian = deg2rad(deg)
    c = np.cos(radian)
    s = np.sin(radian)
    R[0,0] = c
    R[0,1] = -s
    R[1,0] = s
    R[1,1] = c
    return R

def cvtto3mat(Mat,ngon):
    Mat = Mat.T
    l = np.ones(ngon)
    Mat = np.append(Mat,[l],axis=0) 
    return Mat     

def rettomat(Mat):
    Mat = np.delete(Mat,2,axis=0)   
    Mat = Mat.T     
    Mat = Mat.astype('int')
    return Mat

def main():
    theta_h=0
    theta_m=0
    width,height = 1200,700
    P = np.array([ [0,0], [6, 0], [6, 2], [0, 2] ])
    P*=20
    w,h = 150,50
    P = cvtto3mat(P,4)
    while True:
        canvas = np.zeros((height,width,3),dtype='uint8')
        H = makeTmat(600,300)@makeRmat(-90)@makeTmat(0,h/2)@makeRmat((1/120)*theta_h)@makeTmat(0,-h/2)@P
        H = rettomat(H)
        
        M = makeTmat(600,300)@makeRmat(-90)@makeTmat(0,h/2)@makeRmat((1/10)*theta_m)@makeTmat(0,-h/2)@P
        M = rettomat(M)
        
        drawPolygon(canvas,H,(0,0,255))
        drawPolygon(canvas,M,(0,255,0))
        
        cv2.imshow("myWindow",canvas)
        theta_h+=1
        theta_m+=1
        
        if cv2.waitKey(1000) == 27:
            break
    
if __name__ =="__main__":
    main()     