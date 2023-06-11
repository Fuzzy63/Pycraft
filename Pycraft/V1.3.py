'''
I will not be adding an inventory system or crafting. It is a simple creative minecraft clone.
'''
'''TREE UPDATE'''
#Imports:
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController as cam
import random
import math
from ursina.prefabs.memory_counter import MemoryCounter
import pickle
from perlin_noise import PerlinNoise
from os.path import exists
import psutil
#Window and App:
app = Ursina()
window.borderless = False
window.exit_button.visible = False
window.fps_counter.visible = False
#Variables and Lists:
ram = 0
cpu = 0
voxel_list = []
PICK = 0
mouse_e = -1
command_e = -1
command = ''
music_time = 0
debug = -1
shader_enable = -1
#audio:
track_1 = Audio(clip='assets/sweden',autoplay=False,loop=False)
track_2 = Audio(clip='assets/blue_oceans',autoplay=False,loop=False)
track_3 = Audio(clip='assets/dark_sands',autoplay=False,loop=False)
#Classes:



#hotbar slots
grass_h = Text(model='quad',scale=(.1),position=(-.4,-.45),texture='assets/grass')
dirt_h = Text(model='quad',scale=(.1),position=(-.3,-.45),texture='assets/dirt')
stone_h = Text(model='quad',scale=(.1),position=(-.2,-.45),texture='assets/cobblestone')
brick_h = Text(model='quad',scale=(.1),position=(-.1,-.45),texture='assets/brick')
glass_h = Text(model='quad',scale=(.1),position=(0,-.45),texture='assets/glass')
wood_h = Text(model='quad',scale=(.1),position=(.1,-.45),texture='assets/wood')
sand_h = Text(model='quad',scale=(.1),position=(.2,-.45),texture='assets/sand')
log_h = Text(model='quad',scale=(.1),position=(.3,-.45),texture='assets/log')
leaves_h = Text(model='quad',scale=(.1),position=(.4,-.45),texture='assets/leaves')
vc = Text(color=color.white,scale=(1),position=(0,.4),visible = False)
pc = Text(color=color.white,scale=(1),position=(0,.45),visible = False)
muc = Text(color=color.white,scale=(1),position=(0,.35),visible = False)
se = Text(color=color.white,scale=(1),position=(0,.30),visible = False)
mem = Text(color=color.white,scale=(1),position=(.35,.45),visible = False)
cp = Text(color=color.white,scale=(1),position=(.35,.4),visible = False)
class Hand(Entity):
    def __init__(self):
        self.k = 0
        super().__init__(parent=camera.ui,
                         model='cube',
                         scale=(.3),
                         position=(.5,-.3,1),
                         texture='white_cube',rotation=(-10,-10,0))
    def on(self):
        self.position=(.4,-.2,1.4)
    def off(self):
        self.position=(.5,-.3,1)
    def input(self,key):
        if key == 'left mouse down' or key == 'right mouse down':
            self.on()
        else:
            self.off()
    def update(self):
        global PICK
        self.k=PICK
        if self.k == 0:
            self.texture='assets/grass'
        elif self.k == 1:
            self.texture='assets/dirt'
        elif self.k == 2:
            self.texture='assets/cobblestone'
        elif self.k == 3:
            self.texture='assets/brick'
        elif self.k == 4:
            self.texture='assets/glass'
        elif self.k == 5:
            self.texture='assets/wood'
        elif self.k == 6:
            self.texture='assets/sand'
        elif self.k == 7:
            self.texture='assets/log'
        elif self.k == 8:
            self.texture='assets/leaves'
        else:
            self.color=color.violet
hand = Hand()
class Voxel(Button):
    def __init__(self,position=(0,0,0),k=0):
        self.k = k
        self.sd = 0
        super().__init__(parent=scene,
                         model='cube',
                         scale=(1),
                         color=color.white,
                         texture='white_cube',
                         collider='box',
                         position=position,
                         shader=None)
    def update(self):
        global shader_enable
        if shader_enable == 1:
            self.sd = distance(self,player)*8
            self.color=color.rgb(self.sd,self.sd,self.sd)
            self.color=color.inverse(self.color)
        else:
            self.color=color.rgb(255,255,255)
    def input(self,key):
        global PICK
        if key == 'right mouse down' and self.hovered == True and distance(self,player)<5:
            if PICK == 0:
                voxel = Voxel(position=self.position+mouse.normal,k=0)
            if PICK == 1:
                voxel = Voxel(position=self.position+mouse.normal,k=1)
            if PICK == 2:
                voxel = Voxel(position=self.position+mouse.normal,k=2)
            if PICK == 3:
                voxel = Voxel(position=self.position+mouse.normal,k=3)
            if PICK == 4:
                voxel = Voxel(position=self.position+mouse.normal,k=4)
            if PICK == 5:
                voxel = Voxel(position=self.position+mouse.normal,k=5)
            if PICK == 6:
                voxel = Voxel(position=self.position+mouse.normal,k=6)
            if PICK == 7:
                voxel = Voxel(position=self.position+mouse.normal,k=7)
            if PICK == 8:
                voxel = Voxel(position=self.position+mouse.normal,k=8)
            voxel.setup()
        if key == 'left mouse down' and self.hovered == True and distance(self,player)<5:
            del_voxel(self.x,self.y,self.z,self.k)
            self.shake(duration=(.5))
            destroy(self)
        
    def end(self):
        
        destroy(self)
    def setup(self):
        add_voxel_to_save(self.x,self.y,self.z,self.k)
        if self.k == 0:
            self.texture='assets/grass'
        elif self.k == 1:
            self.texture='assets/dirt'
        elif self.k == 2:
            self.texture='assets/cobblestone'
        elif self.k == 3:
            self.texture='assets/brick'
        elif self.k == 4:
            self.texture='assets/glass'
        elif self.k == 5:
            self.texture='assets/wood'
        elif self.k == 6:
            self.texture='assets/sand'
        elif self.k == 7:
            self.texture='assets/log'
        elif self.k == 8:
            self.texture='assets/leaves'
        else:
            self.color=color.violet
#Functions:
def music_update():
    global music_time
    if music_time < 4000:
        music_time += 1
    if music_time > 3999:
        music_time = 0
        if random.randint(0,2):
            track_1.play()
        elif random.randint(0,2):
            track_2.play()
        else:
            track_3.play()
    
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
    noise = PerlinNoise(octaves=2,seed=random.randint(0,100))
    amp = 4
    freq = 24
    ty = 0
    for x in range(-8,8):
        for z in range(-8,8):
            y = floor((noise([x/freq,z/freq]))*amp)
            voxel = Voxel(position=(x,y,z),k=0)
            voxel.setup()
            ty = y
            tx = 0
            tz = 0
            if random.randint(0,100)==0:
                for i in range(4):
                    voxel = Voxel(position=(x,i+(y+1),z),k=7)
                    voxel.setup()
                voxel = Voxel(position=(x,y+5,z),k=8)
                voxel.setup()
                tx = voxel.x
                tz = voxel.z
                xx=0
                zz=0
                rad = 0
                radius = 1.3
                angle = 0
                while True:
                    rad = angle*(3.14/180)
                    #print('X',round(tx),'Z',round(tz))
                    angle += 40
                    xx = 0 + radius * math.cos(rad)
                    zz = 0 + radius * math.sin(rad)
                    if angle > 360:
                        break
                    voxel=Voxel(position=(round(xx)+tx,y+4,round(zz)+tz),k=8)
                    voxel.setup()
                    
                
                
                

        
            
def load():
    global voxel_list
    tx = 0
    ty = 0
    tz = 0
    tk = 0
    with open('save.pysave','rb') as fp:
        temp_list = pickle.load(fp)
    fp.close()
    rep = len(temp_list)/4
    for i in range(int(rep)):
        tx = temp_list.pop(0)
        ty = temp_list.pop(0)
        tz = temp_list.pop(0)
        tk = temp_list.pop(0)
        voxel = Voxel(position=(tx,ty,tz),k=tk)
        voxel.setup()
        
def save():
    global voxel_list
    temp_list = voxel_list
    print('Saving...')
    with open('save.pysave','wb') as fp:
        pickle.dump(voxel_list,fp)
    fp.close()    
    print('Saved')
    voxel_list = temp_list
    
def update():
    global music_time
    if player.y < -15:
        respawn(0,2,0)
    music_update()
    pc.text = player.position
    vc.text = 'Voxels: '+str(len(voxel_list)/4)
    muc.text = 'Music Counter '+str(music_time)
    check_system()
def input(key):
    global PICK,mouse_e,debug,shader_enable
    if key == 'p':
        save()
    if key == '1':
        PICK = 0
    if key == '2':
        PICK = 1
    if key == '3':
        PICK = 2
    if key == '4':
        PICK = 3
    if key == '5':
        PICK = 4
    if key == '6':
        PICK = 5
    if key == '7':
        PICK = 6
    if key == '8':
        PICK = 7
    if key == '9':
        PICK = 8
    if key == 'm':
        mouse_e *= -1
        if mouse_e == 1:
            mouse.locked = False
        else:
            mouse.locked = True
    if key == 'y':
        debug *= -1
        if debug == 1:
            mc.enabled = True
            window.fps_counter.visible = True
            pc.visible = True
            vc.visible = True
            muc.visible = True
            se.visible = True
            mem.visible = True
            cp.visible = True
            
        else:
            mc.enabled = False
            window.fps_counter.visible = False
            pc.visible = False
            vc.visible = False
            muc.visible = False
            se.visible = False
            mem.visible = False
            cp.visible = False
            
    if held_keys['control'] and key == 'r':
        reload_shaders()
    if key == 'r':
        shader_enable *= -1
        if shader_enable == 1:
            se.text = 'Shaders Enabled'
        else:
            se.text = 'Shaders Disabled'
def respawn(x,y,z):
    player.position=(x,y,z)

def check_save():
    file_exists = exists('save.pysave')
    if file_exists == True:
        load()
    else:
        new_terrain()
def check_system():
    global cpu,ram
    ram = (psutil.virtual_memory().used)/1048576
    mem.text = 'RAM in use (MB): '+str(round(ram))
    cpu = psutil.cpu_percent(interval=False, percpu=False)
    cp.text = 'CPU Usage :'+'%'+str(cpu)
    
check_save()
Sky(texture='sky_sunset')
player = cam()
respawn(0,2,0)
mc = MemoryCounter(enabled=False)


app.run()
