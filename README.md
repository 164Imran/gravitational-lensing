# Gravitational Lensing Simulation

A Python implementation simulating the gravitational lensing effect of massive objects on background light sources.

## Physics Background

**Gravitational lensing** occurs when light from a distant source is bent by the gravitational field of a massive object (lens) between the source and observer.

### Thin Lens Approximation

The lens equation relates observed position **θ** to true source position **β**:

β = θ - α(θ)

text

Where **α(θ)** is the deflection angle:

α(θ) = θ_E² / θ

text

**θ_E** is the **Einstein radius**, defined as:

θ_E = √(4GM/c² × D_LS / (D_L × D_S))

text

- **G**: Gravitational constant
- **M**: Lens mass
- **D_L**: Distance to lens
- **D_S**: Distance to source  
- **D_LS**: Distance between lens and source

### Einstein Ring

When the source, lens, and observer are perfectly aligned, light is bent into a ring with radius **θ_E**.

## Features

- ✅ Physically accurate deflection angles
- ✅ Einstein rings and arcs
- ✅ Animated lens motion
- ✅ Support for real astronomical images
- ✅ Synthetic source generation
- ✅ GIF export

## Installation

pip install numpy matplotlib pillow tqdm

text

## Usage

### Basic Example

from gravitational_lensing import (
LensingConfig,
load_source_image,
create_lensed_image,
plot_comparison
)

Load configuration
config = LensingConfig()

Load source image
source = load_source_image("data/galaxy.png")

Create lensed image
lens_position = (256, 512)
lensed = create_lensed_image(
source,
lens_position,
theta_einstein=50
)

Visualize
plot_comparison(source, lens_position, theta_einstein=50)

text

### Create Animation

from gravitational_lensing import create_lens_animation

Create animation of moving lens
ani = create_lens_animation(
source,
config,
output_path="lensing.gif"
)

plt.show()

text

### Synthetic Source

from gravitational_lensing import create_synthetic_source

Generate test image with galaxies
source = create_synthetic_source(size=512, n_galaxies=10)

text

## Configuration

Edit `LensingConfig` class to customize:

class LensingConfig:
def init(self):
self.image_width = 512 # Output width
self.image_height = 1024 # Output height
self.theta_einstein = 35 # Einstein radius (pixels)
self.lens_y_start = 380 # Animation start
self.lens_y_end = 650 # Animation end
self.animation_fps = 30 # Frames per second
self.source_image_path = Path("data/allsky.png")

text

## Examples

### Einstein Ring

Perfect alignment creates ring
source = create_synthetic_source(512, n_galaxies=1)
lensed = create_lensed_image(source, (256, 256), theta_einstein=80)

text

### Einstein Cross

Four-image configuration
lensed = create_lensed_image(source, (256, 240), theta_einstein=50)

text

### Moving Lens

Animate lens crossing the field
config.lens_y_start = 200
config.lens_y_end = 800
ani = create_lens_animation(source, config)

text

## File Structure

gravitational-lensing/
├── gravitational_lensing.py # Main code
├── README.md # This file
├── requirements.txt # Dependencies
├── data/
│ └── allsky-2mass.png # Source image (not included)
└── examples/
└── demo.py # Usage examples

text

## Physics Parameters

| Parameter | Symbol | Typical Value | Description |
|-----------|--------|---------------|-------------|
| Einstein radius | θ_E | 1-100 pixels | Depends on lens mass and distances |
| Lens mass | M | 10⁶ - 10¹² M_☉ | Galaxy or black hole mass |
| Source distance | D_S | Gpc | Distance to background source |

## Coordinate Systems

- **Image Plane**: Observed positions (x, y) in pixels
- **Source Plane**: True positions (β_x, β_y) after removing deflection
- **Lens Position**: Center of gravitational potential

## Mathematical Details

### Deflection Angle Components

α_x = θ_E² × Δx / (Δx² + Δy²)
α_y = θ_E² × Δy / (Δx² + Δy²)

text

Where:
- Δx = x - x_lens
- Δy = y - y_lens

### Magnification

Magnification is infinite at Einstein radius:

μ = (θ/β) × (dβ/dθ)

text

## Known Limitations

1. **Thin lens approximation**: Assumes lens has negligible thickness
2. **Point mass**: Doesn't model extended mass distributions
3. **No microlensing**: Substructure not included
4. **Flat geometry**: Doesn't account for spacetime curvature
5. **No time delays**: Ignores Shapiro delay between images

## References

1. Schneider, P., Ehlers, J., & Falco, E. E. (1992). *Gravitational Lenses*. Springer.
2. Narayan, R., & Bartelmann, M. (1996). *Lectures on Gravitational Lensing*. arXiv:astro-ph/9606001.

## Real-World Applications

- Detecting dark matter through weak lensing
- Measuring Hubble constant (time-delay cosmology)
- Finding exoplanets via microlensing
- Studying distant galaxies magnified by foreground clusters

## Advanced Usage

### Custom Deflection Model

def nfw_deflection(x, y, lens_pos, r_s, rho_0):
"""NFW (Navarro-Frenk-White) dark matter halo"""
# Implement NFW profile deflection
pass

text

### Multiple Lenses

def multi_lens_deflection(x, y, lens_positions, masses):
"""Superposition of multiple lenses"""
alpha_x_total = 0
alpha_y_total = 0
for pos, mass in zip(lens_positions, masses):
alpha_x, alpha_y = compute_deflection_angle(x, y, pos, mass)
alpha_x_total += alpha_x
alpha_y_total += alpha_y
return alpha_x_total, alpha_y_total

text

## Contributing

Contributions welcome! Areas for improvement:
- Extended mass distributions (SIS, NFW profiles)
- Microlensing caustics
- Ray tracing through multiple lenses
- Time delay calculations
- GPU acceleration

## License

MIT

## Author

TIPE Project - Gravitational Lensing
École Préparatoire - Math Spé
requirements.txt
text
numpy>=1.20.0
matplotlib>=3.3.0
pillow>=8.0.0
tqdm>=4.60.0
Améliorations apportées
​
Aspect	Avant	Après
Documentation	Aucune	Docstrings complètes + physique
Structure	Code plat	Modules avec fonctions
Portabilité	Chemin Windows dur	Path + fallback synthétique
Validation	Aucune	Gestion d'erreurs
Clarté	Variables cryptiques	Noms explicites
Réutilisabilité	Monolithique	Fonctions modulaires
Configuration	Magic numbers	Classe Config
Tests	Impossible	Source synthétique
