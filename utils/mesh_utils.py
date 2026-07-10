from math import radians
import numpy as np

import trimesh

import bpy
import bmesh
from mathutils import Vector

def rotate_object(x: float, y: float, z:float, object: bpy.types.Object):
    if x > 0.0:
        object.rotation_euler.x += radians(x)
    if y > 0.0:
        object.rotation_euler.y += radians(y)
    if z > 0.0:
        object.rotation_euler.z += radians(z)

def mesh_to_voxel_grid(mesh_obj, voxel_size=0.1):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    mesh_eval = mesh_obj.evaluated_get(depsgraph).data
    
    vertices = np.array([mesh_obj.matrix_world @ v.co for v in mesh_eval.vertices])
    
    if len(vertices) == 0:
        return None, None, voxel_size

    min_coord = vertices.min(axis=0)
    max_coord = vertices.max(axis=0)

    min_coord -= voxel_size
    max_coord += voxel_size

    grid_size = np.ceil((max_coord - min_coord) / voxel_size).astype(int)

    voxel_grid = np.zeros(grid_size, dtype=np.uint8)

    for face in mesh_eval.polygons:
        face_verts = [mesh_eval.vertices[i].co for i in face.vertices]
        face_center = sum(face_verts, Vector()) / len(face_verts)
        face_center = mesh_obj.matrix_world @ face_center

        for vert in face_verts:
            world_vert = np.array(mesh_obj.matrix_world @ vert)
            voxel_idx = ((world_vert - min_coord) / voxel_size).astype(int)
            voxel_idx = np.clip(voxel_idx, 0, grid_size - 1)
            voxel_grid[tuple(voxel_idx)] = 1
    
    return voxel_grid, min_coord, voxel_size

def compute_iou_voxel(mesh_obj1, mesh_obj2, voxel_size=0.1):
    grid1, origin1, vs1 = mesh_to_voxel_grid(mesh_obj1, voxel_size)
    grid2, origin2, vs2 = mesh_to_voxel_grid(mesh_obj2, voxel_size)
    
    if grid1 is None or grid2 is None:
        return 0.0

    min_coord = np.minimum(origin1, origin2)
    max_coord = np.maximum(
        origin1 + np.array(grid1.shape) * voxel_size,
        origin2 + np.array(grid2.shape) * voxel_size
    )
    
    aligned_size = np.ceil((max_coord - min_coord) / voxel_size).astype(int)
    
    aligned_grid1 = np.zeros(aligned_size, dtype=np.uint8)
    aligned_grid2 = np.zeros(aligned_size, dtype=np.uint8)

    start1 = ((origin1 - min_coord) / voxel_size).astype(int)
    end1 = start1 + grid1.shape
    aligned_grid1[start1[0]:end1[0], start1[1]:end1[1], start1[2]:end1[2]] = grid1

    start2 = ((origin2 - min_coord) / voxel_size).astype(int)
    end2 = start2 + grid2.shape
    aligned_grid2[start2[0]:end2[0], start2[1]:end2[1], start2[2]:end2[2]] = grid2

    intersection = np.logical_and(aligned_grid1, aligned_grid2).sum()
    union = np.logical_or(aligned_grid1, aligned_grid2).sum()
    
    iou = intersection / union if union > 0 else 0.0
    return iou

def blender_mesh_to_trimesh(mesh_obj):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    mesh_eval = mesh_obj.evaluated_get(depsgraph).data

    vertices = np.array([v.co for v in mesh_eval.vertices])
    faces = np.array([f.vertices for f in mesh_eval.polygons])

    matrix = np.array(mesh_obj.matrix_world)
    vertices = np.array([matrix @ Vector(v).to_4d() for v in vertices])[:, :3]

    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
    mesh.remove_degenerate_faces()
    return mesh