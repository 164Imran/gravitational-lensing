"""
Gravitational Lensing Simulation
================================

Simule l'effet de lentille gravitationnelle d'un objet massif (ex : trou noir)
sur une image de fond (ex : carte du ciel).

Idée :
    - On considère un plan image (ce que l'observateur voit).
    - Chaque pixel (x, y) de ce plan est "dévié" par la lentille.
    - On calcule où ce rayon serait allé dans le plan source (β_x, β_y).
    - On prend la couleur du pixel source(β_x, β_y) et on la met en (x, y).

Physique (approximation lentille mince) :
    β = θ − α(θ)
    avec, pour une lentille ponctuelle :
    α(θ) = θ_E² / θ

Ici, tout est exprimé en pixels, θ_E est un rayon d'Einstein "effectif".
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pathlib import Path
from PIL import Image
from tqdm import tqdm


# =============================================================================
# CONFIGURATION
# =============================================================================

# Paramètres de la simulation
IMAGE_HEIGHT = 500          # Hauteur de la zone de travail (en pixels)
IMAGE_WIDTH  = 500          # Largeur de la zone de travail (en pixels)

THETA_E = 35.0              # Rayon d'Einstein (en pixels, paramètre ajustable)

# Position de la lentille (x_lens, y_lens) pour l'image statique
LENS_POS_STATIC = (IMAGE_WIDTH // 2, IMAGE_HEIGHT // 2)

# Paramètres d'animation : la lentille se déplace verticalement
LENS_X_START = 100         # x de départ
LENS_X_END   = 650          # x d'arrivée (exclu dans range)
ANIM_INTERVAL_MS = 50       # Temps entre deux frames (ms)
ANIM_REPEAT_DELAY_MS = 1000 # Pause avant de relancer l'animation (ms)

# Chemin vers l'image de fond (source)
SOURCE_IMAGE_PATH = Path(
    "C:/Users/Administrator/Documents/math_spé/Tipe_lentille_grav/allsky-2mass.png"
)


# =============================================================================
# CHARGEMENT / SYNTHÈSE DE LA SOURCE
# =============================================================================

def load_source_image(path: Path) -> np.ndarray:
    """
    Charge l'image de fond utilisée comme source.

    Parameters
    ----------
    path : Path
        Chemin vers l'image (PNG/JPEG...).

    Returns
    -------
    source : np.ndarray
        Tableau NumPy (H, W[, C]) représentant l'image.
    """
    img = Image.open(path)
    source = np.array(img)
    return source


def create_gaussian_source(height: int, width: int) -> np.ndarray:
    """
    Crée une source artificielle : une "boule" gaussienne au centre.

    Utile pour tester sans image réelle.

    Parameters
    ----------
    height, width : int
        Dimensions de l'image.

    Returns
    -------
    source : np.ndarray, shape (height, width)
        Image de la source (niveaux de gris entre 0 et 1).
    """
    y, x = np.indices((height, width))
    cx, cy = width // 2, height // 2      # centre de la gaussienne
    sigma = 20.0                          # écart-type (taille de la tache)

    source = np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2 * sigma ** 2))
    return source


# =============================================================================
# PHYSIQUE : ANGLE DE DÉFLEXION ET ÉQUATION DE LA LENTILLE
# =============================================================================

def deflection_angle(x: np.ndarray,
                     y: np.ndarray,
                     lens_pos: tuple[float, float],
                     theta_e: float) -> tuple[np.ndarray, np.ndarray]:
    """
    Calcule l'angle de déflexion gravitationnelle en chaque point (x, y).

    Formules (en unités "pixels") :
        Δx = x - x_lens
        Δy = y - y_lens
        r² = Δx² + Δy²

        α_x = θ_E² * Δx / r²
        α_y = θ_E² * Δy / r²

    Parameters
    ----------
    x, y : np.ndarray
        Grilles de coordonnées (mêmes dimensions que l'image).
    lens_pos : (float, float)
        Position (x_lens, y_lens) de la lentille.
    theta_e : float
        Rayon d'Einstein en pixels.

    Returns
    -------
    alpha_x, alpha_y : np.ndarray
        Composantes x et y de l'angle de déflexion.
    """
    x_lens, y_lens = lens_pos

    # Décalage par rapport au centre de la lentille
    dx = x - x_lens
    dy = y - y_lens

    # r² = dx² + dy², on ajoute un epsilon pour éviter la division par zéro
    r2 = dx ** 2 + dy ** 2 + 1e-12

    alpha_x = theta_e ** 2 * dx / r2
    alpha_y = theta_e ** 2 * dy / r2

    return alpha_x, alpha_y


def lens_mapping(x: np.ndarray,
                 y: np.ndarray,
                 lens_pos: tuple[float, float],
                 theta_e: float,
                 source_shape: tuple[int, int]) -> tuple[np.ndarray, np.ndarray]:
    """
    Applique l'équation de lentille pour trouver, pour chaque pixel (x, y)
    de l'image observée, la position correspondante (β_x, β_y) dans le plan source.

    Équation de la lentille (en coordonnées) :
        β_x = x - α_x
        β_y = y - α_y

    On clippe ensuite (β_x, β_y) pour rester dans les bornes de l'image source.

    Parameters
    ----------
    x, y : np.ndarray
        Grilles de coordonnées de l'image observée.
    lens_pos : (float, float)
        Position de la lentille.
    theta_e : float
        Rayon d'Einstein.
    source_shape : (int, int)
        (hauteur, largeur) de l'image source.

    Returns
    -------
    beta_x, beta_y : np.ndarray
        Indices entiers dans l'image source.
    """
    height, width = source_shape

    # Angle de déflexion
    alpha_x, alpha_y = deflection_angle(x, y, lens_pos, theta_e)

    # Coordonnées dans le plan source
    beta_x = x - alpha_x
    beta_y = y - alpha_y

    # Conversion en indices de pixels + clipping dans les bornes
    beta_x = np.clip(beta_x.astype(int), 0, width - 1)
    beta_y = np.clip(beta_y.astype(int), 0, height - 1)

    return beta_x, beta_y


# =============================================================================
# GÉNÉRATION D'UNE IMAGE LENTILLÉE
# =============================================================================

def lens_image(source: np.ndarray,
               lens_pos: tuple[float, float],
               theta_e: float,
               out_height: int,
               out_width: int) -> np.ndarray:
    """
    Calcule une image "observée" après lentille.

    Parameters
    ----------
    source : np.ndarray
        Image de la source (H_source, W_source[, C]).
    lens_pos : (float, float)
        Position (x_lens, y_lens) de la lentille dans le plan image.
    theta_e : float
        Rayon d'Einstein (pixels).
    out_height, out_width : int
        Dimensions de l'image de sortie (ce que voit l'observateur).

    Returns
    -------
    lensed : np.ndarray
        Image lentillée, même nombre de canaux que `source`.
    """
    # Grilles de coordonnées dans le plan image
    y_grid, x_grid = np.indices((out_height, out_width))

    # Coordonnées correspondantes dans le plan source
    beta_x, beta_y = lens_mapping(
        x_grid, y_grid,
        lens_pos,
        theta_e,
        source.shape[:2]
    )

    # Échantillonnage de l'image source
    lensed = source[beta_y, beta_x]

    return lensed


# =============================================================================
# ANIMATION
# =============================================================================

def animate_lens_motion(source: np.ndarray) -> None:
    """
    Crée et affiche une animation montrant le déplacement de la lentille
    devant la source.

    La lentille se déplace verticalement entre LENS_X_START et LENS_Y_END
    au centre horizontal de l'image.

    Parameters
    ----------
    source : np.ndarray
        Image source.
    """
    fig, ax = plt.subplots()
    ax.set_title("Déplacement d'un trou noir (lentille gravitationnelle)")
    ax.axis("off")

    ims = []

    # On fixe x_lens au centre de l'image de sortie
    y_lens = IMAGE_WIDTH // 2

    for x_lens in tqdm(range(LENS_X_START, LENS_X_END), desc="Animation frames"):
        lens_pos = (x_lens, y_lens)

        # Calcul de l'image lentillée pour cette position de lentille
        lensed = lens_image(source, lens_pos, THETA_E, IMAGE_HEIGHT, IMAGE_WIDTH)

        im = ax.imshow(lensed, animated=True)
        ims.append([im])

    ani = animation.ArtistAnimation(
        fig,
        ims,
        interval=ANIM_INTERVAL_MS,
        blit=True,
        repeat_delay=ANIM_REPEAT_DELAY_MS
    )

    plt.show()

    # Pour sauvegarder en GIF, décommenter :
    # writer = animation.PillowWriter(fps=30)
    # ani.save("lensing_animation.gif", writer=writer)


# =============================================================================
# EXEMPLES D'UTILISATION
# =============================================================================

def main() -> None:
    """
    Point d'entrée principal :
      1. charge une image source réelle (ou fabrique une gaussienne si indisponible),
      2. affiche une image lentillée statique,
      3. lance l'animation du déplacement de la lentille.
    """
    # 1) Chargement ou création de la source
    try:
        source = load_source_image(SOURCE_IMAGE_PATH)
        print(f"Source réelle chargée : shape = {source.shape}")
    except FileNotFoundError:
        print("Image source introuvable, utilisation d'une source gaussienne synthétique.")
        source = create_gaussian_source(IMAGE_HEIGHT, IMAGE_WIDTH)

    # 2) Exemple statique : lentille au centre
    lensed_static = lens_image(
        source,
        lens_pos=LENS_POS_STATIC,
        theta_e=THETA_E,
        out_height=IMAGE_HEIGHT,
        out_width=IMAGE_WIDTH
    )

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(source)
    plt.title("Source (avant lentille)")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(lensed_static)
    plt.title("Image lentillée (lentille au centre)")
    plt.axis("off")

    plt.tight_layout()
    plt.show()

    # 3) Animation du déplacement de la lentille
    animate_lens_motion(source)


if __name__ == "__main__":
    main()
