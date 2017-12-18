# This repository hosts sample codes for Light-field dataset generation
# Requiring Light-fieldfield Bledner addon
# https://github.com/lightfield-analysis/blender-addon
# The code generate, RGB, depth, and normal 
__author__ = "Youngjin Yoon"


import bpy,sys,os
from camera_RT import *
from camera_K import *

def making_scene():
	#create(or copy scene)
	bpy.ops.scene.new(type='LINK_OBJECTS') #scene.001 for depth
	
	#scene setting(RGB image)
	bpy.context.screen.scene = bpy.data.scenes['Scene']
	bpy.context.scene.use_nodes = True # only one time 
	tree_00 = bpy.context.scene.node_tree # for each scene
	links = tree_00.links
	# RGB node setting 
	#delete default nodes
	for n in tree_00.nodes:
		tree_00.nodes.remove(n)
		
	r_00 = tree_00.nodes.new('CompositorNodeRLayers')
	rgb  = tree_00.nodes.new('CompositorNodeComposite')
	links.new(r_00.outputs[0], rgb.inputs[0]) 

	# Depth node setting 
	depth = tree_00.nodes.new('CompositorNodeViewer')
	links.new(r_00.outputs[2], depth.inputs[0]) 

	# Normal node setting
	bpy.context.screen.scene = bpy.data.scenes['Scene.001']
	bpy.data.scenes['Scene.001'].render.layers['RenderLayer'].use_pass_normal = True #add normal to compositor
	tree_01 = bpy.context.scene.node_tree # for each scene
	links = tree_01.links
	#delete default nodes
	for n in tree_01.nodes:
		tree_01.nodes.remove(n)
		
	r_01 = tree_01.nodes.new('CompositorNodeRLayers')

	Mul = tree_01.nodes.new(type='CompositorNodeMixRGB')
	Mul.blend_type = 'MULTIPLY'
	Mul.inputs[2].default_value[0]=0.5
	Mul.inputs[2].default_value[1]=0.5
	Mul.inputs[2].default_value[2]=0.5

	Add = tree_01.nodes.new(type='CompositorNodeMixRGB')
	Add.blend_type ='ADD'
	Add.inputs[2].default_value[0]=0.5
	Add.inputs[2].default_value[1]=0.5
	Add.inputs[2].default_value[2]=0.5
		
	invert =tree_01.nodes.new(type='CompositorNodeInvert')
	normal =tree_01.nodes.new(type='CompositorNodeComposite')

	links.new(r_01.outputs[3],Mul.inputs[1])
	links.new(Mul.outputs[0],Add.inputs[1])
	links.new(Add.outputs[0],invert.inputs[1])
	links.new(invert.outputs[0],normal.inputs[0])
	

	print('Finishing built nodes \n')

	

def rendering_data(savepath):
	
	if not os.path.exists(savepath):
		os.mkdir(savepath)
	
	#render RGB and depth 
	bpy.context.screen.scene = bpy.data.scenes['Scene'] #changing scene 
	bpy.context.scene.cycles.device = 'GPU'
	scene = bpy.context.scene

	for ob in scene.objects:
		if ob.type =='CAMERA':
			bpy.context.scene.camera = ob
			cam_name = bpy.context.scene.camera.name
			bpy.context.scene.render.filepath = os.path.join(savepath,'rgb_%s.png' %cam_name)
			bpy.ops.render.render(write_still = True,scene='Scene') # rendering rgb image 
			depthname = os.path.join(savepath,'depth_%s.txt' %cam_name)
			view = bpy.data.images['Viewer Node']
			sz = view.size
			pixels = view.pixels
			arr = np.array(pixels[:])
			filer = open(depthname,'w')
			for y in range(0,sz[1]):
				for x in range(0,sz[0]):
					idx = y*sz[0] + x
					r = arr[idx*4+0]
					filer.write('%.4f ' %r)
				filer.write('\n')
			filer.close()
			
	#Rendering normal
	bpy.context.screen.scene = bpy.data.scenes['Scene.001']
	centercam = bpy.data.objects['LF0_Cam004'] # could be changed 04:3x3, 40:9x9
	bpy.context.scene.camera = centercam
	cam_name = bpy.context.scene.camera.name
	bpy.context.scene.render.filepath = os.path.join(savepath,'normal_%s.png' %cam_name)
	bpy.ops.render.render( write_still=True , scene = 'Scene.001') #normal  
	
	#save camera intrinsic
	K = get_calibration_matrix_K_from_blender(centercam.data) # Camera intrinsic
	nK = np.matrix(K)
	np.savetxt(os.path.join(savepath,'camera_K.txt'), nK)  # to select precision, use e.g. fmt='%.2f'


if __name__ =="__main__":
	savepath = 'C:/Users/rcv/Desktop/test'
	making_scene()
	rendering_data(savepath)
	print('Done \n');
