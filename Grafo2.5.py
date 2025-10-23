import tkinter as tk
import time
import threading
import networkx as nx
import matplotlib.pyplot as plt

class GrafoNumeros:
    def __init__(self, root):
        self.root = root
        self.root.title("Recorrido de grafo - Imagen corregida (con 0–5)")
        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack()

        self.G = nx.DiGraph()
        self.G.add_nodes_from([0, 1, 2, 3, 4, 5, 6])
        self.G.add_edges_from([(2, 0), (0, 6), (0, 5), (6, 3), (6, 5), (6, 4), (1, 4), (0,1)])

        self.pos = {2: (80, 100), 0: (180, 100), 6: (280, 100), 3: (380, 100), 5: (225, 180), 4: (280, 260), 1: (180, 260)}

        self.node_objs = {}
        self.text_objs = {}
        self.dibujar_grafo()

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)
        tk.Label(self.frame, text="Recorrido (ej. 2, 0, 6, 4, 1):").grid(row=0, column=0, padx=5)
        self.recorrido_input = tk.StringVar(value="2, 0, 6, 4, 1")
        self.entry_recorrido = tk.Entry(self.frame, textvariable=self.recorrido_input, width=20, justify="center")
        self.entry_recorrido.grid(row=0, column=1, padx=5)
        self.btn_iniciar = tk.Button(self.frame, text="Iniciar recorrido", command=self.iniciar_recorrido)
        self.btn_iniciar.grid(row=0, column=2, padx=5)
        self.lbl_estado = tk.Label(root, text="Esperando inicio...", font=("Arial", 12))
        self.lbl_estado.pack()
        self.lbl_tiempo = tk.Label(root, text="Tiempo recorrido: 0.0 segundos", font=("Arial", 10))
        self.lbl_tiempo.pack()

    def dibujar_grafo(self):
        for u, v in self.G.edges:
            x1, y1 = self.pos[u]
            x2, y2 = self.pos[v]
            self.canvas.create_line(x1, y1, x2, y2, width=2)

        for n, (x, y) in self.pos.items():
            nodo = self.canvas.create_oval(x-25, y-25, x+25, y+25, fill="lightgray", width=2)
            texto = self.canvas.create_text(x, y, text=str(n), font=("Arial", 18, "bold"))
            self.node_objs[n] = nodo
            self.text_objs[n] = texto

    def iniciar_recorrido(self):
        recorrido_input = self.recorrido_input.get().strip()
        try:
            recorrido = [int(n.strip()) for n in recorrido_input.split(",") if n.strip().isdigit()]
        except Exception:
            self.lbl_estado.config(text="Error en el formato del recorrido.", fg="red")
            return
        if any(n not in self.G.nodes for n in recorrido):
            self.lbl_estado.config(text="Algunos nodos no existen en el grafo.", fg="red")
            return
        self.lbl_estado.config(text=f"Recorriendo: {recorrido}", fg="black")
        threading.Thread(target=self.recorrer_grafo, args=(recorrido,), daemon=True).start()

    def recorrer_grafo(self, recorrido):
        start_time = time.time()
        for i in range(len(recorrido) - 1):
            actual = recorrido[i]
            siguiente = recorrido[i + 1]
            self.iluminar_nodo(actual)
            self.resaltar_arista(actual, siguiente)
            self.lbl_estado.config(text=f"Visitando nodo: {actual} → {siguiente}")
            self.root.update()
            time.sleep(1)
            self.restaurar_nodo(actual)
            self.restaurar_arista()

        self.iluminar_nodo(recorrido[-1])
        self.lbl_estado.config(text=f"Visitando nodo final: {recorrido[-1]}")
        self.root.update()
        time.sleep(1)
        self.restaurar_nodo(recorrido[-1])
        end_time = time.time()
        total_time = end_time - start_time
        self.lbl_estado.config(text="Recorrido finalizado", fg="green")
        self.lbl_tiempo.config(text=f"Tiempo recorrido: {total_time:.2f} segundos")

    def iluminar_nodo(self, nodo):
        self.canvas.itemconfig(self.node_objs[nodo], fill="orange")
        self.canvas.itemconfig(self.text_objs[nodo], fill="white")

    def restaurar_nodo(self, nodo):
        self.canvas.itemconfig(self.node_objs[nodo], fill="lightgray")
        self.canvas.itemconfig(self.text_objs[nodo], fill="black")

    def resaltar_arista(self, n1, n2):
        x1, y1 = self.pos[n1]
        x2, y2 = self.pos[n2]
        self.linea = self.canvas.create_line(x1, y1, x2, y2, width=4, fill="blue", tags="highlighted")

    def restaurar_arista(self):
        self.canvas.delete("highlighted")

root = tk.Tk()
app = GrafoNumeros(root)
root.mainloop()