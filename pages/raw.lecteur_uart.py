import tkinter as tk
from tkinter import scrolledtext, Menu, Spinbox, Text, Radiobutton, filedialog, simpledialog, messagebox, Toplevel, StringVar
from tkinter import ttk
import threading
import datetime
import serial
import serial.tools.list_ports
import os


class UARTLoggerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Filtre Trace")
        self.geometry("600x500")

        # Application State
        self.port = "COM5"
        self.read_speed = 115200
        self.file_name = "Log_UART"
        self.case_path = "./"
        self.filters = []
        self.filter_active = False
        self.filter_type = StringVar(value="or")
        self.read_thread_event = threading.Event()

        # GUI Elements
        self.create_menu()
        self.create_top_bar()
        self.create_text_area()

    def create_top_bar(self):
        frame = tk.Frame(self, bg="lightgrey", height=30)
        frame.pack(fill="x")

        self.canvas = tk.Canvas(frame, width=20, height=20, highlightthickness=0)
        self.canvas.pack(side="left", padx=10)
        self.voyant_id = self.canvas.create_oval(2, 2, 18, 18, fill="red")

        self.label_filter = self._create_status_text(frame, "Filtre désactivé", 18)
        self.label_port = self._create_status_text(frame, f"PORT : {self.port}", 14)
        self.label_speed = self._create_status_text(frame, f"Vitesse : {self.read_speed}")

    def _create_status_text(self, parent, content, width=20):
        widget = Text(parent, height=1, width=width, bg="lightgrey")
        widget.pack(side="left")
        widget.insert(tk.END, content)
        widget.config(state="disabled")
        return widget

    def create_text_area(self):
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill='both')

    def create_menu(self):
        menubar = Menu(self)

        action_menu = Menu(menubar, tearoff=0)
        action_menu.add_command(label="Start", command=self.start_logging)
        action_menu.add_command(label="Stop", command=self.stop_logging)
        action_menu.add_separator()
        action_menu.add_command(label="Effacer", command=lambda: self.text_area.delete("1.0", tk.END))
        action_menu.add_separator()
        action_menu.add_command(label="Quitter", command=self.quit)
        menubar.add_cascade(label="Action", menu=action_menu)

        filter_menu = Menu(menubar, tearoff=0)
        filter_menu.add_command(label="ON/OFF", command=self.toggle_filter)
        filter_menu.add_command(label="Selection filtre", command=self.open_filter_window)
        menubar.add_cascade(label="Filtre", menu=filter_menu)

        settings_menu = Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Serie", command=self.open_serial_settings)
        settings_menu.add_command(label="Fichier Log", command=self.open_file_settings)
        menubar.add_cascade(label="Parametres", menu=settings_menu)

        self.config(menu=menubar)

    def update_status(self):
        self._update_text(self.label_filter, "Filtre activé" if self.filter_active else "Filtre désactivé")
        self._update_text(self.label_port, f"PORT : {self.port}")
        self._update_text(self.label_speed, f"Vitesse : {self.read_speed}")

    def _update_text(self, widget, content):
        widget.config(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, content)
        widget.config(state="disabled")

    def toggle_filter(self):
        self.filter_active = not self.filter_active
        self.update_status()

    def start_logging(self):
        self.text_area.delete("1.0", tk.END)
        try:
            serial.Serial(self.port, baudrate=self.read_speed).close()
        except Exception:
            messagebox.showerror("Erreur", "Connexion impossible au port série")
            return

        self.read_thread_event.clear()
        threading.Thread(target=self.read_uart_thread, daemon=True).start()
        self.canvas.itemconfig(self.voyant_id, fill="green")

    def stop_logging(self):
        self.read_thread_event.set()
        self.canvas.itemconfig(self.voyant_id, fill="red")

    def read_uart_thread(self):
        try:
            ser = serial.Serial(self.port, baudrate=self.read_speed)
            while not self.read_thread_event.is_set():
                with open(os.path.join(self.case_path, datetime.datetime.now().strftime('%d_%m_%Y_') + self.file_name + ".txt"), 'a') as f:
                    raw = ser.readline()
                    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    line = f"{timestamp}:: {raw.decode(errors='replace')}"
                    log_line = line.replace("\n", "")

                    if self.filter_active:
                        if self.apply_filter(line):
                            self.text_area.insert(tk.END, line)
                    else:
                        self.text_area.insert(tk.END, line)

                    f.write(log_line + "\n")
                    self.text_area.see(tk.END)
        finally:
            ser.close()

    def apply_filter(self, line):
        if self.filter_type.get() == "and":
            return all(f in line for f in self.filters)
        return any(f in line for f in self.filters)

    def open_serial_settings(self):
        window = Toplevel(self)
        window.title("Paramètres Serie")
        window.geometry("250x150")

        tk.Label(window, text="Port COM:").pack()
        ports = [p.device for p in serial.tools.list_ports.comports()]
        port_choice = ttk.Combobox(window, values=ports)
        port_choice.set(self.port)
        port_choice.pack()

        tk.Label(window, text="Vitesse:").pack()
        speeds = [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200, 256000]
        speed_choice = ttk.Combobox(window, values=speeds)
        speed_choice.set(str(self.read_speed))
        speed_choice.pack()

        def validate():
            self.port = port_choice.get()
            self.read_speed = int(speed_choice.get())
            self.update_status()
            window.destroy()

        tk.Button(window, text="Valider", command=validate).pack(pady=10)

    def open_file_settings(self):
        window = Toplevel(self)
        window.title("Paramètres Fichier Log")
        window.geometry("500x150")

        def update_display():
            self._update_text(text_path, f"Chemin : {self.case_path}")
            self._update_text(text_name, f"Nom : {self.file_name}")

        def change_path():
            path = filedialog.askdirectory(title="Choisir un dossier")
            if path:
                self.case_path = path
                update_display()

        def change_name():
            name = simpledialog.askstring("Nom du fichier", "Nouveau nom :")
            if name:
                self.file_name = name
                update_display()

        text_path = self._create_status_text(window, f"Chemin : {self.case_path}")
        tk.Button(window, text="Changer de dossier", command=change_path).pack()

        text_name = self._create_status_text(window, f"Nom : {self.file_name}")
        tk.Button(window, text="Changer de nom", command=change_name).pack()

    def open_filter_window(self):
        window = Toplevel(self)
        window.title("Filtres")
        window.geometry("300x200")

        menu_bar = tk.Frame(window, bg="lightgray")
        menu_bar.pack(fill="x")

        tk.Button(menu_bar, text="Ajouter", bg="lightgray", command=self.add_filter).pack(side="left")
        tk.Button(menu_bar, text="Effacer", bg="lightgray", command=self.clear_filters).pack(side="left")
        Radiobutton(menu_bar, text="ET", variable=self.filter_type, value="and").pack(side="left")
        Radiobutton(menu_bar, text="OU", variable=self.filter_type, value="or").pack(side="left")

        self.output_filters = Text(window, height=5, bg="light cyan")
        self.output_filters.pack(expand=True, fill="both")
        self.refresh_filter_display()

    def refresh_filter_display(self):
        self.output_filters.config(state="normal")
        self.output_filters.delete("1.0", tk.END)
        for f in self.filters:
            self.output_filters.insert(tk.END, f + "\n")
        self.output_filters.config(state="disabled")

    def add_filter(self):
        def validate():
            value = entry.get()
            if value:
                self.filters.append(value)
                self.refresh_filter_display()
                entry_window.destroy()

        entry_window = Toplevel(self)
        entry_window.title("Ajouter un filtre")
        entry = tk.Entry(entry_window)
        entry.pack(pady=5)
        tk.Button(entry_window, text="Valider", command=validate).pack(pady=5)

    def clear_filters(self):
        self.filters = []
        self.refresh_filter_display()


if __name__ == "__main__":
    app = UARTLoggerApp()
    app.mainloop()