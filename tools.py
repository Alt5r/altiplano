from math import *
import colorsys
NEIGHBORHOOD_RADIUS = 40

#square cus python dont have it and its ugly

def sqr(x):
	"""
	takes x and squres it and returns it
	
	"""
	return x*x

class Vector:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def __mul__(self, a):
		self.x = self.x * a
		self.y = self.y * a
		return self

	def __add__(self, a):
		self.x = self.x + a.x
		self.y = self.y + a.y
		return self

	def __sub__(self, a):
		self.x = self.x - a.x
		self.y = self.y - a.y
		return self

	def __truediv__(self, a):
		self.x = self.x / a
		self.y = self.y / a
		return self

	def add(self, a):
		self.x = self.x + a.x
		self.y = self.y + a.y

	def scale(self, a):
		self.x *= a
		self.y *= a
	def parseToInt(self):
		return (int(self.x), int(self.y))

	def magnitude(self):
		return sqrt(sqr(self.x) + sqr(self.y))

	def unitv(self):
		mag = self.magnitude()
		if not (mag == 0 ):
			self.x = self.x/mag
			self.y = self.y/mag

	def unitReturn(self):
		mag = self.magnitude()
		if not (mag == 0 ):
			
			return Vector(self.x/mag, self.y/mag)
	def Unitv(self):
		mag = self.magnitude()
		if mag != 0:
			
			return Vector(self.x/mag, self.y/mag)
		else:
			return Vector(1, 1)

	def heading(self):
		angle = atan2(self.y, self.x)
		# in radians
		return angle

	def limit(self, max_length):
		squared_mag = self.magnitude() * self.magnitude()
		if squared_mag > (max_length * max_length):
			self.x = self.x/sqrt(squared_mag)
			self.y = self.y/sqrt(squared_mag)
			self.x = self.x * max_length
			self.y = self.y * max_length
	def reset(self, x=0, y=0):
		self.x = x
		self.y = y

	def __repr__(self):
		return f'vector-> x:{self.x}, y:{self.y}'


def getDistance(v1, v2):
	d = sqrt(sqr(v2.x - v1.x) + sqr(v2.y - v1.y))
	if d != 0:
		return d
	else:
		#not true distance however prevents additoanly length checks if boid is self in boids class sepertaiton
		return 1

def AddVectors(v1, v2):
	return Vector(v1.x + v2.x, v1.y + v2.y)

def translate(value, min1, max1, min2, max2):
    return min2 + (max2 - min2)* ((value-min1)/(max1-min1))

def hsv_to_rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def SubVectors(v1, v2):
	return Vector(v1.x - v2.x, v1.y - v2.y)