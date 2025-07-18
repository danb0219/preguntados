import tkinter as tk
import json
import random
from tkinter import messagebox
import datetime


class TriviaGame:
    def on_enter(self, event):
        event.widget['background'] = '#2a6496'

    def on_leave(self, event):
        event.widget['background'] = '#3c8dbc'

    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#1e1e2f")
        self.root.title("Preguntados")
        self.root.geometry("600x550")

        self.puntaje = 0
        self.indice_pregunta = 0
        self.preguntas_seleccionadas = []
        self.nivel_actual = ""
        self.total_preguntas =0 
        self.temporizador_id = None
        self.tiempo_restante = 15
        self.nombre_jugador_actual = ""
        self.ranking_window = None

        try:
            with open("preguntas.json", "r", encoding="utf-8") as f:
                self.preguntas = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", "El archivo 'preguntas.json' no se encontró. Asegúrate de que está en el mismo directorio.")
            self.root.destroy()
            return

        self.setup_ui()

    def setup_ui(self):
        self.etiqueta_bienvenida = tk.Label(self.root, text="Selecciona la dificultad", font=("Helvetica", 16),
                                             bg="#1e1e2f", fg="white")
        self.etiqueta_bienvenida.pack(pady=20)

        self.etiqueta_nombre = tk.Label(self.root, text="Introduce tu nombre:", font=("Helvetica", 12),
                                        bg="#1e1e2f", fg="white")
        self.etiqueta_nombre.pack(pady=5)

        self.entrada_nombre = tk.Entry(self.root, width=30, font=("Helvetica", 12))
        self.entrada_nombre.pack(pady=5)
        self.entrada_nombre.insert(0, "Jugador1")

        self.botones_dificultad = []
        niveles = [("Fácil", 10), ("Medio", 20), ("Dificil", 40), ("God💀", 100)]

        for texto, cantidad in niveles:
            btn = tk.Button(self.root, text=f"{texto} ({cantidad} preguntas)", width=25, font=("Helvetica", 12),
                            bg="#3c8dbc", fg="white", activebackground="#2a6496", activeforeground="white",
                            command=lambda c=cantidad, t=texto: self.iniciar_juego(c, t))
            btn.bind("<Enter>", self.on_enter)
            btn.bind("<Leave>", self.on_leave)
            btn.pack(pady=5)
            self.botones_dificultad.append(btn)

        self.etiqueta_pregunta = tk.Label(self.root, text="", font=("Helvetica", 14), bg="#1e1e2f", fg="white",
                                          wraplength=550, justify="center")

        self.botones_opciones = []
        for _ in ["A", "B", "C", "D"]:
            btn = tk.Button(self.root, width=50, font=("Helvetica", 11),
                            bg="#3c8dbc", fg="white", activebackground="#2a6496", activeforeground="white")
            btn.bind("<Enter>", self.on_enter)
            btn.bind("<Leave>", self.on_leave)
            self.botones_opciones.append(btn)

        self.etiqueta_resultado = tk.Label(self.root, text="", font=("Helvetica", 12), bg="#1e1e2f", fg="white")
        self.etiqueta_tiempo = tk.Label(self.root, text="", font=("Helvetica", 12, "bold"), bg="#1e1e2f",
                                        fg="#ff5252")

        self.boton_siguiente = tk.Button(self.root, text="Siguiente", font=("Helvetica", 12),
                                         bg="#3c8dbc", fg="white", activebackground="#2a6496", activeforeground="white",
                                         state="disabled", command=self.siguiente_pregunta)
        self.boton_siguiente.bind("<Enter>", self.on_enter)
        self.boton_siguiente.bind("<Leave>", self.on_leave)

    def iniciar_temporizador(self):
        if self.temporizador_id:
            self.root.after_cancel(self.temporizador_id)

        self.tiempo_restante = 15
        self.actualizar_temporizador()

    def actualizar_temporizador(self):
        if self.tiempo_restante > 0:
            self.etiqueta_tiempo.config(text=f"Tiempo restante: {self.tiempo_restante} segundos")
            self.tiempo_restante -= 1
            self.temporizador_id = self.root.after(1000, self.actualizar_temporizador)
        else:
            self.etiqueta_tiempo.config(text="¡Tiempo agotado!", fg="#ff5252")
            for btn in self.botones_opciones:
                btn.config(state="disabled")
            self.boton_siguiente.config(state="normal")
            self.etiqueta_resultado.config(text="❌ ¡Se acabó el tiempo!", fg="#ff5252")

    def iniciar_juego(self, cantidad_preguntas, nivel):
        nombre_jugador = self.entrada_nombre.get().strip()
        if not nombre_jugador:
            messagebox.showwarning("Advertencia", "Por favor, introduce tu nombre para empezar a jugar.")
            return
        self.nombre_jugador_actual = nombre_jugador

        if len(self.preguntas) < cantidad_preguntas:
            messagebox.showwarning("Advertencia", f"No hay suficientes preguntas. Necesitas al menos {cantidad_preguntas}.")
            return

        self.nivel_actual = nivel
        self.puntaje = 0
        self.indice_pregunta = 0
        self.preguntas_seleccionadas = random.sample(self.preguntas, cantidad_preguntas)
        self.total_preguntas = len(self.preguntas_seleccionadas)

        self.etiqueta_bienvenida.pack_forget()
        self.etiqueta_nombre.pack_forget()
        self.entrada_nombre.pack_forget()

        for btn in self.botones_dificultad:
            btn.pack_forget()

        self.etiqueta_pregunta.pack(pady=20)
        for btn in self.botones_opciones:
            btn.pack(pady=5)
        self.etiqueta_resultado.pack(pady=15)
        self.etiqueta_tiempo.pack(pady=5)
        self.boton_siguiente.pack()

        self.mostrar_pregunta_actual()

    def mostrar_pregunta_actual(self):
        if self.indice_pregunta < self.total_preguntas:
            pregunta = self.preguntas_seleccionadas[self.indice_pregunta]
            self.etiqueta_pregunta.config(text=pregunta["pregunta"])
            self.etiqueta_resultado.config(text="")

            opciones_dict = pregunta["opciones"]
            opciones_list = list(opciones_dict.items())
            random.shuffle(opciones_list)

            letras_botones = ["A", "B", "C", "D"]

            for i, (original_letra, texto) in enumerate(opciones_list):
                letra_mostrar = letras_botones[i]
                self.botones_opciones[i].config(
                    text=f"{letra_mostrar}. {texto}",
                    state="normal",
                    command=lambda l=original_letra: self.verificar_respuesta(l)
                )

            self.boton_siguiente.config(state="disabled")
            self.iniciar_temporizador()
        else:
            self.finalizar_juego()

    def verificar_respuesta(self, letra_seleccionada_original):
        if self.temporizador_id:
            self.root.after_cancel(self.temporizador_id)
            self.temporizador_id = None

        pregunta = self.preguntas_seleccionadas[self.indice_pregunta]
        letra_correcta = pregunta["respuesta_correcta"]
        texto_correcto = pregunta["opciones"][letra_correcta]

        if letra_seleccionada_original == letra_correcta:
            self.puntaje += 1
            self.etiqueta_resultado.config(
                text=f"✅Respuesta correcta (+1 punto)",
                fg="#00e676"
            )
        else:
            self.etiqueta_resultado.config(
                text=f"❌Respuesta incorrecta. La respuesta correcta era {letra_correcta}. {texto_correcto}",
                fg="#ff5252"
            )
        for btn in self.botones_opciones:
            btn.config(state="disabled")

        self.boton_siguiente.config(state="normal")

    def siguiente_pregunta(self):
        self.indice_pregunta += 1
        self.mostrar_pregunta_actual()
    
    def _generar_texto_ranking(self):
        rankings_por_dificultad = {
            "Fácil": [],
            "Medio": [],
            "Dificil": [],
            "God💀": []
        }

        try:
            with open("resultados.txt", "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        parts_fecha_jugador = line.strip().split("] Jugador: ")
                        if len(parts_fecha_jugador) < 2:
                            continue
                        fecha_hora = parts_fecha_jugador[0].replace("[", "").strip()

                        resto_jugador_dificultad = parts_fecha_jugador[1].split(" - Dificultad: ")
                        if len(resto_jugador_dificultad) < 2:
                            continue
                        nombre_jugador = resto_jugador_dificultad[0].strip()

                        resto_dificultad_puntuacion = resto_jugador_dificultad[1].split(" - Puntuación: ")
                        if len(resto_dificultad_puntuacion) < 2:
                            continue
                        dificultad = resto_dificultad_puntuacion[0].strip()

                        resto_puntuacion_porcentaje = resto_dificultad_puntuacion[1].split(" - Porcentaje: ")
                        if len(resto_puntuacion_porcentaje) < 2:
                            continue
                        puntuacion_str = resto_puntuacion_porcentaje[0].strip()
                        porcentaje_str = resto_puntuacion_porcentaje[1].replace("%", "").strip()

                        puntaje_num = int(puntuacion_str.split('/')[0])
                        total_preguntas_num = int(puntuacion_str.split('/')[1])
                        porcentaje_num = float(porcentaje_str)

                        if dificultad in rankings_por_dificultad:
                            rankings_por_dificultad[dificultad].append({
                                "fecha": fecha_hora,
                                "nombre": nombre_jugador,
                                "puntaje": puntaje_num,
                                "total": total_preguntas_num,
                                "porcentaje": porcentaje_num
                            })
                    except Exception as e:
                        print(f"[WARNING] Línea inválida ignorada:\n{line.strip()}\n→ {e}")
                        continue
      
        except FileNotFoundError:
            return "No hay resultados guardados aún."
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo de resultados: {str(e)}")
            return "Error al cargar el ranking."


        ranking_mensaje = "🏆 Tabla de Clacificación🏆\n\n"


        for dificultad, resultados in rankings_por_dificultad.items():
            if resultados:
                resultados_ordenados = sorted(resultados, key=lambda r: r["porcentaje"], reverse=True)
                ranking_mensaje += f"--- {dificultad} ---\n"
                for i, r in enumerate(resultados_ordenados[:5]):
                    ranking_mensaje += (
                        f"{i+1}. {r['nombre']}/{r['fecha']}) - "
                        f"Puntuación: {r['puntaje']}/{r['total']} ({r['porcentaje']:.1f}%)\n"
                    )
                ranking_mensaje += "\n"

        if all(not val for val in rankings_por_dificultad.values()):
            ranking_mensaje += "Aún no hay resultados guardados. ¡Juega para empezar!"
        

        return ranking_mensaje

    def finalizar_juego(self):
        self.guardar_resultado()

        self.etiqueta_pregunta.pack_forget()
        for btn in self.botones_opciones:
            btn.pack_forget()
        self.boton_siguiente.pack_forget()
        self.etiqueta_tiempo.pack_forget()

        porcentaje = (self.puntaje / self.total_preguntas) * 100
        mensaje = (
            f"🎉 Juego terminado!\n\n"
            f"Tu puntaje final es: {self.puntaje}/{self.total_preguntas}\n"
            f"Porcentaje: {porcentaje:.1f}%\n"
            f"Dificultad: {self.nivel_actual}\n"
        )

        self.etiqueta_resultado.config(
            text=mensaje,
            font=("Helvetica", 14),
            fg="purple"
        )

        self.mostrar_ranking_en_ventana()

    def guardar_resultado(self):
        try:
            now = datetime.datetime.now()
            fecha_hora_str = now.strftime("%Y-%m-%d %H:%M:%S")
            with open("resultados.txt", "a", encoding="utf-8") as f:
                f.write(
                    f"[{fecha_hora_str}] Jugador: {self.nombre_jugador_actual} - "
                    f"Dificultad: {self.nivel_actual} - "
                    f"Puntuación: {self.puntaje}/{self.total_preguntas} - "
                    f"Porcentaje: {(self.puntaje / self.total_preguntas) * 100:.1f}%\n"
                )
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el resultado: {str(e)}")

    def mostrar_ranking_en_ventana(self):
        if self.ranking_window and self.ranking_window.winfo_exists():
            self.ranking_window.lift()
            return

        self.ranking_window = tk.Toplevel(self.root)
        self.ranking_window.title("Tabla de Clasificación Global")
        self.ranking_window.geometry("600x600")
        self.ranking_window.configure(bg="#f5f5f5")

        ranking_texto = self._generar_texto_ranking()

        ranking_display = tk.Text(self.ranking_window, font=("Helvetica", 12), wrap="word",height=25, width=70)
        ranking_display.insert(tk.END, ranking_texto)
        ranking_display.config(state="disable", bg= "white")
        ranking_display.pack(pady=10, padx=10, fill="both", expand=True)

        btn_frame = tk.Frame(self.ranking_window, bg="#f5f5f5")
        btn_frame.pack(pady=10)

        btn_reiniciar = tk.Button(
            btn_frame, text="Reiniciar Juego", command=self.reiniciar_juego,
            font=("Helvetica", 12), bg="#3c8dbc", fg="white",
            activebackground="#2a6496", activeforeground="white", width=15
        )
        btn_reiniciar.bind("<Enter>", self.on_enter)
        btn_reiniciar.bind("<Leave>", self.on_leave)
        btn_reiniciar.pack(side="left", padx=10)

        btn_salir = tk.Button(
            btn_frame, text="Salir", command=self.salir_del_juego,
            font=("Helvetica", 12), bg="#3c8dbc", fg="white",
            activebackground="#2a6496", activeforeground="white", width=15
        )
        btn_salir.bind("<Enter>", self.on_enter)
        btn_salir.bind("<Leave>", self.on_leave)
        btn_salir.pack(side="right", padx=10)

    def salir_del_juego(self):
        if messagebox.askyesno("Salir", "¿Estás seguro de que quieres salir del juego?"):
            self.root.destroy()

    def reiniciar_juego(self):
        self.cerrar_ranking_window()

        if self.temporizador_id:
            self.root.after_cancel(self.temporizador_id)
            self.temporizador_id = None
        self.etiqueta_tiempo.config(text="")

        self.etiqueta_resultado.pack_forget()
        self.etiqueta_resultado.config(text="", font=("Helvetica", 12), fg="blue")
        self.etiqueta_resultado.pack(pady=15)

        self.etiqueta_bienvenida.pack(pady=20)
        self.etiqueta_nombre.pack(pady=5)
        self.entrada_nombre.pack(pady=5)
        self.entrada_nombre.delete(0, tk.END)
        self.entrada_nombre.insert(0, "Jugador1")

        for btn in self.botones_dificultad:
            btn.pack(pady=5)

    def cerrar_ranking_window(self):
        if self.ranking_window:
            self.ranking_window.destroy()
            self.ranking_window = None


if __name__ == "__main__":
    root = tk.Tk()
    juego = TriviaGame(root)
    root.mainloop()
