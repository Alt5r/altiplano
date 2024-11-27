from tools import *
from random import *
class boid:
    def __init__(self, x=0, y=0, i=0, j=0, h=600, w=800):
        # postiion vector
        self.position = Vector(x,y)
        #height and width for pygame arena for ato avoidance in seperation method
        self.h = h
        self.w = w
        self.acceleration = Vector()
        self.colour = (randint(0,255),randint(0,255),randint(0,255))
        # vecolicty 
        self.velocity = Vector(i,j)

        self.max_speed = 5

        #radius defines our threshold for closeness of other boids, as used in seperation
        self.rad = 5
    
    def getColour(self):
        return self.colour

    
        
    
    
    def behaviour(self, boids):
       # print(self.velocity.parseToInt())

       #weights

        wCoh = 0.5
        wAli = 4
        wSep = 2
        wCohA = 2
        
        self.acceleration.reset()

        
        avoid = self.seperation(boids) * wSep
       
        self.acceleration.add(avoid)

        #print("at cohesion")
        coh = self.cohesion(boids) * wCoh
        #print(coh)
        self.acceleration.add(coh)

        av = self.collision_avoidance(boids) * wCohA
        self.acceleration.add(av)
    
        align = self.alignment(boids) * wAli
       
        self.acceleration.add(align)

        self.velocity += self.acceleration # this changing direction 
        #print(align, coh, avoid)
        if self.velocity.magnitude() > self.max_speed:
            self.velocity.unitv()
            self.velocity *= self.max_speed
        
        
        
        
        #self.acceleration -= self.velocity

        

        self.position += self.velocity #this is changing its position in accordance with velocity vector 
        self.randpos()
    #defining key behaviours here

    def randpos(self):
        if self.position.parseToInt() == (3, 3):
            self.position = Vector(randint(0,self.w), randint(0,self.h))


    def seperation(self, boids):
        """
        Creates a cumulative steering vector based on distances and inverse directions of neighbors,
        determining a total vector for steering away from neighbors optimally.
        """
        total = 0
        steering = Vector()

        for b in boids:
            if b == self:
                continue
            distance = getDistance(self.position, b.position)
            if 0 < distance < self.rad+5:  # Check for closeness
                # Vector pointing away from the nearby boid
                raw_dir_away = self.position - b.position
                clamped_distance = max(distance, 1.0)  # Prevent very small distances
                scaled_dir_away = raw_dir_away / (clamped_distance ** 2)
                steering.add(scaled_dir_away)
                total += 1
            elif distance < 1:
                # Add random nudge to resolve overlap
                nudge = Vector(uniform(-0.5, 0.5), uniform(-0.5, 0.5)) * self.max_speed
                steering.add(nudge)
                total += 1
        # Edge avoidance (considering boundaries of the screen)
        coords_tuple = self.position.parseToInt()

        # Check proximity to the edges
        if coords_tuple[1] < self.rad + 15:  # Top edge
            steering.add(Vector(0, 1))  # Push downward
            total += 1
        elif coords_tuple[1] > self.h - (self.rad + 15):  # Bottom edge
            steering.add(Vector(0, -1))  # Push upward
            total += 1

        if coords_tuple[0] < self.rad + 15:  # Left edge
            steering.add(Vector(1, 0))  # Push right
            total += 1
        elif coords_tuple[0] > self.w - (self.rad + 15):  # Right edge
            steering.add(Vector(-1, 0))  # Push left
            total += 1

        if total > 0:
            steering = steering / total
            steering.unitv()
            steering *= self.max_speed
        return steering

    def collision_avoidance(self, boids):
        """
        Avoids colliding with other boids that are in the same position or very close.
        If two boids are very close or at the same position, it applies a repulsive force.
        """
        steering = Vector()
        total = 0
        threshold = 2  # This is the minimum distance for considering a collision

        for b in boids:
            if b == self:
                continue

            # Check if the boids are in the same position or very close
            distance = getDistance(self.position, b.position)
            if distance < threshold:  # If boids are too close (e.g., almost the same position)
                # Apply a repulsive force in the opposite direction of the other boid
                raw_dir_away = self.position - b.position  # Direction away from the other boid
                steering.add(raw_dir_away)  # Add this force to the total steering
                total += 1

        # If we have any collisions, normalize and apply the steering force
        if total > 0:
            steering = steering / total
            steering.unitv()  # Normalize the steering vector
            steering *= self.max_speed  # Set the magnitude to max speed
            
        return steering


    def alignment(self, boids):
        """
        Aligns the boid's velocity with its neighbors.
        """
        total = 0
        steering = Vector(uniform(-1,1), uniform(-1,1))

        for b in boids:
            if b == self:
                continue
            distance = getDistance(self.position, b.position)
            if distance < self.rad+50 and b.velocity.unitReturn() is not None:
                tmp = b.velocity.unitReturn()
                steering.add(tmp)  # Add neighbor's normalized velocity
                total += 1

        if total > 0:
            
            steering = steering / total
            steering.unitv()
            steering =  steering* self.max_speed
            #steering -= self.velocity
        return steering


    
    def cohesion(self, boids):
        """
        Moves the boid towards the average position of nearby boids.
        """
        total = 0
        steering = Vector()

        for b in boids:
            if b == self:
                continue
            distance = getDistance(self.position, b.position)
            if 0 < distance < self.rad+175:
                steering.add(b.position)
                total += 1

        if total > 0:
            avg_position = steering / total
            desired = avg_position - self.position
            desired.unitv()
            desired *= self.max_speed
            desired -= self.velocity
            return desired
        return Vector(0,0)


    def getPosition(self) -> Vector:
        return self.position

    def setVelocity(self, i, j):
        self.velocity = Vector(i,j)
        """
        to do: 

         - add a movement handeler so I can take the steering directions from the 3 behaviors and acutally move the boids with it 
         - randomly move all the boids around in a list as on slower language you owuld have a "leader" each iteration throuhg boid list as thye 
           would be updated first, neighbors around this oid would be more likley to follow it as its moved first 

        ideas:
         - missile system average coordinate of all  boids and watch them avoid the missile 
        
        """