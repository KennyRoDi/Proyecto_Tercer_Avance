#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#-----------------------------------------------------------------------------------------------------------------------------#

class lista:
    """
    Estructura base de lista para ser heredada por otras clases que requieran su definición como lista de punteros
    """

    def __init__(self) -> None:
        """Construtor de la clase lista, inicaliza el puntero siguiente
        """
        self.sig:lista=None

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#-----------------------------------------------------------------------------------------------------------------------------#

class persona(lista):
    """
    Estructura de datos tipo lista punteros para el registro de personas
    """

    def __init__(self, nombre: str, apellido1:str, apellido2:str) -> None:
        """Constructor de la clase personas

        Args:
            nombre (str): Nombre de la persona
            apellido1 (str): Primer apellido de la persona
            apellido2 (str): Segundo apellido de la persona
        """
        super().__init__()              #Inicaliza el puntero de lista
        self.nombre:str=nombre
        self.apellido1:str=apellido1
        self.apellido2:str=apellido2

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#-----------------------------------------------------------------------------------------------------------------------------#

class discusion(lista):
    """
    Estructura de datos tipo lista, para el registro de discusiones tratadas en los puntos de agenda
    """

    def __init__(self, persona:persona, discusion:str) -> None:
        """constructor de discusiones

        Args:
            persona (persona): Persona quien emite la discusión
            discusion (str): trasncripción de lo comentado en la discusión
        """
        super().__init__()
        self.persona:persona=persona    #Persona quien realiza la discusión
        self.discusion:str=discusion    #Transcrición o SpeechRecognition de lo expuesto por la persona

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#-----------------------------------------------------------------------------------------------------------------------------#

class puntos(lista):
    """
    Estructura de datos tipo árbol m-vías para la representación de puntos de agenda
    """

    def __init__(self,punto:str) -> None:
        """Constructor del tercer nivel del árbol de agenda (puntos)

        Args:
            punto (str): Descripción del tema a tratar
        """
        super().__init__()
        self.punto:str=punto            #Descrición del punto
        self.discusiones:discusion=None #Listado de discusiones del punto

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#-----------------------------------------------------------------------------------------------------------------------------#

class apartados(lista):
    """
    Estructura de datos tipo árbol m-vías para la representación de apartados de agenda
    """

    def __init__(self,apartado:str) -> None:
        """Constructor del tercer nivel del árbol de agenda (apartados)

        Args:
            apartado (str): Descripción del apartado
        """
        super().__init__()
        self.apartado:str=apartado     #Descripcion del apartado
        self.puntos:puntos=None         #Listado de puntos de agenda por apartado

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#-----------------------------------------------------------------------------------------------------------------------------#

class agenda:
    """
    Estructura de datos tipo árbol m-vías para la representación de agendas
    """

    def __init__(self) -> None:
        """Constructor de la agenda
        """
        self.participantes:persona=None     #Listado de participantes
        self.apartados:apartados=None       #Listado de apartados

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#-----------------------------------------------------------------------------------------------------------------------------#

#ejemplo de instancia de agenda del gráfico presente en la documentación del proyecto
agenda1=agenda()

#Registro de participantes en la agenda
agenda1.participantes=persona('Persona1','Sin', 'Apellidos')
agenda1.participantes.sig=persona('Persona2','Sin', 'Apellidos')
agenda1.participantes.sig.sig=persona('Persona3','Sin', 'Apellidos')

#Registro de apartados
agenda1.apartados=apartados('Apartado1')
agenda1.apartados.sig=apartados('Apartado2')
agenda1.apartados.sig.sig=apartados('Apartado3')

#Registro de puntos
agenda1.apartados.puntos=puntos('Punto1')
agenda1.apartados.puntos.sig=puntos('Punto2')
agenda1.apartados.sig.puntos=puntos('Punto3')
agenda1.apartados.sig.sig.puntos=puntos('Punto4')
agenda1.apartados.sig.sig.puntos.sig=puntos('Punto5')

#Registro de discusiones
agenda1.apartados.puntos.discusiones=discusion(agenda1.participantes,'discusión1')
agenda1.apartados.puntos.discusiones.sig=discusion(agenda1.participantes.sig,'discusión2')

agenda1.apartados.puntos.sig.discusiones=discusion(agenda1.participantes,'discusión1')
agenda1.apartados.puntos.sig.discusiones.sig=discusion(agenda1.participantes.sig,'discusión2')
agenda1.apartados.puntos.sig.discusiones.sig=discusion(agenda1.participantes,'discusión3')

agenda1.apartados.sig.puntos.discusiones=discusion(agenda1.participantes,'discusión1')
agenda1.apartados.sig.puntos.discusiones.sig=discusion(agenda1.participantes.sig.sig,'discusión2')

agenda1.apartados.sig.sig.puntos.discusiones=discusion(agenda1.participantes.sig,'discusión3')

agenda1.apartados.sig.sig.puntos.sig.discusiones=discusion(agenda1.participantes,'discusión2')
agenda1.apartados.sig.sig.puntos.sig.discusiones.sig=discusion(agenda1.participantes.sig.sig,'discusión2')

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#-----------------------------------------------------------------------------------------------------------------------------#

pass

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#-----------------------------------------------------------------------------------------------------------------------------#