import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Parameters
v = np.linspace(-np.pi, np.pi, 100)
u = np.linspace(-2, 2, 100)
u, v = np.meshgrid(u, v)

A = np.linspace(-1/2, 5/12, 12)

# Define the catenoid-helicoid transition function
def helicoid_catenoid(u, v, A) :
    l = A*np.pi  #  0 ≤ A ≤ 1/2
    cosT, sinT = np.cos(l), np.sin(l)   
    x =  cosT * np.sinh(u) * np.sin(v) -  sinT * np.cosh(u) * np.cos(v)
    y =  cosT * np.sinh(u) * np.cos(v) +  sinT * np.cosh(u) * np.sin(v)
    z = v *cosT -  u * sinT
    return x,y,z

# Initialize plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot initial surface
x, y, z = helicoid_catenoid(u, v, 0)
surface = ax.plot_surface(x, y, z, color='b')

# Update function for animation
def update(t):
    t_slider.set_val(t)  # Update slider
    ax.clear()
    x, y, z = helicoid_catenoid(u, v, t)
    surface = ax.plot_surface(x, y, z, color='b')
    ax.set_xlim([-3, 3])
    ax.set_ylim([-3, 3])
    ax.set_zlim([-3, 3])
    return surface,

# Create animation -------------------------------------------

t_vals = np.linspace(0, 1, 100)
frames = []
for t in t_vals:
    x, y, z = helicoid_catenoid(u, v, t)
    frames.append(go.Frame(
        data=[go.Surface(
            x=x, y=y, z=z,
            colorscale=[[0, 'royalblue'], [1, 'royalblue']],
            showscale=False,
            lighting=dict(
                ambient=0.1,
                diffuse=0.9,
                specular=0.2,
                roughness=0.9,
                fresnel=0.1
            ),
            lightposition=dict(x=100, y=200, z=0)
        )],
        name=f'{t:.3f}'
    ))

# initial surface
x0, y0, z0 = helicoid_catenoid(u, v, 0)
fig = go.Figure(
    data=[go.Surface(x=x0, y=y0, z=z0, colorscale=[[0, 'royalblue'], [1, 'royalblue']], showscale=False)],
    frames=frames
)

# layout with play/pause buttons
fig.update_layout(
    width=700, height=700,
    scene=dict(
        xaxis=dict(range=[-3, 3]),
        yaxis=dict(range=[-3, 3]),
        zaxis=dict(range=[-3, 3]),
        aspectmode='cube',      # ensures equal scaling on x, y, z
        camera=dict(
            eye=dict(x=1.5, y=1, z=0)
        )
    ),
    updatemenus=[dict(
        type='buttons',
        showactive=False,
        y=1.05,
        x=0.1,
        xanchor='right',
        yanchor='top',
        pad=dict(t=0, r=10),
        buttons=[
            dict(label='Play',
                 method='animate',
                 args=[None, dict(frame=dict(duration=20, redraw=True), fromcurrent=True)]),
            dict(label='Pause',
                 method='animate',
                 args=[[None], dict(frame=dict(duration=0, redraw=False), mode='immediate')])
        ]
    )]
)

# slider
fig.update_layout(sliders=[dict(
    steps=[dict(method='animate',
                args=[[f'{t:.3f}'], dict(mode='immediate', frame=dict(duration=0))],
                label=f'{t:.2f}')
           for t in t_vals],
    transition=dict(duration=0),
    x=0.1, y=0, currentvalue=dict(prefix='t = ')
)])

fig.show()