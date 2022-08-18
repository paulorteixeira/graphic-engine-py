import pygame
import math
import copy
import time

class vec3d:
    def __init__(self,x = 0,y = 0,z = 0):
        self.x = x
        self.y = y
        self.z = z

class triangulo:
    def __init__(self):
        self.p = [vec3d() for i in range(3)]
     
class mesh():
    def __init__(self):
        self.tris = []

class mat4x4():
    def __init__(self):
        self.m = [[0 for j in range(4)] for i in range(4)]

def MultiplyMatrixVector (i,o,m):
    o.x = i.x * m.m[0][0] + i.y * m.m[1][0] + i.z * m.m[2][0] + m.m[3][0]
    o.y = i.x * m.m[0][1] + i.y * m.m[1][1] + i.z * m.m[2][1] + m.m[3][1]
    o.z = i.x * m.m[0][2] + i.y * m.m[1][2] + i.z * m.m[2][2] + m.m[3][2]

    w = i.x * m.m[0][3] + i.y * m.m[1][3] + i.z * m.m[2][3] + m.m[3][3]

    if(w != 0):
        o.x = o.x/w
        o.y = o.y/w
        o.z = o.z/w

def DrawTriangle(x1,y1,x2,y2,x3,y3,color = (255,255,255)):
    pygame.draw.line(screen,color,(x1,y1),(x2,y2))
    pygame.draw.line(screen,color,(x2,y2),(x3,y3))
    pygame.draw.line(screen,color,(x3,y3),(x1,y1))

w = 500
h = 500


## Projeção
fNear = 0.1
fFar = 1000
fFov = 90
fAspectRatio = h/w
fFovRad = 1/(math.tan(fFov*0.5/180*math.pi))


matProj = mat4x4()
matProj.m[0][0] = fAspectRatio*fFovRad
matProj.m[1][1] = fFovRad
matProj.m[2][2] = fFar/(fFar - fNear)
matProj.m[3][2] = (-fFar*fNear)/(fFar - fNear)
matProj.m[2][3] = 1
matProj.m[3][3] = 0

matRotZ = mat4x4()
matRotX = mat4x4()

fTheta = 1

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

for v in cubo:
    triangulo1 = triangulo()
    for index,f in enumerate(v):
        triangulo1.p[index ]= vec3d(f[0],f[1],f[2])
        print(f)
    meshCube.tris.append(triangulo1)
    

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


    # Fill the background with white
    screen.fill((255, 255, 255))
    
    fTheta += 1 * (time.time()-sec)
    sec = time.time()
    # Rotation Z
    matRotZ.m[0][0] = math.cos(fTheta)
    matRotZ.m[0][1] = math.sin(fTheta)
    matRotZ.m[1][0] = -math.sin(fTheta)
    matRotZ.m[1][1] = math.cos(fTheta)
    matRotZ.m[2][2] = 1
    matRotZ.m[3][3] = 1

    # Rotation X
    matRotX.m[0][0] = 1
    matRotX.m[1][1] = math.cos(fTheta * 0.5)
    matRotX.m[1][2] = math.sin(fTheta * 0.5)
    matRotX.m[2][1] = -math.sin(fTheta * 0.5)
    matRotX.m[2][2] = math.cos(fTheta * 0.5)
    matRotX.m[3][3] = 1

    # Draw a solid blue circle in the center
    for tri in meshCube.tris:

        triProjected    = triangulo()
        triTranslado    = triangulo()
        triRotacionaZ   = triangulo()
        triRotacionaZX  = triangulo()

        MultiplyMatrixVector(tri.p[0],triRotacionaZ.p[0],matRotZ)
        MultiplyMatrixVector(tri.p[1],triRotacionaZ.p[1],matRotZ)
        MultiplyMatrixVector(tri.p[2],triRotacionaZ.p[2],matRotZ)

        MultiplyMatrixVector(triRotacionaZ.p[0],triRotacionaZX.p[0],matRotX)
        MultiplyMatrixVector(triRotacionaZ.p[1],triRotacionaZX.p[1],matRotX)
        MultiplyMatrixVector(triRotacionaZ.p[2],triRotacionaZX.p[2],matRotX)

        triTranslado = copy.deepcopy(triRotacionaZX)
        
        triTranslado.p[0].z = triRotacionaZX.p[0].z +5
        triTranslado.p[1].z = triRotacionaZX.p[1].z +5
        triTranslado.p[2].z = triRotacionaZX.p[2].z +5
        
        MultiplyMatrixVector(triTranslado.p[0],triProjected.p[0],matProj)
        MultiplyMatrixVector(triTranslado.p[1],triProjected.p[1],matProj)
        MultiplyMatrixVector(triTranslado.p[2],triProjected.p[2],matProj)

        #modificando a escala
        triProjected.p[0].x = triProjected.p[0].x + 1
        triProjected.p[0].y = triProjected.p[0].y + 1

        triProjected.p[1].x = triProjected.p[1].x + 1
        triProjected.p[1].y = triProjected.p[1].y + 1

        triProjected.p[2].x = triProjected.p[2].x + 1
        triProjected.p[2].y = triProjected.p[2].y + 1

        triProjected.p[0].x = triProjected.p[0].x*0.5*w
        triProjected.p[0].y = triProjected.p[0].y*0.5*h
        triProjected.p[1].x = triProjected.p[1].x*0.5*w
        triProjected.p[1].y = triProjected.p[1].y*0.5*h
        triProjected.p[2].x = triProjected.p[2].x*0.5*w
        triProjected.p[2].y = triProjected.p[2].y*0.5*h

        DrawTriangle(triProjected.p[0].x,triProjected.p[0].y,
                     triProjected.p[1].x,triProjected.p[1].y,
                     triProjected.p[2].x,triProjected.p[2].y,
                     color=(0,0,0))
        #pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)


    # Flip the display

    pygame.display.flip()


# Done! Time to quit.

pygame.quit()