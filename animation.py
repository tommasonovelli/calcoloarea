# Codice aggiuntivo per animazione e stima live
import math
import matplotlib.pyplot as plt
import numpy as np

def montecarlo_geometrico_animato():
    print("Animazione in tempo reale...")

# INSERIMENTO DATI
    # inserisci la funzione di input
    func_str = input("Inserisci la funzione in x (es: x**2 + 3): ")

    def f(x):
        try:
            return eval(func_str, {"x": x, "math": math, "__builtins__": {}})
        except Exception as e:
            print(f"Errore nell'esecuzione della funzione: {e}")
            return 0

    # inserisci l'intervallo della funzione e il numero di punti casuali da generare
    try:
        a = float(input("Estremo inferiore dell'intervallo: "))
        b = float(input("Estremo superiore dell'intervallo: "))
        n_punti = int(input("Numero di punti casuali da generare: "))
    except ValueError:
        print("Errore: inserisci numeri validi.")

    if a >= b or n_punti <= 0:
        print("Errore: intervallo o numero di punti non valido.")

    # trova il massimo della funzione
    x_density = np.linspace(a, b, 1000) # calcoliamo 1000 valori equidistanti sulle x
    y_density = [f(x) for x in x_density]

    y_min = min(0, min(y_density)) # incluso lo 0 per gestire funzioni negative
    y_max = max(0, max(y_density))

# RAPPRESENTAZIONE GRAFICA
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x_density, y_density, color="blue")
    ax.axhline(0, color="black", linewidth=0.5)
    ax.set_xlim(a, b)
    ax.set_ylim(y_min, y_max)
    ax.set_title("Montecarlo Geometrico - Live")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True)
    ax.legend()

    # valore dell'integrale aggiornato in tempo reale
    integral_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12,
                            verticalalignment='top', bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))
    
    # numero punti sparati subito sotto
    points_text = ax.text(0.02, 0.87, '', transform=ax.transAxes, fontsize=12,
                         verticalalignment='top', bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))


    # inizializzo scatter con zero punti
    scatter_under = ax.scatter([], [], color="green", s=10, alpha=0.5, label="Sotto la curva")
    scatter_over = ax.scatter([], [], color="red", s=10, alpha=0.5, label="Sopra la curva")
    
# MONTECARLO    
    # calclo dei punti sottostanti al grafico
    count_under = 0
    
    # area del rettangolo
    area_rect = (b - a) * (y_max - y_min)

    # array di salvataggio dei punti
    x_under, y_under = [], []
    x_over, y_over = [], []

    for i in range(1, n_punti + 1):
        x_rand = a + (b - a) * np.random.random()
        y_rand = y_min + (y_max - y_min) * np.random.random()
        y_func = f(x_rand)

        if (y_rand >= 0 and y_rand <= y_func) or (y_rand < 0 and y_rand >= y_func):
            count_under += 1
            x_under.append(x_rand)
            y_under.append(y_rand)
        else:
            x_over.append(x_rand)
            y_over.append(y_rand)

        # aggiorno i dati dei scatter in batch
        scatter_under.set_offsets(np.column_stack((x_under, y_under)))
        scatter_over.set_offsets(np.column_stack((x_over, y_over)))

        integral_estimate = area_rect * (count_under / i)

        integral_text.set_text(f"Stima attuale: {integral_estimate:.6f}")
        points_text.set_text(f"Punti sparati: {i}")

        plt.pause(0.001)  # pausa brevissima per velocizzare

    plt.ioff()
    plt.show()
    print(f"Stima finale: {integral_estimate:.6f}")

# per eseguire l'animazione subito dopo la versione normale:
montecarlo_geometrico_animato()
