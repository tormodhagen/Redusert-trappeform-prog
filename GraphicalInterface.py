import tkinter as tk
from tkinter import messagebox
import numpy as np
import math
from GaussJordan import GaussJordan

class StepByStepViewer:
    def __init__(self, steps):
        self.steps = steps
        self.step = 0
        self.root = tk.Toplevel()
        self.root.title("Gauss-Jordan Visualisering")

        self.instr_label = tk.Label(self.root, text="", font=("Courier", 12), justify="left")
        self.instr_label.pack(padx=10, pady=10)

        self.frame_matrices = tk.Frame(self.root)
        self.frame_matrices.pack()

        self.text_prev = tk.Text(self.frame_matrices, width=40, height=10, font=("Courier", 14))
        self.text_prev.grid(row=0, column=0, padx=5)
        self.text_arrow = tk.Label(self.frame_matrices, text="→", font=("Courier", 16))
        self.text_arrow.grid(row=0, column=1, padx=5)
        self.text_curr = tk.Text(self.frame_matrices, width=40, height=10, font=("Courier", 14))
        self.text_curr.grid(row=0, column=2, padx=5)

        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack(pady=5)
        self.prev_btn = tk.Button(frame_buttons, text="<< Forrige", command=self.prev_step)
        self.prev_btn.pack(side="left", padx=5)
        self.next_btn = tk.Button(frame_buttons, text="Neste >>", command=self.next_step)
        self.next_btn.pack(side="left", padx=5)

        self.show_step()

    def show_step(self):
        if 0 <= self.step < len(self.steps):
            step_data = self.steps[self.step]
            self.instr_label.config(text=f"Steg {self.step+1}: {step_data['instr']}")
            self._update_matrix_text(self.text_prev, step_data['prev'])
            self._update_matrix_text(self.text_curr, step_data['curr'], highlight=step_data['highlight'])
        else:
            self.instr_label.config(text="Ferdig!")

    def _update_matrix_text(self, text_widget, matrix, highlight=None):
        text_widget.config(state="normal")
        text_widget.delete("1.0", tk.END)
        for i, row in enumerate(matrix):
            row_str = "\t".join(f"{x:6.2f}" for x in row)
            text_widget.insert(tk.END, row_str + "\n")
        if highlight is not None:
            start = f"{highlight+1}.0"
            end = f"{highlight+1}.end"
            text_widget.tag_add("highlight", start, end)
            text_widget.tag_config("highlight", background="yellow")
        text_widget.config(state="disabled")

    def next_step(self):
        if self.step < len(self.steps) - 1:
            self.step += 1
            self.show_step()

    def prev_step(self):
        if self.step > 0:
            self.step -= 1
            self.show_step()


class MatrixSolverApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gauss-Jordan Matriseløser - godtar uttrykk samt math og numpy konstanter i input")
        self.matrix_entries = []
        self.viewer = None

        frame_dim = tk.Frame(self.root)
        frame_dim.pack(pady=5)
        tk.Label(frame_dim, text="Antall rader (m):").pack(side="left")
        self.entry_m = tk.Entry(frame_dim, width=5)
        self.entry_m.pack(side="left", padx=5)
        tk.Label(frame_dim, text="Antall kolonner (n):").pack(side="left")
        self.entry_n = tk.Entry(frame_dim, width=5)
        self.entry_n.pack(side="left", padx=5)
        self.btn_create_matrix = tk.Button(self.root, text="Lag matrise", command=self.create_matrix_entries)
        self.btn_create_matrix.pack(pady=5)

    def create_matrix_entries(self):
        # Remove old matrix frame if it exists
        if hasattr(self, "frame_matrix") and self.frame_matrix is not None:
            self.frame_matrix.destroy()
        if hasattr(self, "submit_btn") and self.submit_btn is not None:
            self.submit_btn.destroy()
                   
        try:
            m = int(self.entry_m.get())
            n = int(self.entry_n.get())
        except ValueError:
            messagebox.showerror("Feil", "Må angi gyldige heltall for m og n")
            return

        for row in self.matrix_entries:
            for e in row:
                e.destroy()
        self.matrix_entries = []

        frame_matrix = tk.Frame(self.root)
        frame_matrix.pack(pady=5)
        self.frame_matrix = frame_matrix

        for i in range(m):
            row_entries = []
            for j in range(n):
                e = tk.Entry(frame_matrix, width=8)
                e.grid(row=i, column=j, padx=2, pady=2)
                e.insert(0, "0")
                row_entries.append(e)
            self.matrix_entries.append(row_entries)

        self.submit_btn = tk.Button(self.root, text="Kjør RREF", command=self.run_gauss_jordan)
        self.submit_btn.pack(pady=5)

    def run_gauss_jordan(self):
        m = len(self.matrix_entries)
        n = len(self.matrix_entries[0])
        A = np.zeros((m, n), dtype=float)

        for i in range(m):
            for j in range(n):
                val_str = self.matrix_entries[i][j].get()
                try:
                    A[i, j] = eval(val_str, {"__builtins__": None}, {**math.__dict__, **np.__dict__})
                except Exception:
                    messagebox.showerror("Feil", f"Ugyldig verdi i rad {i+1}, kolonne {j+1}: {val_str}")
                    return

        gj = GaussJordan(A)
        rref, steps = gj.compute_rref_with_highlight()

        if self.viewer:
            self.viewer.root.destroy()
        self.viewer = StepByStepViewer(steps)

    def start(self):
        self.root.mainloop()
