from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager    

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=150, unique=True, default='default_username')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    objects = UserManager()
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def has_module_perms(self, app_label):
        """
        Determine whether the user has permission to view the app_label module.

        Simplest possible answer: Yes, always.
        """
        return True

    def has_perm(self, perm, obj=None):
        """
        Determine whether the user has the given permission.

        Simplest possible answer: Yes, always.
        """
        return True

class Docente(models.Model):


    FRECUENCIA_OPCIONES = [
        ('nunca', 'Nunca o Casi Nunca'),
        ('algunas_veces', 'Algunas veces'),
        ('muchas_veces', 'Muchas veces'),
        ('siempre', 'Siempre o Casi Siempre'),
    ]
    PORCENTAJE_OPCIONES = [
        ('0-24', '0 - 24%'),
        ('25-49', '25 - 49%'),
        ('50-74', '50 - 74%'),
        ('75-100', '75 - 100%'),
    ]
    


    OPCIONES_SI_NO = [
        ('si', 'Sí'),
        ('no', 'No'),
    ]
    OPCIONES_CANTIDAD = [
        ('no_hay', 'No hay'),
        ('1-2', 'Hay 1 - 2'),
        ('3-4', 'Hay 3 - 4'),
        ('5_mas', 'Hay 5 o más'),
    ]
   
    FRECUENCIA_OPCIONES = [
        ('nunca', 'Nunca'),
        ('a_veces', 'A veces'),
        ('varias_veces', 'Varias veces'),
        ('siempre', 'Siempre o casi siempre'),
    ]

    
    ANOS_EXPERIENCIA_CHOICES = [
        ('0', '0 (esta en su primer año)'),
        ('1-3', '1-3'),
        ('4-6', '4-6'),
        ('7_mas', '7 o más'),
    ]
    SECTOR_EXPERIENCIA_CHOICES = [
        ('Oficial', 'Oficial'),
        ('Particular', 'Particular'),
        ('Ambos', 'Ambos'),
    ]
    NIVEL_IMPARTE_ACTUALMENTE_CHOICES = [
        ('Inicial', 'Inicial'),
        ('Primaria', 'Primaria'),
        ('Premedia', 'Premedia'),
        ('Media', 'Media'),
    ]
    TITULO_ENSENANZA_CHOICES = [
        ('si', 'Sí'),
        ('no', 'No'),
    ]
    NIVEL_TITULO_CHOICES = [
        ('nacional', 'Nacional'),
        ('internacional', 'Internacional'),
    ]
    CERTIFICACION_INGLES_CHOICES = [
        ('si', 'Sí'),
        ('no', 'No'),
    ]
    NIVEL_INGLES_DOCENTE_CHOICES = [
        ('A0', 'A0: Principiante'),
        ('A1-A2', 'A1 - A2: Básico'),
        ('A2-B1', 'A2 - B1: Pre-intermedio'),
        ('B1', 'B1: Intermedio'),
        ('B2', 'B2: Intermedio-Alto'),
        ('C1-C2', 'C1 - C2: Avanzado'),
    ]
    RENOVAR_CERTIFICACION_CHOICES = [
        ('si', 'Sí'),
        ('no', 'No'),
    ]

    
    IMPORTANCE_CHOICES = [
        ('muy_en_desacuerdo', 'Muy en desacuerdo'),
        ('desacuerdo', 'Desacuerdo'),
        ('de_acuerdo', 'De acuerdo'),
        ('muy_de_acuerdo', 'Muy de acuerdo'),
    ]
    YES_NO_CHOICES = [
        ('si', 'Sí'),
        ('no', 'No'),
    ]
    FREQUENCY_CHOICES = [
        ('nunca', 'Nunca o Casi Nunca'),
        ('algunas_veces', 'Algunas veces'),
        ('muchas_veces', 'Muchas veces'),
        ('siempre', 'Siempre o Casi Siempre'),
    ]

    nombre = models.CharField(max_length=100, null=True)
    apellido = models.CharField(max_length=100, null=True)
    cedula = models.CharField(max_length=20, unique=True, null=True)
    telefono_oficina = models.CharField(max_length=20, blank=True, null=True)
    telefono_personal = models.CharField(max_length=20, blank=True, null=True)
    correo_institucional = models.EmailField(null=True)
    porcentaje_planes_completados = models.CharField(max_length=5, null=True)
    ajuste_plan_estudios = models.CharField(max_length=20, null=True)
    dicta_mas_de_un_nivel = models.BooleanField(default=False, null=True)
    niveles = models.TextField(blank=True, null=True)
    horas_clase_ingles = models.CharField(max_length=20, null=True)
    frecuencia_habla_ingles = models.CharField(max_length=20, choices=FRECUENCIA_OPCIONES, null=True)
    porcentaje_tiempo_ingles = models.CharField(max_length=20, choices=PORCENTAJE_OPCIONES, null=True)
    incentiva_hablar_ingles = models.CharField(max_length=20, choices=FRECUENCIA_OPCIONES, null=True)
    porcentaje_promueve_ingles = models.CharField(max_length=20, choices=PORCENTAJE_OPCIONES, null=True)
    tiempo_dialogo_ingles = models.CharField(max_length=20, choices=FRECUENCIA_OPCIONES, null=True)
    senalizaciones_centro_ingles = models.CharField(max_length=2, choices=OPCIONES_SI_NO, null=True)
    senalizaciones_ingles = models.CharField(max_length=2, choices=OPCIONES_SI_NO, blank=True, null=True)
    senalizaciones_ingles_opciones = models.TextField(blank=True, null=True)
    senaletica = models.CharField(max_length=2, choices=OPCIONES_SI_NO, null=True)
    cantidad_senalizaciones_aula = models.CharField(max_length=7, choices=OPCIONES_CANTIDAD, blank=True, null=True)
    frecuencia_interaccion_directivos = models.CharField(max_length=12, choices=FRECUENCIA_OPCIONES, null=True)
    frecuencia_interaccion_docente = models.CharField(max_length=12, choices=FRECUENCIA_OPCIONES, null=True)
    frecuencia_interaccion_padres = models.CharField(max_length=12, choices=FRECUENCIA_OPCIONES, null=True)
    interactua_estudiantes = models.CharField(max_length=18, choices=FRECUENCIA_OPCIONES, null=True)
    actividades_ingles = models.CharField(max_length=2, choices=OPCIONES_SI_NO, null=True)
    actividades_ingles_descripcion = models.TextField(blank=True, null=True)
    frecuencia_actividades = models.CharField(max_length=20, blank=True, null=True)
    anos_experiencia = models.CharField(max_length=5, choices=ANOS_EXPERIENCIA_CHOICES, null=True)
    sector_experiencia = models.CharField(max_length=10, choices=SECTOR_EXPERIENCIA_CHOICES, blank=True, null=True)
    niveles_impartidos = models.TextField(blank=True, null=True)
    nivel_imparte_actualmente = models.CharField(max_length=8, choices=NIVEL_IMPARTE_ACTUALMENTE_CHOICES, null=True)
    titulo_ensenanza = models.CharField(max_length=2, choices=TITULO_ENSENANZA_CHOICES, null=True)
    nivel_titulo = models.CharField(max_length=13, choices=NIVEL_TITULO_CHOICES, blank=True, null=True)
    titulos_formales = models.TextField(blank=True, null=True)
    cursos_educacion_continua = models.TextField(blank=True, null=True)
    certificacion_ingles = models.CharField(max_length=2, choices=CERTIFICACION_INGLES_CHOICES, null=True)
    nombre_titulacion = models.TextField(blank=True, null=True)
    nivel_ingles_docente = models.CharField(max_length=6, choices=NIVEL_INGLES_DOCENTE_CHOICES, blank=True, null=True)
    renovar_certificacion = models.CharField(max_length=2, choices=RENOVAR_CERTIFICACION_CHOICES, null=True)
    importancia_formacion_bilingue = models.CharField(max_length=20, choices=IMPORTANCE_CHOICES, null=True)
    valoracion_formacion_bilingue = models.CharField(max_length=20, choices=IMPORTANCE_CHOICES, null=True)
    involucramiento_direccion_CE = models.CharField(max_length=20, choices=IMPORTANCE_CHOICES, null=True)
    expectativas_director = models.CharField(max_length=2, choices=YES_NO_CHOICES, null=True)
    responsabilidad_director = models.CharField(max_length=20, choices=IMPORTANCE_CHOICES, null=True)
    prioridad_ppb = models.CharField(max_length=20, choices=IMPORTANCE_CHOICES, null=True)
    participacion_padres = models.CharField(max_length=20, choices=IMPORTANCE_CHOICES, null=True)
    frecuencia_recursos = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, null=True)
    acceso_recursos = models.CharField(max_length=2, choices=YES_NO_CHOICES, null=True)
    cooperacion_ppb = models.CharField(max_length=2, choices=YES_NO_CHOICES, null=True)
    cooperacion_participacion_ppb = models.CharField(max_length=2, choices=YES_NO_CHOICES, null=True)
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Coordinador(models.Model):
    # Formulario 1
    docentes_por_asignatura = models.PositiveIntegerField()
    participa_activamente_ppb = models.BooleanField()
    estudiantes_por_nivel_ppb = models.PositiveIntegerField()
    docentes_capacitados_ppb = models.PositiveIntegerField()
    docentes_aprobados_ppb = models.PositiveIntegerField()
    docentes_capacitacion_exterior = models.PositiveIntegerField()

    # Formulario 2
    codigos_plan_estudio = models.CharField(max_length=255)
    planes_estudio = models.CharField(max_length=255)
    asignaturas_ingles_en_plan = models.BooleanField()
    asignaturas_ingles_dictadas = models.BooleanField()
    planes_clase_contraste = models.TextField()
    horas_ingles = models.PositiveIntegerField()
    horas_teoricas = models.PositiveIntegerField()
    horas_practicas = models.PositiveIntegerField()

    # Formulario 3
    actividades_propio_centro = models.BooleanField()
    actividades_meduca_centro = models.BooleanField()
    actividades_externas_centro = models.BooleanField()
    detalle_actividades_anual = models.TextField()
    cantidad_estudiantes_actividades_externas = models.JSONField(default=dict) 

    # Formulario 4
    after_school_existencia = models.BooleanField()
    after_school_descripcion = models.TextField()
    after_school_participacion = models.JSONField(default=dict)

    # Formulario 5
    tipo_senalizaciones_ingles = models.JSONField(default=list)
    senalizaciones_aula_ingles = models.BooleanField()
    cantidad_senalizaciones_aula = models.PositiveIntegerField()

    # Formulario 6
    interactua_directivos_ingles = models.PositiveIntegerField()
    interactua_docentes_ingles = models.PositiveIntegerField()
    interactua_padres_ingles = models.PositiveIntegerField()
    interactua_estudiantes_ingles = models.BooleanField()
    porcentaje_interaccion_estudiantes = models.PositiveIntegerField()
    actividades_ingles_fuera_aula = models.JSONField(default=list)
    frecuencia_actividades_ingles = models.CharField(max_length=20)

    def __str__(self):
        return f"Coordinador ID: {self.id}"

class Director(models.Model):
    # Formulario 1 start
    nombre = models.CharField(max_length=100, default='N/A')
    apellido = models.CharField(max_length=100, default='N/A')
    cedula = models.CharField(max_length=20, default='N/A')
    telefono_oficina = models.CharField(max_length=20, default='N/A')
    telefono_personal = models.CharField(max_length=20, default='N/A')
    correo_institucional = models.EmailField(default='N/A@example.com')
    correo_personal = models.EmailField(default='N/A@example.com')
    telefono_personal = models.CharField(max_length=20, default='N/A')
    coordinador_ingles = models.CharField(max_length=100, default='N/A')
    coordinador_informatica = models.CharField(max_length=100, default='N/A')
    # Formulario 1 end

    # Formulario 2 start
    codigo_siace = models.CharField(max_length=100, default='N/A')
    nombre_centro_educativo = models.CharField(max_length=100, default='N/A')
    nombre_centro_valido = models.CharField(max_length=100, default='N/A')
    region_educativa = models.CharField(max_length=100, default='N/A')
    provincia = models.CharField(max_length=100, default='N/A')
    direccion = models.CharField(max_length=255, default='N/A')
    geolocalizacion = models.CharField(max_length=255, default='N/A')
    nivel_educativo = models.CharField(max_length=255, default='N/A')
    matricula_total = models.IntegerField(default=0)  
    prekinder = models.IntegerField(default=0)
    femenino_prekinder = models.IntegerField(default=0)
    masculino_prekinder = models.IntegerField(default=0)
    kinder = models.IntegerField(default=0)
    femenino_kinder = models.IntegerField(default=0)
    masculino_kinder = models.IntegerField(default=0)
    primaria_1 = models.IntegerField(default=0)
    femenino_primaria_1 = models.IntegerField(default=0)
    masculino_primaria_1 = models.IntegerField(default=0)
    premedia_1 = models.IntegerField(default=0)
    femenino_premedia_1 = models.IntegerField(default=0)
    masculino_premedia_1 = models.IntegerField(default=0)
    media_10 = models.IntegerField(default=0)
    femenino_media_10 = models.IntegerField(default=0)
    masculino_media_10 = models.IntegerField(default=0)
    media_11 = models.IntegerField(default=0)
    femenino_media_11 = models.IntegerField(default=0)
    masculino_media_11 = models.IntegerField(default=0)
    media_12 = models.IntegerField(default=0)
    femenino_media_12 = models.IntegerField(default=0)
    masculino_media_12 = models.IntegerField(default=0)
    total_docentes_media_10 = models.CharField(max_length=10, default='N/A')
    total_docentes_media_11 = models.CharField(max_length=10, default='N/A')
    total_docentes_media_12 = models.CharField(max_length=10, default='N/A')
    numero_estudiantes_salon = models.CharField(max_length=10, default='N/A')
    cantidad_docentes_asignatura = models.CharField(max_length=10, default='N/A')
    # Formulario 2 end

    # Formulario 3 start
    recursos_multimedia = models.CharField(max_length=3, choices=(("si", "Sí"), ("no", "No")), blank=True, default='no')
    material_multimedia = models.CharField(max_length=20, choices=(("muy_en_desacuerdo", "Muy en desacuerdo"), ("desacuerdo", "Desacuerdo"), ("de_acuerdo", "De acuerdo"), ("muy_de_acuerdo", "Muy de acuerdo")), blank=True, default='muy_en_desacuerdo')
    materiales_multimedia = models.CharField(max_length=20, choices=(("muy_en_desacuerdo", "Muy en desacuerdo"), ("desacuerdo", "Desacuerdo"), ("de_acuerdo", "De acuerdo"), ("muy_de_acuerdo", "Muy de acuerdo")), blank=True, default='muy_en_desacuerdo')
    software_ingles = models.CharField(max_length=3, choices=(("si", "Sí"), ("no", "No")), blank=True, default='no')
    software_ingles_cantidad = models.CharField(max_length=10, choices=(("0", "0 (No hay)"), ("1", "1 (Hay)"), ("2", "2 (Hay)"), ("mas_de_2", "Más de 2")), blank=True, default='0')
    software_ingles_nombres = models.TextField(blank=True, default='')
    licencias_softwares = models.CharField(max_length=3, choices=(("si", "Sí"), ("no", "No")), blank=True, default='no')
    acceso_internet_softwares = models.CharField(max_length=13, choices=(("no_requieren", "No requieren"), ("si_requieren", "Sí requieren")), blank=True, default='no_requieren')
    usuarios_disponibles = models.CharField(max_length=30, choices=(("0", "0 (No hay)"), ("uno_por_estudiante", "Uno por estudiante"), ("menos_de_uno_por_estudiante", "Menos de uno por estudiante (comparten licencia)")), blank=True, default='0')
    cuenta_con_internet = models.CharField(max_length=3, choices=(("si", "Sí"), ("no", "No")), blank=True, default='no')
    tipo_enlace_internet = models.CharField(max_length=100, blank=True, default='')
    ancho_banda = models.IntegerField(blank=True, null=True, default=0)
    wifi_solucion_existencia = models.BooleanField(default=False)
    alcance_wifi = models.CharField(max_length=20, choices=(("cobertura_parcial", "Cobertura Parcial"), ("cobertura_completa", "Cobertura Completa")), blank=True, default='cobertura_parcial')
    wifi_cobertura = models.CharField(max_length=7, choices=(("0-24", "0 - 24%"), ("25-49", "25 - 49%"), ("50-74", "50 - 74%"), ("75-100", "75 - 100%")), blank=True, default='0-24')
    acceso_wifi_administrativos = models.CharField(max_length=3, choices=(("si", "Sí"), ("no", "No")), blank=True, default='no')
    acceso_wifi_docentes = models.CharField(max_length=3, choices=(("si", "Sí"), ("no", "No")), blank=True, default='no')
    acceso_wifi_estudiantes = models.CharField(max_length=3, choices=(("si", "Sí"), ("no", "No")), blank=True, default='no')
    percepcion_velocidad = models.CharField(max_length=10, choices=(("muy_mala", "Muy Mala"), ("mala", "Mala"), ("regular", "Regular"), ("buena", "Buena"), ("muy_buena", "Muy Buena")), blank=True, default='muy_mala')
    # Formulario 3 end

    # Formulario 4 start
    participa_ppb = models.CharField(max_length=3, choices=(("si", "Sí"), ("no", "No")), blank=True, default='no')
    estudiantes_ppb_prekinder = models.CharField(max_length=20, choices=(("1-20", "1 - 20"), ("21-40", "21 - 40"), ("41-60", "41 - 60"), ("61-80", "61 - 80"), ("80+", "80 a más")), blank=True, default='1-20')
    estudiantes_ppb_kinder = models.CharField(max_length=20, choices=(("1-20", "1 - 20"), ("21-40", "21 - 40"), ("41-60", "41 - 60"), ("61-80", "61 - 80"), ("80+", "80 a más")), blank=True, default='1-20')
    participa_ppb_grado_1 = models.CharField(max_length=20, choices=(("1-20", "1 - 20"), ("21-40", "21 - 40"), ("41-60", "41 - 60"), ("61-80", "61 - 80"), ("80+", "80 a más")), blank=True, default='1-20')
    participa_ppb_grado_2 = models.CharField(max_length=20, choices=(("1-20", "1 - 20"), ("21-40", "21 - 40"), ("41-60", "41 - 60"), ("61-80", "61 - 80"), ("80+", "80 a más")), blank=True, default='1-20')
    participa_ppb_grado_3 = models.CharField(max_length=20, choices=(("1-20", "1 - 20"), ("21-40", "21 - 40"), ("41-60", "41 - 60"), ("61-80", "61 - 80"), ("80+", "80 a más")), blank=True, default='1-20')
    participa_ppb_grado_4 = models.CharField(max_length=20, choices=(("1-20", "1 - 20"), ("21-40", "21 - 40"), ("41-60", "41 - 60"), ("61-80", "61 - 80"), ("80+", "80 a más")), blank=True, default='1-20')
    participa_ppb_grado_5 = models.CharField(max_length=20, choices=(("1-20", "1 - 20"), ("21-40", "21 - 40"), ("41-60", "41 - 60"), ("61-80", "61 - 80"), ("80+", "80 a más")), blank=True, default='1-20')
    participa_ppb_grado_6 = models.CharField(max_length=20, choices=(("1-20", "1 - 20"), ("21-40", "21 - 40"), ("41-60", "41 - 60"), ("61-80", "61 - 80"), ("80+", "80 a más")), blank=True, default='1-20')
    participa_ppb_grado_7 = models.CharField(max_length=20, choices=(("1-20", "1 - 20"), ("21-40", "21 - 40"), ("41-60", "41 - 60"), ("61-80", "61 - 80"), ("80+", "80 a más")), blank=True, default='1-20')
    participa_ppb_grado_8 = models.CharField(max_length=20, choices=(("1-20", "1 - 20"), ("21-40", "21 - 40"), ("41-60", "41 - 60"), ("61-80", "61 - 80"), ("80+", "80 a más")), blank=True, default='1-20')
    participa_ppb_grado_9 = models.CharField(max_length=20, choices=(("1-20", "1 - 20"), ("21-40", "21 - 40"), ("41-60", "41 - 60"), ("61-80", "61 - 80"), ("80+", "80 a más")), blank=True, default='1-20')
    participa_ppb_grado_10 = models.CharField(max_length=20, choices=(("1-20", "1 - 20"), ("21-40", "21 - 40"), ("41-60", "41 - 60"), ("61-80", "61 - 80"), ("80+", "80 a más")), blank=True, default='1-20')
    participa_ppb_grado_11 = models.CharField(max_length=20, choices=(("1-20", "1 - 20"), ("21-40", "21 - 40"), ("41-60", "41 - 60"), ("61-80", "61 - 80"), ("80+", "80 a más")), blank=True, default='1-20')
    participa_ppb_grado_12 = models.CharField(max_length=20, choices=(("1-20", "1 - 20"), ("21-40", "21 - 40"), ("41-60", "41 - 60"), ("61-80", "61 - 80"), ("80+", "80 a más")), blank=True, default='1-20')
    docentes_capacitados_prekinder = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_capacitados_kinder = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_capacitados_primaria_1 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_capacitados_primaria_2 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_capacitados_primaria_3 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_capacitados_primaria_4 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_capacitados_primaria_5 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_capacitados_primaria_6 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_capacitados_primaria_7 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_capacitados_primaria_8 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_capacitados_primaria_9 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_capacitados_primaria_10 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_capacitados_primaria_11 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_capacitados_primaria_12 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_capacitados_premedia_1 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_capacitados_premedia_2 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_capacitados_premedia_3 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_capacitados_premedia_4 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_capacitados_premedia_5 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_capacitados_premedia_6 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_capacitados_premedia_7 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_capacitados_premedia_8 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_capacitados_premedia_9 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_capacitados_media_10 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_capacitados_media_11 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_capacitados_media_12 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_aprobados_prekinder = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_aprobados_kinder = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_aprobados_primaria_1 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_aprobados_primaria_2 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_aprobados_primaria_3 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_aprobados_primaria_4 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_aprobados_primaria_5 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_aprobados_primaria_6 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_aprobados_primaria_7 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_aprobados_primaria_8 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_aprobados_primaria_9 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_aprobados_primaria_10 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_aprobados_primaria_11 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_aprobados_primaria_12 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_aprobados_premedia_1 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_aprobados_premedia_2 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_aprobados_premedia_3 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_aprobados_premedia_4 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_aprobados_premedia_5 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_aprobados_premedia_6 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_aprobados_premedia_7 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_aprobados_premedia_8 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_aprobados_premedia_9 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_aprobados_media_10 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_aprobados_media_11 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_aprobados_media_12 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_extranjero_prekinder = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_extranjero_kinder = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_extranjero_primaria_1 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_extranjero_primaria_2 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_extranjero_primaria_3 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_extranjero_primaria_4 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_extranjero_primaria_5 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_extranjero_primaria_6 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_extranjero_primaria_7 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_extranjero_primaria_8 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_extranjero_primaria_9 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_extranjero_primaria_10 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_extranjero_primaria_11 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_extranjero_primaria_12 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_extranjero_premedia_1 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_extranjero_premedia_2 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_extranjero_premedia_3 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_extranjero_premedia_4 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_extranjero_premedia_5 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_extranjero_premedia_6 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_extranjero_premedia_7 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_extranjero_premedia_8 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_extranjero_premedia_9 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_extranjero_media_10 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_extranjero_media_11 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    docentes_extranjero_media_12 = models.CharField(max_length=20, choices=(("1-5", "1 - 5"), ("6-10", "6 - 10"), ("11-15", "11 - 15"), ("15+", "15+")), blank=True, default='1-5')
    # Formulario 4 end

    # Formulario 5 start
    DOCENTES_CHOICES = (
    ("1-5", "1 - 5"),
    ("6-10", "6 - 10"),
    ("11-15", "11 - 15"),
    ("15+", "15+"),
    )

    DISPONIBLE_CHOICES = (
        ("si", "Sí"),
        ("no", "No"),
    )

    AJUSTE_PLAN_CHOICES = (
        ("muy_en_desacuerdo", "Muy en desacuerdo"),
        ("en_desacuerdo", "En desacuerdo"),
        ("de_acuerdo", "De acuerdo"),
        ("muy_de_acuerdo", "Muy de acuerdo"),
    )

    horas_choices = (
        ("1-5", "1-5"),
        ("6-10", "6-10"),
        ("11-15", "11-15"),
        ("15+", "15+"),
    )

    ACTIVIDADES_CHOICES = (
        ("nunca", "Nunca o Casi Nunca"),
        ("algunas_veces", "Algunas veces"),
        ("muchas_veces", "Muchas veces"),
        ("siempre", "Siempre o Casi Siempre"),
    )

    senialetica_choices = (
        ("si", "Sí"),
        ("no", "No"),
    )

    cooperacion_choices = (
        ("si", "Sí"),
        ("no", "No"),
    )

    lugar_choices = [
        ('comedor', 'Comedor'),
        ('areas_deportivas', 'Áreas deportivas'),
        ('banos', 'Baños'),
        ('pasillos', 'Pasillos'),
        ('murales', 'Murales')
    ]

    planes_estudio_disponibles = models.CharField(max_length=2, choices=DISPONIBLE_CHOICES, verbose_name="Planes de Estudio Disponibles", default="si")
    planes_estudio_2023_disponibles = models.CharField(max_length=2, choices=DISPONIBLE_CHOICES, verbose_name="Planes de Estudio 2023 Disponibles", default="si")
    asignaturas_ingles_plan_estudio = models.CharField(max_length=2, choices=DISPONIBLE_CHOICES, verbose_name="Asignaturas en Inglés en Plan de Estudios", default="si")
    asignaturas_ingles_centro_educativo = models.CharField(max_length=2, choices=DISPONIBLE_CHOICES, verbose_name="Asignaturas en Inglés en Centro Educativo", default="si")
    ajuste_plan_estudios = models.CharField(max_length=20, choices=AJUSTE_PLAN_CHOICES, verbose_name="Ajuste del Plan de Estudios", default="de_acuerdo")
    horas_ingles = models.CharField(max_length=5, choices=horas_choices, verbose_name="Horas dedicadas a la enseñanza del inglés", default="1-5")
    horas_teoricas = models.CharField(max_length=5, choices=horas_choices, verbose_name="Horas teóricas impartidas dentro del plan de estudio", default="1-5")
    horas_practicas = models.CharField(max_length=5, choices=horas_choices, verbose_name="Horas prácticas impartidas dentro del plan de estudio", default="1-5")
    curso_ingles_after_school = models.CharField(max_length=2, choices=DISPONIBLE_CHOICES, verbose_name="Cursos de inglés tipo 'After School'", default="si")
    cursos_after_school = models.TextField(verbose_name="Cursos de inglés tipo 'After School' mencionados", default="Curso 1, Curso 2")
    participacion_cursos = models.CharField(max_length=20, choices=[
        ('ninguno', 'Ninguno'),
        ('algunos', 'Algunos'),
        ('alrededor_mitad', 'Alrededor de la mitad'),
        ('mas_mitad', 'Más de la mitad'),
        ('todos', 'Todos'),
    ], verbose_name='Participación de Estudiantes', default='ninguno')
    senialetica_ingles = models.CharField(max_length=2, choices=senialetica_choices, verbose_name="Señalética / Rotulaciones / Letreros en Inglés", default="si")
    senalizaciones_ingles = models.CharField(max_length=2, choices=senialetica_choices, verbose_name="Señalizaciones en Inglés", default="si")
    senalizaciones_ingles_opciones = models.CharField(max_length=20, choices=lugar_choices)
    cooperacion_participacion_ppb = models.CharField(max_length=2, choices=cooperacion_choices, verbose_name="Cooperación y participación entre profesores capacitados en PPB", default="si")
    cooperacion_participacion_ppb_no_ppb = models.CharField(max_length=2, choices=cooperacion_choices, verbose_name="Cooperación y participación entre profesores capacitados en PPB y los profesores no capacitados en el Programa", default="si")
    # Formulario 5 end

    # Formulario 6 start
    actividades_ingles = models.CharField(max_length=20, choices=ACTIVIDADES_CHOICES, verbose_name="¿Se realizan actividades especiales que promueven el aprendizaje y uso del idioma inglés que nacen desde su Centro Educativo?", default="si")
    actividades_ingles = models.CharField(max_length=100, choices=ACTIVIDADES_CHOICES, verbose_name="¿Se realizan actividades especiales que promueven el aprendizaje y uso del idioma inglés que nacen desde su Centro Educativo?")
    actividades_ingles = models.CharField(max_length=100, choices=ACTIVIDADES_CHOICES, verbose_name="¿Se realizan actividades especiales que promueven el aprendizaje y uso del idioma inglés que nacen desde su Centro Educativo?")
    actividades_ingles = models.CharField(max_length=100, choices=ACTIVIDADES_CHOICES, verbose_name="¿Se realizan actividades especiales que promueven el aprendizaje y uso del idioma inglés que nacen desde su Centro Educativo?")
    participacion_estudiantes = models.CharField(max_length=20, choices=ACTIVIDADES_CHOICES, verbose_name="¿Cuantos estudiantes participan actualmente en estas actividades por grado?", default="siempre")
    actividades_meduca_centro = models.CharField(max_length=20, choices=ACTIVIDADES_CHOICES, verbose_name="¿Se realizan actividades especiales que promueven el aprendizaje y uso del idioma inglés que nacen desde MEDUCA y se realizan en su Centro Educativo?", default="si")
    actividades_externas_centro = models.CharField(max_length=20, choices=ACTIVIDADES_CHOICES, verbose_name="¿Se realizan actividades especiales que promueven el aprendizaje y uso del idioma inglés que nacen desde fundaciones, otras instituciones, empresa privada u otros organismos que se realizan en su Centro Educativo?", default="si")
    GRADO_CHOICES = [
    ('pre_kinder', 'Pre Kinder'),
    ('kinder', 'Kinder'),
    ('1', '1° Grado'), 
    ('2', '2° Grado'),
    ('3', '3° Grado'),
    ('4', '4° Grado'),
    ('5', '5° Grado'),
    ('6', '6° Grado'),
    ('7', '7° Grado'),
    ('8', '8° Grado'),
    ('9', '9° Grado'),
    ('10', '10° Grado'),
    ('11', '11° Grado'),
    ('12', '12° Grado'),
    ]

    ACTIVIDAD_CHOICES = [
        ('ninguno', 'Ninguno'),
        ('algunos', 'Algunos'),
        ('alrededor_mitad', 'Alrededor de la mitad'),
        ('mas_mitad', 'Más de la mitad'),
        ('todos', 'Todos'),
    ]

    grado = models.CharField(max_length=20, choices=GRADO_CHOICES, verbose_name='Grado', default='pre_kinder')
    participacion = models.CharField(max_length=20, choices=ACTIVIDAD_CHOICES, verbose_name='Participación de Estudiantes', default='ninguno')
    detalle_actividades_anual = models.CharField(max_length=50, default='')
    frecuencia_ingles_clase = models.CharField(max_length=50, default='')
    porcentaje_ingles_clase = models.CharField(max_length=50, default='')
    incentivo_ingles_clase = models.CharField(max_length=50, default='')
    promocion_ingles_estudiantes = models.CharField(max_length=50, default='')
    interes_formacion_bilingue = models.CharField(max_length=50, default='')
    prioridad_ppb = models.CharField(max_length=50, default='')
    responsabilidad_docentes = models.CharField(max_length=50, default='')
    pregunta_1 = models.CharField(max_length=200, default='')
    materiales_ingles = models.CharField(max_length=3, choices=[("si", "Sí"), ("no", "No")], default="si")
    senialetica_ingles = models.TextField(default='')
    folios = models.BooleanField(default=False)
    cuadernos = models.BooleanField(default=False)
    libretas = models.BooleanField(default=False)
    carpetas = models.BooleanField(default=False)
    sobres = models.BooleanField(default=False)
    boligrafos = models.BooleanField(default=False)
    lapices = models.BooleanField(default=False)
    rotuladores = models.BooleanField(default=False)
    gomas_borrar = models.BooleanField(default=False)
    tizas = models.BooleanField(default=False)
    cartulinas = models.BooleanField(default=False)
    pinturas = models.BooleanField(default=False)
    pinceles = models.BooleanField(default=False)
    acuarelas = models.BooleanField(default=False)
    plastilina = models.BooleanField(default=False)
    pegamento = models.BooleanField(default=False)
    tijeras = models.BooleanField(default=False)
    papel_celofan = models.BooleanField(default=False)
    tubos_ensayo = models.BooleanField(default=False)
    probetas = models.BooleanField(default=False)
    pipetas = models.BooleanField(default=False)
    cartuchos_tinta = models.BooleanField(default=False)
    toner_impresoras = models.BooleanField(default=False)
    cds = models.BooleanField(default=False)
    dvds = models.BooleanField(default=False)
    centro_educativo = models.CharField(max_length=255, default='')
    CENTRO_EDUCATIVO_CHOICES = [
    ('fondos_fece', 'Fondos de FECE'),
    ('asociacion_padres', 'Asociación de padres de familia'),
    ('estudiantes_traen', 'Los estudiantes los traen'),
    ('fondos_propios', 'Fondos propios (del director o docente)'),
    ('otro', 'Otro'),
    ]

    SALON_CHOICES = [
        ('si', 'Sí'),
        ('no', 'No'),
    ]

    CANTIDAD_CHOICES = [
        ('no_es_posible_responder', 'No es posible responder'),
        ('1-2', 'Hay 1-2'),
        ('3-4', 'Hay 3-4'),
        ('5_o_mas', 'Hay 5 o más'),
    ]

    nombre = models.CharField(max_length=100, default='')
    centro_educativo = models.CharField(max_length=100, default='')
    medio_compra = models.CharField(max_length=100, choices=CENTRO_EDUCATIVO_CHOICES, default='fondos_fece')
    otro_medio_compra = models.CharField(max_length=100, blank=True, null=True, default='')
    laboratorio = models.CharField(max_length=100, default='')
    numero = models.PositiveIntegerField(default=0)
    salones_laboratorios_informatica = models.CharField(max_length=2, choices=SALON_CHOICES, default='si')
    cantidad_salones_laboratorios = models.CharField(max_length=25, choices=CANTIDAD_CHOICES, blank=True, default='no_es_posible_responder')
    computadora = models.CharField(max_length=100, default='')
    marca = models.CharField(max_length=100, default='')
    ano_fabricacion = models.IntegerField(default=0)
    tiene_bocina = models.BooleanField(default=False)
    tiene_auriculares = models.BooleanField(default=False)
    tiene_microfono = models.BooleanField(default=False)
    tiene_internet = models.BooleanField(default=False)
    laboratorio_idioma_ingles = models.BooleanField(default=False)
    laboratorio_ingles_informatica_mismo = models.BooleanField(default=False)
    recursos_enseñanza_ingles = models.BooleanField(default=False)
    persona_encargada_verificacion = models.BooleanField(default=False)
    nombre_encargado_verificacion = models.CharField(max_length=100, blank=True, null=True, default='')
    persona_encargada_material = models.BooleanField(default=False)
    nombre_encargado_material = models.CharField(max_length=100, blank=True, null=True, default='')
    persona_encargada_capacitacion = models.BooleanField(default=False)
    nombre_encargado_capacitacion = models.CharField(max_length=100, blank=True, null=True, default='')
    persona_encargada_laboratorios = models.BooleanField(default=False)
    nombre_encargado_laboratorios = models.CharField(max_length=100, blank=True, null=True, default='')
    persona_encargada_panama_bilingue = models.BooleanField(default=False)
    nombre_encargado_panama_bilingue = models.CharField(max_length=100, blank=True, null=True, default='')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class CoordinadorTecnologia(models.Model):
    # Multimedia resources
    tiene_multimedia = models.BooleanField(default=False)
    materiales_multimedia = models.JSONField(default=list)
    cantidad_cd = models.IntegerField(default=0)
    cantidad_dvd = models.IntegerField(default=0)
    cantidad_mp4 = models.IntegerField(default=0)
    cantidad_streaming = models.IntegerField(default=0)
    cantidad_otros_multimedia = models.IntegerField(default=0)

    # English learning software details
    software_existencia = models.BooleanField(default=False)
    software_cantidad = models.IntegerField(default=0)
    software_listado = models.TextField(blank=True, null=True)
    software_licencia = models.BooleanField(default=False)
    software_internet_requerido = models.BooleanField(default=False)
    software_usuarios = models.IntegerField(default=0)

    # IT infrastructure
    existencia_laboratorios = models.BooleanField(default=False)
    cantidad_laboratorios = models.IntegerField(default=0)
    computadoras_por_laboratorio = models.IntegerField(default=0)
    marca_equipos = models.CharField(max_length=255, blank=True, null=True)
    ano_fabricacion = models.IntegerField(blank=True, null=True)
    computadoras_bocinas = models.BooleanField(default=False)
    computadoras_auriculares = models.BooleanField(default=False)
    computadoras_microfonos = models.BooleanField(default=False)
    computadoras_internet = models.BooleanField(default=False)

    # Internet and Wi-Fi infrastructure
    internet_existencia = models.BooleanField(default=False)
    tipo_enlace_internet = models.CharField(max_length=100, blank=True, null=True)
    ancho_banda = models.IntegerField(default=0)
    wifi_solucion_existencia = models.BooleanField(default=False)
    wifi_alcance = models.JSONField(default=list)
    wifi_cobertura_porcentaje = models.IntegerField(default=0)
    acceso_wifi_administrativos = models.BooleanField(default=False)
    acceso_wifi_docentes = models.BooleanField(default=False)
    acceso_wifi_estudiantes = models.BooleanField(default=False)
    percepcion_velocidad_internet = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"CoordinadorTecnologia ID: {self.id}"

class OtrosDocentes(models.Model):
    habla_ingles_otras_asignaturas = models.BooleanField(default=False)
    porcentaje_tiempo_ingles_otras = models.IntegerField()
    incentiva_hablar_ingles_otras = models.BooleanField(default=False)

    def __str__(self):
        return f"Docente: {self.id}"

class CoordinadorLengua(models.Model):
    # Formulario 1 - Recursos Multimedia
    presentaciones = models.IntegerField(default=0)
    simulaciones = models.IntegerField(default=0)
    juegos = models.IntegerField(default=0)
    objetos_aprendizaje = models.IntegerField(default=0)
    entornos_virtuales = models.IntegerField(default=0)
    cantidad_cd = models.IntegerField(default=0)
    cantidad_dvd = models.IntegerField(default=0)
    cantidad_mp4 = models.IntegerField(default=0)
    cantidad_streaming = models.IntegerField(default=0)
    cantidad_otros = models.IntegerField(default=0)

    # Formulario 2 - Materiales Fungibles
    fungibles_existencia = models.BooleanField(default=False)
    materiales_tipo_ubicacion = models.TextField(blank=True)
    materiales_inventario = models.TextField(blank=True)
    materiales_reposicion = models.CharField(max_length=255, blank=True)
    medios_compra = models.TextField(blank=True)

    def __str__(self):
        return f"Coordinador de Lengua: {self.id}"
    
class ESTER(models.Model):
    cantidad_cursos = models.IntegerField(default=0, help_text="Cantidad de cursos disponibles en ESTER")
    cantidad_ova = models.IntegerField(default=0, help_text="Cantidad de Objetos Virtuales de Aprendizaje (OVA) disponibles")
    cantidad_libros_ingles = models.IntegerField(default=0, help_text="Cantidad de libros en inglés disponibles")
    cantidad_audiolibros = models.IntegerField(default=0, help_text="Cantidad de audiolibros disponibles")
    cantidad_otros_recursos = models.IntegerField(default=0, help_text="Cantidad de otros recursos disponibles")

    acceso_ester_numero_2023_2024 = models.IntegerField(default=0, help_text="Número total de accesos de directores y docentes al Ecosistema ESTER durante 2023 y 2024")
    acceso_ester_porcentaje_2023_2024 = models.IntegerField(default=0, help_text="Porcentaje de acceso de directores y docentes al Ecosistema ESTER durante 2023 y 2024", validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f"ESTER Recursos ID: {self.id}"