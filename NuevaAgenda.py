from agenda import agenda as Agenda, lista as Lista, persona as Persona, discusion as Discusion, puntos as Puntos, apartados as Apartados
from datetime import datetime

from datetime import datetime

class MiAgenda(Agenda):
    def __init__(self, titulo: str, fecha: datetime) -> None:
        super().__init__()
        self.titulo: str = titulo
        self.fecha: datetime = fecha
        self.participantes: MiPersona = None
        self.apartados: MiApartado = None

    def agregar_participante(self, nombre: str, apellido1: str, apellido2: str):
        if self.participantes is None:
            self.participantes = MiPersona(nombre=nombre, apellido1=apellido1, apellido2=apellido2)
        else:
            self.participantes.agregar(nombre, apellido1, apellido2)

    def agregar_apartado(self, apartado: str):
        if self.apartados is None:
            self.apartados = MiApartado(apartado)
        else:
            self.apartados.agregar(apartado)

    def agregar_punto(self, punto: str, apartado: str):
        if self.apartados is not None:
            apartado_actual = self.apartados

            while apartado_actual is not None:
                if apartado_actual.apartado == apartado:
                    if apartado_actual.puntos is None:
                        apartado_actual.puntos = MisPuntos(punto)
                    else:
                        nodo_punto = apartado_actual.puntos

                        while nodo_punto.sig is not None:
                            nodo_punto = nodo_punto.sig
                        nodo_punto.sig = MisPuntos(punto)
                    break
                else:
                    if apartado_actual.sig is None:
                        apartado_actual.sig = MiApartado(apartado)
                        apartado_actual.sig.puntos = MisPuntos(punto)
                        break
                    else:
                        apartado_actual = apartado_actual.sig
        else:
            self.apartados = MiApartado(apartado)
            self.apartados.puntos = MisPuntos(punto)


    def agregar_discusion(self, persona, apartado, punto, discusión):
        discusion_agregar = MisDiscusiones(persona, discusión)
        pos_actual = self.apartados
        while pos_actual is not None:
            if pos_actual.apartado == apartado:
                puntos_ramas = pos_actual.puntos
                while puntos_ramas is not None:
                    if puntos_ramas.punto == punto:
                        puntos_ramas.discusiones = self._agregar(puntos_ramas.discusiones, discusion_agregar)
                        break
                    puntos_ramas = puntos_ramas.sig
                break
            pos_actual = pos_actual.sig

    @property
    def asDict(self):
        return {"Título":self.titulo,"fecha":self.fecha._str_(),"participantes":self.participantes.asList}

def crear_agenda(titulo:str, fecha:datetime):
    """Funcion que se encarga de crear la instancia de la agenda

    Args:
        titulo (str): recibe el nombre que se asigna a la agenda
        fecha (datetime): recibe el argumento de la fecha y hora
    """
    global agenda
    agenda = MiAgenda(titulo, fecha)

def agregar_participante(nombre:str, apellido1:str, apellido2:str):
    """Funcion que se encarga de agregar un participante a la agenda

    Args:
        nombre (str): nombre del participante
        apellido1 (str): primer apellido del participante
        apellido2 (str): segundo apellido del participante
    """
    global agenda
    agenda.agregar_participante(nombre,apellido1,apellido2)

class MiLista(Lista):
    def __init__(self) -> None:
        super().__init__()

    def _agregar(self, r, e):
        if r is None:
            return e
        else:
            r.sig = self._agregar(r.sig, e)
            return r

class MiPersona(Persona):
    def __init__(self, nombre: str, apellido1: str, apellido2: str) -> None:
        super().__init__(nombre, apellido1, apellido2)

    def agregar(self, nombre: str, apellido1: str, apellido2: str):
        persona_agregar = MiPersona(nombre, apellido1, apellido2)
        self._agregar(self, persona_agregar)

    def _agregar(self, r, p):
        if r is None:
            return p
        else:
            r.sig = self._agregar(r.sig, p)
            return r

    @property
    def asList(self):
        if self is None:
            return []
        else:
            return self._asList(self)

    def _asList(self, r):
        r: MiPersona = r
        if r.sig is None:
            return [r.__str__()]
        else:
            return [r.__str__()] + self._asList(r.sig)

    def __str__(self) -> str:
        return "{0} {1} {2}".format(self.nombre, self.apellido1, self.apellido2)

def participante_asList():
    """Funcion que se encarga de agregar los participantes de la sesion a una lista

    Returns:
        list: lista vacia
    """
    global agenda
    try:
        return agenda.participantes.asList
    except:
        return []

class MisDiscusiones(Discusion):

    def __init__(self, persona: Persona, discusion: str) -> None:
        super().__init__(persona, discusion)

    def agregar_discusion (self, persona, discusion):
        discusion_agregar = MisDiscusiones(persona, discusion)
        self._agregar(self, discusion_agregar)

    def _agregar(self, r, d):
        if r is None:
            return d
        else:
            r.sig = self._agregar(r.sig, d)
            return r

def crear_discusion(participante:str, apartado:str, punto:str, discusion:str):
    """Funcion que se encarga de crear la discusion

    Args:
        participante (str): recibe el nombre del participante
        apartado (str): recibe el nombre del apartado
        punto (str): recibe el nombre del punto
        discusion (str): recibe la discusion
    """
    global agenda
    agenda.agregar_discusion(participante, apartado, punto, discusion)

class MiApartado(Apartados):
    def __init__(self, apartado: str) -> None:
        super().__init__(apartado)
        self.sig:MiApartado = None
        self.puntos: MisPuntos = None

    def agregar_punto(self, punto: str):
        if self.puntos is None:
            self.puntos = MisPuntos(punto)
        else:
            self.puntos.agregar(punto)

    def agregar(self, apartado: str):
        nuevo_apartado = MiApartado(apartado)
        self._agregar(self, nuevo_apartado)

    def _agregar(self, r, a):
        if r is None:
            return a
        else:
            r.sig = self._agregar(r.sig, a)
            return r

    def obtener_puntos(self):
        result = []

        current = self.puntos
        while current is not None:
            result.append(current.punto)
            current = current.sig

        return result

    @property
    def asDict(self):
        result = {}

        current = self
        while current is not None:
            result[current.apartado] = current.obtener_puntos()
            current = current.sig

        return result

def agregar_apartado(apartado:str):
    """Funcion que se encarga de agregar los apartados a la agenda

    Args:
        apartado (str): recibe el nombre de los apartados
    """
    global agenda
    agenda.agregar_apartado(apartado)

class MisPuntos(Puntos):
    def __init__(self, punto: str) -> None:
        super().__init__(punto)
        self.sig: MisPuntos = None
        self.discusiones: MisDiscusiones = None

    def agregar(self, punto: str):
        nuevo_punto = MisPuntos(punto)
        self._agregar(self, nuevo_punto)

    def _agregar(self, r: "MisPuntos", e: "MisPuntos"):
        if r.sig is None:
            r.sig = e
        else:
            self._agregar(r.sig, e)

    @property
    def asList(self):
        if self==None:
            return []
        else:
            return self._asList(self)

    def _asList(self,r):
        r:MisPuntos= r
        if r.sig==None:
            return [r.punto]
        else:
            return [r.punto]+self._asList(r.sig)

def agregar_puntos(apartado:str, punto:str):
    """Se encarga de agregar los puntos a los apartados de la agenda

    Args:
        apartado (str): ubica el punto en el apartado al que se va a agregar
        punto (str): recibe el punto a agregar
    """
    global agenda
    agenda.agregar_punto(punto, apartado)

def puntos_asDict() -> list:
    """Funcion que se encarga de pasar los puntos a listas

    Returns:
        list: lista que guarda los apartados y sus puntos correspondientes
    """
    global agenda
    try:
        return agenda.apartados.asDict
    except:
        return {"" : ""}
