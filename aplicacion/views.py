from django.shortcuts import render, redirect
from django.core import serializers
import json
from microsoft_authentication.auth.auth_decorators import microsoft_login_required
from django.views.generic import TemplateView
import requests
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.http import HttpResponseRedirect, JsonResponse
import xlsxwriter
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.models import User
from aplicacion.models import User, Docente
from django.db.models import Count, Sum, Avg
from django.utils.safestring import mark_safe
import json

# Create your views here.
def home(request):
    if "token_cache" not in request.session.keys():
        return render(request, "aplicacion/index.html")
    else:
        return redirect("formulario")

@microsoft_login_required()
def formulario(request):
    complete_session(request=request)
    usuario_nivel = request.session['user_data']['NIVEL_DESC']
    if usuario_nivel == 'DOCENTE':
        return redirect('docente')
    else:
        if usuario_nivel == 'DIRECTOR':
            return redirect('director')
        else:
            return redirect('microsoft_authentication/logout/')


@microsoft_login_required()
def hello(request):
    complete_session(request=request)
    niveles_educativos = [nivel['Nivel_educativo'] for nivel in request.session["user_data"]["Nivel"]]
    return render(request, "aplicacion/hello.html", {
        'data': request.session["user_data"],
        'niveles_educativos': niveles_educativos
    })

@microsoft_login_required()
def docente(request):
    if is_docente(request):
        nombre_usuario = request.session["user_data"]["NOMBRE_USUARIO"]
        partes_nombre = nombre_usuario.split()
        if len(partes_nombre) == 2:
            nombre, apellido = partes_nombre
        elif len(partes_nombre) > 2:
            nombre = " ".join(partes_nombre[:2])
            apellido = " ".join(partes_nombre[2:])
        else:
            nombre = partes_nombre[0]
            apellido = ""

        return render(request, "aplicacion/docente.html", {
            "nombre": nombre,
            "apellido": apellido,
            "cedula_usuario": request.session["user_data"]["CEDULA_USUARIO"],
            "correo_usuario": request.session["user_data"]["CORREO_USUARIO"],
        })
    else:
        return redirect('formulario')

def docente_bd(request):
    contexto = {'docente': Docente.objects.all()}
    return render(request, "aplicacion/docente_bd.html", contexto)

def export_docente(request):
    # Obtener los datos para exportar
    docentes = Docente.objects.all()

    # Crear un nuevo libro de trabajo de Excel
    workbook = xlsxwriter.Workbook('formulario_docente.xlsx')
    worksheet = workbook.add_worksheet()

    # Escribir los encabezados de las columnas
    headers = [
        'Nombre', 'Apellido', 'Cédula', 'Teléfono Oficina', 'Teléfono Personal',
        'Correo Institucional', 'Habla Inglés en Clase', 'Porcentaje de Tiempo en Inglés',
        'Incentiva Hablar Inglés', 'Tiempo de Diálogo en Inglés', 'Tipo de Señalizaciones en Inglés',
        'Señalizaciones en el Aula de Inglés', 'Cantidad de Señalizaciones en el Aula de Inglés',
        'Interactúa con Directivos en Inglés', 'Interactúa con Docentes en Inglés',
        'Interactúa con Padres en Inglés', 'Interactúa con Estudiantes en Inglés',
        'Porcentaje de Interacción con Estudiantes en Inglés', 'Actividades de Inglés Fuera del Aula',
        'Frecuencia de Actividades de Inglés', 'Experiencia en Años', 'Sector de Experiencia',
        'Niveles Impartidos', 'Nivel Actual', 'Título de Enseñanza de Inglés',
        'Títulos Formales en Inglés', 'Cursos Nacionales de Inglés', 'Cursos Internacionales de Inglés',
        'Certificación de Inglés', 'Nombre de la Titulación', 'Año de Certificación',
        'Vencimiento de la Certificación', 'Nivel de Inglés del Docente',
        'Dispuesto a Renovar Certificación', 'Frecuencia de Uso de Recursos de Inglés',
        'Acceso a Recursos de Inglés'
    ]
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    # Escribir los datos de los docentes en el archivo Excel
    for row, docente in enumerate(docentes):
        worksheet.write(row + 1, 0, docente.nombre)
        worksheet.write(row + 1, 1, docente.apellido)
        worksheet.write(row + 1, 2, docente.cedula)
        worksheet.write(row + 1, 3, docente.telefono_oficina)
        worksheet.write(row + 1, 4, docente.telefono_personal)
        worksheet.write(row + 1, 5, docente.correo_institucional)
        worksheet.write(row + 1, 6, docente.habla_ingles_en_clase)
        worksheet.write(row + 1, 7, docente.porcentaje_tiempo_ingles)
        worksheet.write(row + 1, 8, docente.incentiva_hablar_ingles)
        worksheet.write(row + 1, 9, docente.tiempo_dialogo_ingles)
        worksheet.write(row + 1, 10, docente.tipo_senalizaciones_ingles)
        worksheet.write(row + 1, 11, docente.senalizaciones_aula_ingles)
        worksheet.write(row + 1, 12, docente.cantidad_senalizaciones_aula)
        worksheet.write(row + 1, 13, docente.interactua_directivos_ingles)
        worksheet.write(row + 1, 14, docente.interactua_docentes_ingles)
        worksheet.write(row + 1, 15, docente.interactua_padres_ingles)
        worksheet.write(row + 1, 16, docente.interactua_estudiantes_ingles)
        worksheet.write(row + 1, 17, docente.porcentaje_interaccion_estudiantes)
        worksheet.write(row + 1, 18, docente.actividades_ingles_fuera_aula)
        worksheet.write(row + 1, 19, docente.frecuencia_actividades_ingles)
        worksheet.write(row + 1, 20, docente.experiencia_anos)
        worksheet.write(row + 1, 21, docente.sector_experiencia)
        worksheet.write(row + 1, 22, docente.niveles_impartidos)
        worksheet.write(row + 1, 23, docente.nivel_actual)
        worksheet.write(row + 1, 24, docente.titulo_ensenanza_ingles)
        worksheet.write(row + 1, 25, docente.titulos_formales_ingles)
        worksheet.write(row + 1, 26, docente.cursos_nacionales_ingles)
        worksheet.write(row + 1, 27, docente.cursos_internacionales_ingles)
        worksheet.write(row + 1, 28, docente.certificacion_ingles)
        worksheet.write(row + 1, 29, docente.nombre_titulacion)
        worksheet.write(row + 1, 30, docente.ano_certificacion)
        worksheet.write(row + 1, 31, docente.vencimiento_certificacion)
        worksheet.write(row + 1, 32, docente.nivel_ingles_docente)
        worksheet.write(row + 1, 33, docente.dispuesto_renovar_certificacion)
        worksheet.write(row + 1, 34, docente.frecuencia_uso_recursos_ingles)
        worksheet.write(row + 1, 35, docente.acceso_recursos_ingles)

    # Cerrar el libro de trabajo
    workbook.close()

    # Devolver el archivo Excel como respuesta HTTP para descargar
    with open('formulario_docente.xlsx', 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="formulario_docente.xlsx"'
    return response

def form_docente(request):
    if request.method == 'POST':
        # Recoger los datos del formulario
        docente = Docente(
            nombre=request.POST.get('nombre-docente'),
            apellido=request.POST.get('apellido-docente'),
            cedula=request.POST.get('cedula-docente'),
            telefono_oficina=request.POST.get('tel-ofi-docente', ''),
            telefono_personal=request.POST.get('tel-per-docente', ''),
            correo_institucional=request.POST.get('correo-inst-docente'),
            porcentaje_planes_completados=request.POST.get('porcentaje-planes-completados'),
            ajuste_plan_estudios=request.POST.get('ajuste_plan_estudios'),
            dicta_mas_de_un_nivel=request.POST.get('dicta-mas-de-un-nivel') == 'si',
            niveles=request.POST.get('niveles', ''),
            horas_clase_ingles=request.POST.get('horas-clase-ingles'),
            frecuencia_habla_ingles=request.POST.get('frecuencia-habla-ingles'),
            porcentaje_tiempo_ingles=request.POST.get('porcentaje-tiempo-ingles'),
            incentiva_hablar_ingles=request.POST.get('incentiva-hablar-ingles'),
            porcentaje_promueve_ingles=request.POST.get('porcentaje-promueve-ingles'),
            tiempo_dialogo_ingles=request.POST.get('tiempo-dialogo-ingles'),
            senalizaciones_centro_ingles=request.POST.get('senalizaciones-centro-ingles'),
            senalizaciones_ingles=request.POST.get('senalizaciones_ingles'),
            senalizaciones_ingles_opciones=request.POST.getlist('senalizaciones_ingles_opciones'),
            senaletica=request.POST.get('senaletica'),
            cantidad_senalizaciones_aula=request.POST.get('cantidad-senalizaciones-aula'),
            frecuencia_interaccion_directivos=request.POST.get('frecuencia_interaccion_directivos'),
            frecuencia_interaccion_docente=request.POST.get('frecuencia_interaccion_docente'),
            frecuencia_interaccion_padres=request.POST.get('frecuencia_interaccion_padres'),
            interactua_estudiantes=request.POST.get('interactua-estudiantes'),
            actividades_ingles=request.POST.get('actividades_ingles'),
            actividades_ingles_descripcion=request.POST.get('actividades_ingles_descripcion', ''),
            frecuencia_actividades=request.POST.get('frecuencia_actividades', ''),
            anos_experiencia=request.POST.get('anos-experiencia'),
            sector_experiencia=request.POST.get('sector-experiencia'),
            niveles_impartidos=request.POST.getlist('niveles-impartidos'),
            nivel_imparte_actualmente=request.POST.get('nivel-actual'),
            titulo_ensenanza=request.POST.get('titulo-ensenanza'),
            nivel_titulo=request.POST.get('nivel-titulo-select'),
            titulos_formales=request.POST.get('titulos-formales'),
            cursos_educacion_continua=request.POST.get('tipo-curso'),
            certificacion_ingles=request.POST.get('certificacion-ingles'),
            nombre_titulacion=request.POST.get('nombre-titulacion'),
            nivel_ingles_docente=request.POST.get('nivel-ingles-docente'),
            renovar_certificacion=request.POST.get('renovar-certificacion'),
            importancia_formacion_bilingue=request.POST.get('importancia-formacion-bilingue'),
            valoracion_formacion_bilingue=request.POST.get('valoracion-formacion-bilingue'),
            involucramiento_direccion_CE=request.POST.get('involucramiento-direccion-CE'),
            expectativas_director=request.POST.get('expectativas-director'),
            responsabilidad_director=request.POST.get('responsabilidad-director'),
            prioridad_ppb=request.POST.get('prioridad-ppb'),
            participacion_padres=request.POST.get('participacion-padres'),
            frecuencia_recursos=request.POST.get('frecuencia-recursos'),
            acceso_recursos=request.POST.get('acceso-recursos'),
            cooperacion_ppb=request.POST.get('cooperacion-ppb'),
            cooperacion_participacion_ppb=request.POST.get('cooperacion-participacion-ppb'),

        )
        docente.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': 'Invalid request'}, status=400)


@microsoft_login_required()
def director(request):
    complete_session(request=request)
    niveles_educativos = [nivel['Nivel_educativo'] for nivel in request.session["user_data"]["Nivel"]]
    if is_director(request):
        nombre_usuario = request.session["user_data"]["NOMBRE_USUARIO"]
        partes_nombre = nombre_usuario.split()
        if len(partes_nombre) == 2:
            nombre, apellido = partes_nombre
        elif len(partes_nombre) > 2:
            nombre = " ".join(partes_nombre[:2])
            apellido = " ".join(partes_nombre[2:])
        else:
            nombre = partes_nombre[0]
            apellido = ""


        return render(request, "aplicacion/director.html",{
            "nombre": nombre,
            "apellido": apellido,
            "cedula_usuario": request.session["user_data"]["CEDULA_USUARIO"],
            "correo_usuario": request.session["user_data"]["CORREO_USUARIO"],
            "cod_siace": request.session["user_data"]["COD_SIACE"],
            "nombre_escuela": request.session["user_data"]["NOMBRE_ESCUELA"],
            "distrito": request.session["user_data"]["DISTRITO"],
            "provincia": request.session["user_data"]["PROVINCIA"],
            "corregimiento": request.session["user_data"]["CORREGIMIENTO"],
            "latitud_longitud": request.session["user_data"]["LATITUD_LONGITUD"],
            "nivel": request.session["user_data"]["Nivel"][0]["Nivel_educativo"],

            'data': request.session["user_data"],
            'niveles_educativos': niveles_educativos
            
        })
    else:
        return redirect('formulario')

def director_bd(request):
    contexto = {'director': Director.objects.all()}
    return render(request, "aplicacion/director_bd.html", contexto)

def export_director(request):
    # Obtener los datos para exportar
    directores = Director.objects.all()

    # Crear un nuevo libro de trabajo de Excel
    workbook = xlsxwriter.Workbook('formulario_director.xlsx')
    worksheet = workbook.add_worksheet()

    # Escribir los encabezados de las columnas
    headers = [
        'Nombre', 'Apellido', 'Cédula', 'Teléfono Oficina', 'Teléfono Personal',
        'Correo Institucional', 'Correo Personal 1', 'Correo Personal 2', 'Código SIACE',
        'Nombre Centro Educativo', 'Región Educativa', 'Provincia', 'Dirección',
        'Nivel Escolar', 'Matrícula Total', 'Grado 1', 'Femenino 1', 'Masculino 1',
        'Grado 2', 'Femenino 2', 'Masculino 2', 'Grado 3', 'Femenino 3', 'Masculino 3',
        'Grado 4', 'Femenino 4', 'Masculino 4', 'Total Docentes', 'Docentes 1', 'Docentes 2',
        'Docentes 3', 'Docentes 4', 'Estudiantes Salón', 'Docentes Asignatura',
        'Participa PPB', 'Estudiantes Nivel PPB', 'Docentes Capacitados PPB',
        'Docentes Aprobados PPB', 'Docentes Capacitación Exterior', 'Códigos Plan Estudio',
        'Planes Estudio', 'Asignaturas Inglés Plan Estudios', 'Asignaturas Inglés Dictadas',
        'Planes Clase', 'Horas Inglés', 'Horas Teóricas', 'Horas Prácticas',
        'Actividades Propio Centro', 'Actividades MEDUCA Centro', 'Actividades Externas Centro',
        'Detalle Actividades Anual', 'Cantidad Estudiantes Actividades Externas 1',
        'Cantidad Estudiantes Actividades Externas 2', 'Cantidad Estudiantes Actividades Externas 3',
        'Cantidad Estudiantes Actividades Externas 4', 'After School Existencia',
        'After School Descripción', 'After School Participación 1', 'After School Participación 2',
        'After School Participación 3', 'After School Participación 4', 'After School Recursos'
    ]
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    # Escribir los datos de los directores en el archivo Excel
    for row, director in enumerate(directores):
        worksheet.write(row + 1, 0, director.nombre)
        worksheet.write(row + 1, 1, director.apellido)
        worksheet.write(row + 1, 2, director.cedula)
        worksheet.write(row + 1, 3, director.telefono_oficina)
        worksheet.write(row + 1, 4, director.telefono_personal)
        worksheet.write(row + 1, 5, director.correo_institucional)
        worksheet.write(row + 1, 6, director.correo_personal1)
        worksheet.write(row + 1, 7, director.correo_personal2)
        worksheet.write(row + 1, 8, director.codigo_siace)
        worksheet.write(row + 1, 9, director.nombre_centro_educativo)
        worksheet.write(row + 1, 10, director.region_educativa)
        worksheet.write(row + 1, 11, director.provincia)
        worksheet.write(row + 1, 12, director.direccion)
        worksheet.write(row + 1, 13, director.nivel_escolar)
        worksheet.write(row + 1, 14, director.matricula_total)
        worksheet.write(row + 1, 15, director.grado1)
        worksheet.write(row + 1, 16, director.femenino1)
        worksheet.write(row + 1, 17, director.masculino1)
        worksheet.write(row + 1, 18, director.grado2)
        worksheet.write(row + 1, 19, director.femenino2)
        worksheet.write(row + 1, 20, director.masculino2)
        worksheet.write(row + 1, 21, director.grado3)
        worksheet.write(row + 1, 22, director.femenino3)
        worksheet.write(row + 1, 23, director.masculino3)
        worksheet.write(row + 1, 24, director.grado4)
        worksheet.write(row + 1, 25, director.femenino4)
        worksheet.write(row + 1, 26, director.masculino4)
        worksheet.write(row + 1, 27, director.total_docentes)
        worksheet.write(row + 1, 28, director.docentes1)
        worksheet.write(row + 1, 29, director.docentes2)
        worksheet.write(row + 1, 30, director.docentes3)
        worksheet.write(row + 1, 31, director.docentes4)
        worksheet.write(row + 1, 32, director.estudiantes_salon)
        worksheet.write(row + 1, 33, director.docentes_asignatura)
        worksheet.write(row + 1, 34, director.participa_ppb)
        worksheet.write(row + 1, 35, director.estudiantes_nivel_ppb)
        worksheet.write(row + 1, 36, director.docentes_capacitados_ppb)
        worksheet.write(row + 1, 37, director.docentes_aprobados_ppb)
        worksheet.write(row + 1, 38, director.docentes_capacitacion_exterior)
        worksheet.write(row + 1, 39, director.codigos_plan_estudio)
        worksheet.write(row + 1, 40, director.planes_estudio)
        worksheet.write(row + 1, 41, director.asignaturas_ingles_plan_estudios)
        worksheet.write(row + 1, 42, director.asignaturas_ingles_dictadas)
        worksheet.write(row + 1, 43, director.planes_clase)
        worksheet.write(row + 1, 44, director.horas_ingles)
        worksheet.write(row + 1, 45, director.horas_teoricas)
        worksheet.write(row + 1, 46, director.horas_practicas)
        worksheet.write(row + 1, 47, director.actividades_propio_centro)
        worksheet.write(row + 1, 48, director.actividades_meduca_centro)
        worksheet.write(row + 1, 49, director.actividades_externas_centro)
        worksheet.write(row + 1, 50, director.detalle_actividades_anual)
        worksheet.write(row + 1, 51, director.cantidad_estudiantes_actividades_externas_1)
        worksheet.write(row + 1, 52, director.cantidad_estudiantes_actividades_externas_2)
        worksheet.write(row + 1, 53, director.cantidad_estudiantes_actividades_externas_3)
        worksheet.write(row + 1, 54, director.cantidad_estudiantes_actividades_externas_4)
        worksheet.write(row + 1, 55, director.after_school_existencia)
        worksheet.write(row + 1, 56, director.after_school_descripcion)
        worksheet.write(row + 1, 57, director.after_school_participacion_1)
        worksheet.write(row + 1, 58, director.after_school_participacion_2)
        worksheet.write(row + 1, 59, director.after_school_participacion_3)
        worksheet.write(row + 1, 60, director.after_school_participacion_4)
        worksheet.write(row + 1, 61, director.after_school_recursos)

    # Cerrar el libro de trabajo
    workbook.close()

    # Devolver el archivo Excel como respuesta HTTP para descargar
    with open('formulario_director.xlsx', 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="formulario_director.xlsx"'
    return response

def form_director(request):
    if request.method == 'POST':
        # Procesar el formulario enviado
        nombre = request.POST.get('nombre', 'N/A')
        apellido = request.POST.get('apellido', 'N/A')
        cedula = request.POST.get('cedula', 'N/A')
        telefono_oficina = request.POST.get('telefono_oficina', 'N/A')
        telefono_personal = request.POST.get('telefono_personal', 'N/A')
        correo_institucional = request.POST.get('correo_institucional', 'N/A')
        correo_personal1 = request.POST.get('correo_personal1', 'N/A')
        correo_personal2 = request.POST.get('correo_personal2', 'N/A')
        codigo_siace = request.POST.get('codigo_siace', 'N/A')
        nombre_centro_educativo = request.POST.get('nombre_centro_educativo', 'N/A')
        region_educativa = request.POST.get('region_educativa', 'N/A')
        provincia = request.POST.get('provincia', 'N/A')
        direccion = request.POST.get('direccion', 'N/A')
        nivel_escolar = request.POST.get('nivel_escolar', 'N/A')
        matricula_total = request.POST.get('matricula_total', 0)
        grado1 = request.POST.get('grado1', 0)
        femenino1 = request.POST.get('femenino1', 0)
        masculino1 = request.POST.get('masculino1', 0)
        grado2 = request.POST.get('grado2', 0)
        femenino2 = request.POST.get('femenino2', 0)
        masculino2 = request.POST.get('masculino2', 0)
        grado3 = request.POST.get('grado3', 0)
        femenino3 = request.POST.get('femenino3', 0)
        masculino3 = request.POST.get('masculino3', 0)
        grado4 = request.POST.get('grado4', 0)
        femenino4 = request.POST.get('femenino4', 0)
        masculino4 = request.POST.get('masculino4', 0)
        total_docentes = request.POST.get('total_docentes', 'N/A')
        docentes1 = request.POST.get('docentes1', 'N/A')
        docentes2 = request.POST.get('docentes2', 'N/A')
        docentes3 = request.POST.get('docentes3', 'N/A')
        docentes4 = request.POST.get('docentes4', 'N/A')
        estudiantes_salon = request.POST.get('estudiantes_salon', 'N/A')
        docentes_asignatura = request.POST.get('docentes_asignatura', 'N/A')
        participa_ppb = request.POST.get('participa_ppb', False)
        estudiantes_nivel_ppb = request.POST.get('estudiantes_nivel_ppb', 'N/A')
        docentes_capacitados_ppb = request.POST.get('docentes_capacitados_ppb', 'N/A')
        docentes_aprobados_ppb = request.POST.get('docentes_aprobados_ppb', 'N/A')
        docentes_capacitacion_exterior = request.POST.get('docentes_capacitacion_exterior', 'N/A')
        codigos_plan_estudio = request.POST.get('codigos_plan_estudio', False)
        planes_estudio = request.POST.get('planes_estudio', False)
        asignaturas_ingles_plan_estudios = request.POST.get('asignaturas_ingles_plan_estudios', False)
        asignaturas_ingles_dictadas = request.POST.get('asignaturas_ingles_dictadas', False)
        planes_clase = request.POST.get('planes_clase', 'N/A')
        horas_ingles = request.POST.get('horas_ingles', 'N/A')
        horas_teoricas = request.POST.get('horas_teoricas', 'N/A')
        horas_practicas = request.POST.get('horas_practicas', 'N/A')
        actividades_propio_centro = request.POST.get('actividades_propio_centro', 'Nunca o Casi Nunca')
        cantidad_estudiantes_actividades_externas_1 = request.POST.get('cantidad_estudiantes_actividades_externas_1', 'Nunca o Casi Nunca')
        actividades_meduca_centro = request.POST.get('actividades_meduca_centro', 'Nunca o Casi Nunca')
        cantidad_estudiantes_actividades_especiales_1 = request.POST.get('cantidad_estudiantes_actividades_especiales_1', 'Nunca o Casi Nunca')
        actividades_externas_centro = request.POST.get('actividades_externas_centro', 'Nunca o Casi Nunca')
        cantidad_estudiantes_actividades_centro_1 = request.POST.get('cantidad_estudiantes_actividades_centro_1', 'Nunca o Casi Nunca')
        detalle_actividades_anual = request.POST.get('detalle_actividades_anual', 'Nunca o Casi Nunca')
        after_school_existencia = request.POST.get('after_school_existencia', 'no')
        after_school_descripcion = request.POST.get('after_school_descripcion', 'no')
        after_school_participacion_1 = request.POST.get('after_school_participacion_1', 'Nunca o Casi Nunca')

        # Crear una instancia del modelo Director con los datos obtenidos
        director = Director(
            nombre=nombre,
            apellido=apellido,
            cedula=cedula,
            telefono_oficina=telefono_oficina,
            telefono_personal=telefono_personal,
            correo_institucional=correo_institucional,
            correo_personal1=correo_personal1,
            correo_personal2=correo_personal2,
            codigo_siace=codigo_siace,
            nombre_centro_educativo=nombre_centro_educativo,
            region_educativa=region_educativa,
            provincia=provincia,
            direccion=direccion,
            nivel_escolar=nivel_escolar,
            matricula_total=matricula_total,
            grado1=grado1,
            femenino1=femenino1,
            masculino1=masculino1,
            grado2=grado2,
            femenino2=femenino2,
            masculino2=masculino2,
            grado3=grado3,
            femenino3=femenino3,
            masculino3=masculino3,
            grado4=grado4,
            femenino4=femenino4,
            masculino4=masculino4,
            total_docentes=total_docentes,
            docentes1=docentes1,
            docentes2=docentes2,
            docentes3=docentes3,
            docentes4=docentes4,
            estudiantes_salon=estudiantes_salon,
            docentes_asignatura=docentes_asignatura,
            participa_ppb=participa_ppb,
            estudiantes_nivel_ppb=estudiantes_nivel_ppb,
            docentes_capacitados_ppb=docentes_capacitados_ppb,
            docentes_aprobados_ppb=docentes_aprobados_ppb,
            docentes_capacitacion_exterior=docentes_capacitacion_exterior,
            codigos_plan_estudio=codigos_plan_estudio,
            planes_estudio=planes_estudio,
            asignaturas_ingles_plan_estudios=asignaturas_ingles_plan_estudios,
            asignaturas_ingles_dictadas=asignaturas_ingles_dictadas,
            planes_clase=planes_clase,
            horas_ingles=horas_ingles,
            horas_teoricas=horas_teoricas,
            horas_practicas=horas_practicas,
            actividades_propio_centro=actividades_propio_centro,
            cantidad_estudiantes_actividades_externas_1=cantidad_estudiantes_actividades_externas_1,
            actividades_meduca_centro=actividades_meduca_centro,
            cantidad_estudiantes_actividades_especiales_1=cantidad_estudiantes_actividades_especiales_1,
            actividades_externas_centro=actividades_externas_centro,
            cantidad_estudiantes_actividades_centro_1=cantidad_estudiantes_actividades_centro_1,
            detalle_actividades_anual=detalle_actividades_anual,
            after_school_existencia=after_school_existencia,
            after_school_descripcion=after_school_descripcion,
            after_school_participacion_1=after_school_participacion_1
        )
        director.save()

        return HttpResponseRedirect('/gracias/')

    return render(request, 'aplicacion/director.html')

@microsoft_login_required()
def coordinador_5(request):
    return render(request, "aplicacion/coordinador_5.html")

@microsoft_login_required()
def tecnologia_6(request):
    return render(request, "aplicacion/tecnologia_6.html")

@microsoft_login_required()
def otros_docentes_7(request):
    return render(request, "aplicacion/otros_docentes_7.html")

@microsoft_login_required()
def lengua_8(request):
    return render(request, "aplicacion/lengua_8.html")

@microsoft_login_required()
def ester_9(request):
    return render(request, "aplicacion/ESTER_9.html")

@microsoft_login_required()
def gracias(request):
    return render(request, "aplicacion/gracias.html")

class logout_page(TemplateView):
    template_name = 'admin/logout.html'

def complete_session(request):
    if "user_data" not in request.session.keys():
        session_data = json.loads(request.session["token_cache"])
        access_token_dict = session_data["AccessToken"]
        account_dict = session_data["Account"]
        token_data_id = next(iter(access_token_dict))
        account_data_id = next(iter(account_dict))
        account = account_dict[account_data_id]["username"]
        access_token = access_token_dict[token_data_id]["secret"]

        url = f"https://formulario-api-aeekxgs7da-uc.a.run.app/api/user/{account}"
        headers = {'Authorization': access_token}
        response = requests.get(url, headers = headers)
        response_json = response.json()
        request.session["user_data"] = response_json
        
def is_docente(request):
    return request.session['user_data']['NIVEL_DESC'] == 'DOCENTE'

def is_director(request):
    return request.session['user_data']['NIVEL_DESC'] == 'DIRECTOR'
# def make_redirect(request):
#     sesion_data = serializers.deserialize('json', request.session["token_cache"])

# def request_user_data(token):
#     return token
def crear_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin:index')  # Redirige al panel de administración
    else:
        form = UserCreationForm()
    return render(request, 'aplicacion/crear_user.html', {'form': form})

def editar_user(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin:index')  # Redirige al panel de administración
    else:
        form = UserEditForm(instance=user)
    return render(request, 'aplicacion/editar_user.html', {'form': form})

def eliminar_user(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('admin:index')  # Redirige al panel de administración
    return render(request, 'aplicacion/eliminar_user.html', {'user': user})

def user(request):
    users = User.objects.all()
    return render(request, 'admin/user.html', {'users': users})


#VISTAS PARA LOS GRAFICOS

@microsoft_login_required()
def graficos(request):
    # Lógica para obtener y procesar los datos de centros educativos
    complete_session_centros_educativos(request)
    data = request.session.get("centros_educativos_data", {})

    if data:
        for centro in data:
            for key, value in centro.items():
                if value is None:
                    centro[key] = 'No disponible'

    data_json = mark_safe(json.dumps(data))

    # Indicadores
    porcentaje_certificados = porcentaje_docentes_certificados()

    # Renderizar la plantilla con el contexto necesario
    return render(request, "aplicacion/graficos.html", {
        'data_json': data_json,
        'porcentaje_certificados': porcentaje_certificados
    })

def datos_nivel_bilinguismo(request):
    niveles = Docente.objects.values('nivel_ingles_docente').annotate(total=Count('nivel_ingles_docente')).order_by('nivel_ingles_docente')
    data = {
        'niveles': list(niveles)
    }
    return JsonResponse(data)

#Promedio porcentaje de actividades de bilinguismo
def promedios_generales(request):
    promedio_tiempo_ingles = Docente.objects.aggregate(Avg('porcentaje_tiempo_ingles'))['porcentaje_tiempo_ingles__avg'] or 0
    promedio_tiempo_dialogo_ingles = Docente.objects.aggregate(Avg('tiempo_dialogo_ingles'))['tiempo_dialogo_ingles__avg'] or 0
    promedio_cantidad_senalizaciones = Docente.objects.aggregate(Avg('cantidad_senalizaciones_aula'))['cantidad_senalizaciones_aula__avg'] or 0
    promedio_interaccion_estudiantes = Docente.objects.aggregate(Avg('porcentaje_interaccion_estudiantes'))['porcentaje_interaccion_estudiantes__avg'] or 0
    
    data = {
        'promedio_tiempo_ingles': promedio_tiempo_ingles,
        'promedio_tiempo_dialogo_ingles': promedio_tiempo_dialogo_ingles,
        'promedio_cantidad_senalizaciones': promedio_cantidad_senalizaciones,
        'promedio_interaccion_estudiantes': promedio_interaccion_estudiantes,
    }
    return JsonResponse(data)

# Llamada API para obtener informacionde de centros eduativos
def complete_session_centros_educativos(request):
    if "centros_educativos_data" not in request.session.keys():
        session_data = json.loads(request.session["token_cache"])
        access_token_dict = session_data["AccessToken"]
        token_data_id = next(iter(access_token_dict))
        access_token = access_token_dict[token_data_id]["secret"]

        url = "https://formulario-api-aeekxgs7da-uc.a.run.app/api/centroseducativos"
        headers = {'Authorization': access_token}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_json = response.json()
            request.session["centros_educativos_data"] = response_json
        else:
            print("Error al obtener datos de centros educativos: ", response.status_code)


#Indicador matricula total
def get_matricula_total(request, cod_siace):
    try:
        director = Director.objects.get(codigo_siace=cod_siace)
        return JsonResponse({"matricula_total": director.matricula_total})
    except Director.DoesNotExist:
        return JsonResponse({"error": "Director not found"}, status=404)

def get_docentes_total(request, cod_siace):
    try:
        director = Director.objects.get(codigo_siace=cod_siace)
        return JsonResponse({"docentes_total": director.total_docentes})
    except Director.DoesNotExist:
        return JsonResponse({"error": "Director not found"}, status=404)
        

# Indicador de docentes certificados del idioma ingles
def porcentaje_docentes_certificados():
    total_docentes = Docente.objects.count()
    docentes_certificados = Docente.objects.filter(certificacion_ingles="Sí").count()
    porcentaje_certificados = (docentes_certificados / total_docentes) * 100 if total_docentes > 0 else 0
    return porcentaje_certificados
