import os
import sys
import io
import pdfplumber
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas

# ==========================================
# CONFIGURACIÓN DE TU PRODUCTO (EDITABLE)
# ==========================================
VERSION = "2.0 Pro"
DESARROLLADOR = "CAPITANA ALBATROS"
# Esta fecha es tu seguro. Si quieres dar una prueba de 7 días, 
# cambia el mes o el día aquí.
FECHA_EXPIRACION = datetime(2026, 12, 31) 

class AplicacionComercial:
    def __init__(self, root):
        self.root = root
        self.root.title(f"RENTAR IMSS - {VERSION}")
        self.root.geometry("500x420")
        self.root.configure(bg="#f8f9fa")

        # --- BLOQUEO POR LICENCIA ---
        if datetime.now() > FECHA_EXPIRACION:
            messagebox.showerror("Licencia", "La licencia de este software ha expirado.\nContacta a Capitana Albatros para renovación.")
            sys.exit()

        # --- DISEÑO DE LA VENTANA ---
        self.main_frame = tk.Frame(root, bg="#f8f9fa")
        self.main_frame.pack(expand=True, fill="both", padx=30, pady=20)

        # Encabezado
        tk.Label(self.main_frame, text="SISTEMA PROFESIONAL IMSS", 
                 font=("Helvetica", 16, "bold"), bg="#f8f9fa", fg="#1a5276").pack(pady=10)
        tk.Label(self.main_frame, text=f"Desarrollado por: {DESARROLLADOR}", 
                 font=("Helvetica", 10, "italic"), bg="#f8f9fa", fg="#566573").pack()

        # Línea divisoria
        ttk.Separator(self.main_frame, orient='horizontal').pack(fill='x', pady=20)

        # Instrucciones
        instrucciones_txt = (
            "INSTRUCCIONES DE USO:\n\n"
            "1. Coloque los reportes PDF en la carpeta 'ENTRADA'.\n"
            "2. Presione el botón de procesar.\n"
            "3. Los archivos corregidos aparecerán en 'LISTOS'."
        )
        tk.Label(self.main_frame, text=instrucciones_txt, justify="left", 
                 font=("Helvetica", 10), bg="#f8f9fa", fg="#2c3e50").pack(pady=10)

        # Botón de Acción
        self.btn_run = tk.Button(self.main_frame, text="⚡ PROCESAR REPORTES", 
                                 command=self.procesar_archivos, 
                                 bg="#28b463", fg="white", font=("Helvetica", 12, "bold"),
                                 relief="flat", padx=25, pady=12, cursor="hand2")
        self.btn_run.pack(pady=25)

        # Barra de estado
        self.status_var = tk.StringVar(value="Estado: Sistema listo")
        self.lbl_status = tk.Label(self.main_frame, textvariable=self.status_var, 
                                   font=("Helvetica", 9), bg="#f8f9fa", fg="#7f8c8d")
        self.lbl_status.pack(side="bottom")

    def procesar_archivos(self):
        ENTRADA = "ENTRADA"
        LISTOS = "LISTOS"
        os.makedirs(ENTRADA, exist_ok=True)
        os.makedirs(LISTOS, exist_ok=True)

        archivos = [f for f in os.listdir(ENTRADA) if f.lower().endswith('.pdf')]
        
        if not archivos:
            messagebox.showwarning("Carpeta Vacía", "No se encontraron archivos PDF en la carpeta 'ENTRADA'.")
            return

        self.status_var.set("Procesando archivos... por favor espere.")
        self.root.update()

        exitos = 0
        for nombre in archivos:
            try:
                self.logica_pdf(os.path.join(ENTRADA, nombre), os.path.join(LISTOS, f"LISTO_{nombre}"))
                exitos += 1
            except Exception as e:
                print(f"Error en {nombre}: {e}")

        self.status_var.set(f"✅ Finalizado: {exitos} archivos listos")
        messagebox.showinfo("Proceso Completo", f"Se han generado {exitos} reportes con éxito.")

    def logica_pdf(self, ruta_in, ruta_out):
        # Esta es la lógica de precisión que ya perfeccionamos
        anotaciones = []
        with pdfplumber.open(ruta_in) as pdf:
            for i, pagina in enumerate(pdf.pages):
                palabras = pagina.extract_words()
                renglones = {}
                for p in palabras:
                    y_key = round(p['top'] / 3) * 3
                    if y_key not in renglones: renglones[y_key] = []
                    renglones[y_key].append(p)

                for y in renglones:
                    linea = " ".join([p['text'] for p in renglones[y]])
                    if "Fecha de alta" in linea:
                        fechas = [p['text'] for p in renglones[y] if "/" in p['text']]
                        if fechas:
                            f_alta = fechas[0]
                            target = "Vigente" if "Vigente" in linea else (fechas[1] if len(fechas) > 1 else f_alta)
                            try:
                                d1 = datetime.strptime(f_alta, "%d/%m/%Y")
                                d2 = datetime.now() if target == "Vigente" else datetime.strptime(target, "%d/%m/%Y")
                                semanas = ((d2 - d1).days + 1) // 7
                                
                                for p in renglones[y]:
                                    if target in p['text']:
                                        anotaciones.append({
                                            'p': i, 
                                            'x': p['x1'] + 10, 
                                            'y': pagina.height - p['bottom'] - 2, 
                                            'txt': f"({semanas} sem)"
                                        })
                                        break
                            except: continue

        # --- Reconstrucción del PDF ---
        reader = PdfReader(ruta_in)
        writer = PdfWriter()
        for n, pag in enumerate(reader.pages):
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=(float(pag.mediabox.width), float(pag.mediabox.height)))
            can.setFont("Helvetica-Bold", 8)
            can.setFillColorRGB(0, 0, 0.7) # Azul profesional
            
            for a in [at for at in anotaciones if at['p'] == n]:
                can.drawString(a['x'], a['y'], a['txt'])
            can.save()
            packet.seek(0)
            pag.merge_page(PdfReader(packet).pages[0])
            writer.add_page(pag)

        with open(ruta_out, "wb") as f:
            writer.write(f)

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionComercial(root)
    root.mainloop()