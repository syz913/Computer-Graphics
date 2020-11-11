from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import PIL.Image as Image

class myGraph():
	def __init__(self):
		self.wallPts()
		self.bindTexture()
		self.light()
	def wallPts(self):
        #定义墙的几何坐标，分别对应：
        # 正面左下，正面右下，正面右上，正面左上
        # 左侧面左下，右侧面右下，上面右上，上面左上
		self.pts = [[-0.5,-0.5,0],[0.5,-0.5,0],[0.5,0.5,0],[-0.5,0.5,0], \
						[-0.5,-0.5,-0.3],[0.5,-0.5,-0.3],[0.5,0.5,-0.3],[-0.5,0.5,-0.3]]
		#self.lines = [[0,1],[0,2],[1,3],[2,3],[0,4],[1,5],[2,6],[3,7],[1,5],[4,5],[4,6],[5,7],[6,7]]
        #要显示的墙的三个面
		self.faces = [[0,1,2,3],[2,6,7,3],[0,3,7,4]]#,[4,5,6,7],[0,1,5,4],[1,2,6,5]]
        #设置纹理坐标
		self.cor = [[0.0,0.0],[1.0,0.0],[1.0,1.0],[0.0,1.0],[0.0,0.0],[1.0,0.0],[1.0,1.0],[0.0,1.0]]
	def drawCube(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) #清除当前帧的颜色、把所有像素的深度值设置为最大值
		glPushMatrix()

		glMatrixMode(GL_MODELVIEW) #将当前矩阵指定为模型视图矩阵
		glRotatef(20.0,0.0,1.0,0.0) #旋转 20°
		glRotatef(30.0,1.0,0.0,0.0) #侧向旋转 30°

		glBegin(GL_QUADS)
		glNormal3f(0.0,0.0,1.0) #设置法向量指向
        #遍历每个面中的点，绘制三个面
		for pt in self.faces[0]:
			glTexCoord2fv(self.cor[pt])
			glVertex3fv(self.pts[pt])
		glNormal3f(0.0,1.0,0.0)
		for pt in self.faces[1]:
			glTexCoord2fv(self.cor[pt])
			glVertex3fv(self.pts[pt])
		glNormal3f(-1.0,0.0,0.0)
		for pt in self.faces[2]:
			glTexCoord2fv(self.cor[pt])
			glVertex3fv(self.pts[pt])
		glEnd()

		glPopMatrix()
		glFlush()
	def light(self):
        #设置光源
		light_position =  [-1.0, 1.0, 2.0, 0.0]
		mat_diffuse = [0.9,0.9,0.9,1.0]
		glShadeModel ( GL_SMOOTH ) #glShadeModel函数用于控制颜色的过渡模式，参数一般为GL_SMOOTH与GL_FLAT
                                   #opengl在指定的两点之间进行插值，绘制其他点。当两点颜色不同时，GL_SMOOTH将出现过渡效果，而GL_FLAT只是以指定的某一点的单一色绘制其他所有点。
                                   #由于本项目需要绘制静态实感的实物，因此，若使用GL_FLAT则会出现颜色断层的不和谐情况，因此采用GL_SMOOTH参数。
		glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse) #glMaterialfv函数可以指定材质对漫射光的反射率。
                                                        #第一个参数一般可以取GL_FRONT、GL_BACK、GL_FRONT_AND_BACK等，分别表示材质属性运用于对象的正面、反面、或是正反两面。我选取的是GL_FRONT_AND_BACK
                                                        #第二个参数表示对何种光进行设置。我选用的参数为GL_AMBIENT_AND_DIFFUSE，表示对环境光和漫射光反射率进行设置。
                                                        #第三个参数是一个四维数组，描述了反光率的RGBA值，每一项取值都为0-1之间。这里我选取了一个我相对喜欢的颜色。
		glLightfv ( GL_LIGHT0, GL_POSITION, light_position) #glLightfv函数用于创建指定光源
                                                            #第一个参数表示选择0号光源
                                                            #第二个参数用于指定光源的属性，这里需要指定的属性是位置
                                                            #第三个参数表示第二个参数所对应属性的具体的值
		glEnable (GL_LIGHTING) #光源在默认情况下式关闭的。由于在后续的渲染中需要使用，因此设置开启。
		glEnable (GL_LIGHT0) #为了使用第0号光源，需要指定GL_LIGHT0。
		glEnable (GL_DEPTH_TEST) #启用深度测试，只绘制最靠前的一层。
		glDisable(GL_COLOR_MATERIAL)
	def bindTexture(self):
		glEnable(GL_TEXTURE_2D);
		img = Image.open("./images/wall.jpg")
		img = np.asarray(img, dtype=np.uint8)
		self.textures = glGenTextures(1) #创建纹理
		#glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
		glBindTexture(GL_TEXTURE_2D, self.textures) #将一个命名的纹理绑定到一个纹理目标上
        #纹理过滤
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.shape[0], img.shape[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img)
		return self.textures

def main():
	glutInit() #初始化 GLUT
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH) #设置初始显示模式，这里的参数分别对应了指定单缓存窗口、指定RGBA颜色模式的窗口、指定R深度缓冲区
	glutInitWindowSize(600,600) #设置窗口大小
	glutCreateWindow("realisticGraph") #给窗口命名
	g = myGraph()
	glutDisplayFunc(g.drawCube)
	glutMainLoop()

if __name__ == "__main__":
	main()