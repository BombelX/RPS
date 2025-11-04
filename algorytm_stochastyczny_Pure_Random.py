from tkinter import *
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


master = Tk()
master.title("Losowe strzały do hipersześcianu S (1–6D)")

Label(master, text="Ile wymiarów").grid(row=0, column=0, sticky="w", padx=6, pady=4)
Label(master, text="Ile procent to S").grid(row=1, column=0, sticky="w", padx=6, pady=4)

e1 = Scale(master, from_=1, to=6, orient=HORIZONTAL)      
e2 = Scale(master, from_=0, to=100, orient=HORIZONTAL)
e1.set(2)
e1.grid(row=0, column=1, sticky="we", padx=6)
e2.grid(row=1, column=1, sticky="we", padx=6)

status_var = StringVar(value="Gotowy.")
Label(master, textvariable=status_var, anchor="w").grid(row=3, column=0, columnspan=2, sticky="we", padx=6, pady=(4,8))

fig, ax = plt.subplots(figsize=(5, 5))
canvas = FigureCanvasTkAgg(fig, master)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=4, column=0, columnspan=2, padx=6, pady=6, sticky="nsew")
master.grid_rowconfigure(4, weight=1)
master.grid_columnconfigure(1, weight=1)

L = 100.0               
shooting_active = False
target_w = 0.0            
points_count = 0          
shot_ms_delay = 10       
current_dim = 2
S_patch = None            
S_poly3d = None           
start_coords = []         


def _make_cube_3d(ax3d, sx, sy, sz, w):
    x1, x2 = sx, sx + w
    y1, y2 = sy, sy + w
    z1, z2 = sz, sz + w
    verts = [
        [(x1,y1,z1), (x2,y1,z1), (x2,y2,z1), (x1,y2,z1)],
        [(x1,y1,z2), (x2,y1,z2), (x2,y2,z2), (x1,y2,z2)],
        [(x1,y1,z1), (x2,y1,z1), (x2,y1,z2), (x1,y1,z2)],
        [(x1,y2,z1), (x2,y2,z1), (x2,y2,z2), (x1,y2,z2)],
        [(x1,y1,z1), (x1,y2,z1), (x1,y2,z2), (x1,y1,z2)],
        [(x2,y1,z1), (x2,y2,z1), (x2,y2,z2), (x2,y1,z2)],
    ]
    poly = Poly3DCollection(verts, alpha=0.15, edgecolor="black", linewidths=0.5)
    ax3d.add_collection3d(poly)
    return poly

def generate_figure(dimensions: int, S_percentage: int):
    """Przygotuj wykres i wylosuj pozycję hipersześcianu S we wszystkich wymiarach."""
    global S_patch, S_poly3d, target_w, points_count, current_dim, ax, start_coords
    current_dim = dimensions
    points_count = 0

    target_w = (S_percentage / 100.0) * L
    start_coords = [random.uniform(0, max(0.0, L - target_w)) for _ in range(dimensions)]

    fig.clf()
    S_patch = None
    S_poly3d = None

    if dimensions == 1:
        ax = fig.add_subplot(111)
        sx = start_coords[0]
        ax.set_title(f"1D — S = {S_percentage}%  (x ∈ [{sx:.1f}, {sx+target_w:.1f}])")
        ax.set_xlabel("X")
        ax.set_yticks([])
        ax.set_xlim(0, L)
        ax.set_ylim(-1, 1)
        ax.grid(True, linewidth=0.5, axis="x")
        S_patch = Rectangle((sx, -1), target_w, 2, alpha=0.25, edgecolor="black")
        ax.add_patch(S_patch)
        ax.text(sx + target_w * 0.5, 0.8, "S", ha="center", va="center")

    elif dimensions == 2:
        ax = fig.add_subplot(111)
        sx, sy = start_coords
        ax.set_title(f"2D — S = {S_percentage}%  (kwadrat {target_w:.1f}×{target_w:.1f})")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_xlim(0, L)
        ax.set_ylim(0, L)
        ax.set_aspect("equal", adjustable="box")
        ax.grid(True, linewidth=0.5)
        S_patch = Rectangle((sx, sy), target_w, target_w, alpha=0.25, edgecolor="black")
        ax.add_patch(S_patch)
        ax.text(sx + target_w * 0.5, sy + target_w * 0.5, "S", ha="center", va="center")

    elif dimensions == 3:
        ax = fig.add_subplot(111, projection="3d")
        sx, sy, sz = start_coords
        ax.set_title(
            f"3D — S = {S_percentage}%  (sześcian {target_w:.1f}³)\n"
            f"x∈[{sx:.1f},{sx+target_w:.1f}], y∈[{sy:.1f},{sy+target_w:.1f}], z∈[{sz:.1f},{sz+target_w:.1f}]"
        )
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_xlim(0, L)
        ax.set_ylim(0, L)
        ax.set_zlim(0, L)
        S_poly3d = _make_cube_3d(ax, sx, sy, sz, target_w)

    else:
        ax = fig.add_subplot(111)
        rngs = ", ".join(
            [f"x{i+1}∈[{start_coords[i]:.1f},{start_coords[i]+target_w:.1f}]" for i in range(dimensions)]
        )
        ax.set_title(f"{dimensions}D — bez wizualizacji (S = {S_percentage}%)")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_xlim(0, L)
        ax.set_ylim(0, L)
        ax.grid(True, linewidth=0.5)
        ax.text(0.5, 0.5, f"Hipersześcian S: {rngs}", transform=ax.transAxes, ha="center", va="center")

    canvas.draw_idle()

def point_in_S(coords):
    """sprawdzamy czy punkt lezy w S"""
    for i, x in enumerate(coords):
        if not (start_coords[i] <= x <= start_coords[i] + target_w):
            return False
    return True

def shoot_once(dim: int):
    """jeden losowy strzal D o wymiarze dim"""
    coords = [random.uniform(0, L) for _ in range(dim)]
    hit = point_in_S(coords)
    if dim == 1:
        return hit, (coords[0], 0.0)
    elif dim == 2:
        return hit, (coords[0], coords[1])
    elif dim == 3:
        return hit, (coords[0], coords[1], coords[2])
    else:
        return hit, None

def draw_shot(dim: int, point, hit: bool):
    """Rysowanie strzału (1D/2D/3D)."""
    if dim == 1:
        x, _ = point
        ax.plot([x], [0], "o" if hit else "x", markersize=10 if hit else 8)
    elif dim == 2:
        x, y = point
        ax.plot(x, y, "o" if hit else "x", markersize=10 if hit else 8)
    elif dim == 3:
        x, y, z = point
        ax.scatter([x], [y], [z], marker="o" if hit else "x", s=80 if hit else 35)

def schedule_shots():
    global shooting_active, points_count, current_dim

    if not shooting_active:
        return

    hit, pt = shoot_once(current_dim)
    points_count += 1

    if current_dim in (1, 2, 3) and pt is not None:
        draw_shot(current_dim, pt, hit)
        canvas.draw_idle()

    status_var.set(
        f"Wymiar: {current_dim}D | Strzały: {points_count} | "
        f"{'TRAFIONO S!' if hit else 'Szukam...'}"
    )

    if hit:
        shooting_active = False
        return
    if current_dim > 3:
        master.after(1, schedule_shots)
    else:
        master.after(shot_ms_delay, schedule_shots)

def start():
    """Start symulacji."""
    global shooting_active
    dimensions = int(e1.get())
    S_percentage = int(e2.get())

    if S_percentage < 0 or S_percentage > 100:
        status_var.set("Błędny procent S. Wybierz 0–100.")
        return

    generate_figure(dimensions, S_percentage)

    if S_percentage == 0:
        status_var.set("S ma 0% miary. Trafienie niemożliwe.")
        shooting_active = False
        return

    shooting_active = True
    status_var.set(
        f"Start: {dimensions}D, S = {S_percentage}% — szukam punktu w S..."
    )
    schedule_shots()

def stop():
    """Zatrzymanie symulacji."""
    global shooting_active
    shooting_active = False
    status_var.set(f"Zatrzymano. Strzałów: {points_count}")

# Przyciski
button_start = Button(master, text="Start", width=40, command=start)
button_start.grid(row=2, column=0, padx=6, pady=4, sticky="we")

button_stop = Button(master, text="Stop", width=40, command=stop)
button_stop.grid(row=2, column=1, padx=6, pady=4, sticky="we")

# Inicjalny rysunek
generate_figure(e1.get(), e2.get())

mainloop()




