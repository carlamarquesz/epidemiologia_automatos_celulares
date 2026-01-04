import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os

os.makedirs("resultados", exist_ok=True)

# Parâmetros do modelo
sigma = 0.5  # taxa de incubação (E -> I)
gamma = 0.14  # taxa de recuperação (I -> R)
N = 100  # tamanho do grid (NxN)
STEPS = 250  # número de passos da simulação

# Cenários variando Beta
scenarios = {
    "Cenario_1_Beta_010": 0.10,
    "Cenario_2_Beta_018": 0.18,
    "Cenario_3_Beta_035": 0.35,
}


# MODELO CA-SEIR
def initialize_grid(N):
    """Inicializa o grid com único infectado no centro."""
    grid = np.zeros((N, N), dtype=int)
    grid[N // 2, N // 2] = 2
    return grid


def count_infected_neighbors(grid, x, y):
    """Conta quantos vizinhos infectados existem."""
    N = grid.shape[0]
    count = 0
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < N and 0 <= ny < N and grid[nx, ny] == 2:
                count += 1
    return count


def update_seir_ca(grid, beta, sigma, gamma):
    """Aplica as regras SEIR ao grid e retorna o novo grid."""
    N = grid.shape[0]
    new_grid = grid.copy()
    for x in range(N):
        for y in range(N):
            state = grid[x, y]
            if state == 0:
                nI = count_infected_neighbors(grid, x, y)
                p_inf = 1 - (1 - beta) ** nI
                if np.random.random() < p_inf:
                    new_grid[x, y] = 1
            elif state == 1:
                if np.random.random() < sigma:
                    new_grid[x, y] = 2
            elif state == 2:
                if np.random.random() < gamma:
                    new_grid[x, y] = 3
    return new_grid


# GERAR SNAPSHOTS DO GRID
def plot_grid_snapshot(grid, step, scenario_name):
    """Salva uma imagem do grid em um determinado passo."""
    cmap = mcolors.ListedColormap(["blue", "orange", "red", "green"])
    plt.figure(figsize=(6, 6))
    plt.imshow(grid, cmap=cmap, vmin=0, vmax=3)
    plt.title(f"Evolução Espacial - {scenario_name} - Passo {step}")
    plt.colorbar(ticks=[0, 1, 2, 3], label="Estados (S, E, I, R)")
    file_name = f"resultados/grid_{scenario_name}_step_{step}.png"
    plt.savefig(file_name)
    plt.close()


# Roda a simulação SEIR e registra S, E, I, R; salva snapshots no Cenário 1.
def simulate_seir_ca_with_snapshots(
    initial_grid, beta_val, sigma_val, gamma_val, steps, scenario_name
):
    g = initial_grid.copy()
    counts = []
    snapshot_steps = (
        [0, steps // 3, 2 * steps // 3, steps - 1]
        if "Cenario_1" in scenario_name
        else []
    )
    for step in range(steps):
        unique, cnt = np.unique(g, return_counts=True)
        count_dict = {s: 0 for s in (0, 1, 2, 3)}
        count_dict.update(dict(zip(unique, cnt)))
        counts.append((count_dict[0], count_dict[1], count_dict[2], count_dict[3]))
        if step in snapshot_steps:
            plot_grid_snapshot(g, step, scenario_name)
        g = update_seir_ca(g, beta_val, sigma_val, gamma_val)
    return np.array(counts)


# GRÁFICOS INDIVIDUAIS SEIR
def plot_and_save_seir_counts(scenarios_data):
    colors = ["blue", "orange", "red", "green"]
    labels = ["Suscetível", "Exposto", "Infectado", "Recuperado"]
    for name, counts in scenarios_data.items():
        plt.figure(figsize=(10, 6))
        ax = plt.gca()
        for i in range(4):
            ax.plot(counts[:, i], label=labels[i], color=colors[i], linewidth=2)
        ax.set_xlabel("Tempo (Passos)")
        ax.set_ylabel("Número de Células")
        display_name = name.replace("_", " ").replace("Cenario", "Cenário")
        ax.set_title(f"Evolução SEIR - {display_name}")
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.7)
        file_name = f"resultados/grafico_seir_{name}.png"
        plt.savefig(file_name)
        plt.close()


# GRÁFICO COMPARATIVO DE INFECTADOS
def plot_comparative_infected(results):
    plt.figure(figsize=(10, 6))
    for name, counts in results.items():
        infectados = counts[:, 2]
        label = (
            name.replace("_", " ").replace("Cenario", "Cenário").replace("Beta", "β =")
        )
        plt.plot(infectados, linewidth=2, label=label)
    plt.title("Comparação das Curvas de Infectados nos Três Cenários")
    plt.xlabel("Tempo (Passos)")
    plt.ylabel("Número de Infectados")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()
    file_name = "resultados/comparativo_infectados.png"
    plt.savefig(file_name)
    plt.close()


# EXECUÇÃO PRINCIPAL
results = {}
print("\nInício\n")

for name, beta_val in scenarios.items():
    print(f"Simulando {name} | Beta = {beta_val}")
    initial_g = initialize_grid(N)
    counts = simulate_seir_ca_with_snapshots(
        initial_g, beta_val, sigma, gamma, STEPS, name
    )
    results[name] = counts

print("\nGerando gráficos SEIR individuais...\n")
plot_and_save_seir_counts(results)

print("\nGerando gráfico comparativo dos infectados...\n")
plot_comparative_infected(results)

print("\nFim.\n")
