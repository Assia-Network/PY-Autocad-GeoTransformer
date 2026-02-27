import tkinter as tk
import win32com.client
import pythoncom
from pyproj import Transformer

# IMAGEN B64 LOGO
ICONO_B64 = "CODIGO-B64"

class AutoCADConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoCAD Geo-Detector")
        self.root.geometry("550x400")

        try:
            img_icono = tk.PhotoImage(data=ICONO_B64)
            self.root.iconphoto(True, img_icono)
        except Exception as e:
            print(f"xd - Falló el ícono. El error real es: {e}")
            pass
        # Inicializar COM para el hilo principal
        pythoncom.CoInitialize()

        # Variables de entrada con valores por defecto
        self.src_crs = tk.StringVar(value="epsg:32718")
        self.dst_crs = tk.StringVar(value="epsg:4326")

        # Interfaz de coordenadas
        frame_coords = tk.Frame(root)
        frame_coords.pack(pady=10, padx=10, fill="x")

        tk.Label(frame_coords, text="Origen (UTM):").grid(row=0, column=0, sticky="w")
        tk.Entry(frame_coords, textvariable=self.src_crs, width=15).grid(row=0, column=1, padx=5, sticky="ew")
        tk.Label(frame_coords, text="(Ej: epsg:32718 - Zona 18 Sur)", fg="gray").grid(row=0, column=2, sticky="w")

        tk.Label(frame_coords, text="Destino (Geo):").grid(row=1, column=0, sticky="w")
        tk.Entry(frame_coords, textvariable=self.dst_crs, width=15).grid(row=1, column=1, padx=5, sticky="ew")
        tk.Label(frame_coords, text="(Ej: epsg:4326 - Lat/Lon WGS84)", fg="gray").grid(row=1, column=2, sticky="w")

        # Área de resultados
        self.lbl_titulo_res = tk.Label(root, text="", font=('Arial', 10, 'bold'))
        self.lbl_titulo_res.pack(pady=(5,0))
        
        self.txt_output = tk.Text(root, height=15, state="disabled", bg="#f4f4f4")
        self.txt_output.pack(padx=10, pady=5, fill="both", expand=True)

        # Estado
        self.lbl_status = tk.Label(root, text="Buscando AutoCAD...", fg="blue")
        self.lbl_status.pack(side="bottom")

        self.last_selection_ids = set()
        
        # Iniciar el monitoreo
        self.check_selection()

    def to_gms(self, val, is_lat):
        abs_v = abs(val)
        g = int(abs_v)
        m = int((abs_v - g) * 60)
        s = (abs_v - g - m/60) * 3600
        cardinal = ("N" if val>=0 else "S") if is_lat else ("E" if val>=0 else "W")
        return f"{g}°{m}'{s:.2f}\" {cardinal}"

    def update_log(self, text, show_title=True):
        self.lbl_titulo_res.config(text="Resultados de selección actual:" if show_title else "")
        self.txt_output.config(state="normal")
        self.txt_output.delete(1.0, tk.END)
        self.txt_output.insert(tk.END, text)
        self.txt_output.config(state="disabled")

    def check_selection(self):
        try:
            acad = win32com.client.GetActiveObject("AutoCAD.Application")
            doc = acad.ActiveDocument
            
            # Usar la selección previa (Pickfirst) en lugar de crear una nueva
            # Esto lee directamente los objetos resaltados sin interferir
            selection = doc.PickfirstSelectionSet
            
            # Lógica de actualización de pantalla
            if selection.Count == 0:
                # Si presionas Esc o das clic al vacío, limpiar inmediatamente
                if self.last_selection_ids:
                    self.update_log("", show_title=False)
                    self.last_selection_ids = set()
                self.lbl_status.config(text=f"Conectado a: {doc.Name} | Esperando selección...", fg="green")
            
            else:
                # Extraer ObjectIDs reales
                current_ids = {selection.Item(i).ObjectID for i in range(selection.Count)}

                # Si la selección es nueva o diferente
                if current_ids != self.last_selection_ids:
                    self.process_objects(selection)
                    self.last_selection_ids = current_ids
                
                self.lbl_status.config(text=f"Conectado a: {doc.Name} | {selection.Count} objeto(s)", fg="blue")

        except Exception:
            # Pasa en silencio si AutoCAD está cerrado o bloqueado temporalmente
            pass 
        
        # Para repetir bucle cada 300 ms
        self.root.after(300, self.check_selection)

    def process_objects(self, selection):
        try:
            transformer = Transformer.from_crs(self.src_crs.get(), self.dst_crs.get(), always_xy=True)
            output = ""
            
            for i in range(selection.Count):
                obj = selection.Item(i)
                try:
                    point = obj.InsertionPoint
                    e, n = point[0], point[1]
                    
                    lon, lat = transformer.transform(e, n)
                    
                    output += f"Objeto: {obj.ObjectName}\n"
                    output += f"UTM: E={e:.2f}, N={n:.2f}\n"
                    output += f"DEC: Lat={lat:.6f}, Lon={lon:.6f}\n"
                    output += f"GMS: {self.to_gms(lat, True)}, {self.to_gms(lon, False)}\n"
                    output += "-" * 40 + "\n"
                except:
                    continue
            
            if not output:
                output = "El objeto seleccionado no tiene un punto de inserción válido (ej. Polilínea o Línea simple)."
            
            self.update_log(output, show_title=True)
            
        except Exception as e:
            self.update_log(f"Error procesando coordenadas.\nDetalle: {str(e)}", show_title=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoCADConverterApp(root)
    root.mainloop()

# python -m nuitka --onefile --windows-console-mode=disable --enable-plugin=tk-inter --windows-icon-from-ico=ico.ico --include-package-data=pyproj convertidor.py