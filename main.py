from gzip import FTEXT
from operator import mod
from turtle import Vec2D, color, pos
import pygame
import math
import copy
import time
import random
from utils import *


def cubos(x,y,z):
    return [
		[           [x,y,z],   [   x , y+1.0 , z], [x+1.0 ,y+ 1.0 , z]  ],
		[           [x,y,z],   [x+1.0 ,y+ 1.0 ,z], [x+1.0 , y , z]      ],
                                                     
		[   [x+1.0 , y , z],        [x+1.0 , y+1.0 , z],    [x+1.0, y+1.0 ,z+1.0] ],
		[   [x+1.0 , y , z],    [x+1.0 , y+1.0 , z+1.0],    [x+1.0 , y , z+1.0]   ],
                                                 
		[ [x+1.0 , y , z+1.0],    [x+1.0 ,y+1.0 , z+1.0],   [x , y+1.0 , z+1.0]   ],
		[ [x+1.0 , y , z+1.0],    [   x , y+1.0 , z+1.0],   [x , y , z+1.0]     ],
                                                   
		[     [x , y , z+1.0],        [x , y+1.0, z+1.0],   [x , y+1.0 , z]   ],
		[     [x , y , z+1.0],           [x , y+1.0 , z],   [x,y,z]             ],
                                                     
		[    [x , y+1.0 , z ],       [x , y+1.0 , z+1.0] ,  [x+1.0 , y+1.0 , z+1.0]  ],
		[     [x , y+1.0 , z],   [x+1.0 , y+1.0 , z+1.0] ,  [x+1.0 , y+1.0 ,z ] ],
                                                  
		[ [x+1.0 , y , z+1.0 ],       [x, y , z+1.0] ,  [x,y,z]  ],
		[ [x+1.0 , y , z+1.0 ],              [x,y,z] ,  [x+1.0, y , z]  ],
]

def DrawTriangle(x1,y1,x2,y2,x3,y3,color = (255,255,255)):
    pygame.draw.line(screen,color,(x1,y1),(x2,y2))
    pygame.draw.line(screen,color,(x2,y2),(x3,y3))
    pygame.draw.line(screen,color,(x3,y3),(x1,y1))

def FillTriangle(x1,y1,x2,y2,x3,y3,color = (255,255,255)):
    try:
        
        if(x1>500):
            x1 = 520
        elif(x1<0):
            x1 = 0
        if(x2>500):
            x2 = 520
        elif(x2<0):
            x2 = 0 
        if(x3>500):
            x3 = 520
        elif(x3<0):
            x3 = 0

        if(y1>500):
            y1 = 520
        elif(y1<0):
            y1 = 0
        if(y2>500):
            y2 = 520
        elif(y2<0):
            y2 = 0 
        if(y3>500):
            y3 = 520
        elif(y3<0):
            y3 = 0

        pygame.draw.polygon(screen,color,((x1,y1),(x2,y2),(x2,y2),(x3,y3),(x3,y3),(x1,y1)))
    except e:
        print(color,e)

def ordenacao_vetor(e):
    return (e.p[0].z+e.p[1].z+e.p[2].z)/3



w = 500
h = 500

linha = False
face = True


matProj = Matrix_MakeProjection(90,h/w, 0.1,1000)

vCamera = vec3d(0,2,0)
vLookDir = vec3d()

fYaw = 0
fTheta = 0

cubo = cubos(0,0,0)
print(cubo)
meshCube = mesh()
#meshCube.LoadFromObjectFile('nave.obj')
i = 0
j = 0
k = 0
while(i<10):
    j = 0
    while(j<8):
        if(random.random()>1):
            k = k + 1
        else:
            k = 0
        cubo = cubos(i,k,j)
        for v in cubo:
            triangulo1 = triangulo()
            for index,f in enumerate(v):
                triangulo1.p[index ]= vec3d(f[0],f[1],f[2])
                #triangulo1.color = (0,255,0)
                #print(f)
            if (triangulo1.p[0].y == triangulo1.p[1].y == triangulo1.p[2].y ):
                triangulo1.color = (0,255,123)
            else:
                triangulo1.color = (134,79,43)

            meshCube.tris.append(triangulo1)
        j = j + 1
    i = i + 1


## SLIME
slime =[]
aa=1


pygame.init()


# Set up the drawing window

screen = pygame.display.set_mode([w, h])

# Run until the user asks to quit

running = True

sec = time.time()
posSol= 0

font = pygame.font.Font('freesansbold.ttf', 15)

text = font.render('fps', True, (0,0,0), (255,255,255))
text1 = font.render('pos', True, (0,0,0), (255,255,255))
text2 = font.render('pos', True, (0,0,0), (255,255,255))

textRect = text.get_rect()
textRect.center = (70,10)

textRect1 = text1.get_rect()
textRect1.center = (70,30)

textRect2 = text2.get_rect()
textRect2.center = (70,50)

while running:


    # Did the user click the window close button?
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False
        
        vForward = Vector_Mul(vLookDir,8*((time.time()-sec)))
        mover = False
        tecla = -1
        
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_UP:
                vCamera.y = vCamera.y -2*((time.time()-sec))
            if event.key == pygame.K_RIGHT:
                vCamera.x = vCamera.x +2*((time.time()-sec))
            if event.key == pygame.K_DOWN:
                vCamera.y = vCamera.y +2*((time.time()-sec))
            if event.key == pygame.K_LEFT:
                vCamera.x = vCamera.x -2*((time.time()-sec))
            mover = True
            tecla = event.key

           
            if tecla == ord('z'):
                linha = not linha
            if tecla == ord('x'):

                face = not face
            if tecla == ord('c'):
                cubo = cubos(vTarget.x,vTarget.y,vTarget.z)
                for v in cubo:
                    triangulo1 = triangulo()
                    for index,f in enumerate(v):
                        triangulo1.p[index ]= vec3d(f[0],f[1],f[2])
                        triangulo1.color = (0,255,0)
                        #print(f)
                    meshCube.tris.append(triangulo1)

            if tecla == ord('a'):
                fYaw = fYaw - 2*((time.time()-sec))
            if tecla == ord('d'):
                fYaw = fYaw + 2*((time.time()-sec))
            if tecla == ord('w'):
                vCamera = Vector_Add(vCamera, vForward)
            if tecla == ord('s'):
                vCamera = Vector_Sub(vCamera, vForward)
                      

    # Fill the background with white
    screen.fill((69, 166, 213))
    if(time.time()!=sec):  
        #print('fps:',1/(time.time()-sec))
        fps_str = str(1/(time.time()-sec))
        text = font.render('FPS: '+fps_str, True, (0,0,0), (255,255,255))
    #fTheta += 1 * ((time.time()-sec))

    fThetaSol = math.sin(posSol) 
    posSol += 0.5*((time.time()-sec))
    
    sec = time.time()

    # Rotation Z
    matRotZ = Matrix_MakeRotationZ(fTheta*0.5)

    # Rotation X
    matRotX = Matrix_MakeRotationX(fTheta)

    # Translate
    matTrans = Matrix_MakeTranslation(0,0,5)

    matWorld = Matrix_MakeIdentity()
    matWorld = Matrix_MultiplyMatrix(matRotZ,matRotX)
    matWorld = Matrix_MultiplyMatrix(matWorld, matTrans)
    
    vUp          = vec3d(0,1,0)
    vTarget      = vec3d(0,0,1)
    matCameraRot = Matrix_MakeRotationY(fYaw)
    vLookDir     = Matrix_MultiplyVector(matCameraRot,vTarget)
    vTarget      = Vector_Add(vCamera,vLookDir)

    matCamera = Matrix_PointAt(vCamera,vTarget,vUp)
    matView = Matrix_QuickInverse(matCamera)

    triangulos_to_render = []

    ajuste = 0
    for ss in slime:
        meshCube.tris.pop(ss-ajuste)
        ajuste = ajuste + 1

    ##    creeper
    aa = aa+0.01
    slime = []
    cubo = cubos(aa,2.1+math.cos(2*aa),3)
    for v in cubo:
        triangulo1 = triangulo()
        for index,f in enumerate(v):
            triangulo1.p[index]= vec3d(f[0],f[1],f[2])
            triangulo1.color = (123,123,123)
            #print(f)
        slime.append( len(meshCube.tris)-1)
        meshCube.tris.append(triangulo1)

    # Draw a solid blue circle in the center
    for tri in meshCube.tris:

        triProjected    = triangulo()
        triTransformado = triangulo()
        triViewed       = triangulo()
        
        triTransformado.p[0] = Matrix_MultiplyVector(matWorld,tri.p[0])
        triTransformado.p[1] = Matrix_MultiplyVector(matWorld,tri.p[1])
        triTransformado.p[2] = Matrix_MultiplyVector(matWorld,tri.p[2])
        triTransformado.color = tri.color

        line1 = Vector_Sub(triTransformado.p[1],triTransformado.p[0])
        line2 = Vector_Sub(triTransformado.p[2],triTransformado.p[0])
        
        normal = Vector_CrossProduct(line1,line2)

        normal = Vector_Normalise(normal)

        vCameraRay = Vector_Sub(triTransformado.p[0],vCamera)

        if(Vector_DotProduct(normal,vCameraRay)<0) :
            #iluminação
            #light_direction = vec3d(3,5+5*fThetaSol,-1)
            light_direction = vec3d(0,1,-1)
            light_direction = Vector_Normalise(light_direction)

            #produto escalar entre a iluminação e a normal da face da figura
            light_direction_dot_normal = max(0.1,Vector_DotProduct(light_direction,normal))
            #print(light_direction_dot_normal)
            triViewed.p[0] = Matrix_MultiplyVector(matView,triTransformado.p[0])
            triViewed.p[1] = Matrix_MultiplyVector(matView,triTransformado.p[1])
            triViewed.p[2] = Matrix_MultiplyVector(matView,triTransformado.p[2])
            triViewed.color = triTransformado.color

            nClippedTriangles = 0
            clipped = [triangulo() for i in range(2)]
            nClippedTriangles, clipped[0], clipped[1] = Triangle_ClipAgainstPlane(vec3d(0,0,0.1),vec3d(0,0,1), triViewed)

            for n in range(nClippedTriangles):
               
                triProjected.p[0] = Matrix_MultiplyVector(matProj,clipped[n].p[0])
                triProjected.p[1] = Matrix_MultiplyVector(matProj,clipped[n].p[1])
                triProjected.p[2] = Matrix_MultiplyVector(matProj,clipped[n].p[2])

                triProjected.p[0] = Vector_Div(triProjected.p[0], triProjected.p[0].w)
                triProjected.p[1] = Vector_Div(triProjected.p[1], triProjected.p[1].w)
                triProjected.p[2] = Vector_Div(triProjected.p[2], triProjected.p[2].w)
                            
                #modificando a escala
                vOffsetView = vec3d(1,1,0)
                triProjected.p[0] = Vector_Add(triProjected.p[0],vOffsetView)
                triProjected.p[1] = Vector_Add(triProjected.p[1],vOffsetView)
                triProjected.p[2] = Vector_Add(triProjected.p[2],vOffsetView)

                triProjected.p[0].x = triProjected.p[0].x*0.5*w
                triProjected.p[0].y = triProjected.p[0].y*0.5*h
                triProjected.p[1].x = triProjected.p[1].x*0.5*w
                triProjected.p[1].y = triProjected.p[1].y*0.5*h
                triProjected.p[2].x = triProjected.p[2].x*0.5*w
                triProjected.p[2].y = triProjected.p[2].y*0.5*h
                
                triProjected.color = (math.floor(clipped[n].color[0]*abs(light_direction_dot_normal) % 255),
                                      math.floor(clipped[n].color[1]*abs(light_direction_dot_normal) % 255),
                                      math.floor(clipped[n].color[2]*abs(light_direction_dot_normal) % 255))
                      
                triangulos_to_render.append(triProjected)

    triangulos_to_render.sort(key = ordenacao_vetor,reverse=True)

    for triProjected in triangulos_to_render:
        if face:
            FillTriangle(w-triProjected.p[0].x,h-triProjected.p[0].y,
                        w-triProjected.p[1].x,h-triProjected.p[1].y,
                        w-triProjected.p[2].x,h-triProjected.p[2].y,
                        color=triProjected.color)
        if(linha):
            DrawTriangle(w-triProjected.p[0].x,h-triProjected.p[0].y,
                        w-triProjected.p[1].x,h-triProjected.p[1].y,
                        w-triProjected.p[2].x,h-triProjected.p[2].y,
                        color=(0,0,0))
    
    # Flip the display
    text1 = font.render('POS X:'+str(math.floor(vCamera.x))+ ' Y:'+str(math.floor(vCamera.y))+' Z:'+str(math.floor(vCamera.z)), True, (0,0,0), (255,255,255))
    text2 = font.render('POS at X:'+str(math.floor(vCameraRay.x))+ ' Y:'+str(math.floor(vCamera.y))+' Z:'+str(math.floor(vCamera.z)), True, (0,0,0), (255,255,255))

    screen.blit(text, textRect)
    screen.blit(text1, textRect1)
    screen.blit(text2, textRect2)
    pygame.display.flip()


# Done! Time to quit.

pygame.quit()