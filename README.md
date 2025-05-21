# helicoid-catenoid-transition

![transition](https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExc3phZW84dThndGo1ZHZldzJpYjJoZThhcWZoY2puM2N1ZjA0Y3Z3NCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/qqLbZSMgtqfZINq1As/giphy.gif)

This repository implements a smooth geometric transition between two minimal surfaces: the **catenoid** and the **helicoid**. We both animate this transition and make it possible to generate 3D-printable meshes of different phases of it in STL format. The project consists of two main scripts:

* **`helicoid_catenoid.py`**: Animates the continuous transition between the catenoid and helicoid using either Matplotlib and Plotly.
* **`export_transition.py`**: Generates closed meshes with adjustable thickness at discrete transition steps and exports them as `.stl` files.

This work is based on the parametrization described in the paper:

> \***A.H. Louie, R.L. Somorjai* (1982). Differential geometry of proteins: A structural and dynamical representation of patterns. *Journal of Theoretical Biology*, 98, 189-209.*

---

## Mathematical Background

Each shape is given by two parameters, u and v. Below are their parameterizations:

    # Catenoid parameterization
    x = cosh(u) * cos(v)
    y = cosh(u) * sin(v)
    z = u
    
    # Helicoid parameterization
    x = sinh(u) * sin(v)
    y = sinh(u) * cos(v)
    z = v

To transition between these two surfaces, we take a "weighted average" of the surfaces. That is, we weight the catenoid (cosh terms) and the helicoid (sinh terms) by cos θ and sin θ, respectively.

    # Catenoid-Helicoid Transition parameterization
    θ = A × π
    x =  cos(θ)·sinh(u)·sin(v)  –  sin(θ)·cosh(u)·cos(v)
    y =  cos(θ)·sinh(u)·cos(v)  +  sin(θ)·cosh(u)·sin(v)
    z =  v·cos(θ)  –  u·sin(θ)

Note that θ slides us from catenoid (θ=0) to helicoid (θ=π/2). By increasing A, θ goes from 0 to π/2, so the surface shifts from purely catenoid to purely helicoid.

Here's a link to the a Desmos simulation of this transition: https://www.desmos.com/3d/kghlbeljz2

---

## Usage

### 1. Seeing an Animation of the Transition

Run:

```bash
python helicoid_catenoid.py
```

Here's another nice visualization we found: https://s3dlib.org/examples/animations/anim_cat2heli.html

### 2. Generating STL Models

Run:

```bash
python export_transition.py
```

This produces 12 (this number can be changed) STL files in the `Models/` directory. Each file captures an equally spaced phase of the transition at an adjustable thickness. Our current settings were used to create a zoetrope!

---

*Happy exploring!*

