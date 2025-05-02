import numpy as np
from scipy.spatial import Delaunay
from stl.mesh import Mesh
import plotly.graph_objects as go

# Define parameters for the catenoid-helicoid transition
u = np.linspace(-2, 2, 100)
v = np.linspace(-np.pi, np.pi, 100)
u, v = np.meshgrid(u, v)
A = np.linspace(0, 1/2, 12)

# Define the catenoid-helicoid transition function
def catenoid_helicoid(u, v, A) :
    l = A*np.pi  #  0 ≤ A ≤ 1/2
    cosT, sinT = np.cos(l), np.sin(l)   
    x =  cosT * np.sinh(u) * np.sin(v) -  sinT * np.cosh(u) * np.cos(v)
    y =  cosT * np.sinh(u) * np.cos(v) +  sinT * np.cosh(u) * np.sin(v)
    z = v *cosT -  u * sinT
    return x,y,z

# Generate the mesh and .stl files for each model in the transition
for model in range(0, 12, 1):
    # Generate the mesh for the catenoid-helicoid transition
    x, y, z = catenoid_helicoid(u, v, A[model])

    # Flatten to list of vertices
    iu, iv = u.shape
    verts = np.vstack([x.ravel(), y.ravel(), z.ravel()]).T

    # Triangulate the parameter domain (u,v)
    points_uv = np.vstack([u.ravel(), v.ravel()]).T
    tri = Delaunay(points_uv)
    faces = tri.simplices

    # OPTIONAL: Compute per-vertex normals by averaging adjacent face normals
    def compute_vertex_normals(vertices, faces):
        normals = np.zeros(vertices.shape, dtype=float)
        face_normals = np.cross(
            vertices[faces[:,1]] - vertices[faces[:,0]],
            vertices[faces[:,2]] - vertices[faces[:,0]]
        )
        fnorm = np.linalg.norm(face_normals, axis=1, keepdims=True)
        face_normals /= np.where(fnorm==0, 1, fnorm)
        for i, f in enumerate(faces):
            for idx in f:
                normals[idx] += face_normals[i]
        norm = np.linalg.norm(normals, axis=1, keepdims=True)
        return normals / np.where(norm==0, 1, norm)

    normals = compute_vertex_normals(verts, faces)

    # Set thickness (total thickness = 2 * offset)
    offset = 0.05  # half-thickness
    verts_outer = verts + normals * offset
    verts_inner = verts - normals * offset

    # Build closed mesh: top, bottom, and side walls
    # Combine vertices
    verts_all = np.vstack([verts_outer, verts_inner])

    # Top faces (using outer surface)
    faces_top = faces.copy()

    # Bottom faces (using inner surface, reverse orientation)
    faces_bottom = faces[:, ::-1] + verts_outer.shape[0]

    # Side walls: each quad in the uv-grid needs 2 triangles
    side_faces = []
    for i in range(iu - 1):
        for j in range(iv - 1):
            # indices of four corners in flattened grid
            i1 = i * iv + j
            i2 = (i+1) * iv + j
            i3 = (i+1) * iv + (j+1)
            i4 = i * iv + (j+1)
            # outer indices
            o1, o2, o3, o4 = i1, i2, i3, i4
            # inner indices
            i1i = i1 + verts_outer.shape[0]
            i2i = i2 + verts_outer.shape[0]
            i3i = i3 + verts_outer.shape[0]
            i4i = i4 + verts_outer.shape[0]
            # 4 side quads -> 8 triangles
            side_faces += [
                [o1, o2, i2i], [o1, i2i, i1i],
                [o2, o3, i3i], [o2, i3i, i2i],
                [o3, o4, i4i], [o3, i4i, i3i],
                [o4, o1, i1i], [o4, i1i, i4i]
            ]
    side_faces = np.array(side_faces)

    # Combine all faces
    total_faces = np.vstack([faces_top, faces_bottom, side_faces])

    # Create STL mesh
    a_mesh = Mesh(np.zeros(total_faces.shape[0], dtype=Mesh.dtype))
    for i, f in enumerate(total_faces):
        for j in range(3):
            a_mesh.vectors[i][j] = verts_all[f[j], :]

    filename = (f'Model_{model}.stl')
    a_mesh.save(filename)
    print(f"Saved STL: {filename} (A = {A[model]})")