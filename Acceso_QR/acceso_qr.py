import cv2
from pyzbar import pyzbar
import datetime
import time
import os
import csv

# --- CONFIGURACIÓN ---
ESPERA = 20 
cap = cv2.VideoCapture(0)
ultimo_acceso = 0
ARCHIVO_EXCEL = "reporte_accesos.csv"

def cargar_residentes():
    residentes = {}
    if not os.path.exists("residentes.txt"):
        with open("residentes.txt", "w") as f:
            f.write("ALBATROS-001,Capitana Albatros,Lote 10\n")
    if os.path.exists("residentes.txt"):
        with open("residentes.txt", "r") as f:
            for linea in f:
                partes = linea.strip().split(",")
                if len(partes) == 3:
                    residentes[partes[0]] = [partes[1], partes[2]]
    return residentes

def registrar_en_excel(nombre, lote, status):
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        archivo_existe = os.path.isfile(ARCHIVO_EXCEL)
        # El modo 'a' es para añadir, encoding utf-8-sig es para Excel
        with open(ARCHIVO_EXCEL, mode='a', newline='', encoding='utf-8-sig') as f:
            escritor = csv.writer(f, delimiter=';')
            if not archivo_existe:
                escritor.writerow(["Fecha y Hora", "Nombre", "Lote", "Resultado"])
            escritor.writerow([ahora, nombre, lote, status])
        print(f"✅ REGISTRO EXITOSO en Excel: {nombre} a las {ahora}")
    except Exception as e:
        print(f"❌ ERROR AL ESCRIBIR EN EXCEL: {e}")

bd = cargar_residentes()
cv2.namedWindow("Monitor de Seguridad", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Monitor de Seguridad", cv2.WND_PROP_TOPMOST, 1)

print("--- Sistema Rastreador Iniciado ---")

while True:
    ret, frame = cap.read()
    if not ret: break
    
    tiempo_actual = time.time()
    
    if tiempo_actual - ultimo_acceso > ESPERA:
        cv2.circle(frame, (30, 30), 12, (0, 255, 0), -1) 
        
        codigos = pyzbar.decode(frame)
        for objeto in codigos:
            codigo_leido = objeto.data.decode('utf-8')
            print(f"🔍 QR Detectado: {codigo_leido}") # Esto nos dirá si la cámara lo vio
            
            if codigo_leido in bd:
                nombre, lote = bd[codigo_leido][0], bd[codigo_leido][1]
                mensaje, color, status = f"ACCESO: {nombre}", (0, 255, 0), "AUTORIZADO"
            else:
                nombre, lote = "DESCONOCIDO", "N/A"
                mensaje, color, status = "ALERTA: DESCONOCIDO", (0, 0, 255), "DENEGADO"

            # Intentamos registrar
            registrar_en_excel(nombre, lote, status)
            
            # Foto
            cv2.imwrite(f"Evidencia_{datetime.datetime.now().strftime('%H%M%S')}.jpg", frame)
            
            # Visual en pantalla
            cv2.rectangle(frame, (0, 0), (frame.shape[1], 70), (0,0,0), -1)
            cv2.putText(frame, mensaje, (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            cv2.imshow("Monitor de Seguridad", frame)
            cv2.waitKey(2000)
            ultimo_acceso = tiempo_actual
    else:
        restante = int(ESPERA - (tiempo_actual - ultimo_acceso))
        cv2.rectangle(frame, (10, 15), (320, 55), (0,0,0), -1)
        cv2.putText(frame, f"SISTEMA LISTO EN: {restante}s", (25, 43), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)

    cv2.imshow("Monitor de Seguridad", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()