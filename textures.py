import bpy

def createWoodTex():

    # used names
    matname = "Wood Mat"
    texname = "Wood Tex"

    # new material
    if not matname in bpy.data.materials:
        material = bpy.data.materials.new(matname)
        material.diffuse_color = (0.376, 0.209, 0.05)

    # new texture
    tex = bpy.data.textures.new(texname, type="WOOD")
    tex.noise_basis_2 = 'SAW'
    tex.wood_type = 'RINGNOISE'
    tex.noise_scale = 1

    # new slot
    slot = bpy.data.materials[matname].texture_slots.add()
    slot.scale[0] = 2
    slot.scale[1] = 4
    slot.color = (0.730, 0.479, 0.242)


def createLeafTex():

    # used names
    matname = "Leaf Mat"
    texname = "Leaf Tex"

    # new material
    if not matname in bpy.data.materials:
        material = bpy.data.materials.new(matname)
        material.diffuse_color = (0.011, 0.133, 0.011)

    # new texture
    tex = bpy.data.textures.new(texname, type="MARBLE")
    tex.noise_basis_2 = 'TRI'
    tex.marble_type = 'SHARP'
    tex.noise_scale = 0.45
    tex.noise_basis = 'VORONOI_CRACKLE'

    # new slot
    slot = bpy.data.materials[matname].texture_slots.add()
    slot.scale[0] = 2
    slot.color = (0.011, 0.867, 0.051)

def addTexture(obj, texName):

    matName = texName.split(' ')[0] + ' Mat'

    # if material already exists, just add it to object
    if texName in bpy.data.textures:
        material = bpy.data.materials[matName]
        obj.data.materials.append(material)
        tex = bpy.data.textures[texName]
        bpy.data.materials[matName].active_texture = tex
        bpy.data.materials[matName].texture_slots[0].texture_coords = "GLOBAL"
        return

    # create right material
    if texName == 'Wood Tex':
        createWoodTex()
    elif texName == 'Leaf Tex':
        createLeafTex()

    # add material to object
    material = bpy.data.materials[matName]
    obj.data.materials.append(material)
    
    # connect texture with material
    tex = bpy.data.textures[texName]
    bpy.data.materials[matName].active_texture = tex
    bpy.data.materials[matName].texture_slots[0].texture_coords = "GLOBAL"
