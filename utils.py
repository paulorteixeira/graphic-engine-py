from cmath import sqrt
import math
import copy

class vec3d:
    def __init__(self,x: float = 0,y: float = 0,z: float = 0,w=1):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

class triangulo:
    def __init__(self):
        self.p = [vec3d() for i in range(3)]
        self.color = (0,0,0)
     
class mesh():
    def __init__(self):
        self.tris = []

    def LoadFromObjectFile(self,sFilename):
        f = open(sFilename)
        vertices = []
   
        for linha in f:
            if(linha[0]=='v'):
                linha = linha.strip('\n')
                posicoes = linha.split(' ')
                vertices.append(vec3d(float(posicoes[1]),float(posicoes[2]),float(posicoes[3])))
            if(linha[0]=='f'):
                linha =linha.strip('\n')
                posicoes = linha.split(' ')
                triangulo1 = triangulo()
                triangulo1.p[0]=vertices[int(posicoes[1])-1]
                triangulo1.p[1]=vertices[int(posicoes[2])-1]
                triangulo1.p[2]=vertices[int(posicoes[3])-1]
                self.tris.append(triangulo1)
        return True

class mat4x4():
    def __init__(self):
        self.m = [[0 for j in range(4)] for i in range(4)]

def Matrix_MultiplyVector (m,i):
    o = vec3d()
    o.x = i.x * m.m[0][0] + i.y * m.m[1][0] + i.z * m.m[2][0] + i.w*m.m[3][0]
    o.y = i.x * m.m[0][1] + i.y * m.m[1][1] + i.z * m.m[2][1] + i.w*m.m[3][1]
    o.z = i.x * m.m[0][2] + i.y * m.m[1][2] + i.z * m.m[2][2] + i.w*m.m[3][2]
    o.w = i.x * m.m[0][3] + i.y * m.m[1][3] + i.z * m.m[2][3] + i.w*m.m[3][3]
    return o

def Matrix_MakeIdentity():
    matrix = mat4x4()
    matrix.m[0][0] = 1
    matrix.m[1][1] = 1
    matrix.m[2][2] = 1
    matrix.m[3][3] = 1    
    return matrix

def Matrix_MakeRotationX(fAngleRad):
    matRotX = mat4x4()
    matRotX.m[0][0] = 1
    matRotX.m[1][1] = math.cos(fAngleRad * 0.5)
    matRotX.m[1][2] = math.sin(fAngleRad * 0.5)
    matRotX.m[2][1] = -math.sin(fAngleRad * 0.5)
    matRotX.m[2][2] = math.cos(fAngleRad * 0.5)
    matRotX.m[3][3] = 1
    return matRotX

def Matrix_MakeRotationY(fAngleRad):
    matRotY = mat4x4()
    matRotY.m[0][0] = math.cos(fAngleRad)
    matRotY.m[0][2] = math.sin(fAngleRad)
    matRotY.m[2][0] = -math.sin(fAngleRad)
    matRotY.m[1][1] = 1
    matRotY.m[2][2] = math.cos(fAngleRad)
    matRotY.m[3][3] = 1
    return matRotY

def Matrix_MakeRotationZ(fAngleRad):
    matRotZ = mat4x4()
    matRotZ.m[0][0] = math.cos(fAngleRad)
    matRotZ.m[0][1] = math.sin(fAngleRad)
    matRotZ.m[1][0] = -math.sin(fAngleRad)
    matRotZ.m[1][1] = math.cos(fAngleRad)
    matRotZ.m[2][2] = 1
    matRotZ.m[3][3] = 1
    return matRotZ

def Matrix_MakeTranslation(x,y,z):
    matrix = mat4x4()
    matrix.m[0][0] = 1
    matrix.m[1][1] = 1
    matrix.m[2][2] = 1
    matrix.m[3][3] = 1
    matrix.m[3][0] = x
    matrix.m[3][1] = y
    matrix.m[3][2] = z
    return matrix

def Matrix_MakeProjection(fFovDegrees,fAspectRatio,fNear,fFar):
 
    fFovRad = 1/(math.tan(fFovDegrees*0.5/180*math.pi))

    matProj = mat4x4()
    matProj.m[0][0] = fAspectRatio*fFovRad
    matProj.m[1][1] = fFovRad
    matProj.m[2][2] = fFar/(fFar - fNear)
    matProj.m[3][2] = (-fFar*fNear)/(fFar - fNear)
    matProj.m[2][3] = 1
    matProj.m[3][3] = 0

    return matProj

def Matrix_MultiplyMatrix(m1,m2):
    matrix = mat4x4()
    for c in range(4):
        for r in range(4):
            matrix.m[r][c] = m1.m[r][0] * m2.m[0][c] + m1.m[r][1] * m2.m[1][c] + m1.m[r][2] * m2.m[2][c] + m1.m[r][3] * m2.m[3][c]
    return matrix
	


def Vector_Add(v1,v2):
    return vec3d(v1.x+v2.x,v1.y+v2.y,v1.z+v2.z)

def Vector_Sub(v1,v2):
    return vec3d(v1.x-v2.x,v1.y-v2.y,v1.z-v2.z)

def Vector_Mul(v1,k):
    return vec3d(v1.x*k,v1.y*k,v1.z*k)

def Vector_Div(v1,k):
    return vec3d(v1.x/k,v1.y/k,v1.z/k)

def Vector_DotProduct(v1,v2):
    return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z

def Vector_Length(v):
    return math.sqrt(Vector_DotProduct(v,v))

def Vector_Normalise(v):
    l = math.sqrt(v.x*v.x + v.y*v.y + v.z*v.z)
    if(l !=0 ):
        p = vec3d(v.x/l,v.y/l,v.z/l)
    else:
        p = vec3d(v.x/0.00000000001,v.y/0.00000000001,v.z/0.00000000001)
    return p

def Vector_CrossProduct(v1,v2):
    v = vec3d()
    v.x = v1.y * v2.z - v1.z * v2.y
    v.y = v1.z * v2.x - v1.x * v2.z
    v.z = v1.x * v2.y - v1.y * v2.x
    return v

def Matrix_PointAt(pos,target,up):
    #new forward 
    newForward = Vector_Sub(target,pos)
    newForward = Vector_Normalise(newForward)
    #new up
    a = Vector_Mul(newForward, Vector_DotProduct(up,newForward))
    newUp = Vector_Sub(up,a)
    newUp = Vector_Normalise(newUp)

    #new right
    newRight = Vector_CrossProduct(newUp, newForward)

    matrix = mat4x4()

    matrix.m[0][0] = newRight.x
    matrix.m[0][1] = newRight.y
    matrix.m[0][2] = newRight.z
    matrix.m[0][3] = 0.0
    matrix.m[1][0] = newUp.x
    matrix.m[1][1] = newUp.y
    matrix.m[1][2] = newUp.z
    matrix.m[1][3] = 0.0
    matrix.m[2][0] = newForward.x
    matrix.m[2][1] = newForward.y
    matrix.m[2][2] = newForward.z
    matrix.m[2][3] = 0.0
    matrix.m[3][0] = pos.x    
    matrix.m[3][1] = pos.y
    matrix.m[3][2] = pos.z
    matrix.m[3][3] = 1.0

    return matrix

def Matrix_QuickInverse(m) :
	
    matrix = mat4x4()
    matrix.m[0][0] = m.m[0][0]
    matrix.m[0][1] = m.m[1][0] 
    matrix.m[0][2] = m.m[2][0] 
    matrix.m[0][3] = 0.0
    matrix.m[1][0] = m.m[0][1]
    matrix.m[1][1] = m.m[1][1] 
    matrix.m[1][2] = m.m[2][1] 
    matrix.m[1][3] = 0.0
    matrix.m[2][0] = m.m[0][2] 
    matrix.m[2][1] = m.m[1][2] 
    matrix.m[2][2] = m.m[2][2] 
    matrix.m[2][3] = 0.0
    matrix.m[3][0] = -(m.m[3][0] * matrix.m[0][0] + m.m[3][1] * matrix.m[1][0] + m.m[3][2] * matrix.m[2][0])
    matrix.m[3][1] = -(m.m[3][0] * matrix.m[0][1] + m.m[3][1] * matrix.m[1][1] + m.m[3][2] * matrix.m[2][1])
    matrix.m[3][2] = -(m.m[3][0] * matrix.m[0][2] + m.m[3][1] * matrix.m[1][2] + m.m[3][2] * matrix.m[2][2])
    matrix.m[3][3] = 1.0
    return matrix

def Vector_IntersectPlane(plane_p, plane_n, lineStart, lineEnd):
	
    plane_n = Vector_Normalise(plane_n)
    plane_d = -Vector_DotProduct(plane_n, plane_p)
    ad = Vector_DotProduct(lineStart, plane_n)
    bd = Vector_DotProduct(lineEnd, plane_n)
    t = (-plane_d - ad) / (bd - ad)
    lineStartToEnd = Vector_Sub(lineEnd, lineStart)
    lineToIntersect = Vector_Mul(lineStartToEnd, t)
    return Vector_Add(lineStart, lineToIntersect)


def Triangle_ClipAgainstPlane( plane_p,  plane_n,  in_tri):
    plane_n = Vector_Normalise(plane_n)
    out_tri1 = triangulo()
    out_tri2 = triangulo()
    def dist(p):
        n =  Vector_Normalise(p)
        return (plane_n.x * p.x + plane_n.y * p.y + plane_n.z * p.z - Vector_DotProduct(plane_n, plane_p))

    inside_points = []
    outside_points = []

    nInsidePointCount = 0
    nOutsidePointCount = 0

    d0 = dist(in_tri.p[0])
    d1 = dist(in_tri.p[1])
    d2 = dist(in_tri.p[2])
 
    if(d0>=0):
        inside_points.append(in_tri.p[0])
        nInsidePointCount = nInsidePointCount +1
    else:
        outside_points.append(in_tri.p[0])
        nOutsidePointCount = nOutsidePointCount +1
    if(d1>=0):
        inside_points.append(in_tri.p[1])
        nInsidePointCount = nInsidePointCount +1
    else:
        outside_points.append(in_tri.p[1])
        nOutsidePointCount = nOutsidePointCount +1
    if(d2>=0):
        inside_points.append(in_tri.p[2])
        nInsidePointCount = nInsidePointCount +1
    else:
        outside_points.append(in_tri.p[2])
        nOutsidePointCount = nOutsidePointCount +1

    if(nInsidePointCount == 0):
        return 0, vec3d(),vec3d() 
    if(nInsidePointCount == 3):
        out_tri1 = copy.copy(in_tri)
        return 1, out_tri1, vec3d() 
    if(nInsidePointCount == 1 and nOutsidePointCount ==2):
        out_tri1.color = in_tri.color

        out_tri1.p[0] = copy.copy(inside_points[0])
        out_tri1.p[1] = Vector_IntersectPlane(plane_p,plane_n,inside_points[0],outside_points[0])
        out_tri1.p[2] = Vector_IntersectPlane(plane_p,plane_n,inside_points[0],outside_points[1])
        return 1, out_tri1, vec3d() 
    if(nInsidePointCount == 2 and nOutsidePointCount == 1):
        out_tri1.color = in_tri.color
        out_tri2.color = in_tri.color

        out_tri1.p[0] = copy.copy(inside_points[0])
        out_tri1.p[1] = copy.copy(inside_points[1])
        out_tri1.p[2] = Vector_IntersectPlane(plane_p,plane_n,inside_points[0],outside_points[0])
        
        out_tri2.p[0] = copy.copy(inside_points[1])
        out_tri2.p[1] = copy.copy(out_tri1.p[2])
        out_tri2.p[2] = Vector_IntersectPlane(plane_p,plane_n,inside_points[1],outside_points[0])
        return 1, out_tri1, out_tri2 
        