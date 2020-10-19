
import sys
import bpy
import bmesh

from uuid import uuid4
from copy import copy
from mathutils import Matrix, Vector

#
#   Davi Vilalva - 2020
#
#   This function creates invisible objects used for 3d clipping
#   around other objects.
#
#   root - The bpy.types.Object where the clip objects will be placed/updated. (as children objects)
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

def _set_clips(root, objs, config):
    
    def pick_best(criteria, iterable):
        max_score = len(criteria)

        pick = None
        pick_score = -1
        pick_criteria = tuple()

        for i in iterable:
            i_criteria = tuple(c for c, f in criteria.items() if f(i))
            i_score = len(i_criteria)

            if i_score == max_score:
                return (i, i_criteria)
            elif i_score > pick_score:
                pick = i
                pick_score = i_score
                pick_criteria = i_criteria

        return (pick, pick_criteria)
    
    def remove_all(predicate, iterable, remove_fn):
        for i in list(filter(predicate, iterable)):
            remove_fn(i)

    # Clip obj

    def clip_obj_new(axis_name):
        obj_name = f'{root.name}{axis_name.replace("-", "Minus")}Clip'

        mesh = bpy.data.meshes.new(obj_name)
        bm = bmesh.new()

        bm.from_mesh(mesh)
        bmesh.ops.create_cube(bm, size=2.0)
        bm.to_mesh(mesh)
        bm.free()

        clip_obj = bpy.data.objects.new(obj_name, object_data=mesh)
        clip_obj.parent = root
        clip_obj['ClipAxis'] = axis_name

        bpy.context.collection.objects.link(clip_obj)

        return clip_obj
                
    def clip_obj_get_color(clip_obj):
        pass

    def clip_obj_set_color(clip_obj, color):
        #clip_obj.hide_render = True
        #clip_obj.display_type = 'WIRE'
        pass

    def clip_obj_remove_dependencies(clip_obj):
        for obj in filter(lambda o: o.type == 'MESH', root.children):
            remove_all(
                lambda m: m.type == 'BOOLEAN' and m.object is clip_obj,
                    obj.modifiers,
                        obj.modifiers.remove)


    # End clip obj

    EXPECTED_AXIS = 0
    EXPECTED_MATERIAL = 1

    available_clip_objs = [o for o in root.children if o.get('ClipAxis')]


#_set_clips(bpy.context.object, None, None)

def set_background_material(obj):
    obj.data.at

def set_clips(root, objs, config):
    # No objects, nothing to do.
    if len(objs) == 0:
        return

    # Some floating point info.
    fp_info = sys.float_info

    # Computing the surroundings of the objects.
    mi = [fp_info.max] * 3
    ma = [fp_info.min] * 3
    for obj in objs:
        for point in obj.bound_box:
            x, y, z = obj.matrix_world @ Vector(point)
            mi[0], mi[1], mi[2] = min(x, mi[0]), min(y, mi[1]), min(z, mi[2])
            ma[0], ma[1], ma[2] = max(x, ma[0]), max(y, ma[1]), max(z, ma[2])
    size = [ma[0] - mi[0], ma[1] - mi[1], ma[2] - mi[2]]

    def get_or_insert(predicate, iterable, insert_fn):
        try:
            return next(filter(predicate, iterable))
        except StopIteration:
            return insert_fn()
    
    def remove_all(predicate, iterable, remove_fn):
        for i in list(filter(predicate, iterable)):
            remove_fn(i)

    def find(predicate, iterable):
        return next(filter(predicate, iterable), None)
    
    def new_clip_obj(axis_name):
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

        return clip_obj
    
    def remove_clip_obj(clip_obj):
        for obj in filter(lambda o: o.type == 'MESH', root.children):
            remove_all(                                                 \
                lambda m: m.type == 'BOOLEAN' and m.object is clip_obj, \
                    obj.modifiers,                                      \
                        lambda m: obj.modifiers.remove(m))

        bpy.data.objects.remove(clip_obj)

    def mesh_from_obj(obj):
        try:
            mesh = obj.to_mesh().copy()
            obj.to_mesh_clear()

            return mesh
        except Exception:
            return None
    
    def new_mesh_obj_from(obj):
        mesh = mesh_from_obj(obj)

        if mesh is None:
            return None

        uuid = f'{obj.name_full}_{uuid4()}'

        obj['Link'] = uuid 

        mesh_obj = bpy.data.objects.new(f'{obj.name}Mesh', object_data=mesh)
        mesh_obj.parent = root
        mesh_obj.matrix_world = obj.matrix_world
        mesh_obj['Link'] = uuid
        mesh_obj['IsGeneratedMesh'] = True

        bpy.context.collection.objects.link(mesh_obj)
        
        return mesh_obj

    def copy_animation_data(_from, to):
        from_data = _from.animation_data 

        if from_data is None:
            return

        props = list(p.identifier \
            for p in from_data.bl_rna.properties if not p.is_readonly)
        
        to_data = to.animation_data

        if to_data is None:
            to.animation_data_create()
            to_data = to.animation_data

        for prop in props:
            setattr(to_data, prop, getattr(from_data, prop))

    clip_obj_by_axis_name = {}

    for axis_name, settings in config.items():
        # Computing the axis from key.
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

        # Getting or inserting clip object.
        clip_obj = get_or_insert(                     \
            lambda c: c.get('ClipAxis') == axis_name, \
                root.children,                        \
                    lambda: new_clip_obj(axis_name))
        
        # Setting the world matrix.
        clip_obj.matrix_world = mat

        # Mapping the clip object.
        clip_obj_by_axis_name[axis_name] = clip_obj

    to_exclude = {'X', '-X', 'Y', '-Y', 'Z', '-Z'} - set(config.keys())

    # Excluding unnecessary clip objs.
    remove_all(                                    \
        lambda o: o.get('ClipAxis') in to_exclude, \
            root.children,                         \
                remove_clip_obj)

    # Adding/Updating existing clip objs modifiers.
    for axis_name, clip_obj in clip_obj_by_axis_name.items():
        for obj in objs:
            if obj.get('IsGeneratedMesh'):
                continue

            # Attempting to generate a new mesh from non mesh object.
            if obj.type != 'MESH':
                old_mesh_obj = find(                                \
                    lambda o: o.get('IsGeneratedMesh')              \
                              and o.get('Link') == obj.get('Link'), \
                            root.children)

                mesh_obj = new_mesh_obj_from(obj)

                if mesh_obj is None:
                    continue

                if old_mesh_obj is not None:
                    copy_animation_data(old_mesh_obj, mesh_obj)  
                    bpy.data.objects.remove(old_mesh_obj)  

                obj = mesh_obj

            # Getting or inserting the modifier.
            modifier = get_or_insert(                                \
                lambda m: m.type == 'BOOLEAN'                        \
                          and m.object is not None                   \
                          and m.object.get('ClipAxis') == axis_name, \
                            obj.modifiers,                           \
                                lambda: obj.modifiers.new('', 'BOOLEAN'))
            
            modifier.object = clip_obj