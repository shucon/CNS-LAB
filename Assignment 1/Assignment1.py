from sympy import *
import numpy as np
import math as m
import matplotlib.pyplot as plt
numParticles = 256
# boxsize and sigma are in angstrong
boxSize = 10
sigma = 3.4
epsilon = 9.93 * 10**-6
distance = Symbol('distance')
pow = sigma / distance
# Lennard-Jones potential
potential = 4 * epsilon * (pow ** 12 - pow ** 6)
# Differentiating potential wrt distance
potentialPrime = -potential.diff(distance)
# Creating functions for force and calculations
force = lambdify(distance, potentialPrime, 'numpy')
potential = lambdify(distance, potential, 'numpy')
class Particle:

	# Initializer / Instance Attributes
	def __init__(self, velocityX, velocityY, velocityZ, positionX, positionY, positionZ):
		self.velocityX = velocityX
		self.velocityY = velocityY
		self.velocityZ = velocityZ
		self.positionX = positionX
		self.positionY = positionY
		self.positionZ = positionZ
		self.forceX = 0
		self.forceY = 0
		self.forceZ = 0
		self.potential = 0
		self.mass = 39.94

	# Calculate force using the force function
	def force(self, particle):
		self.forceX += force(self.positionX - particle.positionX)
		self.forceY += force(self.positionY - particle.positionY)
		self.forceZ += force(self.positionZ - particle.positionZ)

	# Calculating the potential energy using distance b/w particles and using potential function
	def potentialCalc(self, particle):
		r = m.sqrt((self.positionX - particle.positionX)**2 + (self.positionY - particle.positionY)**2 + (self.positionZ - particle.positionZ)**2)
		self.potential += potential(r)
	
	# Update coordinates and velocity after calculating force
	def coordUpdate(self):
		acceleration = self.forceX / self.mass
		#as time frame is 1fs we could directly add acc. to velocity
		self.velocityX += acceleration
		acceleration = self.forceY / self.mass
		self.velocityY += acceleration
		acceleration = self.forceZ / self.mass
		self.velocityZ += acceleration
		#as time frame is 1fs we could directly add velocity to position
		self.positionX += self.velocityX
		self.positionY += self.velocityY
		self.positionZ += self.velocityZ
		#change potential and force back to zero before next time frame
		self.forceX = 0
		self.forceY = 0
		self.forceZ = 0
		self.potential = 0
	
	# Calculates Kinetic Energy
	def kineticEnergy(self):
		self.kinetic = 0.5 * self.mass * (self.velocityX**2 + self.velocityY**2 + self.velocityZ**2)
	

particle = []
x = 0 
y = 0
z = 0
for i in range(numParticles):

	# Random cordinates such that the coordinates don't overlap
	x += i * 0.0390625
	y += i * 0.0390625
	z += i * 0.0390625
	# Initial velocity of particles is zero
	vX = 0
	vY = 0
	vZ = 0
	particle.append(Particle(vX, vY, vZ, x, y, z))

# Simulation for each time frame
timeFrame = []
energy = []
for time in range(100):
	print ("time frame {0}".format(time))
	tempTotalEnergy = 0
	for i in range(numParticles):
		for j in range(numParticles):
			if (i != j):
				particle[i].force(particle[j])
				particle[i].potentialCalc(particle[j])
	for i in range(numParticles):
		tempPotential = particle[i].potential
		particle[i].coordUpdate()
		particle[i].kineticEnergy()
		total = tempPotential + particle[i].kinetic
		tempTotalEnergy += total
		print ("Particle {0} x {1} y {2} z {3}".format(i,particle[i].positionX,particle[i].positionY,particle[i].positionZ))
		print ("Particle {0} potential {1} kinetic {2} total {3}".format(i,tempPotential,particle[i].kinetic,total))
	timeFrame.append(time)
	energy.append(tempTotalEnergy)

plt.plot(timeFrame,energy)
plt.ylabel('Total Energy of the system')
plt.xlabel('Time in femto seconds')
plt.show()