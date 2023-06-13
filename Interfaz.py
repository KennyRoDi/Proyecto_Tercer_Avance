#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#SE IMPORTAN LAS LIBRERIAS Y FUNCIONES DE OTROS ARCHIVOS HACIA ESTE ARCHIVO
import tkinter.messagebox as messagebox
import customtkinter as ctk
from nuevaAgenda import crear_agenda, agregar_participante, agregar_apartado, agregar_puntos, participante_asList, puntos_asDict, crear_discusion
from datetime import datetime

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class VentanaPrincipal:
    """Clase que crea la ventana principal de la aplicación
    """
    def __init__(self):
        """Constructor de la clase VentanaPrincipal"""
        # SE CREA LA VENTANA PRINCIPAL Y SE LE DA UN TAMAÑO Y UN TITULO
        self.ventana_principal = ctk.CTk()
        self.ventana_principal.geometry("800x600")
        self.ventana_principal.title("Agenda para sesiones de órganos colegiados")
        self.ventana_principal._set_appearance_mode("dark")

        # SE CREA EL BOTON DE OPCIONES Y SE LE DA UN TAMAÑO Y UNA POSICION, CONJUNTO DE TODA SU CONFIGURACION Y DETALLES
        self.btn_opciones = ctk.CTkSegmentedButton(self.ventana_principal, selected_color="red", values=["Apartados", "Participantes", "Discusiones"], command=lambda value: self.botones_opciones(value))
        self.btn_opciones.configure(unselected_color="blue", font=("Arial", 15), fg_color="sky blue", corner_radius=10, border_width=5)
        self.btn_opciones.pack(side="top", fill="x", padx=30, pady=70)

        # SE CREA EL LABEL DE NOMBRE DE LA AGENDA Y SE LE DA UNA POSICION Y UNA CONFIGURACION
        self.nombre_agenda = ctk.CTkLabel(self.ventana_principal, text="Nombre Agenda:", bg_color="cyan", font=("Arial", 18, "bold"))
        self.nombre_agenda.place(x=20, y=20)

        # SE CREA EL BOTON DE AGREGAR NOMBRE DE LA AGENDA Y SE LE DA UNA POSICION Y UNA CONFIGURACION
        self.btn_agregar_agenda = ctk.CTkButton(self.ventana_principal, text="Agregar nombre de la agenda", command=self.agregar_nombre_agenda)
        self.btn_agregar_agenda.place(x=440, y=20)
        self.btn_agregar_agenda.configure(fg_color="black")

        # SE CREA EL BOTON DE GUARDAR Y SE LE DA UNA POSICION Y UNA CONFIGURACION
        self.btn_guardar_agenda = ctk.CTkButton(self.ventana_principal, text="Guardar", command= self.guardar_agenda)
        self.btn_guardar_agenda.place(x=640, y=20)
        self.btn_guardar_agenda.configure(fg_color="black")

        # SE CREA LA VARIABLE DE INSTANCIA PARA LA BARRA DE ENTRADA DE LA AGENDA
        self.agenda_nombre_asignado = False  # VARIABLE DE INSTANCIA PARA SABER SI SE HA ASIGNADO UN NOMBRE A LA AGENDA

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def botones_opciones(self, value):
        """Función que se ejecuta cuando se presiona un botón del SegmentedButton de opciones de la ventana principal
        """
        if not self.agenda_nombre_asignado:  # Verificar si se ha asignado un nombre a la agenda
            messagebox.showerror("Error", "Debe asignar un nombre a la agenda primero.")
            return
        VentanaSecundaria(self.ventana_principal, value, self.btn_opciones) # aca se ejecutan las opciones de menu de acuerdo a lo que presione el usuario

    def agregar_nombre_agenda(self):
        """Función que se ejecuta cuando se presiona el botón de agregar nombre de la agenda"""
        self.barra_agenda = ctk.CTkEntry(self.ventana_principal, width=250, placeholder_text="Ingrese el nombre de la agenda", justify="center")
        self.barra_agenda.place(x=180, y=20)
        self.btn_agregar_agenda.configure(state="disabled")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def guardar_agenda(self):
        """Función que se ejecuta al presionar el botón de guardar"""
        if not hasattr(self, 'barra_agenda') or not self.barra_agenda:
            messagebox.showerror("Error", "Debe ingresar un nombre para la agenda.")
            return

        titulo_agenda = self.barra_agenda.get()  # Obtener el título de la agenda desde la barra de entrada

        if not titulo_agenda:
            messagebox.showerror("Error", "El nombre de la agenda no puede estar vacío.")
            return

        fecha_agenda = datetime.now()  # Obtener la fecha actual

        self.label_fecha = ctk.CTkLabel(self.ventana_principal, text=fecha_agenda.strftime("%d/%m/%Y %H:%M:%S"), fg_color="light green", font=("Arial", 16, "bold"))
        self.texto_fecha_label = ctk.CTkLabel(self.ventana_principal, text= "Fecha y hora: ", font=("Arial", 18, "bold"), fg_color= "cyan")
        self.label_fecha.place(x=630, y=20)
        self.texto_fecha_label.place(x=500, y=20)

        crear_agenda(titulo_agenda, fecha_agenda)  # Llamar a la función "crear_agenda" con los valores obtenidos

        self.barra_agenda.destroy()
        self.btn_agregar_agenda.destroy()
        self.btn_guardar_agenda.destroy()
        self.label_agenda = ctk.CTkLabel(self.ventana_principal, text=titulo_agenda, fg_color="light green", font=("Arial", 20, "bold"))
        self.label_agenda.place(x=200, y=20)

        self.agenda_nombre_asignado = True  # Cambiar el valor de la variable de instancia a True

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class VentanaSecundaria:
    """Clase que crea la ventana secundaria de la aplicación"""

    def __init__(self, ventana_principal, value, btn_opciones):
        """Constructor de la clase VentanaSecundaria"""
        self.participantes_sesion = participante_asList() # se almacenan los participantes en listas para poder ser elegidos
        self.diccionario_apartados_puntos = puntos_asDict()
        self.apartados_sesion = list(self.diccionario_apartados_puntos.keys())
        self.puntos_sesion = []

        self.frame_ventana_secundaria = ctk.CTkFrame(ventana_principal, fg_color="gray")
        self.frame_ventana_secundaria.place(x=30, y=110, relwidth=btn_opciones.winfo_width() / ventana_principal.winfo_width(), relheight=0.75)
        self.barra_discusion = None  # VARIABLE PARA AGREGAR DISCUSIONES EN APARTADOS
        self.entries = None

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

        # Ventana Apartados

        if value == "Apartados":
            #SE CREA EL LABEL APARTADOS
            self.label_apartados = ctk.CTkLabel(self.frame_ventana_secundaria, bg_color="green", text=" Ingrese los apartados: ", font=("Arial", 15))
            self.label_apartados.place(x=10, y=10) # se le da una ubicacion

            self.label_puntos = ctk.CTkLabel(self.frame_ventana_secundaria, bg_color= "green", text=" ¿Cuántos puntos desea agregar? ", font=("Arial", 15)) # se crea un label para preguntar cuantos puntos se desean agregar
            self.label_puntos.place(x=10, y=50) # se le da una ubicacion

            self.barra_entrada_puntos = ctk.CTkEntry(self.frame_ventana_secundaria, width=250, placeholder_text= "Ingrese el numero de puntos", justify="center")
            self.barra_entrada_puntos.place(x=250, y=50) # se le da una ubicacion

            self.barra_entrada = ctk.CTkEntry(self.frame_ventana_secundaria, width=250, placeholder_text="Ingrese el apartado", justify="center") # se crea una barra deentrada para los apartados
            self.barra_entrada.place(x=250, y=10) # Creamos la barra de entrada

            self.btn_agregar_puntos = ctk.CTkButton(self.frame_ventana_secundaria, text="Agregar Puntos", command=self.crear_entradas_puntos)
            self.btn_agregar_puntos.place(x=520, y=50) # se le da una ubicacion

            self.btn_guardar = ctk.CTkButton(self.frame_ventana_secundaria, text="Guardar", command= self.guardar_puntos_apartados) # se crea el boton guardar para guardar la informacion en la opcion de menu
            self.btn_guardar.place(x=520, y= 10) # Le damos una posicion al boton de guardar

            self.btn_eliminar = ctk.CTkButton(self.frame_ventana_secundaria, text="Eliminar") # se crea el boton eliminar
            self.btn_eliminar.place(x=520, y=90) # se le da una posicion

        # Ventana participantes

        elif value == "Participantes":
            self.nombre = ctk.CTkLabel(self.frame_ventana_secundaria, text="Nombre: ", font=("Arial", 15), bg_color="green") # se crea un label para pedir el nombre
            self.apellido1 = ctk.CTkLabel(self.frame_ventana_secundaria, text="Primer Apellido: ", font=("Arial", 15), bg_color="green") # se crea un label para pedir el apellido 1
            self.apellido2 = ctk.CTkLabel(self.frame_ventana_secundaria, text="Segundo Apellido: ", font=("Arial", 15), bg_color="green") # se crea un label para pedir el apellido 2

            self.nombre.place(x=10, y=10) # se le da una ubicacion al label de nombre
            self.apellido1.place(x=10, y=60) # se le da una ubicacion al label de apellido 1
            self.apellido2.place(x=10, y=110) # se le da una ubicacion al label de apellido 2

            self.barra_entrada_nombre = ctk.CTkEntry(self.frame_ventana_secundaria, width=250, placeholder_text="Ingrese el nombre", justify="center") # se crea una barra de entrada para colocar el nombre
            self.barra_entrada_apellido1 = ctk.CTkEntry(self.frame_ventana_secundaria, width=250, placeholder_text="Ingrese el primer apellido", justify="center") # se crea una barra de entrada para colocar el apellido1
            self.barra_entrada_apellido2 = ctk.CTkEntry(self.frame_ventana_secundaria, width=250, placeholder_text="Ingrese el segundo apellido", justify="center") # se crea una barra de entrada para colocar el apellido2

            self.barra_entrada_nombre.place(x=220, y=10) # le damos una ubicacion a la barra de entrada del nombre
            self.barra_entrada_apellido1.place(x=220, y=60) # le damos una ubicacion a la barra de entrada de apellido 1
            self.barra_entrada_apellido2.place(x=220, y=110) # le damos una ubicacion a la barra de entrada de apellido 2

            self.btn_guardar = ctk.CTkButton(self.frame_ventana_secundaria, text="Guardar", command= self.agregar_participante) # se crea el boton de guardar
            self.btn_guardar.place(x=520, y=10) # se le da una ubicacion al boton de guardar

            self.btn_eliminar = ctk.CTkButton(self.frame_ventana_secundaria, text="Eliminar") # se crea el boton de eliminar
            self.btn_eliminar.place(x=520, y=45) # se le da una ubicacion

        # Ventana Discusiones

        elif value == "Discusiones":
            self.label_seleccionar_apartados = ctk.CTkLabel(self.frame_ventana_secundaria, text=" Seleccione el apartado: ", font=("Arial", 15), bg_color="orange") # se crea el label que indica seleccionar el apartado
            self.label_seleccionar_punto = ctk.CTkLabel(self.frame_ventana_secundaria, text=" Seleccione el punto: ", font=("Arial", 15), bg_color="orange") # se crea el label que indica seleccionar el punto
            self.label_seleccionar_participante = ctk.CTkLabel(self.frame_ventana_secundaria, text=" Seleccione el participante: ", font=("Arial", 15), bg_color="orange") # se crea el label que indica seleccionar el participante
            self.label_seleccionar_discusiones = ctk.CTkLabel(self.frame_ventana_secundaria, text=" Seleccione la discusión: ", font=("Arial", 15), bg_color="orange") # se crea el label que indicia seleccionar la discusion
            self.discusion = ctk.CTkLabel(self.frame_ventana_secundaria, text=" Discusion: ", font=("Arial", 15), bg_color="orange") # se crea el label que indica la discusion que se va a crear

            self.menu_opciones_apartados = ctk.CTkOptionMenu(self.frame_ventana_secundaria, values= self.apartados_sesion, dropdown_fg_color="cyan")  # se crea el menu de apartados
            self.menu_opciones_puntos = ctk.CTkOptionMenu(self.frame_ventana_secundaria, values= self.puntos_sesion, dropdown_fg_color="cyan")  # se crea el menu de puntos
            self.menu_opciones_participantes = ctk.CTkOptionMenu(self.frame_ventana_secundaria, values= self.participantes_sesion, dropdown_fg_color="cyan")  # se crea el menu de participantes
            self.menu_opciones_discusion = ctk.CTkOptionMenu(self.frame_ventana_secundaria, values=["Discusiones"], dropdown_fg_color="cyan")  # se crea el menu de discusiones

            self.label_seleccionar_apartados.place(x=50, y=10) # se le da una ubicacion al label de seleccionar
            self.label_seleccionar_punto.place(x=50, y=80) # se le da una ubicaion al label al label de seleccionar punto
            self.label_seleccionar_participante.place(x=50, y=150) # se le da una ubicacion al label de seleccionar participante
            self.label_seleccionar_discusiones.place(x=50, y=210) # se le da una ubicacion al label de seleccionar discusiones
            self.discusion.place(x=50, y=260) # se la da una ubicacion al label de donde se ingresan las discusiones

            self.menu_opciones_apartados.place(x=250, y=10) # se le da una ubicacion al menu de apartados
            self.menu_opciones_puntos.place(x=250, y=80) # se le da una ubicacion al menu de puntos
            self.menu_opciones_participantes.place(x=250, y=150) # se le da una ubicacion al menu de participantes
            self.menu_opciones_discusion.place(x=250, y=210) # se le da una ubicacion al menu de discusiones

            self.btn_guardar = ctk.CTkButton(self.frame_ventana_secundaria, text="Guardar", command=self.agregar_discusion) # se crea el boton guardar
            self.btn_guardar.place(x=520, y=10) # se le da una ubicacion

            self.btn_eliminar = ctk.CTkButton(self.frame_ventana_secundaria, text="Eliminar") # se crea el boton de eliminar
            self.btn_eliminar.place(x=520, y=45) # se le da una ubicacion

            self.btn_modificar = ctk.CTkButton(self.frame_ventana_secundaria, text="Modificar", command=self.desplegar_entrada_discusion) # se crea el boton de modificar
            self.btn_modificar.place(x=520, y=80) # se le da una ubicacion

            self.btn_imprimir = ctk.CTkButton(self.frame_ventana_secundaria, text= "Imprimir en HTML") # se crea un boton de imprimir HTML
            self.btn_imprimir.place(x=520, y=115) # se le da una ubicaion al boton

            self.btn_actualizar_puntos = ctk.CTkButton(self.frame_ventana_secundaria, text="Puntos", command= self.actualizar_puntos)
            self.btn_actualizar_puntos.place(x=520, y=160)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def crear_entradas_puntos(self):
        """Funcion que se encarga de crear las barras de entrada para indicar cuantos puntos se quieren agregar para un apartado
        """
        num_puntos = self.barra_entrada_puntos.get()  # Obtener el número de puntos ingresado como una cadena

        # se crean algunos mensajes para algunos posibles problemas que se pueden presentar
        if num_puntos == "":
            messagebox.showerror("OOPSS!!!", "No pueden estar vacios los puntos")
            return

        if num_puntos == "0":
            messagebox.showerror("OOPSS!!!", "No pueden haber 0 puntos, debe tener mínimo 1")
            return

        try:
            num_puntos = int(num_puntos)  # Convertir a entero
        except ValueError:
            messagebox.showerror("OOPSS!!!", "No puede ingresar palabras/letras, deben ser numeros")
            return

        self.entries = []

        for i in range(num_puntos):
            entry = ctk.CTkEntry(self.frame_ventana_secundaria, width=250, placeholder_text=f"Ingrese el punto {i+1}", justify="center")
            entry.place(x=250, y=50 + i * 40)
            self.entries.append(entry)

        self.barra_entrada_puntos.delete(0, ctk.END)
        self.barra_entrada_puntos.configure(state = "disabled")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def agregar_participante(self):
        """Se encarga de agregar los participantes desde la interfaz a la agenda
        """
        nombre = self.barra_entrada_nombre.get()
        apellido1 = self.barra_entrada_apellido1.get()
        apellido2 = self.barra_entrada_apellido2.get()

        # se crean algunos mensajes para mostrar en algunos casos que pueden dar errores
        if nombre.isdigit() or nombre == "":
            messagebox.showerror("OJO!", "Debe ingresar un nombre válido")
            return

        if apellido1.isdigit() or apellido1 == "":
            messagebox.showerror("OJO!", "Debe ingresar el primer apellido válido")
            return

        if apellido2.isdigit() or apellido2 == "":
            messagebox.showerror("OJO!", "Debe ingresar el segundo apellido válido")
            return

        self.barra_entrada_nombre.delete(0, "end")
        self.barra_entrada_apellido1.delete(0, "end")
        self.barra_entrada_apellido2.delete(0, "end")

        agregar_participante(nombre, apellido1, apellido2) # se crea el participante con los valores ingresados en las barras anteriores

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def agregar_apartados(self):
        """Se encarga de agregar los apartados desde la interfaz a la agenda
        """
        self.apartado = self.barra_entrada.get()

        if self.apartado == "" or all(entry.get() == "" for entry in self.entries):
            messagebox.showerror("CUIDADO!!", "No puede estar vacío el apartado o los puntos")
            return

        self.barra_entrada.delete(0, ctk.END)

        agregar_apartado(self.apartado)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def guardar_punto(self, apartado):
        """Se encarga de guardar los puntos en la agenda
        """
        puntos = []
        for i in self.entries:
            puntos.append(i.get())
            i.destroy()

        for j in puntos:
            agregar_puntos(j, apartado)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def guardar_puntos_apartados(self):
        """Se encarga de guardar los puntos de los apartados en la agenda"""
        self.agregar_apartados()
        self.guardar_punto(self.apartado)
        
        self.barra_entrada_puntos.configure(state = "normal")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def desplegar_entrada_discusion(self):
        """Esta funcion de encarga de desplegar una barra para introducir las discusiones
        """
        self.textbox = ctk.CTkEntry(self.frame_ventana_secundaria, text_color="dark blue", width=510, height=150, corner_radius=8, fg_color= "sky blue")
        self.textbox.place(x=150, y=260)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def actualizar_puntos(self): # Actualizar los puntos
        self.apartado_seleccionado=self.menu_opciones_apartados.get() # Obtener el apartado seleccionado
        self.puntos = list(self.diccionario_apartados_puntos.get(self.apartado_seleccionado, [])) # Obtener los puntos del apartado seleccionado
        self.menu_opciones_puntos.configure(values= self.puntos) # Actualizar los puntos en el menú de opciones

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def agregar_discusion(self):
        self.menu_opciones_apartados.get()
        self.menu_opciones_puntos.get()
        self.menu_opciones_participantes.get()
        discusiones = self.textbox.get()
        crear_discusion (self.menu_opciones_participantes, self.menu_opciones_apartados, self.menu_opciones_puntos, discusiones)

        self.textbox.delete(0, "end")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

#SE EJECUTA LA VENTANA PRINCIPAL
ventana = VentanaPrincipal()
ventana.ventana_principal.mainloop()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
