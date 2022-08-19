from operator import mod
from turtle import Vec2D, pos
import pygame
import math
import copy
import time
from utils import *


def DrawTriangle(x1,y1,x2,y2,x3,y3,color = (255,255,255)):
    pygame.draw.line(screen,color,(x1,y1),(x2,y2))
    pygame.draw.line(screen,color,(x2,y2),(x3,y3))
    pygame.draw.line(screen,color,(x3,y3),(x1,y1))

def FillTriangle(x1,y1,x2,y2,x3,y3,color = (255,255,255)):
    try:
        pygame.draw.polygon(screen,color,((x1,y1),(x2,y2),(x2,y2),(x3,y3),(x3,y3),(x1,y1)))
    except:
        print(color)

def ordenacao_vetor(e):
    return (e.p[0].z+e.p[1].z+e.p[2].z)/3

w = 500
h = 500

linha = False
face = True


matProj = Matrix_MakeProjection(90,h/w, 0.1,1000)

vCamera = vec3d()
vLookDir = vec3d()

fYaw = 0
fTheta = 0

cubo = [
		[ [0.0 , 0.0 , 0.0],    [0.0 , 1.0 , 0.0],    [1.0 , 1.0 , 0.0]  ],
		[ [0.0 , 0.0 , 0.0],    [1.0 , 1.0 , 0.0],    [1.0 , 0.0 , 0.0]  ],
                                                     
		[ [1.0 , 0.0 , 0.0],    [1.0 , 1.0 , 0.0],    [1.0 , 1.0 , 1.0]  ],
		[ [1.0 , 0.0 , 0.0],    [1.0 , 1.0 , 1.0],    [1.0 , 0.0 , 1.0]  ],
                                                 
		[ [1.0 , 0.0 , 1.0],    [1.0 , 1.0 , 1.0],    [0.0 , 1.0 , 1.0]  ],
		[ [1.0 , 0.0 , 1.0],    [0.0 , 1.0 , 1.0],    [0.0 , 0.0 , 1.0]  ],
                                                   
		[ [0.0 , 0.0 , 1.0],    [0.0 , 1.0 , 1.0],    [0.0 , 1.0 , 0.0]  ],
		[ [0.0 , 0.0 , 1.0],    [0.0 , 1.0 , 0.0],    [0.0 , 0.0 , 0.0]  ],
                                                     
		[ [0.0 , 1.0 , 0.0 ],   [0.0 , 1.0 , 1.0] ,   [1.0 , 1.0 , 1.0]  ],
		[ [0.0 , 1.0 , 0.0] ,   [1.0 , 1.0 , 1.0] ,   [1.0 , 1.0 , 0.0 ] ],
                                                  
		[ [1.0 , 0.0 , 1.0 ],   [0.0 , 0.0 , 1.0] ,   [0.0 , 0.0 , 0.0]  ],
		[ [1.0 , 0.0 , 1.0 ],   [0.0 , 0.0 , 0.0] ,   [1.0 , 0.0 , 0.0]  ],
]

meshCube = mesh()
meshCube.LoadFromObjectFile('nave.obj')
#for v in cubo:
#    triangulo1 = triangulo()
#    for index,f in enumerate(v):
#        triangulo1.p[index ]= vec3d(f[0],f[1],f[2])
#        print(f)
#    meshCube.tris.append(triangulo1)
    

pygame.init()


# Set up the drawing window

screen = pygame.display.set_mode([w, h])

# Run until the user asks to quit

running = True

sec = time.time()
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
                vCamera.y = vCamera.y -4*((time.time()-sec))
            if event.key == pygame.K_RIGHT:
                vCamera.x = vCamera.x +4*((time.time()-sec))
            if event.key == pygame.K_DOWN:
                vCamera.y = vCamera.y +4*((time.time()-sec))
            if event.key == pygame.K_LEFT:
                vCamera.x = vCamera.x -4*((time.time()-sec))
            mover = True
            tecla = event.key
        
        if event.type == pygame.KEYUP :
            mover = False

        if(mover):
            if tecla == ord('z'):
                linha = not linha
            if tecla == ord('x'):
                face = not face

            if tecla == ord('a'):
                fYaw = fYaw - 2*((time.time()-sec))
            if tecla == ord('d'):
                fYaw = fYaw + 2*((time.time()-sec))
            if tecla == ord('w'):
                vCamera = Vector_Add(vCamera, vForward)
            if tecla == ord('s'):
                vCamera = Vector_Sub(vCamera, vForward)

            


    # Fill the background with white
    screen.fill((0, 0, 0))
    if(time.time()!=sec):  
        print(1/(time.time()-sec))
    #fTheta += 1 * (time.time()-sec)
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

    # Draw a solid blue circle in the center
    for tri in meshCube.tris:

        triProjected    = triangulo()
        triTransformado = triangulo()
        triViewed       = triangulo()
        
        triTransformado.p[0] = Matrix_MultiplyVector(matWorld,tri.p[0])
        triTransformado.p[1] = Matrix_MultiplyVector(matWorld,tri.p[1])
        triTransformado.p[2] = Matrix_MultiplyVector(matWorld,tri.p[2])
        

        line1 = Vector_Sub(triTransformado.p[1],triTransformado.p[0])
        line2 = Vector_Sub(triTransformado.p[2],triTransformado.p[0])
        
        normal = Vector_CrossProduct(line1,line2)

        normal = Vector_Normalise(normal)

        vCameraRay = Vector_Sub(triTransformado.p[0],vCamera)

        if(Vector_DotProduct(normal,vCameraRay)<0) :
            #iluminação
            light_direction = vec3d(0,1,-1)
            light_direction = Vector_Normalise(light_direction)

            #produto escalar entre a iluminação e a normal da face da figura
            light_direction_dot_normal = max(0.1,Vector_DotProduct(light_direction,normal))

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

                triProjected.color = (255*abs(light_direction_dot_normal) % 255,
                                255*abs(light_direction_dot_normal) % 255,
                                255*abs(light_direction_dot_normal) % 255)
                triangulos_to_render.append(triProjected)

    triangulos_to_render.sort(key = ordenacao_vetor,reverse=True)

    for tritoRaster in triangulos_to_render:
        if face:
            FillTriangle(triProjected.p[0].x,h-triProjected.p[0].y,
                        triProjected.p[1].x,h-triProjected.p[1].y,
                        triProjected.p[2].x,h-triProjected.p[2].y,
                        color=triProjected.color)
        if(linha):
            DrawTriangle(triProjected.p[0].x,h-triProjected.p[0].y,
                        triProjected.p[1].x,h-triProjected.p[1].y,
                        triProjected.p[2].x,h-triProjected.p[2].y,
                        color=(255,0,0))

    # Flip the display

    pygame.display.flip()


# Done! Time to quit.

pygame.quit()