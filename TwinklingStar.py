#20210974 강채원
import cv2
import numpy as np
import random

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

def draw_diag(canvas,polygon,color):
    num = polygon.shape[0] #몇각형인지 //5각형이면 5
    for i in range(num): #0-4
        for count in range(num):
            if(2<=abs(i-count)<num-1):
                getline(canvas,polygon[count,0],polygon[count,1],polygon[i,0],polygon[i,1],color)
       
def makeTmat(a,b):
    T = np.eye(3,3)
    T[0,2] = a
    T[1,2] = b
    return T

def cvtto3mat(Mat,ngon):
    l = np.ones(ngon)
    Mat = np.append(Mat,[l],axis=0) 
    return Mat     

def rettomat(Mat):
    Mat = np.delete(Mat,2,axis=0)   
    Mat = Mat.T     
    Mat = Mat.astype('int')
    return Mat

class Star:
    def __init__(self,canvas,pts,size,vt): #pts:점 좌표, size:별의 크기 조정, vt:별의 깜빡임 속도
        self.canvas = canvas
        self.pts = (pts*size).T
        self.pts = cvtto3mat(self.pts,5)
        self.vt = vt 
        self.t = 0
        self.num=0
        self.x,self.y = random.randint(1,1170),random.randint(1,670)
    def twinkle(self):
        self.star = makeTmat(self.x,self.y) @ self.pts
        self.star = rettomat(self.star)
        if(self.num%2==0): #검 -> 흰
            self.color = (self.t,self.t,self.t)
            if(self.t<256):
                draw_diag(self.canvas,self.star,self.color)
            self.t+=self.vt
            if(self.t>=255):
                self.num+=1
        if(self.num%2==1): #흰 -> 검
            self.color = (self.t,self.t,self.t)
            if(self.t<256):
                draw_diag(self.canvas,self.star,self.color)
            self.t-=self.vt
            if(self.t<=0):
                self.num+=1
def main():
    width,height = 1200,700
    ngon=5
    p = getRegularNgon(ngon)
    canvas = np.zeros((height,width,3),dtype='uint8')
    S = []
    for i in range(45): #45개의 별 찍기
        S.append(Star(canvas,p,random.randint(1,31),random.randint(1,6)))
    while True:
        for k in range(45):
            S[k].twinkle()
        cv2.imshow("myWindow",canvas)
        if cv2.waitKey(20) == 27:
            break
if __name__ =="__main__":
    main()
    
