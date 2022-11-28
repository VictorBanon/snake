import random as r
import numpy as np

class snake:
    def __init__(self,size=3,x_origine=5,y_origine=5 ,coordinates_x=None,coordinates_y=None):
        self.name = "snake"
        self.size      = size
        self.x_origine = x_origine
        self.y_origine = y_origine 

        if coordinates_x is None:
            self.coordinates_x=np.linspace(x_origine, x_origine            , self.size, dtype=int)
            print(self.coordinates_x)
        else: self.coordinates_x=coordinates_x

        if coordinates_y is None:
            self.coordinates_y=np.linspace(y_origine, y_origine-self.size+1, self.size, dtype=int)
        else: self.coordinates_y=coordinates_y
        
    def eat(self,value,coordinates_x,coordinates_y):
        # No funca
        self.size=self.size+value
        #coordinates
        self.coordinates_x=np.concatenate((np.array([coordinates_x]),self.coordinates_x[:]))
        self.coordinates_y=np.concatenate((np.array([coordinates_y]),self.coordinates_y[:]))

    def move(self,direction,step=1):
        if direction=='x': 
            self.x_origine     = self.x_origine+step
            self.coordinates_x = np.concatenate((self.coordinates_x[0:1]+step,self.coordinates_x[:-1]))
            self.coordinates_y = np.concatenate((self.coordinates_y[0:1]     ,self.coordinates_y[:-1]))
        if direction=='y': 
            self.y_origine     = self.y_origine+step
            self.coordinates_x = np.concatenate((self.coordinates_x[0:1]     ,self.coordinates_x[:-1]))
            self.coordinates_y = np.concatenate((self.coordinates_y[0:1]+step,self.coordinates_y[:-1]))
        #coordinates
        # Nota funciona solo si step=1

class cookies:
    def __init__(self,x,y):
        self.name = "cookie"
        self.size = 1
        self.x    = x
        self.y    = y 

class snakeGame:
    def __init__(self):
        self.x_size=10
        self.y_size=10

        self.time   =0

        self.board = np.zeros( (self.x_size+2, self.y_size+2) )
        self.snake=snake()
        self.game  = True # False implica fin del juego
        
        self.list_cookies={}

        for i in range(20):
            self.add_cookies()
        self.updateMap()

    def updateMap(self):
        self.board = np.zeros( (self.x_size+2, self.y_size+2) )
        # PONEMOS LOS MUROS
        for i in range(self.x_size+2):
            for j in range(self.y_size+2):
                if (i==0)+(j==0)+(i==self.x_size+1)+(j==self.y_size+1):
                    self.board[i,j]=3

        # PONEMOS La serpiente
        for i in range(self.snake.size):
            self.board[self.snake.coordinates_x[i],self.snake.coordinates_y[i]]=2

        #añadirlo en el mapa
        for x in self.list_cookies.keys():
            for y in self.list_cookies[x].keys():
                self.board[x][y]=1


        

    def add_cookies(self):

        x=r.randint(1, self.x_size)
        y=r.randint(1, self.x_size)

        value=cookies(x,y)

        if self.list_cookies.__contains__(x):
            self.list_cookies[x][y] = value
        else:
            self.list_cookies[x]    = {y:value} 



    def print(self):
        print("Estado de la serpiente al momento:",self.time)
        self.updateMap()
        for i in range(self.x_size+2):
            for j in range(self.y_size+2):
                if self.board[i,j]==0:
                    # Espacio Vacio
                    print(" ",end="")
                if self.board[i,j]==1:
                    # banzana
                    print("x",end="") 
                if self.board[i,j]==2:
                    # Serpiente
                    print("o",end="") 
                if self.board[i,j]==3:
                    # Muro
                    print("#",end="") 
                print("|",end="") 
            print("")
            #print("_"*(self.x_size+2))

    def launch(self):
        while self.game:
            self.timeStep()
            self.print()

    def timeStep(self):
        self.time = self.time+1

        direcion  = r.choice([ 0,1])
        sentido   = r.choice([-1,1]) 

        flag=False

        new_x = self.snake.x_origine+(1-direcion)*sentido 
        new_y = self.snake.y_origine+(direcion  )*sentido

        if self.list_cookies.__contains__(new_x):
            if self.list_cookies[new_x].__contains__(new_y):
                flag=True

        # Si no, se come una mierda
        if flag:
            self.snake.eat(1,new_x,new_y)
            del self.list_cookies[new_x][new_y]
            print("se la comio:",self.snake.size)
        # Si hay comida, se la come
        else:
            if direcion==0:
                self.snake.move('x',sentido)
            else:
                self.snake.move('y',sentido)
        
        

    def stopGame(self):
        self.game=False
        print("END GAME")

if __name__ == '__main__':
    snakeGame().launch()

