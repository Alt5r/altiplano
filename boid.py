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
        print(self.velocity.parseToInt())
        self.position += self.velocity
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

        self.acceleration.unitv()
        self.acceleration *= self.max_speed
        
        self.acceleration -= self.velocity

        self.velocity += self.acceleration # this changing direction 

        self.position += self.velocity #this is changing its position in accordance with velocity vector 
    #defining key behaviours here


    def seperation(self, boids):
        """
        creates a cumulative steering vector based of distances and inverse directions of neighbors and then determines a total vector for steering 
        away from neighbors at a optimal direction
        """

        #sepeariotion is also assumign 360 degree vision

        #total is the amount of boids we need to move away from as they are "too close"
        total = 0 
        #steering is the overall direction that we need to move in to move away from as many of the close boids as possible
        steering = Vector()

        #iterating through the entire flock of boids
        for b in boids:
            distance = getDistance(self.position, b.position)
            if distance < self.rad:
                #determinign a flockmate is too close, and direction to move away from it

                #hopefully how to get from self to b, therefore using direction as acceleration on a should move away from b
                raw_dir_away = SubVectors(b,self.position)
                #scale magnitude of vector to move by making it bigger if the flockmate is closer, i.e higher priority on moving away from closer neighbors
                scaled_dir_away = raw_dir_away/(distance**2)
                #adding the scaled vector to total steering direction
                steering.add(scaled_dir_away)
                #increasing total amount of moves by 1
                total += 1

        
        # checkign for phygame edge of screen HEIGHT
        coords_tuple = self.position.parseToInt()
        if  coords_tuple[1] - (self.rad+15) == 0:
            # + 15 here is "vision" for where the border is rather than it touchign it and possible going 
            #over if too close and many boids surrounding it 

            edge_coords = Vector(coords_tuple[0], 0)
            raw_dir_away = SubVectors(edge_coords,self.position)
            #scale magnitude of vector to move by making it bigger if the flockmate is closer, i.e higher priority on moving away from closer neighbors
            scaled_dir_away = raw_dir_away/(distance**2)
            #adding the scaled vector to total steering direction
            steering.add(scaled_dir_away)
            #increasing total amount of moves by 1
            total += 1

        

        if coords_tuple[1] + (self.rad+15) == self.h:
            #the above will have added movments scaled by importance to the steering vector, 
            edge_coords = Vector(coords_tuple[0], self.h)
            raw_dir_away = SubVectors(edge_coords,self.position)
            #scale magnitude of vector to move by making it bigger if the flockmate is closer, i.e higher priority on moving away from closer neighbors
            scaled_dir_away = raw_dir_away/(distance**2)
            #adding the scaled vector to total steering direction
            steering.add(scaled_dir_away)
            #increasing total amount of moves by 1
            total += 1

        ################################################# width
        if  coords_tuple[0] - (self.rad+15) == 0:
            # + 15 here is "vision" for where the border is rather than it touchign it and possible going 
            #over if too close and many boids surrounding it 

            edge_coords = Vector(0, coords_tuple[1])
            raw_dir_away = SubVectors(edge_coords,self.position)
            #scale magnitude of vector to move by making it bigger if the flockmate is closer, i.e higher priority on moving away from closer neighbors
            scaled_dir_away = raw_dir_away/(distance**2)
            #adding the scaled vector to total steering direction
            steering.add(scaled_dir_away)
            #increasing total amount of moves by 1
            total += 1

        if  coords_tuple[0] + (self.rad+15) == self.w:
                    # + 15 here is "vision" for where the border is rather than it touchign it and possible going 
                    #over if too close and many boids surrounding it 

                    edge_coords = Vector(self.w, coords_tuple[1])
                    raw_dir_away = SubVectors(edge_coords,self.position)
                    #scale magnitude of vector to move by making it bigger if the flockmate is closer, i.e higher priority on moving away from closer neighbors
                    scaled_dir_away = raw_dir_away/(distance**2)
                    #adding the scaled vector to total steering direction
                    steering.add(scaled_dir_away)
                    #increasing total amount of moves by 1
                    total += 1


        if total > 0:
            steering = steering / total
            #avrg vector to steer away from all
            steering.unitv()
            steering = steering * self.max_speed
            steering = steering - self.velocity
            #steering.limit(self.max_length)

        return steering


    def alignment(self, boids):
        """
        try to align boid most heavily with nearest neighbor 
        """
        #same logic as seperation in distance and movement 
        total = 0

        steering = Vector()

        for b in boids:
            distance = getDistance(self.position, b.position)
            if distance < self.rad:
                #heading
                
                b_heading = b.velocity.Unitv()

                #importance of heading based of neighbor distance
                scaled_b = b_heading/(distance**2)
                steering += scaled_b
                total += 1
        if total > 0:
            return (steering/total).Unitv()
        else:
            return Vector()

    
    def cohesion(self, boids) -> Vector:
        """
        the desire to stay near other flockmates
        """

        total = 0
        steering = Vector()

        for b in boids:
            distance = getDistance(self.position, b.position)
            if distance < self.rad:
                steering.add(b.position)
                total+=1
            
        if total > 0:
            avg = steering/total
            #how to get there
            temp = avg - self.position 
            #unit vector of direction to move to get to average coordinates of all boids
            temp.unitv()

            temp *= self.max_speed
            temp -= self.velocity
            #print(f"{temp} is maybe none")
            return temp
        return Vector()


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