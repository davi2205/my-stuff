
import sys
import bpy
import bmesh

from copy import copy
from bpy import types
from mathutils import Matrix, Vector

#
#   Davi Vilalva - 2020
#
#   This function creates invisible objects used for 3d clipping
#   around other objects.
#
#   root - The bpy.types.Object where the clip objects will be placed/updated.
#   objs - The bpy.types.Object-s the clips will surround.
# config - A dictionary that specifies which clip objects the 'objs' should have.
#          If config is empty, all existing clip objects will be deleted.
#
#   The config format { <axis_name>: <optional spacing params> or None, ... }
#
#        config = {
#           'X': {'padding': 0.1, 'spacing': 0.4}, 
#           'Y': {'padding': 0.1},
#           'Z': None,
#            ...
#        }
#

def set_clips(root, objs, config):
    # No objects, nothing to do.
    if len(objs) == 0:
        return

    # Get some floating point info.
    fp_info = sys.float_info

    # Get the surroundings of the objects.
    mi = [fp_info.max] * 3
    ma = [fp_info.min] * 3
    for obj in objs:
        for point in obj.bound_box:
            x, y, z = obj.matrix_world @ Vector(point)
            mi[0], mi[1], mi[2] = min(x, mi[0]), min(y, mi[1]), min(z, mi[2])
            ma[0], ma[1], ma[2] = max(x, ma[0]), max(y, ma[1]), max(z, ma[2])
    size = [ma[0] - mi[0], ma[1] - mi[1], ma[2] - mi[2]]

    clip_obj_by_axis_name = {}

    for axis_name, settings in config.items():
        # Get axis from key.
        axis = None

        if axis_name == 'X':
            axis = (1.0, 0.0, 0.0)
        elif axis_name == '-X':
            axis = (-1.0, 0.0, 0.0)
        elif axis_name == 'Y':
            axis = (0.0, 1.0, 0.0)
        elif axis_name == '-Y':
            axis = (0.0, -1.0, 0.0)
        elif axis_name == 'Z':
            axis = (0.0, 0.0, 1.0)
        elif axis_name == '-Z':
            axis = (0.0, 0.0, -1.0)
        else:
            # Error here.
            return None

        spacing = 0.0
        padding = 0.1

        if settings is not None:
            spacing = settings.get('spacing', 0.0)
            padding = settings.get('padding', 0.1)
        
        # Computing bounds.
        offset = (
            axis[0] * (size[0] + spacing + padding),
            axis[1] * (size[1] + spacing + padding),
            axis[2] * (size[2] + spacing + padding),
        )

        _mi = copy(mi)
        _ma = copy(ma)

        _mi[0] += offset[0] - padding
        _mi[1] += offset[1] - padding
        _mi[2] += offset[2] - padding
        _ma[0] += offset[0] + padding
        _ma[1] += offset[1] + padding
        _ma[2] += offset[2] + padding

        # Computing matrix from bounds.
        center = (
            (_ma[0] + _mi[0]) / 2.0,
            (_ma[1] + _mi[1]) / 2.0,
            (_ma[2] + _mi[2]) / 2.0,
        )
        radius = (
            (_ma[0] - _mi[0]) / 2.0,
            (_ma[1] - _mi[1]) / 2.0,
            (_ma[2] - _mi[2]) / 2.0,
        )

        mat = Matrix([
            (radius[0],       0.0,       0.0, center[0]),
            (      0.0, radius[1],       0.0, center[1]),
            (      0.0,       0.0, radius[2], center[2]),
            (      0.0,       0.0,       0.0,       1.0),
        ])

        # Creating/Updating clip object.
        clip_obj = next(filter( \
            lambda c: c.get('ClipAxis') == axis_name, root.children), None)

        if clip_obj is None:
            obj_name = f'{root.name}{axis_name.replace("-", "Minus")}Clip'
            mesh = bpy.data.meshes.new(obj_name)
            bm = bmesh.new()

            bm.from_mesh(mesh)
            bmesh.ops.create_cube(bm, size=2.0)
            bm.to_mesh(mesh)
            bm.free()

            clip_obj = bpy.data.objects.new(obj_name, object_data=mesh)
            clip_obj.parent = root
            clip_obj.hide_render = True
            clip_obj.display_type = 'WIRE'
            clip_obj['ClipAxis'] = axis_name

            bpy.context.collection.objects.link(clip_obj)
        
        # Setting the world matrix.
        clip_obj.matrix_world = mat

        # Map clip object.
        clip_obj_by_axis_name[axis_name] = clip_obj

    to_exclude = {'X', '-X', 'Y', '-Y', 'Z', '-Z'} - set(config.keys())

    # Excluding unnecessary clip objs.
    for clip_obj in filter( \
        lambda o: o.get('ClipAxis') in to_exclude, root.children):

        # Make sure the corresponding modifiers are deleted as well.
        for obj in filter(lambda o: o.type == 'MESH', objs):
            for modifier in list(filter( \
                lambda m: m.type == 'BOOLEAN' \
                    and m.object is clip_obj, obj.modifiers)):
                obj.modifiers.remove(modifier)    

        bpy.data.objects.remove(clip_obj)
    
    # Add/Update existing clip objs modifiers.
    for axis_name, clip_obj in clip_obj_by_axis_name.items():
        for obj in filter(lambda o: o.type == 'MESH', objs):
            modifier = next(filter( \
                lambda m: m.object is not None \
                    and m.object.get('ClipAxis', None) == axis_name, \
                        obj.modifiers), None)

            if modifier is None:
                modifier = obj.modifiers.new('', 'BOOLEAN')
            
            modifier.object = clip_obj