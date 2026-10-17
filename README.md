# Python Software Wireframe Renderer

A lightweight software 3D wireframe renderer built from scratch in Python using **Pygame** and **NumPy**, without any hardware acceleration or external graphics APIs (like OpenGL or DirectX).

## Features

- **Custom OBJ Parser:** Parses Wavefront `.obj` files to extract raw vertices (`v`) and face definitions (`f`).
- **3D Transformation Pipeline:** Implements manual rotation matrices around the X, Y, and Z axes using NumPy.
- **Perspective Projection:** Projects 3D world coordinates onto a 2D screen space using a custom field-of-view (FOV) and depth division formula (`z`).
- **Custom Rasterization Algorithms:** Features hand-written anti-aliased line drawing (`drawLineAA`) and efficient Bresenham-style line drawing algorithms (`drawLineH`, `drawLineV`) to render wireframe triangles.
- **Real-time Visualization:** Uses Pygame surfaces and pixel manipulation to render frames in real time.

## Technical Overview

The renderer transforms local 3D vertices into 2D screen coordinates through matrix multiplication and perspective division:

`v_screen = M_viewport * M_projection * M_view * M_model * v_local`

1. **Vertex Transformation & Rotation:** Rotates raw vertex coordinates using rotation matrices around X, Y, and Z axes, then translates along the Z-axis.
2. **Perspective Projection:** Divides coordinates by depth (`z`) factored by the FOV and scale parameters to simulate depth perception.
3. **Wireframe Rasterization:** Extracts triangle vertex indices from face definitions and draws edges using custom rasterization functions.

## File Format Support

- **Wavefront .obj:** Vertex data (`v`) and face connectivity (`f`).

## Usage

Ensure you have Python, Pygame, and NumPy installed, then run:

```bash
python Renderer.py
```
