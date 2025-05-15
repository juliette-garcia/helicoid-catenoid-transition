# helicoid-catenoid-transition

This repository implements a smooth geometric transition between two minimal surfaces: the **catenoid** and the **helicoid**. We both animate this transition and make it possible to generate 3D-printable meshes of different phases of it in STL format. The project consists of two main scripts:

* **`animate_surface.py`**: Animates the continuous transition between the catenoid and helicoid using either Matplotlib and Plotly.
* **`generate_stl.py`**: Generates closed meshes with adjustable thickness at discrete transition steps and exports them as `.stl` files.

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


---

## Usage

### 1. Seeing an Animation of the Transition

Run:

```bash
python animate_surface.py
```

### 2. Generating STL Models

Run:

```bash
python generate_stl.py
```

* Produces 12 (this number can be changed) STL files in the `Models/` directory. Each STL file represents a phase of the transition with a set thickness (this number can also be changed). Note that the phases that are exporte are equally spaced.

---

*Happy exploring!*

