# Eric Blau
# Final Project

from visual import *
import math
import random

class Player:
    """ a collection of VPython parts that
        will move together == a robot!
    """

    # make x, y, z axes with labels
    
    def __init__(self, pos, heading=vector(0,0,1)):
        """ constructor for our player class """
        # list of vPython 3D shapes that make up this player
        self.parts = []
        
        self.pos = vector(pos)
        # Direction in which robot is moving, normalized to unit length
        self.heading = norm(heading)

        self.radius = 1.0

        self.velocity = vector(0,0,0)

        face = cylinder(pos=self.pos, axis = (0,1.5,0), radius=.75,
                           color=color.white,  material = materials.chrome)
        self.parts += [face] 

        self.head = sphere(pos=self.pos, radius = .75, color = color.white,  material = materials.chrome)
        self.parts += [self.head]

        
        left_eye = sphere(pos=self.pos+vector(.35,.4,.6), 
                          radius=0.36, color=color.blue, material = materials.emissive)
        self.parts += [left_eye]
        right_eye = sphere(pos=self.pos+vector(-.35,.4,.6),
                           radius=0.36, color=color.blue, material = materials.emissive)
        self.parts += [right_eye]

        neck = cylinder(pos=self.pos+vector(0,-1,0), axis = (0,.5,0), radius = .05, color=color.white)
        self.parts += [neck]

        self.body = cylinder(pos=self.pos+vector(0,-1.75,0),axis = (0,.75,-.2), radius = .35, color=color.white, material = materials.chrome)
        self.parts += [self.body]

        bottom = sphere(pos=self.pos+vector(0,-1.75,0), radius =.35, color = color.white, material = materials.chrome)
        self.parts += [bottom]

        right_shoulder = sphere(pos = self.pos+vector(-.35,-1,0), radius = .20, color = color.blue,  material = materials.chrome)
        self.parts += [right_shoulder]

        left_shoulder = sphere(pos= self.pos+vector(.35,-1,0), radius = .20, color = color.blue,  material = materials.chrome)
        self.parts += [left_shoulder]

        right_arm = cone(pos = self.pos+vector(-.36, -1.1, 0), axis = (-.2, -.7, -.4), radius = .12, color = color.white,  material = materials.chrome)
        self.parts += [right_arm]

        left_arm = cone(pos = self.pos+vector(.36, -1.1, 0), axis = (.2, -.7, -.4), radius = .12, color = color.white,  material = materials.chrome)
        self.parts += [left_arm]

        right_leg = cone(pos = self.pos+vector(-.32, -2.85, 0), axis = (.1, .8, .1), radius = .2, color = color.white,  material = materials.chrome)
        self.parts += [right_leg]

        left_leg = cone(pos = self.pos+vector(.32,-2.15,.8), axis = (-.1, .1, -.8), radius = .2, color = color.white,  material = materials.chrome)
        self.parts += [left_leg]    


    def __repr__(self):
        """ prints the pieces, position, and heading of self """
        s = "  position:" + str(self.pos) + "\n"
        s += "  heading: " + str(self.heading) + "\n"
        return s

    def forward(self, amount):
        ''' Change robot's location by moving in 
            the heading direction by a given amount '''
        motion_vector = amount * self.heading
        self.pos += motion_vector
        self.velocity = motion_vector
        for part in self.parts:
            part.pos += motion_vector

    def strafe(self, amount):
        ''' move the robot left or right without changing its heading'''
        strafe_direction = rotate(self.heading, angle=math.pi/2.0, axis = (0,1,0))
        motion_vector = amount * strafe_direction
        self.pos += motion_vector
        self.velocity = motion_vector
        for part in self.parts:
            part.pos += motion_vector

    def up(self, amount):
        '''move up by a given amount'''
        motion_vector = amount * vector(0,1,0)
        self.pos += motion_vector
        self.velocity = movion_vector
        for part in self.parts:
            part.pos += motion_vector

    def turn(self, angle):
        ''' Turn the robot by the given angle, in degrees '''
        # convert the angle to radians first
        theta = math.radians(angle)
        # rotate the heading vector around the vertical y-axis
        self.heading = rotate(self.heading, angle=theta, axis=(0,1,0))
        # rotate all of the parts around the current position
        for part in self.parts:
            part.rotate(angle=theta, axis=(0,1,0), origin=self.pos)

def chain_reaction( b1, b2):
    """ chain_reaction checks to see if an exploding bomb is within reach
        of another bomb; if so, both bombs become exploding bombs
    """
    if b1.color == color.red or b2.color == color.red:
        if mag(b1.pos-b2.pos) < b1.radius + b2.radius:
            return True

    return False
        
def collide(b1,b2):
    """checks if two balls collide"""
    if mag(b1.pos-b2.pos) < (b1.radius + b2.radius - .05):
        return True

def divideList(L):
    """ divides a list by 100.0"""
    for x in range(len(L)):
        L[x] = L[x]/100.0
    return L

def main():
    scene.autoscale = True
    scene.background = color.cyan
    scene.title = "BomberPool!"
    dead = False

    score = 0
    
    ground = box(pos = vector(0,0,0), length = 100.0, height = 0.25, width = 100.0, color=color.green)
    wall1 = box(pos = (0,0,50), length = 100.0, height = 3, width = 0.2, color = color.red)
    wall2 = box(pos = (50,0,0), length = 0.2, height = 3, width =100, color=color.red)
    wall3 = box(pos = (-50,0, 0), length = 0.2, height = 3, width = 100, color = color.red)
    wall4 = box(pos = (0, 0, -50), length = 100, height = 3, width = 0.2, color = color.red)
    player = Player(pos = (0,3,0))

    sphere(pos = (0,0,50))
    sphere(pos = (50,0,0))
    sphere(pos = (-50,0,0))
    sphere(pos = (0,0,-50))

# Bonus points
    Bonus = []
    T = 0 # Timer for Nice! +1000 sign

# the enemy ball!
    eBALLS = []
    enemyBall = sphere(pos = (5, 3, 5), radius = 3, color = color.black)
    eBALLS += [enemyBall]
    
# frequency of shooting
    chanceOfShooting = range(300)

# frequency of new enemyBalls being generated
    Location = range(-42, 42)
    chanceOfRegen = range(300)
    
# randomness of direction
    newDi = range(-100, 101)
    divideList(newDi)
    enemyBall.heading = vector(random.choice(newDi), 0, random.choice(newDi))

    L = []
    b1 = sphere(pos = (2,1.25,0), radius = 1, color = color.white)
    L += [b1]
    b2 = sphere(pos = (10,1.25,0), radius = 1, color = color.white)
    L += [b2]
    b3 = sphere(pos = (10.02+math.sqrt(3),1.25,1.05), radius = 1, color = color.white)
    L += [b3]
    b4 = sphere(pos = (10.02+math.sqrt(3),1.25,-1.05), radius = 1, color = color.white)
    L += [b4]

# Velocity
    b1.velocity = vector(2,0,0)
    for i in range(1, len(L)):
        L[i].velocity = vector(0,0,0)

# Set the explode to 'off'

    for i in range(len(L)):
        L[i].t = 250
        L[i].explode = 'off'

    dt = 0.05

    while True:
        Turn_Amount = 15
        Move_Amount = 1
        BMove_Amount = -1
        RTurn_Amount = -15

        rate(100)


# Difficulty level

        if score >= 20000:

            chanceOfShooting = range(250)
            chanceOfRegen = range(200)

        if score >= 40000:

            chanceOfShooting = range(200)
            chanceOfRegen = range(150)

        if score >= 60000:

            chanceOfShooting = range(100)
            chanceOfRegen = range(100)


# are new enemyBalls created...?

        if random.choice(chanceOfRegen) == 0:

            enemyBall = sphere(pos = (random.choice(Location), 1.25, random.choice(Location)),
                               radius = 3, color = color.black)
            eBALLS.append(enemyBall)

            
# enemyBall shoots at you!

        for e in range(len(eBALLS)):

            eBALLS[e].heading = vector(random.choice(newDi), 0, random.choice(newDi))

            if random.choice(chanceOfShooting) == 0:
                bomb = sphere(pos=(eBALLS[e].pos), radius = 1, color = color.black)
                bomb.pos.y = 1.25
                bomb.velocity = eBALLS[e].heading
                bomb.t = 250
                bomb.explode = 'off'
                L += [bomb]

        
# Did you die? GAME OVER scenario


        for i in range(len(L)):

            if collide(L[i], player) == True and L[i].color == color.red:

                text(text='GAME OVER', pos = vector(0, 10, 0), height = 10,
                     width = 10, align='center', depth=2, color=color.red)
                
                dead = True

        if dead:

            return score

        score += 1


# Bonus points sign

        T -= 1

        killListBonus = []

        if T == 0:

            for i in range(len(Bonus)):

                killListBonus.append(Bonus[i])

        while len(killListBonus) != 0:

            Bonus.remove(killListBonus[0])
            killListBonus[0].visible = False
            del killListBonus[0]

        

# Did the enemyBall die?

        killListEnemies = []

        for i in range(len(L)):

            for e in range(len(eBALLS)):

                if collide(L[i], eBALLS[e]) == True and L[i].color == color.red:

                    if eBALLS[e] not in killListEnemies:

                        killListEnemies.append(eBALLS[e])

                        Nice = text(text='Nice!\n+1000', pos = vector(0, 15, -60), height = 5,
                                    width = 5, align='center', depth=2, color=color.green)
                        T = 25 # Timer reset to 25
                        Bonus = [Nice]

        while len(killListEnemies) != 0:

            eBALLS.remove(killListEnemies[0])
            killListEnemies[0].visible = False
            del killListEnemies[0]

            score += 1000


# BOMBS! OMG

        killList = []

        for i in range(len(L)):

            if L[i].radius >= 3:
                killList.append(L[i])

        while len(killList) != 0:
            L.remove(killList[0])
            killList[0].visible = False
            del killList[0]

        for i in range(len(L)):

            if L[i].explode == 'on':

                L[i].color = color.red
                L[i].radius += .01


        for i in range(len(L)):

            for j in range(i+1, len(L)):

                if chain_reaction( L[i], L[j]) == True:

                    L[i].explode = 'on'
                    L[j].explode = 'on'


# Player Controls

        if scene.kb.keys:
            s = scene.kb.getkey()
            if s == "w":
                player.forward(Move_Amount)
            if s == "s":
                player.forward(BMove_Amount)
            if s == "a":
                player.turn(Turn_Amount)
            if s == "d":
                player.turn(RTurn_Amount)
            if s == "e":
                player.strafe(-Move_Amount)
            if s =="q":
                player.strafe(Move_Amount)
            if s == " ":
                bomb = sphere(pos=(player.pos+(player.heading*2)), radius = 1, color = color.black)
                bomb.pos.y = 1.25
                bomb.velocity = player.heading
                bomb.t = 250
                bomb.explode = 'off'
                L += [bomb]


# COLLISIONS!

        for i in range(len(L)):
            for j in range(i+1,len(L)):
                if collide(L[i],L[j]) == True:
                    n = L[i].pos-L[j].pos
                    un = n/n.mag
                    ut = (-un.z,0,un.x)
                    v1n=L[i].velocity.proj(un)
                    v1t=L[i].velocity.proj(ut)
                    v2n=L[j].velocity.proj(un)
                    v2t=L[j].velocity.proj(ut)
                    L[i].velocity = v2n + v1t
                    L[j].velocity = v1n + v2t
                   
                    L[i].pos = L[i].pos + (L[i].velocity*0.9)
                    L[j].pos = L[j].pos + (L[j].velocity*0.9)                   

                

            if collide (L[i], player) == True:
                n = L[i].pos-player.pos
                un = n/n.mag
                ut = (-un.z,0,un.x)
                v1n=L[i].velocity.proj(un)
                v1t=L[i].velocity.proj(ut)
                v2n=player.velocity.proj(un)
                v2t=player.velocity.proj(ut)
                L[i].velocity = v2n + v1t
                L[i].pos += L[i].velocity*dt
            if L[i].pos.z > wall1.pos.z:
                L[i].velocity.z = -L[i].velocity.z
            if L[i].pos.z < wall4.pos.z:
                L[i].velocity.z = -L[i].velocity.z
            if L[i].pos.x > wall2.pos.x:
                L[i].velocity.x = -L[i].velocity.x
            if L[i].pos.x < wall3.pos.x:
                L[i].velocity.x = -L[i].velocity.x
            
            L[i].pos = L[i].pos + L[i].velocity*dt                  

    # Check if any should be exploding

        for i in range(len(L)):

            if L[i].t != 0:
                L[i].t -= 1

            else:
                L[i].explode = 'on'


