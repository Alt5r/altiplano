from tools import *

class boid:
    def __init__(self, x=0, y=0, i=0, j=0, h=600, w=800):
        # postiion vector
        self.position = Vector(x,y)
        #height and width for pygame arena for ato avoidance in seperation method
        self.h = h
        self.w = w
        self.acceleration = Vector()
        # vecolicty 
        self.velocity = Vector(i,j)

        self.max_speed = 5

        #radius defines our threshold for closeness of other boids, as used in seperation
        self.rad = 10
    
    
    
    def behaviour(self, boids):
       # print(self.velocity.parseToInt())
        
        self.acceleration.reset()

        
        avoid = self.seperation(boids)
       
        self.acceleration.add(avoid)

        #print("at cohesion")
        coh = self.cohesion(boids)
        #print(coh)
        self.acceleration.add(coh)

    
        align = self.alignment(boids)
       
        self.acceleration.add(align)

        print(align, coh, avoid)
        if self.velocity.magnitude() > self.max_speed:
            self.velocity.unitv()
            self.velocity *= self.max_speed
        
        
        #self.acceleration -= self.velocity

        self.velocity += self.acceleration # this changing direction 

        self.position += self.velocity #this is changing its position in accordance with velocity vector 
    #defining key behaviours here


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
            if 0 < distance < self.rad+50:  # Check for closeness
                # Vector pointing away from the nearby boid
                raw_dir_away = self.position - b.position
                scaled_dir_away = raw_dir_away / (distance ** 2)  # Inverse distance weighting
                steering.add(scaled_dir_away)
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



    def alignment(self, boids):
        """
        Aligns the boid's velocity with its neighbors.
        """
        total = 0
        steering = Vector()

        for b in boids:
            if b == self:
                continue
            distance = getDistance(self.position, b.position)
            if 0 < distance < self.rad+50:
                tmp = b.velocity.unitReturn()
                steering.add(tmp)  # Add neighbor's normalized velocity
                total += 1

        if total > 0:
            
            steering = steering / total
            steering.unitv()
            steering =  steering* self.max_speed
            steering -= self.velocity
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