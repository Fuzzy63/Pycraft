from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController as cam
import random
from ursina.prefabs.memory_counter import MemoryCounter
import pickle
from ursina.shaders import lit_with_shadows_shader
from perlin_noise import PerlinNoise 
app = Ursina()
window.borderless = False
window.exit_button.visible = False
MemoryCounter()
voxel_list = []
PICK = 0

#hotbar slots
grass_h = Text(model='quad',scale=(.1),position=(-.1,-.45),color=color.green,texture='white_cube')
dirt_h = Text(model='quad',scale=(.1),position=(0,-.45),color=color.rgb(155,118,83),texture='white_cube')
stone_h = Text(model='quad',scale=(.1),position=(.1,-.45),color=color.rgb(138,127,128),texture='white_cube')
#0 is grass
#1 is dirt
#2 is stone
class Voxel(Button):
    def __init__(self,position=(0,0,0),k=0):
        self.k = k
        super().__init__(parent=scene,
                         model='cube',
                         scale=(1),
                         color=color.white,
                         texture='white_cube',
                         collider='box',
                         position=position)
    def input(self,key):
        global PICK
        if key == 'right mouse down' and self.hovered == True and distance(self,player)<5:
            if PICK == 0:
                voxel = Voxel(position=self.position+mouse.normal,k=0)
            if PICK == 1:
                voxel = Voxel(position=self.position+mouse.normal,k=1)
            if PICK == 2:
                voxel = Voxel(position=self.position+mouse.normal,k=2)
            voxel.setup()
        if key == 'left mouse down' and self.hovered == True and distance(self,player)<5:
            del_voxel(self.x,self.y,self.z,self.k)
            self.shake(duration=(.5))
            destroy(self)
    def setup(self):
        add_voxel_to_save(self.x,self.y,self.z,self.k)
        if self.k == 0:
            self.color=color.green
        elif self.k == 1:
            self.color=color.rgb(155,118,83)
        elif self.k == 2:
            self.color=color.rgb(138,127,128)
        else:
            self.color=color.violet
def add_voxel_to_save(x,y,z,k):
    voxel_list.append(x)
    voxel_list.append(y)
    voxel_list.append(z)
    voxel_list.append(k)
def del_voxel(x,y,z,k):
    global voxel_list
    temp = 0
    tx = 0
    ty = 0
    tz = 0
    tk = 0
    while True:
        tx = voxel_list.pop(0)
        ty = voxel_list.pop(0)
        tz = voxel_list.pop(0)
        tk = voxel_list.pop(0)
        if tx == x and ty == y and tz == z and tk == k:
            #print('Found voxel')
            break
        else:
            voxel_list.append(tx)
            voxel_list.append(ty)
            voxel_list.append(tz)
            voxel_list.append(tk)
def new_terrain():
    for x in range(-8,8):
        for z in range(-8,8):
            voxel = Voxel(position=(x,0,z),k=0)
            voxel.setup()
            
def load():
    global voxel_list
    tx = 0
    ty = 0
    tz = 0
    tk = 0
    with open('save','rb') as fp:
        temp_list = pickle.load(fp)
    rep = len(temp_list)/4
    for i in range(int(rep)):
        tx = temp_list.pop(0)
        ty = temp_list.pop(0)
        tz = temp_list.pop(0)
        tk = temp_list.pop(0)
        voxel = Voxel(position=(tx,ty,tz),k=tk)
        voxel.setup()
def save():
    print('Saving...')
    with open('save','wb') as fp:
        pickle.dump(voxel_list,fp)
    fp.close()    
    print('Saved')
def update():
    if player.y < -15:
        respawn(0,2,0)
        
def input(key):
    global PICK
    if key == 'p':
        save()
    if key == '1':
        PICK = 0
    if key == '2':
        PICK = 1
    if key == '3':
        PICK = 2
def respawn(x,y,z):
    player.position=(x,y,z)
#new_terrain()
load()
Sky()
player = cam()
respawn(0,2,0)
app.run()
