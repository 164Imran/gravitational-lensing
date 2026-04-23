# Gravitational Lensing Simulation

A Python simulation of the gravitational lensing effect of a point mass using the thin lens approximation. The program applies backward ray-tracing to compute distorted images of a background source and animates the lens sweeping across the field of view.

## Physics

Gravitational lensing arises from the deflection of light by the spacetime curvature induced by a massive object. In the thin lens regime, the mapping from observed position **θ** to true source position **β** is:

```
β = θ − α(θ)
```

For a point-mass lens, the deflection angle has the closed form:

```
α(θ) = θ_E² / θ
```

where **θ_E** is the Einstein radius — the angular scale at which a perfect ring (Einstein ring) forms when source, lens, and observer are perfectly aligned.

### Ray-Tracing Implementation

Each pixel (x, y) in the observer plane is traced back to its origin (β_x, β_y) in the source plane:

```
α_x = θ_E² · Δx / (Δx² + Δy² + ε)
α_y = θ_E² · Δy / (Δx² + Δy² + ε)

β_x = x − α_x
β_y = y − α_y
```

A small ε regularizes the singularity at the lens position. The observed image is obtained by sampling the source image at the mapped coordinates.

## Features

- Static lensed image with configurable Einstein radius
- Animated sequence of a lens crossing the source plane
- Supports real astronomical imagery or a synthetic Gaussian source as fallback

## Requirements

```
numpy
matplotlib
pillow
tqdm
```

Install:

```bash
pip install numpy matplotlib pillow tqdm
```

## Usage

```bash
python "grav lens II.py"
```

Set `SOURCE_IMAGE_PATH` to point to a local sky image (e.g. 2MASS all-sky survey). If not found, a Gaussian synthetic source is used automatically.

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `THETA_E` | 35.0 px | Einstein radius (effective, in pixels) |
| `IMAGE_HEIGHT / WIDTH` | 500 px | Output image dimensions |
| `LENS_X_START / END` | 100–650 | Horizontal sweep range for animation |
| `ANIM_INTERVAL_MS` | 50 ms | Frame duration |

## References

- Schneider, P., Ehlers, J., & Falco, E. E. (1992). *Gravitational Lenses*. Springer.
- Wambsganss, J. (1998). Gravitational lensing in astronomy. *Living Reviews in Relativity*, 1, 12.
