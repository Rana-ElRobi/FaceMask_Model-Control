from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import math
import numpy

name = "Scene" 
a = -0.05
b = 0.28
c = 1

global WIDTH 
global HEIGHT  
WIDTH = 1000
HEIGHT = 1000

global H
global Normal_ON
Normal_ON = 0

global DeltaX
global DeltaY
global LEFT_BUTTON
global RIGHT_BUTTON
global X_Old
global Y_Old
global P
global ppmList
DeltaX = 0
DeltaY = 0
LEFT_BUTTON = 0
RIGHT_BUTTON = 0
X_Old = 0
Y_Old = 0
P = 0
H = 0

def LoadVTK():    
    global VerticesLIST
    global PolygonsList
    # Carry all texture coordinates
    global textureLIST 
    #Carry Texure Coordinates
    global coordnaitesLIST 
    VerticesLIST = []
    # this is list of all verticeses with no boarders
    vers = []
    vertsData = []
    PolygonsList = [] 
    textureLIST =[]
    coordnaitesLIST = []
    vtkFile = open ("face.vtk","r")
    #Loop on file
    # Start from line 
    for i,line in enumerate(vtkFile) :
        #go to Verticeses Section
        if (i > 4) and(i < 8825):
            pList = line.split(' ')
            #each line have 3 vertices each have 3 dims
            for x in pList:
                if x != "\n":
                    vers.append(float(x))
                    
            VerticesLIST.append([float(pList[0]),float(pList[1]),float(pList[2])])
            VerticesLIST.append([float(pList[3]),float(pList[4]),float(pList[5])])
            VerticesLIST.append([float(pList[6]),float(pList[7]),float(pList[8])])
            
        #Go to polygons section
        elif (i > 8825) and (i < 61086 ):
            polyLine = line.split(' ')
            PolygonsList.append([int(polyLine[1]),int(polyLine[2]),int(polyLine[3])])
        # GO To Texture section
        elif i > 61087:
            points = line.split(' ')
            for c in points:
                if c != "\n":
                    textureLIST.append(float(c))
    vtkFile.close()

    t =0
    # make coordinates
    while True:
        if t > 52919:
            break
        else :
            cord = [textureLIST[t],textureLIST[t+1]]
            coordnaitesLIST.append(cord)
            t=t+2
    return VerticesLIST, PolygonsList

# Function that read color intisties fron ppm file and return list of list
def loadppm():
    #LIST of RGB texture intensity
    global ppmList 
    global List_1
    ppmList = []
    #Opening the PPM file
    PPM_File = open ("face.ppm")
    #Initializing lists and counter values
    List_1 = []
    j = 0
    #Inserting values of PPM File in one list
    for i, line in enumerate (PPM_File):
        if (i > 3):
            Element = int(line)
            List_1.append(Element)   
    #Closing PPM File
    PPM_File.close()
    return List_1

def NormalDraw (VerticesLIST, PolygonsList):
    
    #Values Initialization
    global VertexList
    global LVertex
    global LPolygon
    global Vertex_Normal
    global Normal_Point
    global Normal
    
    VertexList = VerticesLIST
    PolygonList = PolygonsList
    
    LVertex = len(VertexList)
    LPolygon = len(PolygonList)   
    
    Normal = []
    TempList_1 = [0]*3
    TempList_2 = []
    TempList_2.append(TempList_1)
    Vertex_Normal = TempList_2*LVertex
    Count = [0]*LVertex
    Normal_Point = []
    
    #First for loop calculating the normals of each polygon (after normalization) and putting them in a list
    for i in range (0, LPolygon):
        x1 = VertexList [PolygonList[i] [0]]
        x2 = VertexList [PolygonList[i] [1]]
        x3 = VertexList [PolygonList[i] [2]] 
        z1 = (x1[0] - x2[0], x1[1] - x2[1], x1[2] - x2[2])
        z2 = (x1[0] - x3[0], x1[1] - x3[1], x1[2] - x3[2])
        c = [z1[1]*z2[2] - z1[2]*z2[1],
             z1[2]*z2[0] - z1[0]*z2[2],
             z1[0]*z2[1] - z1[1]*z2[0]] 
        c_Scalar = math.sqrt((c[0]*c[0]) + (c[1]*c[1]) + (c[2]*c[2]))
        c = [(c[0]/c_Scalar), (c[1]/c_Scalar), (c[2]/c_Scalar)]
        Normal.append(c) 
     
    #Second for loop calculating the sum of polygons normals shared at each vertex    
    for j in range (0, LPolygon):
        for k in range (0, len(PolygonList[j])):
            Temp_1 = PolygonList[j] [k]
            Vertex_Normal [Temp_1] = [Vertex_Normal [Temp_1] [0] + Normal[j] [0], Vertex_Normal [Temp_1] [1] + Normal[j] [1], Vertex_Normal [Temp_1] [2] + Normal[j] [2]]
            Count [Temp_1] = (Count [Temp_1] + 1)
    
    #Third for loop calculating the average of the normals at each vertex        
    for l in range (0, LVertex):
        Vertex_Normal [l] = [Vertex_Normal [l] [0]/Count [l], Vertex_Normal [l] [1]/Count [l], Vertex_Normal [l] [2]/Count [l]]
    
    #Fourth for loop calculating a point on the normal to be used in visualizing the normals
    for m in range (0, LVertex):
        TempList_3 = []
        for n in range (0, 3):
            TempList_3.append(VertexList [m] [n] + 0.02*Vertex_Normal [m] [n])
        Normal_Point.append(TempList_3)      
    return VertexList, LVertex, LPolygon, Vertex_Normal, Normal_Point, Normal

def LightsON1 (): 
    glEnable(GL_LIGHT0)             
    LightZeroPosition = [5.0, 2, 0.0]
    LightZeroColor = [255, 255, 251]
    glLightfv(GL_LIGHT0, GL_POSITION, LightZeroPosition)
    glLightfv(GL_LIGHT0, GL_SPECULAR, LightZeroColor)
    glutPostRedisplay() 
    
def LightsON2 ():  
    glEnable(GL_LIGHT1)
    LightOnePosition = [-5.0, 0.0, 10.0]
    LightOneColor = [1.0, 1.0, 0.5]
    glLightfv(GL_LIGHT1, GL_POSITION, LightOnePosition)    
    glLightfv(GL_LIGHT1, GL_DIFFUSE, LightOneColor) 
    glutPostRedisplay() 
    
def LightsOFF1 ():  
    glDisable(GL_LIGHT0)
    glutPostRedisplay() 
    
def LightsOFF2 ():
    glDisable(GL_LIGHT1)
    glutPostRedisplay() 
    
def keyboard(key, x, y):
    global c
    global Normal_ON
    global P
    global H
    if (key == b'a'): LightsON1()
    if (key == b'q'): LightsON2()
    if (key == b's'): LightsOFF1()
    if (key == b'w'): LightsOFF2()
    if (key == b'z'): c = c*1.1     
    if (key == b'x'): c = c*0.99    
    if (key == b'n'): Normal_ON = 1
    if (key == b'f'): Normal_ON = 0 
    if (key == b'p'): P = 1
    if (key == b'c'): P = 0
    if (key == b'h'): H = 1
    if (key == b'u'): H = 0
    glutPostRedisplay()  

def SpecialInput(key, x, y):
    global a
    global b
    if (key == GLUT_KEY_UP): b = b + 0.05
    if (key == GLUT_KEY_DOWN): b = b - 0.05        
    if (key == GLUT_KEY_LEFT): a = a + 0.05       
    if (key == GLUT_KEY_RIGHT): a = a - 0.05        
    glutPostRedisplay() 
    
def Draw (): 
    glTranslatef (a, b, 0.4)
    glScalef (c, c, c)
    glBegin(GL_TRIANGLES)
    for q1 in range (0, LPolygon):
	    for q2 in range (0, 3):
		    glTexCoord2f(coordnaitesLIST[PolygonsList[q1][q2]][0], coordnaitesLIST[PolygonsList[q1][q2]][1])
		    glVertex3f(VertexList[PolygonsList[q1][q2]][0], VertexList[PolygonsList[q1][q2]][1], VertexList[PolygonsList[q1][q2]][2])
		    if (H == 0):
		            glNormal3f(Normal[q1][0], Normal[q1][1], Normal[q1][2])
		    if (H == 1):
			    glNormal3f(Vertex_Normal[PolygonsList[q1][q2]][0], Vertex_Normal[PolygonsList[q1][q2]][1], Vertex_Normal[PolygonsList[q1][q2]][2])
    glEnd()  
    if (Normal_ON == 1):  
	    glBegin(GL_LINES)
	    x = [5,255,0]
	    glMaterialfv(GL_FRONT,GL_AMBIENT,x)	
	    for s1 in range (0, LPolygon):
		    for s2 in range (0, 3):        
			    glVertex3f(VertexList[PolygonsList[s1][s2]][0], VertexList[PolygonsList[s1][s2]][1], VertexList[PolygonsList[s1][s2]][2])
			    glVertex3f(Normal_Point[PolygonsList[s1][s2]][0], Normal_Point[PolygonsList[s1][s2]][1], Normal_Point[PolygonsList[s1][s2]][2])
	    glEnd()        
       
def Reshape(width, height):
    if (height == 0):
        height = 1000
        width = 1000
    global WIDTH 
    global HEIGHT  
    WIDTH = width
    HEIGHT = height
    ASPECT = WIDTH/HEIGHT
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode (GL_PROJECTION)
    glLoadIdentity ()
    gluPerspective(5,ASPECT,0.1,1000)
    glMatrixMode (GL_MODELVIEW)  
    glutPostRedisplay()  

def MouseButton(button, state, x, y):
    global X
    global X_Old
    global Y_Old
    global LEFT_BUTTON
    global RIGHT_BUTTON
    if (button == GLUT_LEFT_BUTTON and state == GLUT_DOWN):
	    X_Old = x
	    Y_Old = y
	    LEFT_BUTTON = 1
	    RIGHT_BUTTON = 0
    if (button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN):
	    X_Old = x
	    Y_Old = y
	    RIGHT_BUTTON = 1
	    LEFT_BUTTON = 0	

def MouseMove(x, y):
    global DeltaX
    global DeltaY    
    global X_Old
    global Y_Old 
    if (LEFT_BUTTON == 1): 
	    DeltaX = (x - X_Old)*0.1
	    DeltaY = (y - Y_Old)*0.1	    	    
	    glRotatef(DeltaX, 0, 1, 0)	
	    glRotatef(DeltaY, 1, 0, 0)
	    X_Old = x
	    Y_Old = y	    
    if (RIGHT_BUTTON == 1 and P == 0):
	    DeltaX = (x - X_Old)*0.001
	    DeltaY = -(y - Y_Old)*0.001			 
	    glTranslatef(DeltaX, DeltaY, 0)
	    X_Old = x
	    Y_Old = y  
    if (RIGHT_BUTTON == 1 and P == 1 and y > Y_Old):
	    glScalef(0.99, 0.99, 0.99)	    
	    X_Old = x
	    Y_Old = y
    if (RIGHT_BUTTON == 1 and P == 1 and y < Y_Old):
	    glScalef(1.01, 1.01, 1.01)
	    X_Old = x
	    Y_Old = y 	    
    glutPostRedisplay() 

def LoadTextures():
    # create a 64x64 texture, defaults to rgb / ubyte
    #texture = Texture.create(size=(512, 512), colorfmt='rgb')
    #texture = 0
    texdata = numpy.zeros((256,256,3))
    # then load RGB values
    texdata = List_1
    # Create Texture    
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 512, 512, 0, GL_RGB, GL_UNSIGNED_BYTE, texdata)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 1000)
    glutCreateWindow(name)  
    glutMouseFunc(MouseButton)
    glutMotionFunc(MouseMove)
    gluLookAt(0,0,10, 0,0,0, 0,1,0)
    #glutPassiveMotionFunc(MouseMove)
    glEnable(GL_LIGHTING) 
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.,0.,0.,1.)
    glEnable(GL_NORMALIZE)  
    glEnable(GL_DEPTH_TEST)
    LoadTextures()
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard) #Keyboard Function for Lightining & Z Movement
    glutSpecialFunc(SpecialInput) #Kepboard Function for X & Y Movement
    glutReshapeFunc(Reshape)
    glShadeModel(GL_SMOOTH) 
    glutMainLoop()

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)   
    glPushMatrix()
    z = [0.8,0.8,0.8, 1]
    glMaterialfv(GL_FRONT,GL_AMBIENT,z)   
    glRotatef(-120, 0, 1, 0)
    glTranslatef(0, 0, -0.35)
    Draw()
    glPopMatrix()
    glPushMatrix()
    x = [5,255,0]
    glMaterialfv(GL_FRONT,GL_AMBIENT,x)
    #glRotatef(-60, 0, 1, 0)
    glutSolidCube(0.15)
    glPopMatrix()
    glPushMatrix()
    glBegin(GL_POLYGON)
    y = [0,0,3]
    glMaterialfv(GL_FRONT_AND_BACK,GL_AMBIENT,y)    
    glVertex3f(-0.25, -0.08, -0.5)
    glVertex3f(0.25, -0.08, -0.5)
    glVertex3f(0.25, -0.08, 0.5)
    glVertex3f(-0.25, -0.08, 0.5)  
    glEnd()
    glPopMatrix()   
    glutSwapBuffers()
    glFlush()

[VerticesLIST, PolygonsList] = LoadVTK ()
[VertexList, LVertex, LPolygon, Vertex_Normal, Normal_Point, Normal] = NormalDraw(VerticesLIST, PolygonsList) 
List_1 = loadppm()

main ()