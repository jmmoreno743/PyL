#!/usr/bin/python

import xml.dom.minidom
import pprint


POSITION_SCALE_W = 16
POSITION_SCALE_H = 8
DEFAULT_CAMERA_ALTITUDE = 12 
FRAME_STEP = 2
NUM_POINTS_CURVE = 5
NUM_FRAMES_ANIMATION = 99

import os

#MODELS_PATH = os.getenv('MODELS_PATH')
MODELS_PATH = '/home/david/PyL'
RENDER_LOW_QUALITY = "True"
RENDER_VIDEO = os.getenv('RENDER_VIDEO') == "True"
SCRIPT_XML_FILENAME = MODELS_PATH + '/script002.xml'
SCORE_XML_FILENAME = MODELS_PATH + '/score.xml'

# Cargar el archivo XML a memoria, en una estructura mas facilmente entendible
# {

from time import gmtime, strftime

print ('################################################################################')
print ('Launchin at:')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

doc = xml.dom.minidom.parse(SCRIPT_XML_FILENAME)

print ('Creatin dictionary at:')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

actors = {}

for xmlActor in doc.getElementsByTagName('actor'):
    a = {}

    # Asigno los valores de los atributos de este elemento
    for attr_key in xmlActor.attributes.keys():
        a[attr_key] = xmlActor.getAttribute(attr_key)

    #Asigno el valor de la posicion del elemento
    for xmlPosition in xmlActor.getElementsByTagName('position'):
        a['position'] = ( float(xmlPosition.getAttribute('x')) * POSITION_SCALE_W , -float(xmlPosition.getAttribute('z')) * POSITION_SCALE_H, 0 )

    # Asigno la trayectoria que tiene este elemento
    a['trajectory'] = []
    for xmlPoint in xmlActor.getElementsByTagName('point'):
        a['trajectory'].append( ( float(xmlPoint.getAttribute('x')) * POSITION_SCALE_W , -float(xmlPoint.getAttribute('z')) * POSITION_SCALE_H , 0 ) )

    # Por ultimo agrego este elemento a la lista de actores de la composicion, pero me cuido de no sobreescribir otro actor que tenga el mismo nombre
    currIndex = 0
    assetName = a['asset']
    while assetName in actors: # Seria mas bonito con un do..while , pero Python no lo tiene
        assetName = "%s_%d" % ( a['asset'] , currIndex )
        currIndex += 1
    a['asset'] = assetName
    actors[assetName] = a

# }

# Invocar al API de Blender para crear los actores y acomodar todos los elementos en la escena
# {

print ('Cleanin at:')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

import bpy
import mathutils

# Borrar todo lo que haya en la escena:
#bpy.ops.object.mode_set(mode = 'OBJECT') 
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

#bpy.ops.object.mode_set(mode = 'EDIT') 
#bpy.ops.mesh.select_all(action='SELECT')
#bpy.ops.mesh.delete()

for tmp_curve in bpy.data.curves:
    bpy.data.curves.remove(tmp_curve)

#bpy.ops.curve.select_all(action='SELECT')
#bpy.ops.curve.delete()

for tmp_mesh in bpy.data.meshes:
    bpy.data.meshes.remove(tmp_mesh)

print ('Creatin objects from models at:')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

# Para el calculo del BoundingBox de la escena mas abajo
bb_min = None
bb_max = None

# bpy.ops.sequencer.sound_strip_add(filepath='/Users/barcodepandora/Sites/VideoGenerator/sound/jazz.mp3', frame_start=1, channel=1)

# Crear los objetos en las posiciones que nos hayan dicho en el XML
for actor in actors.keys():
    if actors[actor]['asset'] == 'SBCamera':
        continue
    
    if actor.startswith("elven") or actor.startswith("casa"):
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius=0.3, depth=1, cap_end=True)
    elif actor.startswith("medieval"):
        #bpy.ops.mesh.primitive_cube_add()
        bpy.ops.mesh.primitive_monkey_add()
        bpy.context.object.scale = (0.3, 0.3, 0.3)
    elif actor.startswith("dessert") or actor.startswith("carro"):
        bpy.ops.wm.link_append(directory=MODELS_PATH + "/desertTruck.blend/Object/", filename="DragonMO", link=False)
        bpy.context.scene.objects.active = bpy.data.objects['Dragon']
        bpy.context.object.scale = (0.3,0.3,0.3)
    elif actor.startswith("robot") or actor.startswith("hombre") :
        bpy.ops.import_scene.autodesk_3ds(filepath=MODELS_PATH + "/robot.3ds")
        bpy.context.scene.objects.active = bpy.data.objects['Dexter']
        bpy.context.object.scale = (0.01,0.01,0.01)
    elif actor.startswith("ninja") or actor.startswith("mujer"):
        bpy.ops.wm.link_append(directory=MODELS_PATH + "/sackboy.blend/Object/", filename="SackboyMO", link=False)
        bpy.context.scene.objects.active = bpy.data.objects['Sackboy']
        bpy.context.object.scale = (0.3, 0.3, 0.3)
    elif actor.startswith("Conejo"):
        bpy.ops.wm.link_append(directory=MODELS_PATH + "/models/rabbit.blend/Object/", filename="rabbit", link=False)
        bpy.context.scene.objects.active = bpy.data.objects['rabbit']
        bpy.context.object.scale = (0.6,0.6,0.6)
    elif actor.startswith("Ardilla"):
        bpy.ops.wm.link_append(directory=MODELS_PATH + "/models/squirrel.blend/Object/", filename="squirrel", link=False)
        bpy.context.scene.objects.active = bpy.data.objects['squirrel']
        bpy.context.object.scale = (1.2,1.2,1.2)
    elif actor.startswith("Chinchilla"):
        bpy.ops.wm.link_append(directory=MODELS_PATH + "/models/chinchilla.blend/Object/", filename="chinchilla", link=False)
        bpy.context.scene.objects.active = bpy.data.objects['chinchilla']
        bpy.context.object.scale = (1.1,1.1,1.1)
    elif actor.startswith("Mariposa"):
        bpy.ops.wm.link_append(directory=MODELS_PATH + "/models/butterfly.blend/Object/", filename="butterfly_body", link=False)
        bpy.context.scene.objects.active = bpy.data.objects['butterfly_body']
        bpy.context.object.scale = (4,4,4)
    elif actor.startswith("Pajaro"):
        bpy.ops.wm.link_append(directory=MODELS_PATH + "/models/bird.blend/Object/", filename="Bird", link=False)
        bpy.context.scene.objects.active = bpy.data.objects['Bird']
        bpy.context.object.scale = (0.09,0.09,0.09)
    elif actor.startswith("Manzana"):
        bpy.ops.wm.link_append(directory=MODELS_PATH + "/models/apple.blend/Object/", filename="apple1", link=False)
        bpy.context.scene.objects.active = bpy.data.objects['apple1']
        bpy.context.object.scale = (2,2,2)
    else:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.3)
        
    ob = bpy.context.object
    ob.name = actors[actor]['asset']
    ob.location = actors[actor]['position']
    
    # Voy calculando donde debe quedar la camara (en caso de que no me digan donde de manera explicita) con base en la posicion de cada elemento de la escena:
    # La camara debe estar por sobre el centro del BoundingBox que contiene a todos los elementos, y mirando
    # hacia abajo
    if bb_min is None:
        bb_min = mathutils.Vector(ob.location)
    else:
        bb_min[0] = min( bb_min[0] , ob.location[0] )
        bb_min[1] = min( bb_min[1] , ob.location[1] )
        bb_min[2] = min( bb_min[2] , ob.location[2] )
        
    if bb_max is None:
        bb_max = mathutils.Vector(ob.location)
    else: 
        bb_max[0] = max( bb_max[0] , ob.location[0] )
        bb_max[1] = max( bb_max[1] , ob.location[1] )
        bb_max[2] = max( bb_max[2] , ob.location[2] )
    
print ('Creatin camera at:')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

# Crear la camara y moverla al lugar donde debe quedar (en caso de que nos hayan dado esta informacion para la camara)
bpy.ops.object.camera_add()
camera = bpy.context.object
bpy.ops.object.lamp_add()
lamp = bpy.context.object
#if 'SBCamera' in actors:
#    camera.location = actors['SBCamera']['position']
#    lamp.location = actors['SBCamera']['position']
#else:
camera.location =  ( bb_max + bb_min ) / 2
camera.location[2] = DEFAULT_CAMERA_ALTITUDE
lamp.location = mathutils.Vector(camera.location)
lamp.location[2] = DEFAULT_CAMERA_ALTITUDE / 2

print ('Creatin plane at:')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

# Crear el piso
bpy.ops.mesh.primitive_plane_add()
ground_plane = bpy.context.object
ground_mat = bpy.data.materials.new(name="GroundMat")
ground_plane.active_material = ground_mat
ground_tex = bpy.data.textures.new(name ="GroundTex", type='CLOUDS')
ground_tex_slot = ground_mat.texture_slots.add()
ground_tex_slot.texture = ground_tex

ground_plane.scale = ( bb_max[0] - bb_min[0] , bb_max[1] - bb_min[1] , 1)
ground_plane.location = camera.location
ground_plane.location[2] = 0

ground_mat.diffuse_color = (0,1,0)
ground_mat.diffuse_intensity = 0.5

ground_tex_slot.color = (1,1,1)

# }

print ('Drawing at:')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

# Realizar animaciones
# {

bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = NUM_FRAMES_ANIMATION

score = xml.dom.minidom.parse(SCORE_XML_FILENAME)

# Crear el sonido de ambiente
#for xmlScore in score.getElementsByTagName('score'):
#	for xmlAmbient in xmlScore.getElementsByTagName('scene'):
#		bpy.ops.sequencer.sound_strip_add(filepath=xmlAmbient.getAttribute('value'), frame_start=1, channel=1)

for actor in actors.keys():
    if len(actors[actor]['trajectory']) == 0:
        continue
        
    obj = bpy.data.objects[actor]
    obj.select = True
    bpy.context.scene.objects.active = obj
    obj.location = (0,0,0)
    bpy.ops.object.constraint_add(type = 'FOLLOW_PATH')
    
    bpy.ops.curve.primitive_nurbs_path_add()
    curve_curve = bpy.data.curves[bpy.context.object.name]
    spline_points = bpy.data.curves[bpy.context.object.name].splines[0].points
    
    obj.constraints[0].target = bpy.context.object
    obj.constraints[0].use_curve_follow = True
    
    curve_curve.path_duration = NUM_FRAMES_ANIMATION
    
    bpy.context.scene.frame_current = 1
    curve_curve.eval_time = 0
    curve_curve.keyframe_insert(data_path = 'eval_time') 
    
    bpy.context.scene.frame_current = NUM_FRAMES_ANIMATION
    curve_curve.eval_time = NUM_FRAMES_ANIMATION
    curve_curve.keyframe_insert(data_path = 'eval_time') 
    
    # Muestreo la trayectoria que debe seguir el objeto en 5 puntos equidistantes, y con ellos construyo un spline
    trajectory_points = actors[actor]['trajectory'];
    
    # Voy a muestrear algunos puntos de la trayectoria apra hcrear la curva, es decir que no los voy a suar todos necesariamente
    # 'traj_step' es cada cuatos puntos voy a tomar una muestra.
    # 'num_points_curve' es cuantos puntos en total tendra la curva
    if len(trajectory_points) < NUM_POINTS_CURVE:
        traj_step = 1
        num_points_curve = len(trajectory_points)
    else:
        traj_step = int(len(trajectory_points) / NUM_POINTS_CURVE)
        num_points_curve = NUM_POINTS_CURVE
    
    if num_points_curve > 5:
        spline_points.add(num_points_curve - 5) # por defecto vienen 5 puntos

    print(ground_plane.active_material.name.split('.')[0])
    print(actor.split('_')[0])

    for i in range(num_points_curve):
        spline_points[i].co = ( trajectory_points[i*traj_step][0] , trajectory_points[i*traj_step][1] , trajectory_points[i*traj_step][2] , 1)
        if spline_points[i].co[0] < ground_plane.dimensions[0]:
        	floor = ground_plane.active_material.name.split('.')[0]
        	frame_limit = (NUM_FRAMES_ANIMATION / num_points_curve) * (i + 1)
        	for xmlScore in score.getElementsByTagName('score'):
        		for xmlActor in xmlScore.getElementsByTagName('actor'):
        			if xmlActor.getAttribute('asset') == actor.split('_')[0]:
        				for xmlFrame in xmlActor.getElementsByTagName('frame'):
        					if frame_limit > int(xmlFrame.getAttribute('number')):
        						for xmlSound in xmlFrame.getElementsByTagName('sound'):
        							if xmlSound.getAttribute('key') == floor:
        								bpy.ops.sequencer.sound_strip_add(filepath=xmlSound.getAttribute('value'), frame_start=int(xmlFrame.getAttribute('number')), channel=2)
    obj.select = False
    

bpy.context.scene.frame_current = 1

# }

print ('TEST RENDERIN PROPERTIES:')
print ('bpy.context.scene.render.use_raytrace = False')
print ('bpy.context.scene.render.use_envmaps = False')
print ('bpy.context.scene.render.use_textures = False')
print ('bpy.context.scene.render.use_shadows = False')
print ('bpy.context.scene.render.use_antialiasing = False\n')
print ('Renderin at: ')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

# Renderizar la imagen o el video
# {
bpy.context.scene.camera = camera
bpy.context.scene.render.parts_x = 1
bpy.context.scene.render.parts_y = 1
bpy.context.scene.render.use_sss = False

    
bpy.context.scene.render.use_raytrace = False
bpy.context.scene.render.use_envmaps = False
bpy.context.scene.render.use_textures = False
bpy.context.scene.render.use_shadows = False
bpy.context.scene.render.use_antialiasing = False
'''
bpy.context.scene.render.use_raytrace = True
bpy.context.scene.render.use_envmaps = True
bpy.context.scene.render.use_textures = True
bpy.context.scene.render.use_shadows = True
bpy.context.scene.render.use_antialiasing = True
'''

# renderizo a video MPEG
bpy.context.scene.render.image_settings.file_format='FFMPEG'
bpy.context.scene.render.filepath = MODELS_PATH + '/output_we.mpg'
bpy.context.scene.render.ffmpeg.audio_codec = 'MP3'
bpy.context.scene.render.ffmpeg.video_bitrate = 1024 # Quota de transmision de video
bpy.ops.render.render(animation=True)

# }

'''
print ('Blendin at ')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

bpy.ops.wm.save_mainfile(filepath="output.blend", check_existing=False)
'''

print ('THE END AT: ')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')


