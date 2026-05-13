import pywhatkit as kit
import pyautogui
import csv
import os
import time

ARCHIVO = "lista_clientes.csv"

def enviar_cobranza():
    if not os.path.exists(ARCHIVO):
        print(f"❌ No veo el archivo {ARCHIVO}")
        return

    with open(ARCHIVO, mode='r', encoding='utf-8') as f:
        lector = csv.DictReader(f, delimiter=';')
        
        print("--- INICIANDO COBRANZA ALBATROS V2 ---")
        
        for fila in lector:
            nombre = fila['Nombre']
            numero = fila['Telefono']
            monto = fila['Deuda']
            mensaje = f"Hola {nombre}, te recordamos tu pendiente de ${monto}. ¡Gracias!"
            
            print(f"🚀 Intentando enviar a {nombre}...")
            
            try:
                # 1. Aumentamos a 25 segundos la espera para que cargue WhatsApp
                kit.sendwhatmsg_instantly(numero, mensaje, 25, True, 5)
                
                # 2. Espera extra para asegurar que el texto ya se pegó
                time.sleep(8) 
                
                # 3. Presionamos ENTER fuerte
                pyautogui.press('enter')
                
                print(f"✅ Proceso terminado para {nombre}")
                time.sleep(10)
                
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    enviar_cobranza()