import os
import xml.etree.ElementTree as ET
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time  # Importar el módulo time
import logging
import re
import inspect
import ast
import streamlit as st
import pandas as pd

# Configuración del registro de errores
logging.basicConfig(filename='error.log', level=logging.ERROR)

def print_with_line_number(msg):
    caller_frame = inspect.currentframe().f_back
    line_number = caller_frame.f_lineno
    print(f"Linea {line_number}: {msg}")
    print("")         




def extract_osb_services_with_http_provider_id(project_path):
    #print_with_line_number("************EXTRACT_OSB_SERVICES_WITH_HTTP_PROVIDER_ID****************")
    #print_with_line_number("")
    osb_services = []
    print_with_line_number(f"project_path: {project_path}")
    for root, dirs, files in os.walk(project_path):
        #print_with_line_number(f"root: {root}")
        if os.path.basename(root) == "Proxies":
            for file in files:
                if file.endswith('.ProxyService'):
                    osb_file_path = os.path.join(root, file)
                    #print_with_line_number("************EXTRACT_OSB_SERVICES_WITH_HTTP_PROVIDER_ID****************")
                    #print_with_line_number("")
                    #print_with_line_number(f"osb_file_path: {osb_file_path}")
                    project_name = extract_project_name_from_proxy(osb_file_path)
                    #print_with_line_number("")
                    #print_with_line_number("************EXTRACT_OSB_SERVICES_WITH_HTTP_PROVIDER_ID****************")
                    #print_with_line_number("")
                    #print_with_line_number(f"project_name: {project_name}")
                    if project_name is None:
                        continue  # Salta este registro y continúa con el siguiente
                    pipeline_path = extract_pipeline_path_from_proxy(osb_file_path, project_path)
                    #print_with_line_number("************EXTRACT_OSB_SERVICES_WITH_HTTP_PROVIDER_ID****************")
                    #print_with_line_number("")
                    #print_with_line_number(f"pipeline_path: {pipeline_path}")
                    with open(osb_file_path, 'r', encoding="utf-8") as f:
                        content = f.read()
                        #print_with_line_number(f"content: {content}")
                        if has_http_provider_id(content):
                            service_name = os.path.splitext(file)[0]
                            service_url = extract_service_url(content)
                            wsdl_relative_path = extract_wsdl_relative_path(content)
                            print_with_line_number("************EXTRACT_OSB_SERVICES_WITH_HTTP_PROVIDER_ID****************")
                            print_with_line_number("")
                            print_with_line_number("_________PRUEBA__________")
                            print_with_line_number("")
                            print_with_line_number(f"osb_file_path: {osb_file_path}")
                            print_with_line_number(f"project_name: {project_name}")
                            print_with_line_number(f"pipeline_path: {pipeline_path}")
                            print_with_line_number(f"service_name: {service_name}")
                            print_with_line_number(f"service_url: {service_url}")
                            print_with_line_number(f"wsdl_relative_path: {wsdl_relative_path}")
                            print_with_line_number("")
                            print_with_line_number("_________PRUEBA__________")
                            print_with_line_number("")
                            if wsdl_relative_path:
                                wsdl_path = os.path.join(project_path, wsdl_relative_path + ".WSDL")
                                print_with_line_number("************EXTRACT_OSB_SERVICES_WITH_HTTP_PROVIDER_ID****************")
                                print_with_line_number("")
                                print_with_line_number(f"wsdl_path: {wsdl_path}")
                                print_with_line_number("")
                                operations = extract_wsdl_operations(wsdl_path)
                                print_with_line_number("************EXTRACT_OSB_SERVICES_WITH_HTTP_PROVIDER_ID****************")
                                print_with_line_number("")
                                print_with_line_number(f"operations: {operations}")
                                print_with_line_number("")
                                service_for_operations = extract_service_for_operations_audibpel(pipeline_path, operations)
                                print_with_line_number("************EXTRACT_OSB_SERVICES_WITH_HTTP_PROVIDER_ID****************")
                                print_with_line_number("")
                                print_with_line_number(f"service_for_operations: {service_for_operations}")
                                print_with_line_number("")
                                operations_audibpel_exp = {}
                                service_for_operations_new = {}
                                
                                for operation_name, service_refs in service_for_operations.items():
                                    for service_ref, exp_name in service_refs:
                                        
                                        if ' ' in exp_name or 'N/A' in exp_name:
                                            # Extraer el nombre del flujo de trabajo de exp_name
                                            exp_name_cleaned = exp_name  # Obtener 'GestionMediosManejoOficinasVirtualesABC PKG_MEDIOS_MANEJO_OFICINAS_VRT_PR_CONSULTAR_MMAN_OFICINAS_VRT'

                                            # Construir las nuevas variables
                                            operations_audibpel_exp[operation_name] = f"{exp_name_cleaned}"
                                        else:
                                            # Si no hay espacio en blanco, tomar exp_name completo
                                            exp_name_cleaned = exp_name

                                            # Construir las nuevas variables
                                            operations_audibpel_exp[operation_name] = f"{exp_name_cleaned}"

                                        if operation_name not in service_for_operations_new:
                                            service_for_operations_new[operation_name] = []
                                    
                                        service_for_operations_new[operation_name].append(service_ref)                                                              
                                
                                print_with_line_number(f"operations_audibpel_exp: {operations_audibpel_exp}")
                                print_with_line_number("")
                                print_with_line_number(f"service_for_operations_new: {service_for_operations_new}")
                                print_with_line_number("")
                                
                                service_for_operations = service_for_operations_new
                                operaciones_y_ebs = service_for_operations_new
                                # Generar los datos en el formato deseado
                                service_for_operations_resultado = []
                                for operation_name, service_refs in service_for_operations_new.items():
                                    for service_ref in service_refs:
                                        service_for_operations_resultado.append({operation_name: service_ref})
                                
                                
                                for service_for_operations in service_for_operations_resultado:
                                    
                                    print_with_line_number(f"service_for_operations: {service_for_operations}")   
                                    
                                    referencias_for_operations = extract_osb_services_with_given_path(project_path, service_for_operations)
                                    print_with_line_number("************EXTRACT_OSB_SERVICES_WITH_HTTP_PROVIDER_ID****************")
                                    print_with_line_number("")
                                    print_with_line_number(f"referencias_for_operations: {referencias_for_operations}")
                                    print_with_line_number("")
                                    
                                    grouped_data = {}
                                    
                                    
                                    # for service, reference in referencias_for_operations:
                                        # if service not in grouped_data:
                                            # grouped_data[service] = []
                                        # grouped_data[service].append(reference)
                                    
                                    for key, value in referencias_for_operations:
                                        grouped_data[key] = value
                                    
                                    print_with_line_number("************EXTRACT_OSB_SERVICES_WITH_HTTP_PROVIDER_ID****************")
                                    print_with_line_number("")
                                    print_with_line_number(f"grouped_data: {grouped_data}")
                                    
                                    print_with_line_number("")
                                    for service, references in grouped_data.items():
                                        print_with_line_number(f"{service}: {references}")
                                    print_with_line_number("")
                                    print_with_line_number("************VERIFICACION GROUPED_DATA****************")
                                    print_with_line_number("")
                                    
                                    grupo_referencia = []
                                    # Lista para almacenar las claves encontradas
                                    tuplas_extendidas = []
                                    
                                    for operacion, proxies in grouped_data.items():
                                        if isinstance(proxies, list):
                                            grupo = {operacion: proxies}
                                            print_with_line_number(grupo)
                                            print_with_line_number("-------------")
                                            
                                            if(es_operacion_lista_referencias(grupo)):
                                                print_with_line_number("grouped_data_1 sigue la estructura del caso 1")
                                                
                                                
                                                for operacion, proxies in grupo.items():
                                                    for proxy in proxies:
                                                        grupo_referencia_temporal = []

                                                        if 'Business' in proxy:
                                                            print_with_line_number("")
                                                            print_with_line_number(f"El proxy '{proxy}' contiene 'BusinessServices'")
                                                            servicio = service_for_operations.get(operacion, None)
                                                            
                                                            print_with_line_number(f"servicio: {servicio}")
                                                            print_with_line_number("")
                                                            
                                                            # Verificar si el servicio es encontrado
                                                            if servicio:
                                                                # Extraer el nombre del servicio de la ruta del servicio
                                                                nombre_servicio = servicio.split('/')[-1]
                                                                operacion_proxy = proxy.split('/')[-1]
                                                                
                                                                print_with_line_number(f"nombre_servicio: {nombre_servicio}")
                                                                print_with_line_number("")
                                                                print_with_line_number(f"operacion_proxy: {operacion_proxy}")
                                                                print_with_line_number("")
                                                                
                                                                ruta_completa_proxy = os.path.join(project_path, servicio + ".ProxyService")
                                                                
                                                                if os.path.exists(ruta_completa_proxy):
                                                                    ruta_completa_pipeline = extract_pipeline_path_from_proxy(ruta_completa_proxy, project_path)
                                                                    print_with_line_number(f"ruta_completa_pipeline: {ruta_completa_pipeline}")
                                                                    print_with_line_number("")
                                                                    def_op_internas_pipeline = definir_operaciones_internas_pipeline(ruta_completa_pipeline)
                                                                    print_with_line_number(f"def_op_internas_pipeline: {def_op_internas_pipeline}")
                                                                    print_with_line_number("")
                                                                    
                                                                    operacion_proxy = obtener_operacion_por_proxy(def_op_internas_pipeline, proxy)
                                                                    
                                                                    print_with_line_number(f"operacion_proxy: {operacion_proxy}")
                                                                    print_with_line_number("")

                                                                tupla_extendida = (operacion,nombre_servicio,proxy,operacion_proxy)
                                                                
                                                                tuplas_extendidas.append(tupla_extendida)
                                                                
                                                                print_with_line_number(f"tupla_extendida: {tupla_extendida}")
                                                                print_with_line_number("")
                                                                
                                                        else:
                                                            print_with_line_number("")
                                                            print_with_line_number(f"El proxy '{proxy}' no contiene 'BusinessServices'")
                                                            
                                                            ruta_completa_proxy = os.path.join(project_path, proxy + ".ProxyService")
                                                            print_with_line_number(f"ruta_completa_proxy: {ruta_completa_proxy}")
                                                            if os.path.exists(ruta_completa_proxy):
                                                                ruta_completa_pipeline = extract_pipeline_path_from_proxy(ruta_completa_proxy, project_path)
                                                                print_with_line_number(f"ruta_completa_pipeline: {ruta_completa_pipeline}")                                   
                                                                operacion_pipeline = extract_service_refs_from_pipeline(ruta_completa_pipeline)
                                                                print_with_line_number(f"operacion_pipeline: {operacion_pipeline}") 
                                                                if not operacion_pipeline:
                                                                    continue
                                                                ruta_completa_wsdl = os.path.join(project_path, devolver_ruta_wsdl_proxy(ruta_completa_proxy) + ".WSDL")
                                                                print_with_line_number(f"ruta_completa_wsdl: {ruta_completa_wsdl}") 
                                                                operaciones_internas = extract_wsdl_operations(ruta_completa_wsdl)
                                                                print_with_line_number(f"operaciones_internas: {operaciones_internas}")
                                                                operacion_pipeline_por_nombre = extract_service_for_operations(ruta_completa_pipeline, operaciones_internas)
                                                                print_with_line_number(f"operacion_pipeline_por_nombre: {operacion_pipeline_por_nombre}")
                                                                def_op_internas_pipeline = definir_operaciones_internas_pipeline(ruta_completa_pipeline)
                                                                print_with_line_number(f"def_op_internas_pipeline: {def_op_internas_pipeline}")
                                                            
                                                                referencia_operacion = {operacion: proxy}
                                                                print_with_line_number(f"referencia_operacion: {referencia_operacion}")
                                                                grupo_referencia_temporal.append(referencia_operacion)
                                                                print_with_line_number("")
                                                                referencias_for_operations = extract_osb_services_with_given_path_dict(project_path, grupo_referencia_temporal)
                                                                print_with_line_number("")
                                                                print_with_line_number("************GRUPO_REFERENCIA****************")
                                                                print_with_line_number("")
                                                                print_with_line_number(f"referencias_for_operations GRUPO: {referencias_for_operations}")
                                                                print_with_line_number("")
                                                                # print_with_line_number("************GRUPO_REFERENCIA****************")
                                                                print_with_line_number("")
                                                                # grupo_referencia.append(referencias_for_operations)
                                                                print_with_line_number("")


                                                                # Iterar sobre cada tupla en referencias_for_operations
                                                                for tupla in referencias_for_operations:
                                                                    # Obtener el valor de la tercera posición de la tupla
                                                                    valor_tercera_posicion = tupla[2]
                                                                    # Verificar si este valor está en def_op_internas_pipeline
                                                                    if valor_tercera_posicion in def_op_internas_pipeline.values():
                                                                        # Si está, encontrar la clave correspondiente en def_op_internas_pipeline
                                                                        clave_encontrada = next(key for key, value in def_op_internas_pipeline.items() if value == valor_tercera_posicion)
                                                                        # Extender la tupla con la clave encontrada
                                                                        tupla_extendida = tupla + (clave_encontrada,)
                                                                        # Agregar la tupla extendida a la lista
                                                                        tuplas_extendidas.append(tupla_extendida)
                                                                        
                                                                        print_with_line_number(f"tupla_extendida: {tupla_extendida}")


                                                                
                                                                print_with_line_number("")
                                                                print_with_line_number("")
      
                                            if es_operacion_clave_valor(grupo):
                                                print_with_line_number("grouped_data_2 sigue la estructura del caso 2")
                                            
                                        else:
                                            # Si los proxies no son una lista, imprimimos la operación y el proxy directamente
                                            print_with_line_number({operacion: proxies})
                                            print_with_line_number("-------------")
                                            
                                            print_with_line_number("")
                                    
                                    # print_with_line_number(f"grupo_referencia: {grupo_referencia}")
                                    print_with_line_number("")
                                    print_with_line_number("************VERIFICACION GROUPED_DATA****************")
                                    print_with_line_number("")
                                    
                                    print_with_line_number(f"tuplas_extendidas: {tuplas_extendidas}")
                                    print_with_line_number("")
                                    referencias_abc2 = extract_osb_services_references_abc2(project_path, tuplas_extendidas)
                                    print_with_line_number("")
                                    print_with_line_number("")
                                    
                                    # referencias_abc = extract_osb_services_references_abc(project_path, grupo_referencia)
                                    
                                    #referencias_finales = extract_osb_services_finals(project_path, grouped_data)
                                    print_with_line_number("")
                                    print_with_line_number("************EXTRACT_OSB_SERVICES_WITH_HTTP_PROVIDER_ID****************")
                                    print_with_line_number("") 
                                    
                                    print_with_line_number("")
                                    print_with_line_number("-----------------INFO-----------------------")
                                    print_with_line_number(f"project_name: {project_name}")
                                    print_with_line_number("")
                                    print_with_line_number(f"service_name: {service_name}")
                                    print_with_line_number("")
                                    print_with_line_number(f"service_url: {service_url}")
                                    print_with_line_number("")
                                    print_with_line_number(f"operations: {operations}")
                                    print_with_line_number("")
                                    print_with_line_number(f"pipeline_path: {pipeline_path}")
                                    print_with_line_number("")
                                    print_with_line_number(f"operacion_proxy: {service_for_operations}")
                                    print_with_line_number("")
                                    print_with_line_number(f"grouped_data: {grouped_data}")
                                    print_with_line_number("")
                                    print_with_line_number(f"grupo_referencia: {grupo_referencia}")
                                    print_with_line_number("")
                                    print_with_line_number(f"referencias_abc2: {referencias_abc2}")
                                    print_with_line_number("")
                                    print_with_line_number(f"tuplas_extendidas: {tuplas_extendidas}")
                                    print_with_line_number("")
                                    print_with_line_number(f"operations_audibpel_exp: {operations_audibpel_exp}")                                                                                                    
                                    print_with_line_number("-----------------INFO-----------------------")
                                    
                                    print_with_line_number("")
                                    
                                    
                                    print_with_line_number("-----------------INICIO ANALISIS-----------------------")
                                    
                                    
                                    print_with_line_number("")
                                    # Lista para almacenar los resultados
                                    for index, referencia in enumerate(referencias_abc2, start=1):
                                        operacion_abc = referencia[0]
                                        proxy_ebs_completo = service_for_operations.get(operacion_abc)
                                        parts_proxy = proxy_ebs_completo.split('/')
                                        ruta_proxy_ebs = parts_proxy[0]
                                        nombre_ebs = operaciones_y_ebs.get(operacion_abc, None)
                                        print_with_line_number(f"nombre_ebs: {nombre_ebs}")  
                                        cadena = nombre_ebs[0]
                                        proxy_ebs1 = cadena.split("/")[-1]
                                        proxy_ebs2 = referencia[2]
                                        proxy_ebs3 = referencia[3]
                                        num_barras = proxy_ebs3.count("/")
                                        
                                        if num_barras >= 1:
                                            indice_ultimo = proxy_ebs3.rfind("/")
                                            if indice_ultimo != -1:
                                                proxy_abc =  proxy_ebs3[indice_ultimo + 1:]
                                                proxy_ebs3 = proxy_ebs3[:indice_ultimo]
                                        else:
                                            proxy_abc = referencia[3]

                                        ruta_business_completa = referencia[4]
                                        nombre_flujo_audibpel_exp = operations_audibpel_exp.get(operacion_abc)                                                                      
                                        
                                        parts_business = ruta_business_completa.split('/')
                                        proyecto_abc = parts_business[0]
                                        nombre_business = parts_business[-1]
                                        
                                        if 'PS' not in proxy_abc and 'RegistrarAuditoriaSOADATV1.0' not in proxy_abc:
                                            proxy_abc = nombre_business
                                        
                                        url_business = referencia[6]
                                        tipo_business = referencia[7]
                                        operacion_business = referencia[5]
                                        
                                        datos = f"({index},'{service_name}','{operacion_abc}','{project_name}','{service_url}','{nombre_flujo_audibpel_exp}','{ruta_proxy_ebs}','{proxy_ebs1}','{proxy_ebs2}','{proxy_ebs3}','{proxy_abc}', '{proyecto_abc}', '{nombre_business}','{operacion_business}', '{url_business}', '{tipo_business}')"
                                        
                                        print_with_line_number(f"({datos})")
                                        
                                        osb_services.append(datos)
                                        
                                    print_with_line_number("")
                                    
                                    print_with_line_number("-----------------INICIO ANALISIS-----------------------")
                                    
                                    
                                    
                                    print_with_line_number("************EXTRACT_OSB_SERVICES_WITH_HTTP_PROVIDER_ID****************")
                                    print_with_line_number(f"OSB: {osb_services}")
                                    print_with_line_number("")
                                    print_with_line_number("///////////////////////////////////////////////////////")
                                
    return osb_services

def obtener_operacion_por_proxy(dicc_proxies, proxy):
    for operacion, valor_proxy in dicc_proxies.items():
        if valor_proxy == proxy:
            return operacion
    return None
    

# Verificar si grouped_data sigue la estructura del caso 1
def es_operacion_lista_referencias(grouped_data):
    # Iterar sobre los valores del diccionario
    for value in grouped_data.values():
        # Si algún valor no es una lista, retorna False
        if not isinstance(value, list):
            return False
        # Si algún elemento de la lista no es una cadena, retorna False
        if not all(isinstance(item, str) for item in value):
            return False
    # Si todos los valores son listas de cadenas, retorna True
    return True

# Verificar si grouped_data sigue la estructura del caso 2
def es_operacion_clave_valor(grouped_data):
    # Iterar sobre los valores del diccionario
    for value in grouped_data.values():
        # Si algún valor no es una lista, retorna False
        if not isinstance(value, list):
            return False
        # Si algún elemento de la lista no es un diccionario, retorna False
        if not all(isinstance(item, dict) for item in value):
            return False
        # Si algún diccionario tiene más de un elemento, retorna False
        if any(len(item) != 1 for item in value):
            return False
        # Si algún diccionario no tiene una cadena como valor, retorna False
        if not all(isinstance(list(item.values())[0], str) for item in value):
            return False
    # Si todos los valores son listas de diccionarios con un solo elemento, retorna True
    return True

def extract_osb_services_with_given_path(jdeveloper_projects_dir, services_for_operations):
    osb_services = []
    for operacion, path2 in services_for_operations.items():
        print_with_line_number("")
        print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_WITH_GIVEN_PATH*********************************************")
        print_with_line_number("")
        print_with_line_number(f"path2: {path2}")
        print_with_line_number(f"Operacion: {operacion}")
        print_with_line_number("")
        if 'Proxies' in path2:    
            osb_file_path = os.path.join(jdeveloper_projects_dir, path2 + ".ProxyService")
            proxy_abc = os.path.join(jdeveloper_projects_dir, path2)
            print_with_line_number(f"osb_file_path: {osb_file_path}")
            print_with_line_number("")
            project_name = extract_project_name_from_proxy(osb_file_path)
            print_with_line_number(f"project_name: {project_name}")
            print_with_line_number("")
            if project_name is None:
                continue  # Salta este registro y continúa con el siguiente
            pipeline_path = extract_pipeline_path_from_proxy(osb_file_path, jdeveloper_projects_dir)
            print_with_line_number(f"pipeline_path: {pipeline_path}")
            print_with_line_number("")
            with open(osb_file_path, 'r', encoding="utf-8") as f:
                content = f.read()
                service_name = os.path.splitext(os.path.basename(osb_file_path))[0]
                wsdl_relative_path = extract_wsdl_relative_path(content)
                print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_WITH_GIVEN_PATH*********************************************")
                print_with_line_number("")
                print_with_line_number(f"service_name: {service_name}")
                print_with_line_number(f"wsdl_relative_path: {wsdl_relative_path}")
                print_with_line_number("")
                if wsdl_relative_path:
                    wsdl_path = os.path.join(jdeveloper_projects_dir, wsdl_relative_path + ".WSDL")
                    print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_WITH_GIVEN_PATH*********************************************")
                    print_with_line_number("")
                    print_with_line_number(f"wsdl_path: {wsdl_path}")
                    print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_WITH_GIVEN_PATH*********************************************")
                    print_with_line_number("")
                    operations = extract_wsdl_operations(wsdl_path)
                    print_with_line_number(f"operations: {operations}")
                    print_with_line_number("")
                    print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_WITH_GIVEN_PATH*********************************************")
                    print_with_line_number("")
                    service_for_operations = definir_operaciones_internas_pipeline(pipeline_path)
                    print_with_line_number(f"service_for_operations: {service_for_operations}")
                    print_with_line_number("")
                    if not service_for_operations:
                        service_refs = extract_service_refs_from_pipeline(pipeline_path)
                        print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_WITH_GIVEN_PATH*********************************************")
                        print_with_line_number("")
                        print_with_line_number(f"service_refs: {service_refs}")
                        print_with_line_number("")
                        print_with_line_number("")
                        #for service_ref in service_refs:
                            #osb_services.append((operacion, service_ref)) 
                        osb_services.append((operacion, proxy_abc))
                        print_with_line_number(f"osb_services: {osb_services}")
                        print_with_line_number("")
                    else:
                        print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_WITH_GIVEN_PATH*********************************************")
                        print_with_line_number("")
                        rutas_de_servicio = []
                        for ruta in service_for_operations.values():
                            rutas_de_servicio.append(ruta)
                        osb_services.append((operacion, rutas_de_servicio))
                        print_with_line_number(f"osb_services: {osb_services}")
                        print_with_line_number("")
        
        if 'Pipeline' in path2:    
            osb_file_path = os.path.join(jdeveloper_projects_dir, path2 + ".Pipeline")
            proxy_abc = os.path.join(jdeveloper_projects_dir, path2)
            print_with_line_number(f"osb_file_path: {osb_file_path}")
            print_with_line_number("")
            project_name = extract_project_name_from_proxy(osb_file_path)
            print_with_line_number(f"project_name: {project_name}")
            print_with_line_number("")
            if project_name is None:
                continue  # Salta este registro y continúa con el siguiente
            pipeline_path = osb_file_path
            print_with_line_number(f"pipeline_path: {pipeline_path}")
            print_with_line_number("")
            with open(osb_file_path, 'r', encoding="utf-8") as f:
                content = f.read()
                service_name = os.path.splitext(os.path.basename(osb_file_path))[0]
                wsdl_relative_path = extract_wsdl_relative_path(content)
                print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_WITH_GIVEN_PATH*********************************************")
                print_with_line_number("")
                print_with_line_number(f"service_name: {service_name}")
                print_with_line_number(f"wsdl_relative_path: {wsdl_relative_path}")
                print_with_line_number("")
                if wsdl_relative_path:
                    wsdl_path = os.path.join(jdeveloper_projects_dir, wsdl_relative_path + ".WSDL")
                    print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_WITH_GIVEN_PATH*********************************************")
                    print_with_line_number("")
                    print_with_line_number(f"wsdl_path: {wsdl_path}")
                    print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_WITH_GIVEN_PATH*********************************************")
                    print_with_line_number("")
                    operations = extract_wsdl_operations(wsdl_path)
                    print_with_line_number(f"operations: {operations}")
                    print_with_line_number("")
                    print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_WITH_GIVEN_PATH*********************************************")
                    print_with_line_number("")
                    service_for_operations = definir_operaciones_internas_pipeline(pipeline_path)
                    print_with_line_number(f"service_for_operations: {service_for_operations}")
                    print_with_line_number("")
                    if not service_for_operations:
                        service_refs = extract_service_refs_from_pipeline(pipeline_path)
                        print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_WITH_GIVEN_PATH*********************************************")
                        print_with_line_number("")
                        print_with_line_number(f"service_refs: {service_refs}")
                        print_with_line_number("")
                        print_with_line_number("")
                        #for service_ref in service_refs:
                            #osb_services.append((operacion, service_ref)) 
                        osb_services.append((operacion, proxy_abc))
                        print_with_line_number(f"osb_services: {osb_services}")
                        print_with_line_number("")
                    else:
                        print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_WITH_GIVEN_PATH*********************************************")
                        print_with_line_number("")
                        rutas_de_servicio = []
                        for ruta in service_for_operations.values():
                            rutas_de_servicio.append(ruta)
                        osb_services.append((operacion, rutas_de_servicio))
                        print_with_line_number(f"osb_services: {osb_services}")
                        print_with_line_number("")
    
        
    print_with_line_number("*****************************FIN EXTRACT_OSB_SERVICES_WITH_GIVEN_PATH*********************************************")
    print_with_line_number("")
    return osb_services

def extract_osb_services_with_given_path_dict(jdeveloper_projects_dir, services_for_operations):
    osb_services = []
    for service_dict in services_for_operations:
        for service_path, path2 in service_dict.items():
            #print_with_line_number("")
            #print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_WITH_GIVEN_PATH DICT*********************************************")
            #print_with_line_number("")
            #print_with_line_number(f"path2: {path2}")
            proxy_name = path2.split('/')[-1]
            if 'Proxies' in path2:    
                osb_file_path = os.path.join(jdeveloper_projects_dir, path2 + ".ProxyService")
                #print_with_line_number(f"osb_file_path: {osb_file_path}")
                #print_with_line_number("")
                project_name = extract_project_name_from_proxy(osb_file_path)
                #print_with_line_number(f"project_name: {project_name}")
                #print_with_line_number("")
                if project_name is None:
                    osb_services.append((service_path, proxy_name, 'N/A'))
                    continue  # Salta este registro y continúa con el siguiente
                pipeline_path = extract_pipeline_path_from_proxy(osb_file_path, jdeveloper_projects_dir)
                #print_with_line_number(f"pipeline_path: {pipeline_path}")
                #print_with_line_number("")
                with open(osb_file_path, 'r', encoding="utf-8") as f:
                    content = f.read()
                    service_name = os.path.splitext(os.path.basename(osb_file_path))[0]
                    wsdl_relative_path = extract_wsdl_relative_path(content)
                    #print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_WITH_GIVEN_PATH DICT*********************************************")
                    #print_with_line_number("")
                    #print_with_line_number(f"service_name: {service_name}")
                    #print_with_line_number(f"wsdl_relative_path: {wsdl_relative_path}")
                    #print_with_line_number("")
                    if wsdl_relative_path:
                        wsdl_path = os.path.join(jdeveloper_projects_dir, wsdl_relative_path + ".WSDL")
                        #print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_WITH_GIVEN_PATH DICT*********************************************")
                        #print_with_line_number("")
                        #print_with_line_number(f"wsdl_path: {wsdl_path}")
                        #print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_WITH_GIVEN_PATH DICT*********************************************")
                        #print_with_line_number("")
                        operations = extract_wsdl_operations(wsdl_path)
                        #print_with_line_number(f"operations: {operations}")
                        #print_with_line_number("")
                        #print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_WITH_GIVEN_PATH DICT*********************************************")
                        #print_with_line_number("")
                        #Se comenta linea para revisar como se hace:
                        #service_for_operations = extract_service_for_operations(pipeline_path, operations)
                        
                        service_for_operations = ""
                        #print_with_line_number(f"service_for_operations: {service_for_operations}")
                        #print_with_line_number("")
                        if not service_for_operations:
                            service_refs = extract_service_refs_from_pipeline(pipeline_path)
                            #print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_WITH_GIVEN_PATH DICT*********************************************")
                            #print_with_line_number("")
                            #print_with_line_number(f"service_refs: {service_refs}")
                            #print_with_line_number("")
                            for service_ref in service_refs:
                                osb_services.append((service_path, proxy_name, service_ref))
                            if not service_refs:
                                osb_services.append((service_path, proxy_name, 'N/A'))
                        else:
                            #print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_WITH_GIVEN_PATH DICT*********************************************")
                            #print_with_line_number("")
                            business_service = list(service_for_operations.values())[0]
                            osb_services.append((service_path, proxy_name, business_service))
                            #print_with_line_number(f"osb_services: {osb_services}")
                            #print_with_line_number("")
            
            #elif 'BusinessServices' in path2:
                            
            
            else:
                osb_services.append((service_path, proxy_name, 'N/A'))
                continue
    #print_with_line_number("*****************************FIN EXTRACT_OSB_SERVICES_WITH_GIVEN_PATH DICT*********************************************")
    #print_with_line_number("")
    return osb_services

def extract_osb_services_references_abc(jdeveloper_projects_dir, services_for_operations):
    osb_services = []
    
    #print_with_line_number("")
    #print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_REFERENCES_ABC*********************************************")
    #print_with_line_number("")
    
    #print_with_line_number("Revisa aqui", services_for_operations)
    
    if services_for_operations is not None:  # Verifica que services_for_operations no sea None
        for sublistas in services_for_operations:
            if sublistas is not None:  # Verifica que la sublista no sea None
                for operacion, proxy, referencia in sublistas:
                    palabras_invalidas = ['ComponentesComunes/Proxies/PS_ManejadorGenericoErroresV1.0', 'UtilitariosEBS/Proxies/AuditoriaSOA/RegistrarAuditoriaSOADATV1.0', 'N/A', 'Resources/Jars']
                    if referencia not in palabras_invalidas:
                        #print_with_line_number("")
                        #print_with_line_number(f"Operación: {operacion}")
                        #print_with_line_number(f"Proxy: {proxy}")
                        #print_with_line_number(f"Referencia asociada: {referencia}")
                        #print_with_line_number("")
                        
                        if 'Proxies' in referencia:
                            osb_file_path = os.path.join(jdeveloper_projects_dir, referencia + ".ProxyService")
                            #print_with_line_number("")
                            #print_with_line_number(f"Referencia Proxy : {referencia}")
                            #print_with_line_number("")
                            project_name = extract_project_name_from_proxy(osb_file_path)
                            #print_with_line_number(f"project_name : {project_name}")
                            #print_with_line_number("")
                            if project_name is None:
                                osb_services.append((operacion , proxy, referencia,'N/A',  'N/A', 'N/A','N/A'))
                                #print_with_line_number(f"REVISA [-6]!!!: {osb_services}")
                                continue
            
                            pipeline_path = extract_pipeline_path_from_proxy(osb_file_path, jdeveloper_projects_dir)
                            #print_with_line_number(f"PIPELINE: {pipeline_path}")
                            
                            with open(osb_file_path, 'r', encoding="utf-8") as f:
                                content = f.read()
                                service_name = os.path.splitext(os.path.basename(osb_file_path))[0]
                                wsdl_relative_path = extract_wsdl_relative_path(content)
                                
                                if wsdl_relative_path:
                                    wsdl_path = os.path.join(jdeveloper_projects_dir, wsdl_relative_path + ".WSDL")
                                    #print_with_line_number("")
                                    #print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_FINALS*********************************************")
                                    #print_with_line_number(f"WSDL: {wsdl_path}")
                                    #print_with_line_number("")
                                    operations = extract_wsdl_operations(wsdl_path)
                                    #print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_FINALS*********************************************")
                                    #print_with_line_number("")
                                    #print_with_line_number(f"OPERACION DEL PIPELINE: {operations}")
                                    service_for_operations = extract_service_for_operations(pipeline_path, operations)
                                    
                                    
                                    if not service_for_operations:
                                        #print_with_line_number("")
                                        #print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_FINALS*********************************************")
                                        #print_with_line_number(f"OPERACIONES INTERNAS: {service_for_operations}")
                                        service_refs = extract_service_refs_from_pipeline(pipeline_path)
                                        #print_with_line_number("")
                                        #print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_FINALS*********************************************")
                                        #print_with_line_number("")
                                        #print_with_line_number("Service for operations no devolvió datos. Obteniendo referencias de servicio desde el archivo .pipeline...")
                                        #print_with_line_number(f" ")
                                        
                                        #print_with_line_number("__________________________________________________________________________")
                                        #print_with_line_number(f"PROXY ABC: {proxy}")
                                        #print_with_line_number("__________________________________________________________________________")
                                        #print_with_line_number("")
                                        #print_with_line_number("")
                                        
                                        for service_ref in service_refs:
                                            #print_with_line_number("___________________1________________________")
                                            #print_with_line_number(f"   OPERACION EBS: {service_name}")
                                            #print_with_line_number(f"   OPERACION ABC: {operations[0]} ")
                                            #print_with_line_number(f"   PROXY ABC: {proxy}")
                                            #print_with_line_number(f"   REFERENCIAS PL: {service_ref} ")
                                            #print_with_line_number("____________________________________________")
                                            
                                            osb_services.append((operacion , proxy, referencia, service_name, operations[0], service_ref,operations[0]))
                                            #print_with_line_number(f"REVISA [-5]!!!: {osb_services}")
                                            #extract_osb_businessService(jdeveloper_projects_dir, osb_services)
                                                
                                    else:
                                        for operation, proxy_interno in service_for_operations.items():
                                            #print_with_line_number("__________________2__________________________")
                                            #print_with_line_number(f"   OPERACION EBS: {service_name}")
                                            #print_with_line_number(f"   PROXY ABC: {proxy}")
                                            #print_with_line_number(f"   REFERENCIAS PL: {proxy_interno}")
                                            #print_with_line_number("____________________________________________")
                                            
                                            osb_services.append((operacion , proxy, referencia,service_name, operations[0], proxy_interno,operations[0]))
                                            #print_with_line_number(f"REVISA [-4]!!!: {osb_services}")
                                            #extract_osb_businessService(jdeveloper_projects_dir, osb_services)


                        elif 'BusinessServices' in referencia:
                            osb_file_path = os.path.join(jdeveloper_projects_dir, referencia + ".BusinessService")
                            #print_with_line_number("")
                            #print_with_line_number("/////////////")
                            #print_with_line_number(f"BUSINESS SERVICE : {referencia}")
                            project_name = extract_project_name_from_business(osb_file_path)
                            if project_name is None:
                                continue
            
                            with open(osb_file_path, 'r', encoding="utf-8") as f:
                                content = f.read()
                                service_name = os.path.splitext(os.path.basename(osb_file_path))[0]
                                wsdl_relative_path = extract_wsdl_relative_path(content)
                                
                                if wsdl_relative_path:
                                    wsdl_path = os.path.join(jdeveloper_projects_dir, wsdl_relative_path + ".WSDL")
                                    #print_with_line_number(f"WSDL: {wsdl_path}")
                                    operations = extract_wsdl_operations(wsdl_path)
                                    #print_with_line_number(f"OPERACIONES WSDL: {operations}")
                                    service_refs = extract_uri_and_provider_id_from_bix(osb_file_path)
                                    #print_with_line_number("Service for operations no devolvió datos. Obteniendo referencias de servicio desde el archivo .pipeline...")
                                    #print_with_line_number(f" ")
                                    #print_with_line_number(f"Referencias de servicio encontradas: {service_refs}")
                                    
                                    for uri_value, provider_id_value in service_refs:
                                        #print_with_line_number(f"SERVICE REFS BUSINESS: {uri_value}  {provider_id_value} ")
                                        osb_services.append((operacion , proxy, referencia,service_name, uri_value, provider_id_value,operations[0]))
                                        #print_with_line_number(f"REVISA [-3]!!!: {osb_services}")
                                else:
                                    service_refs = extract_uri_and_provider_id_from_bix(osb_file_path)
                                    #print_with_line_number("__________________________________________________________________________")
                                    #print_with_line_number(f"BUSINESS ABC: {referencia}")
                                    #print_with_line_number("__________________________________________________________________________")
                                    
                                    for uri_value, provider_id_value in service_refs:
                                        print_with_line_number("____________________________________________")
                                        #print_with_line_number(f"   OPERACION EBS: {service_name}")
                                        #print_with_line_number(f"   URI: {uri_value}")
                                        #print_with_line_number(f"   TIPO: {provider_id_value}")
                                        #print_with_line_number("____________________________________________")
                                        
                                    osb_services.append((operacion , proxy, referencia,service_name,  uri_value, provider_id_value,'N/A'))
                                    #print_with_line_number(f"REVISA [-2]!!!: {osb_services}")
                            #print_with_line_number("**************************FIN DEL BUSINESS SERVICE*********************************")  
                        else:
                            osb_services.append((operacion , proxy, referencia,'N/A',  'N/A', 'N/A','N/A'))
                            #print_with_line_number(f"REVISA [-1]!!!: {osb_services}")
                    else:
                        osb_services.append((operacion , proxy, referencia,'N/A',  'N/A', 'N/A','N/A'))
                        #print_with_line_number("")
                        #print_with_line_number(f" PALABRA INVALIDA REVISA [0]!!!: {osb_services}")
                        #print_with_line_number("")
        
        #print_with_line_number("")
        #print_with_line_number(f"REVISA [1]!!!: {osb_services}")
        #print_with_line_number("")
        #print_with_line_number("")
    #print_with_line_number("")
    #print_with_line_number("*****************************FIN EXTRACT_OSB_SERVICES_REFERENCES_ABC*********************************************")
    #print_with_line_number("")
    #print_with_line_number(f"REVISA1: {osb_services}")    
    return osb_services

def extract_osb_services_references_abc2(jdeveloper_projects_dir, services_for_operations):
    osb_services = []
    es_ebs = False
    service_ref = ""
    
    print_with_line_number("Entro a extract_osb_services_references_abc2")
    print_with_line_number("")
    print_with_line_number(f"jdeveloper_projects_dir : {jdeveloper_projects_dir}")
    print_with_line_number("")
    
    if services_for_operations is not None:
        for operacion, proxy_ebs1, referencia, operacion_legado in services_for_operations:
            print_with_line_number(f"operacion: {operacion}")
            print_with_line_number(f"proxy_ebs1: {proxy_ebs1}")
            proxy_ebs2 = proxy_ebs1
            proxy_ebs3 = proxy_ebs1
            print_with_line_number(f"referencia: {referencia}")
            print_with_line_number(f"operacion_legado: {operacion_legado}")
            print_with_line_number("")
            palabras_invalidas = ['ComponentesComunes/Proxies/PS_ManejadorGenericoErroresV1.0', 'N/A', 'Resources/Jars']
            if referencia not in palabras_invalidas:
                if 'EBS' in referencia: #Saber si es un EBS
                    es_ebs = True
                    print_with_line_number("Es EBS")
                    
                    if 'Proxies' in referencia:
                        print_with_line_number(f"Proxies esta en referencia : {referencia}")
                        print_with_line_number("")
                        osb_file_path = os.path.join(jdeveloper_projects_dir, referencia + ".ProxyService")
                        print_with_line_number(f"osb_file_path : {osb_file_path}")
                        print_with_line_number("")
                        project_name = extract_project_name_from_proxy(osb_file_path)
                        if project_name is None:
                            osb_services.append((operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, referencia, operacion_legado, 'N/A', 'N/A'))
                            print_with_line_number(f"project_name es 'None' : {project_name}")
                            print_with_line_number("")
                            print_with_line_number("")
                            print_with_line_number(f"osb_services: {osb_services}")
                            print_with_line_number("")
                            continue

                        pipeline_path = extract_pipeline_path_from_proxy(osb_file_path, jdeveloper_projects_dir)
                        print_with_line_number(f"pipeline_path: {pipeline_path}")
                        print_with_line_number("")
                        with open(osb_file_path, 'r', encoding="utf-8") as f:
                            content = f.read()
                            service_name = os.path.splitext(os.path.basename(osb_file_path))[0]
                            wsdl_relative_path = extract_wsdl_relative_path(content)

                            if wsdl_relative_path:
                                wsdl_path = os.path.join(jdeveloper_projects_dir, wsdl_relative_path + ".WSDL")
                                print_with_line_number(f"wsdl_path: {wsdl_path}")
                                print_with_line_number("")
                                operations = extract_wsdl_operations(wsdl_path)
                                print_with_line_number(f"operations: {operations}")
                                print_with_line_number("")
                                service_for_operations = extract_service_for_operations(pipeline_path, operacion_legado)
                                print_with_line_number(f"service_for_operations: {service_for_operations}")
                                print_with_line_number("")

                                if not service_for_operations:
                                    service_refs = extract_service_refs_from_pipeline(pipeline_path)
                                    print_with_line_number(f"service_for_operations 2: {service_for_operations}")
                                    print_with_line_number("")

                                    for service_ref in service_refs:
                                        osb_services.append((operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, referencia, operacion_legado, service_ref, operacion_legado))
                                        print_with_line_number(f"operacion {operacion}")
                                        print_with_line_number(f"proxy_ebs1 {proxy_ebs1}")
                                        print_with_line_number(f"referencia {referencia}")
                                        print_with_line_number(f"operacion_legado {operacion_legado}")
                                        print_with_line_number(f"service_ref {service_ref}")
                                        print_with_line_number(f"operacion_legado {operacion_legado}")
                                        print_with_line_number("")
                                        print_with_line_number("")
                                        print_with_line_number(f"osb_services: {osb_services}")
                                        print_with_line_number("")

                                else:
                                    for operation, proxy_interno in service_for_operations.items():
                                        print_with_line_number(f"operacion {operacion}")
                                        print_with_line_number(f"proxy_ebs1 {proxy_ebs1}")
                                        print_with_line_number(f"referencia {referencia}")
                                        print_with_line_number(f"operacion_legado {operacion_legado}")
                                        print_with_line_number(f"proxy_interno {proxy_interno}")
                                        print_with_line_number("")
                                        if 'EBS' in referencia and 'PS' in proxy_interno:
                                            proxy_ebs2 = referencia.split("/")[-1]
                                            proxy_ebs3 = proxy_interno.split("/")[-1]
                                        elif 'EBS' in proxy_interno:
                                            proxy_ebs3 = proxy_interno.split("/")[-1]
                                        else:
                                            proxy_ebs3 = proxy_interno
                                        
                                        es_business_service = '/BusinessServices'
                                        if es_business_service not in proxy_interno:
                                            osb_file_path = os.path.join(jdeveloper_projects_dir, proxy_interno + ".ProxyService")
                                            print_with_line_number("")
                                            print_with_line_number(f"osb_file_path {osb_file_path}")
                                            print_with_line_number("")
                                            ruta_pipeline = extract_pipeline_path_from_proxy(osb_file_path, jdeveloper_projects_dir)
                                            print_with_line_number(f"ruta_pipeline: {ruta_pipeline}")
                                            if ruta_pipeline is None:
                                                osb_services.append((operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, referencia, operacion_legado, 'N/A', 'N/A'))
                                                print_with_line_number(f"ruta_pipeline es 'None' : {project_name}")
                                                print_with_line_number(f"operacion {operacion}")
                                                print_with_line_number(f"proxy_ebs1 {proxy_ebs1}")
                                                print_with_line_number(f"referencia {referencia}")
                                                print_with_line_number(f"operacion_legado {operacion_legado}")
                                                print_with_line_number(f"service_ref {service_ref}")
                                                print_with_line_number(f"operacion_legado {operacion_legado}")
                                                print_with_line_number("")
                                                print_with_line_number("")
                                                print_with_line_number(f"osb_services: {osb_services}")
                                                print_with_line_number("")
                                                continue
                                            operaciones_internas = definir_operaciones_internas_pipeline(ruta_pipeline)
                                            print_with_line_number("")
                                            print_with_line_number(f"operaciones_internas {operaciones_internas}")
                                            proxy_ebs3_momento = proxy_ebs3
                                            print_with_line_number(f"proxy_ebs3_momento {proxy_ebs3_momento}")
                                            
                                            for clave, valor in operaciones_internas.items():
                                                operacion_legado = clave
                                                proxy_interno = valor.split("/")[-1]
                                                print_with_line_number(f"clave {clave}")
                                                print_with_line_number("")
                                                print_with_line_number(f"valor {valor}")
                                                proxy_ebs3 = proxy_ebs3_momento
                                                print_with_line_number(f"proxy_ebs3 {proxy_ebs3}")
                                                
                                                if es_business_service in valor:
                                                    
                                                    proxy_abc_ebs = proxy_ebs2+"/"+proxy_ebs3
                                                    osb_file_path = os.path.join(jdeveloper_projects_dir, valor + ".BusinessService")
                                                    project_name = extract_project_name_from_business(osb_file_path)
                                                    print_with_line_number(f"project_name es : {project_name}")
                                                    if project_name is None:
                                                        print_with_line_number(f"project_name es 'None' : {project_name}")
                                                        print_with_line_number("")
                                                        continue

                                                    with open(osb_file_path, 'r', encoding="utf-8") as f:
                                                        content = f.read()
                                                        service_name = os.path.splitext(os.path.basename(osb_file_path))[0]
                                                        print_with_line_number(f"service_name: {service_name}")
                                                        wsdl_relative_path = extract_wsdl_relative_path(content)

                                                        wsdl_path = os.path.join(jdeveloper_projects_dir, wsdl_relative_path + ".WSDL")
                                                        operations = extract_wsdl_operations(wsdl_path)
                                                        service_refs = extract_uri_and_provider_id_from_bix(osb_file_path)
                                                        print_with_line_number(f"service_refs: {service_refs}")
                                                        print_with_line_number("")

                                                        for uri_value, provider_id_value in service_refs:
                                                            
                                                            print_with_line_number(f"DATOS {operacion , proxy_ebs1, proxy_ebs2, proxy_abc_ebs, valor, operacion_legado, uri_value, provider_id_value}")
                                                            osb_services.append((operacion , proxy_ebs1, proxy_ebs2, proxy_abc_ebs, valor, operacion_legado, uri_value, provider_id_value))
                                                
                                                else:
                                                
                                                    if 'EBS' in valor:
                                                        valor_limpio = valor.split("/")[-1]
                                                        print_with_line_number(f"valor_limpio: {valor_limpio}")
                                                        proxy_ebs3 = proxy_ebs3_momento+"/"+valor_limpio
                                                        print_with_line_number(f"proxy_ebs2: {proxy_ebs2}")
                                                        print_with_line_number(f"proxy_ebs3: {proxy_ebs3}")
                                                        proxy_anterior = proxy_ebs3
                                                        
                                                        if 'Proxies' in valor:
                                                            print_with_line_number(f"Proxies esta en valor : {valor}")
                                                            print_with_line_number("")
                                                            osb_file_path = os.path.join(jdeveloper_projects_dir, valor + ".ProxyService")
                                                            print_with_line_number(f"osb_file_path : {osb_file_path}")
                                                            print_with_line_number("")
                                                            project_name = extract_project_name_from_proxy(osb_file_path)
                                                            if project_name is None:
                                                                osb_services.append((operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, valor, operacion_legado, 'N/A', 'N/A'))
                                                                print_with_line_number(f"project_name es 'None' : {project_name}")
                                                                print_with_line_number("")
                                                                print_with_line_number("")
                                                                print_with_line_number(f"osb_services: {osb_services}")
                                                                print_with_line_number("")
                                                                continue

                                                            pipeline_path = extract_pipeline_path_from_proxy(osb_file_path, jdeveloper_projects_dir)
                                                            print_with_line_number(f"pipeline_path: {pipeline_path}")
                                                            print_with_line_number("")
                                                            with open(osb_file_path, 'r', encoding="utf-8") as f:
                                                                content = f.read()
                                                                service_name = os.path.splitext(os.path.basename(osb_file_path))[0]
                                                                wsdl_relative_path = extract_wsdl_relative_path(content)

                                                                if wsdl_relative_path:
                                                                    wsdl_path = os.path.join(jdeveloper_projects_dir, wsdl_relative_path + ".WSDL")
                                                                    print_with_line_number(f"wsdl_path: {wsdl_path}")
                                                                    print_with_line_number("")
                                                                    operations = extract_wsdl_operations(wsdl_path)
                                                                    print_with_line_number(f"operations: {operations}")
                                                                    print_with_line_number("")
                                                                    service_for_operations = extract_service_for_operations(pipeline_path, operacion_legado)
                                                                    print_with_line_number(f"service_for_operations: {service_for_operations}")
                                                                    print_with_line_number("")
                                                                    proxy_ebs3_momento = proxy_ebs3

                                                                    if not service_for_operations:
                                                                        service_refs = extract_service_refs_from_pipeline(pipeline_path)
                                                                        print_with_line_number(f"service_for_operations 2: {service_for_operations}")
                                                                        print_with_line_number("")

                                                                        for service_ref in service_refs:
                                                                            osb_services.append((operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, referencia, operacion_legado, service_ref, operacion_legado))
                                                                            print_with_line_number(f"operacion {operacion}")
                                                                            print_with_line_number(f"proxy_ebs1 {proxy_ebs1}")
                                                                            print_with_line_number(f"referencia {referencia}")
                                                                            print_with_line_number(f"operacion_legado {operacion_legado}")
                                                                            print_with_line_number(f"service_ref {service_ref}")
                                                                            print_with_line_number(f"operacion_legado {operacion_legado}")
                                                                            print_with_line_number("")
                                                                            print_with_line_number("")
                                                                            print_with_line_number(f"osb_services: {osb_services}")
                                                                            print_with_line_number("")

                                                                    else:
                                                                        for operation, proxy_interno in service_for_operations.items():
                                                                            print_with_line_number(f"operacion {operacion}")
                                                                            print_with_line_number(f"proxy_ebs1 {proxy_ebs1}")
                                                                            print_with_line_number(f"referencia {referencia}")
                                                                            print_with_line_number(f"proxy_ebs3_momento {proxy_ebs3_momento}")
                                                                            print_with_line_number(f"operacion_legado {operacion_legado}")
                                                                            print_with_line_number(f"proxy_interno {proxy_interno}")
                                                                            print_with_line_number("")
                                                                            if 'EBS' in referencia and 'PS' in proxy_ebs3_momento:
                                                                                proxy_ebs2 = referencia.split("/")[-1]
                                                                                proxy_ebs3 = proxy_interno.split("/")[-1]
                                                                                print_with_line_number(f"proxy_ebs2: {proxy_ebs2}")
                                                                                print_with_line_number(f"proxy_ebs3: {proxy_ebs3}")
                                                                            
                                                                            es_business_service = '/BusinessServices'
                                                                            proxy_concatenado = proxy_interno.split("/")[-1]
                                                                            print_with_line_number(f"proxy_concatenado {proxy_concatenado}")
                                                                            proxy_ebs3 = proxy_ebs3_momento+"/"+proxy_concatenado
                                                                            print_with_line_number(f"proxy_ebs3 {proxy_ebs3}")
                                                                            if es_business_service not in proxy_interno:
                                                                                osb_file_path = os.path.join(jdeveloper_projects_dir, proxy_interno + ".ProxyService")
                                                                                print_with_line_number("")
                                                                                print_with_line_number(f"osb_file_path {osb_file_path}")
                                                                                print_with_line_number("")
                                                                                ruta_pipeline = extract_pipeline_path_from_proxy(osb_file_path, jdeveloper_projects_dir)
                                                                                print_with_line_number(f"ruta_pipeline: {ruta_pipeline}")
                                                                                if ruta_pipeline is None:
                                                                                    osb_services.append((operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, referencia, operacion_legado, 'N/A', 'N/A'))
                                                                                    print_with_line_number(f"ruta_pipeline es 'None' : {project_name}")
                                                                                    print_with_line_number(f"operacion {operacion}")
                                                                                    print_with_line_number(f"proxy_ebs1 {proxy_ebs1}")
                                                                                    print_with_line_number(f"referencia {referencia}")
                                                                                    print_with_line_number(f"operacion_legado {operacion_legado}")
                                                                                    print_with_line_number(f"service_ref {service_ref}")
                                                                                    print_with_line_number(f"operacion_legado {operacion_legado}")
                                                                                    print_with_line_number("")
                                                                                    print_with_line_number("")
                                                                                    print_with_line_number(f"osb_services: {osb_services}")
                                                                                    print_with_line_number("")
                                                                                    continue
                                                                                operaciones_internas = definir_operaciones_internas_pipeline(ruta_pipeline)
                                                                                print_with_line_number("")
                                                                                print_with_line_number(f"operaciones_internas {operaciones_internas}")
                                                                                
                                                                                for clave, valor in operaciones_internas.items():
                                                                                    operacion_legado = clave
                                                                                    proxy_externo = valor.split("/")[-1]
                                                                                    print_with_line_number(f"clave {clave}")
                                                                                    print_with_line_number("")
                                                                                    print_with_line_number(f"valor {valor}")
                                                                                    
                                                                                    if es_business_service in valor:
                                                                                        
                                                                                        osb_file_path = os.path.join(jdeveloper_projects_dir, valor + ".BusinessService")
                                                                                        project_name = extract_project_name_from_business(osb_file_path)
                                                                                        print_with_line_number(f"project_name es : {project_name}")
                                                                                        if project_name is None:
                                                                                            print_with_line_number(f"project_name es 'None' : {project_name}")
                                                                                            print_with_line_number("")
                                                                                            continue

                                                                                        with open(osb_file_path, 'r', encoding="utf-8") as f:
                                                                                            content = f.read()
                                                                                            service_name = os.path.splitext(os.path.basename(osb_file_path))[0]
                                                                                            print_with_line_number(f"service_name: {service_name}")
                                                                                            wsdl_relative_path = extract_wsdl_relative_path(content)

                                                                                            wsdl_path = os.path.join(jdeveloper_projects_dir, wsdl_relative_path + ".WSDL")
                                                                                            operations = extract_wsdl_operations(wsdl_path)
                                                                                            service_refs = extract_uri_and_provider_id_from_bix(osb_file_path)
                                                                                            print_with_line_number(f"service_refs: {service_refs}")
                                                                                            print_with_line_number("")

                                                                                            for uri_value, provider_id_value in service_refs:
                                                                                                print_with_line_number(f"DATOS {operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, valor, operacion_legado, uri_value, provider_id_value}")
                                                                                                osb_services.append((operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, valor, operacion_legado, uri_value, provider_id_value))
                                                                                    
                                                                                    else:
                                                                                    
                                                                                        if 'EBS' in valor:
                                                                                            valor_limpio = valor.split("/")[-1]
                                                                                            proxy_ebs3 = proxy_ebs3+"/"+valor_limpio
                                                                                            
                                                                                            
                                                                                    
                                                                                        
                                                                                        
                                                                                        
                                                                                        else:
                                                                                            print_with_line_number(f"proxy_ebs2: {proxy_ebs2}")
                                                                                            print_with_line_number(f"proxy_ebs3: {proxy_ebs3}")
                                                                                            print_with_line_number(f"DATOS {operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, valor, operacion_legado, proxy_externo, clave}")
                                                                                            osb_services.append((operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, valor, operacion_legado, proxy_externo, clave))
                                                                                            print_with_line_number(f"operacion {operacion}")
                                                                                            print_with_line_number(f"proxy_ebs1 {proxy_ebs1}")
                                                                                            print_with_line_number(f"referencia {referencia}")
                                                                                            print_with_line_number(f"operacion_legado {operacion_legado}")
                                                                                            print_with_line_number(f"operacion_legado {operacion_legado}")
                                                                                            print_with_line_number("")
                                                                                            print_with_line_number("")
                                                                                            print_with_line_number(f"osb_services: {osb_services}")
                                                                                            print_with_line_number("")
                                                                            
                                                                            else:
                                                                                osb_file_path = os.path.join(jdeveloper_projects_dir, proxy_interno + ".BusinessService")
                                                                                project_name = extract_project_name_from_business(osb_file_path)
                                                                                print_with_line_number(f"project_name es : {project_name}")
                                                                                if project_name is None:
                                                                                    print_with_line_number(f"project_name es 'None' : {project_name}")
                                                                                    print_with_line_number("")
                                                                                    continue

                                                                                with open(osb_file_path, 'r', encoding="utf-8") as f:
                                                                                    content = f.read()
                                                                                    service_name = os.path.splitext(os.path.basename(osb_file_path))[0]
                                                                                    print_with_line_number(f"service_name: {service_name}")
                                                                                    wsdl_relative_path = extract_wsdl_relative_path(content)

                                                                                    wsdl_path = os.path.join(jdeveloper_projects_dir, wsdl_relative_path + ".WSDL")
                                                                                    operations = extract_wsdl_operations(wsdl_path)
                                                                                    service_refs = extract_uri_and_provider_id_from_bix(osb_file_path)
                                                                                    print_with_line_number(f"service_refs: {service_refs}")
                                                                                    print_with_line_number("")

                                                                                    for uri_value, provider_id_value in service_refs:
                                                                                        osb_services.append((operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, referencia, operacion_legado, uri_value, provider_id_value))
                                                                                        print_with_line_number(f"operacion {operacion}")
                                                                                        print_with_line_number(f"proxy_ebs1 {proxy_ebs1}")
                                                                                        print_with_line_number(f"referencia {referencia}")
                                                                                        print_with_line_number(f"operacion_legado {operacion_legado}")
                                                                                        print_with_line_number(f"uri_value {uri_value}")
                                                                                        print_with_line_number(f"provider_id_value {provider_id_value}")
                                                                                        print_with_line_number("")
                                                                                        print_with_line_number(f"osb_services: {osb_services}")
                                                                                        print_with_line_number("")
                                                                                
                                                                            print_with_line_number("")
                                                                            print_with_line_number(f"osb_services: {osb_services}")
                                                                            print_with_line_number("")
                                                                            proxy_ebs3 = ""
                                                                            

                                                    else:
                                                        
                                                        if 'Proxies' in valor:
                                                            valor_limpio = valor.split("/")[-1]
                                                            print_with_line_number(f"valor_limpio: {valor_limpio}")
                                                            proxy_ebs3 = proxy_ebs3_momento+"/"+valor_limpio
                                                            print_with_line_number(f"proxy_ebs3: {proxy_ebs3}")
                                                            print_with_line_number(f"Proxies esta en valor : {valor}")
                                                            print_with_line_number("")
                                                            osb_file_path = os.path.join(jdeveloper_projects_dir, valor + ".ProxyService")
                                                            print_with_line_number(f"osb_file_path : {osb_file_path}")
                                                            print_with_line_number("")
                                                            project_name = extract_project_name_from_proxy(osb_file_path)
                                                            if project_name is None:
                                                                osb_services.append((operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, valor, operacion_legado, 'N/A', 'N/A'))
                                                                print_with_line_number(f"project_name es 'None' : {project_name}")
                                                                print_with_line_number("")
                                                                print_with_line_number("")
                                                                print_with_line_number(f"osb_services: {osb_services}")
                                                                print_with_line_number("")
                                                                continue

                                                            pipeline_path = extract_pipeline_path_from_proxy(osb_file_path, jdeveloper_projects_dir)
                                                            print_with_line_number(f"pipeline_path: {pipeline_path}")
                                                            print_with_line_number("")
                                                            with open(osb_file_path, 'r', encoding="utf-8") as f:
                                                                content = f.read()
                                                                service_name = os.path.splitext(os.path.basename(osb_file_path))[0]
                                                                wsdl_relative_path = extract_wsdl_relative_path(content)

                                                                if wsdl_relative_path:
                                                                    wsdl_path = os.path.join(jdeveloper_projects_dir, wsdl_relative_path + ".WSDL")
                                                                    print_with_line_number(f"wsdl_path: {wsdl_path}")
                                                                    print_with_line_number("")
                                                                    operations = extract_wsdl_operations(wsdl_path)
                                                                    print_with_line_number(f"operations: {operations}")
                                                                    print_with_line_number("")
                                                                    service_for_operations = extract_service_for_operations(pipeline_path, operacion_legado)
                                                                    print_with_line_number(f"service_for_operations: {service_for_operations}")
                                                                    print_with_line_number("")

                                                                    if not service_for_operations:
                                                                        service_refs = extract_service_refs_from_pipeline(pipeline_path)
                                                                        print_with_line_number(f"service_for_operations 2: {service_for_operations}")
                                                                        print_with_line_number("")

                                                                        for service_ref in service_refs:
                                                                            osb_services.append((operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, valor, operacion_legado, service_ref, operacion_legado))
                                                                            print_with_line_number(f"operacion {operacion}")
                                                                            print_with_line_number(f"proxy_ebs1 {proxy_ebs1}")
                                                                            print_with_line_number(f"valor {valor}")
                                                                            print_with_line_number(f"operacion_legado {operacion_legado}")
                                                                            print_with_line_number(f"service_ref {service_ref}")
                                                                            print_with_line_number(f"operacion_legado {operacion_legado}")
                                                                            print_with_line_number("")
                                                                            print_with_line_number("")
                                                                            print_with_line_number(f"osb_services: {osb_services}")
                                                                            print_with_line_number("")

                                                                    else:
                                                                        for operation, proxy_interno in service_for_operations.items():
                                                                            print_with_line_number(f"operacion {operacion}")
                                                                            print_with_line_number(f"proxy_ebs1 {proxy_ebs1}")
                                                                            print_with_line_number(f"valor {valor}")
                                                                            print_with_line_number(f"operacion_legado {operacion_legado}")
                                                                            print_with_line_number(f"proxy_interno {proxy_interno}")
                                                                            print_with_line_number("")
                                                                            if 'EBS' in valor and 'PS' in proxy_interno:
                                                                                proxy_ebs2 = valor.split("/")[-1]
                                                                                proxy_ebs3 = proxy_interno.split("/")[-1]
                                                                            elif 'EBS' in proxy_interno:
                                                                                proxy_ebs3 = proxy_interno.split("/")[-1]
                                                                            else:
                                                                                proxy_ebs3 = proxy_interno
                                                                            
                                                                            es_business_service = '/BusinessServices'
                                                                            if es_business_service not in proxy_interno:
                                                                                osb_file_path = os.path.join(jdeveloper_projects_dir, proxy_interno + ".ProxyService")
                                                                                print_with_line_number("")
                                                                                print_with_line_number(f"osb_file_path {osb_file_path}")
                                                                                print_with_line_number("")
                                                                                ruta_pipeline = extract_pipeline_path_from_proxy(osb_file_path, jdeveloper_projects_dir)
                                                                                print_with_line_number(f"ruta_pipeline: {ruta_pipeline}")
                                                                                if ruta_pipeline is None:
                                                                                    osb_services.append((operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, valor, operacion_legado, 'N/A', 'N/A'))
                                                                                    print_with_line_number(f"ruta_pipeline es 'None' : {project_name}")
                                                                                    print_with_line_number(f"operacion {operacion}")
                                                                                    print_with_line_number(f"proxy_ebs1 {proxy_ebs1}")
                                                                                    print_with_line_number(f"valor {valor}")
                                                                                    print_with_line_number(f"operacion_legado {operacion_legado}")
                                                                                    print_with_line_number(f"service_ref {service_ref}")
                                                                                    print_with_line_number(f"operacion_legado {operacion_legado}")
                                                                                    print_with_line_number("")
                                                                                    print_with_line_number("")
                                                                                    print_with_line_number(f"osb_services: {osb_services}")
                                                                                    print_with_line_number("")
                                                                                    continue
                                                                                operaciones_internas = definir_operaciones_internas_pipeline(ruta_pipeline)
                                                                                print_with_line_number("")
                                                                                print_with_line_number(f"operaciones_internas {operaciones_internas}")
                                                                                proxy_ebs3_momento = proxy_ebs3
                                                                                print_with_line_number(f"proxy_ebs3_momento {proxy_ebs3_momento}")
                                                                                
                                                                                for clave, valor in operaciones_internas.items():
                                                                                    operacion_legado = clave
                                                                                    proxy_interno = valor.split("/")[-1]
                                                                                    print_with_line_number(f"clave {clave}")
                                                                                    print_with_line_number("")
                                                                                    print_with_line_number(f"valor {valor}")
                                                                                    
                                                                                    if es_business_service in valor:
                                                                                        
                                                                                        osb_file_path = os.path.join(jdeveloper_projects_dir, valor + ".BusinessService")
                                                                                        project_name = extract_project_name_from_business(osb_file_path)
                                                                                        print_with_line_number(f"project_name es : {project_name}")
                                                                                        if project_name is None:
                                                                                            print_with_line_number(f"project_name es 'None' : {project_name}")
                                                                                            print_with_line_number("")
                                                                                            continue

                                                                                        with open(osb_file_path, 'r', encoding="utf-8") as f:
                                                                                            content = f.read()
                                                                                            service_name = os.path.splitext(os.path.basename(osb_file_path))[0]
                                                                                            print_with_line_number(f"service_name: {service_name}")
                                                                                            wsdl_relative_path = extract_wsdl_relative_path(content)

                                                                                            wsdl_path = os.path.join(jdeveloper_projects_dir, wsdl_relative_path + ".WSDL")
                                                                                            operations = extract_wsdl_operations(wsdl_path)
                                                                                            service_refs = extract_uri_and_provider_id_from_bix(osb_file_path)
                                                                                            print_with_line_number(f"service_refs: {service_refs}")
                                                                                            print_with_line_number("")

                                                                                            for uri_value, provider_id_value in service_refs:
                                                                                                
                                                                                                print_with_line_number(f"DATOS {operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, valor, operacion_legado, uri_value, provider_id_value}")
                                                                                                osb_services.append((operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, valor, operacion_legado, uri_value, provider_id_value))
                                                                                
                                                    
                                                    
                                                        else:
                                                            valor_limpio = valor.split("/")[-1]
                                                            print_with_line_number(f"valor_limpio: {valor_limpio}")
                                                            proxy_ebs3 = proxy_ebs3_momento+"/"+valor_limpio
                                                            print_with_line_number(f"DATOS {operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, valor, operacion_legado, proxy_interno, clave}")
                                                            osb_services.append((operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, valor, operacion_legado, proxy_interno, clave))
                                                            print_with_line_number(f"operacion {operacion}")
                                                            print_with_line_number(f"proxy_ebs1 {proxy_ebs1}")
                                                            print_with_line_number(f"referencia {referencia}")
                                                            print_with_line_number(f"operacion_legado {operacion_legado}")
                                                            print_with_line_number(f"operacion_legado {operacion_legado}")
                                                            print_with_line_number("")
                                                            print_with_line_number("")
                                                            print_with_line_number(f"osb_services: {osb_services}")
                                                            print_with_line_number("")
                                                    
                                                    valor_limpio = ""
                                        
                                        else:
                                            osb_file_path = os.path.join(jdeveloper_projects_dir, proxy_interno + ".BusinessService")
                                            project_name = extract_project_name_from_business(osb_file_path)
                                            print_with_line_number(f"project_name es : {project_name}")
                                            if project_name is None:
                                                print_with_line_number(f"project_name es 'None' : {project_name}")
                                                print_with_line_number("")
                                                continue

                                            with open(osb_file_path, 'r', encoding="utf-8") as f:
                                                content = f.read()
                                                service_name = os.path.splitext(os.path.basename(osb_file_path))[0]
                                                print_with_line_number(f"service_name: {service_name}")
                                                wsdl_relative_path = extract_wsdl_relative_path(content)

                                                wsdl_path = os.path.join(jdeveloper_projects_dir, wsdl_relative_path + ".WSDL")
                                                operations = extract_wsdl_operations(wsdl_path)
                                                service_refs = extract_uri_and_provider_id_from_bix(osb_file_path)
                                                print_with_line_number(f"service_refs: {service_refs}")
                                                print_with_line_number("")

                                                for uri_value, provider_id_value in service_refs:
                                                    ruta_proxy_completa = proxy_interno
                                                    proxy_ebs3 = referencia.split("/")[-1]
                                                    print_with_line_number(f"ruta_proxy_completa {ruta_proxy_completa}")
                                                    print_with_line_number(f"proxy_ebs3 {proxy_ebs3}")
                                                    print_with_line_number(f"proxy_interno {proxy_interno}")
                                                    print_with_line_number(f"DATOS {operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, ruta_proxy_completa, operacion_legado, uri_value, provider_id_value}")
                                                    osb_services.append((operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, ruta_proxy_completa, operacion_legado, uri_value, provider_id_value))
                                                    print_with_line_number(f"operacion {operacion}")
                                                    print_with_line_number(f"proxy_ebs1 {proxy_ebs1}")
                                                    print_with_line_number(f"referencia {referencia}")
                                                    print_with_line_number(f"operacion_legado {operacion_legado}")
                                                    print_with_line_number(f"uri_value {uri_value}")
                                                    print_with_line_number(f"provider_id_value {provider_id_value}")
                                                    print_with_line_number("")
                                                    print_with_line_number(f"osb_services: {osb_services}")
                                                    print_with_line_number("")
                                            
                                        print_with_line_number("")
                                        print_with_line_number(f"osb_services: {osb_services}")
                                        print_with_line_number("")
                                        proxy_ebs3 = ""
                                        

                    elif 'Business' in referencia:
                        print_with_line_number("Es BUSINESS SERVICE!!")
                        osb_file_path = os.path.join(jdeveloper_projects_dir, referencia + ".BusinessService")
                        print_with_line_number("")
                        print_with_line_number(f"osb_file_path: {osb_file_path}")
                        print_with_line_number("")
                        project_name = extract_project_name_from_business(osb_file_path)
                        print_with_line_number(f"project_name: {project_name}")
                        print_with_line_number("")
                        if project_name is None:
                            print_with_line_number(f"project_name es 'None' : {project_name}")
                            print_with_line_number("")
                            continue
                            
                        if len(project_name) <= 0:
                            project_name = extract_project_name_from_business_tuxedo(osb_file_path)
                            print_with_line_number(f"project_name: {project_name}")
                            print_with_line_number("")
                            
                            service_refs = extract_uri_and_provider_id_from_bix(osb_file_path)
                            print_with_line_number(f"service_refs: {service_refs}")
                            print_with_line_number("")

                            for uri_value, provider_id_value in service_refs:
                                osb_services.append((operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, referencia, operacion_legado, uri_value, provider_id_value))
                                print_with_line_number(f"operacion {operacion}")
                                print_with_line_number(f"proxy_ebs1 {proxy_ebs1}")
                                print_with_line_number(f"proxy_ebs2 {proxy_ebs2}")
                                print_with_line_number(f"proxy_ebs3 {proxy_ebs3}")
                                print_with_line_number(f"referencia {referencia}")
                                print_with_line_number(f"operacion_legado {operacion_legado}")
                                print_with_line_number(f"uri_value {uri_value}")
                                print_with_line_number(f"provider_id_value {provider_id_value}")
                                print_with_line_number("")
                                print_with_line_number(f"osb_services: {osb_services}")
                                print_with_line_number("")

                        with open(osb_file_path, 'r', encoding="utf-8") as f:
                            content = f.read()
                            service_name = os.path.splitext(os.path.basename(osb_file_path))[0]
                            print_with_line_number(f"service_name: {service_name}")
                            print_with_line_number("")
                            wsdl_relative_path = extract_wsdl_relative_path(content)
                            print_with_line_number(f"wsdl_relative_path: {wsdl_relative_path}")
                            print_with_line_number("")

                            if wsdl_relative_path:
                                wsdl_path = os.path.join(jdeveloper_projects_dir, wsdl_relative_path + ".WSDL")
                                print_with_line_number(f"wsdl_path: {wsdl_path}")
                                print_with_line_number("")
                                operations = extract_wsdl_operations(wsdl_path)
                                print_with_line_number(f"operations: {operations}")
                                print_with_line_number("")
                                service_refs = extract_uri_and_provider_id_from_bix(osb_file_path)
                                print_with_line_number(f"service_refs: {service_refs}")
                                print_with_line_number("")

                                for uri_value, provider_id_value in service_refs:
                                    osb_services.append((operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, referencia, operacion_legado, uri_value, provider_id_value))
                                    print_with_line_number(f"operacion {operacion}")
                                    print_with_line_number(f"proxy_ebs1 {proxy_ebs1}")
                                    print_with_line_number(f"proxy_ebs2 {proxy_ebs2}")
                                    print_with_line_number(f"proxy_ebs3 {proxy_ebs3}")
                                    print_with_line_number(f"referencia {referencia}")
                                    print_with_line_number(f"operacion_legado {operacion_legado}")
                                    print_with_line_number(f"uri_value {uri_value}")
                                    print_with_line_number(f"provider_id_value {provider_id_value}")
                                    print_with_line_number("")
                                    print_with_line_number(f"osb_services: {osb_services}")
                                    print_with_line_number("")
                    
                    
                else: #Es un ABC
                    if 'Proxies' in referencia:
                        print_with_line_number(f"Proxies esta en referencia : {referencia}")
                        print_with_line_number("")
                        osb_file_path = os.path.join(jdeveloper_projects_dir, referencia + ".ProxyService")
                        print_with_line_number(f"osb_file_path : {osb_file_path}")
                        print_with_line_number("")
                        project_name = extract_project_name_from_proxy(osb_file_path)
                        if project_name is None:
                            osb_services.append((operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, referencia, operacion_legado, 'N/A', 'N/A'))
                            print_with_line_number(f"project_name es 'None' : {project_name}")
                            print_with_line_number("")
                            print_with_line_number("")
                            print_with_line_number(f"osb_services: {osb_services}")
                            print_with_line_number("")
                            continue

                        pipeline_path = extract_pipeline_path_from_proxy(osb_file_path, jdeveloper_projects_dir)
                        print_with_line_number(f"pipeline_path: {pipeline_path}")
                        print_with_line_number("")
                        with open(osb_file_path, 'r', encoding="utf-8") as f:
                            content = f.read()
                            service_name = os.path.splitext(os.path.basename(osb_file_path))[0]
                            wsdl_relative_path = extract_wsdl_relative_path(content)

                            if wsdl_relative_path:
                                wsdl_path = os.path.join(jdeveloper_projects_dir, wsdl_relative_path + ".WSDL")
                                print_with_line_number(f"wsdl_path: {wsdl_path}")
                                print_with_line_number("")
                                operations = extract_wsdl_operations(wsdl_path)
                                print_with_line_number(f"operations: {operations}")
                                print_with_line_number("")
                                service_for_operations = extract_service_for_operations(pipeline_path, operacion_legado)
                                print_with_line_number(f"service_for_operations: {service_for_operations}")
                                print_with_line_number("")

                                if not service_for_operations:
                                    service_refs = extract_service_refs_from_pipeline(pipeline_path)
                                    print_with_line_number(f"service_for_operations 2: {service_for_operations}")
                                    print_with_line_number("")

                                    for service_ref in service_refs:
                                        osb_services.append((operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, referencia, operacion_legado, service_ref, operacion_legado))
                                        print_with_line_number(f"operacion {operacion}")
                                        print_with_line_number(f"proxy_ebs1 {proxy_ebs1}")
                                        print_with_line_number(f"referencia {referencia}")
                                        print_with_line_number(f"operacion_legado {operacion_legado}")
                                        print_with_line_number(f"service_ref {service_ref}")
                                        print_with_line_number(f"operacion_legado {operacion_legado}")
                                        print_with_line_number("")
                                        print_with_line_number("")
                                        print_with_line_number(f"osb_services: {osb_services}")
                                        print_with_line_number("")

                                else:
                                    for operation, proxy_interno in service_for_operations.items():
                                        print_with_line_number(f"operacion {operacion}")
                                        print_with_line_number(f"proxy_ebs1 {proxy_ebs1}")
                                        print_with_line_number(f"referencia {referencia}")
                                        print_with_line_number(f"operacion_legado {operacion_legado}")
                                        print_with_line_number(f"proxy_interno {proxy_interno}")
                                        print_with_line_number("")
                                        es_business_service = '/BusinessServices'
                                        if es_business_service not in proxy_interno:
                                        
                                            osb_file_path = os.path.join(jdeveloper_projects_dir, proxy_interno + ".ProxyService")
                                            print_with_line_number("")
                                            print_with_line_number(f"osb_file_path {osb_file_path}")
                                            print_with_line_number("")
                                            ruta_pipeline = extract_pipeline_path_from_proxy(osb_file_path, jdeveloper_projects_dir)
                                            print_with_line_number(f"ruta_pipeline: {ruta_pipeline}")
                                            if ruta_pipeline is None:
                                                osb_services.append((operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, referencia, operacion_legado, 'N/A', 'N/A'))
                                                print_with_line_number(f"ruta_pipeline es 'None' : {project_name}")
                                                print_with_line_number(f"operacion {operacion}")
                                                print_with_line_number(f"proxy_ebs1 {proxy_ebs1}")
                                                print_with_line_number(f"referencia {referencia}")
                                                print_with_line_number(f"operacion_legado {operacion_legado}")
                                                print_with_line_number(f"service_ref {service_ref}")
                                                print_with_line_number(f"operacion_legado {operacion_legado}")
                                                print_with_line_number("")
                                                print_with_line_number("")
                                                print_with_line_number(f"osb_services: {osb_services}")
                                                print_with_line_number("")
                                                continue
                                            operaciones_internas = definir_operaciones_internas_pipeline(ruta_pipeline)
                                            print_with_line_number("")
                                            print_with_line_number(f"operaciones_internas {operaciones_internas}")
                                            
                                            for clave in operaciones_internas.keys():
                                                print_with_line_number(f"clave {clave}")
                                                print_with_line_number("")
                                                osb_services.append((operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, referencia, operacion_legado, proxy_interno, clave))
                                                print_with_line_number(f"operacion {operacion}")
                                                print_with_line_number(f"proxy_ebs1 {proxy_ebs1}")
                                                print_with_line_number(f"referencia {referencia}")
                                                print_with_line_number(f"operacion_legado {operacion_legado}")
                                                print_with_line_number(f"service_ref {service_ref}")
                                                print_with_line_number(f"operacion_legado {operacion_legado}")
                                                print_with_line_number("")
                                                print_with_line_number("")
                                                print_with_line_number(f"osb_services: {osb_services}")
                                                print_with_line_number("")
                                        
                                        else:
                                            osb_file_path = os.path.join(jdeveloper_projects_dir, proxy_interno + ".BusinessService")
                                            project_name = extract_project_name_from_business(osb_file_path)
                                            print_with_line_number(f"project_name es : {project_name}")
                                            if project_name is None:
                                                print_with_line_number(f"project_name es 'None' : {project_name}")
                                                print_with_line_number("")
                                                continue

                                            with open(osb_file_path, 'r', encoding="utf-8") as f:
                                                content = f.read()
                                                service_name = os.path.splitext(os.path.basename(osb_file_path))[0]
                                                print_with_line_number(f"service_name: {service_name}")
                                                wsdl_relative_path = extract_wsdl_relative_path(content)

                                                wsdl_path = os.path.join(jdeveloper_projects_dir, wsdl_relative_path + ".WSDL")
                                                operations = extract_wsdl_operations(wsdl_path)
                                                service_refs = extract_uri_and_provider_id_from_bix(osb_file_path)
                                                print_with_line_number(f"service_refs: {service_refs}")
                                                print_with_line_number("")

                                                for uri_value, provider_id_value in service_refs:
                                                    proxy_ebs2 = proxy_ebs1
                                                    proxy_ebs3 = referencia.split("/")[-1]
                                                    referencia = service_name
                                                    operacion_legado = operation
                                                    print_with_line_number(f"DATOS {operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, proxy_interno, operacion_legado, uri_value, provider_id_value}")
                                                    osb_services.append((operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, proxy_interno, operacion_legado, uri_value, provider_id_value))
                                                    print_with_line_number(f"operacion {operacion}")
                                                    print_with_line_number(f"proxy_ebs1 {proxy_ebs1}")
                                                    print_with_line_number(f"referencia {referencia}")
                                                    print_with_line_number(f"operacion_legado {operacion_legado}")
                                                    print_with_line_number(f"uri_value {uri_value}")
                                                    print_with_line_number(f"provider_id_value {provider_id_value}")
                                                    print_with_line_number("")
                                                    print_with_line_number(f"osb_services: {osb_services}")
                                                    print_with_line_number("")
                                            
                                        print_with_line_number("")
                                        print_with_line_number(f"osb_services: {osb_services}")
                                        print_with_line_number("")
                                        

                    elif 'Business' in referencia:
                        print_with_line_number("Es BUSINESS SERVICE!!")
                        osb_file_path = os.path.join(jdeveloper_projects_dir, referencia + ".BusinessService")
                        print_with_line_number("")
                        print_with_line_number(f"osb_file_path: {osb_file_path}")
                        print_with_line_number("")
                        project_name = extract_project_name_from_business(osb_file_path)
                        print_with_line_number(f"project_name: {project_name}")
                        print_with_line_number("")
                        if project_name is None:
                            print_with_line_number(f"project_name es 'None' : {project_name}")
                            print_with_line_number("")
                            continue
                            
                        if len(project_name) <= 0:
                            project_name = extract_project_name_from_business_tuxedo(osb_file_path)
                            print_with_line_number(f"project_name: {project_name}")
                            print_with_line_number("")
                            
                            service_refs = extract_uri_and_provider_id_from_bix(osb_file_path)
                            print_with_line_number(f"service_refs: {service_refs}")
                            print_with_line_number("")

                            for uri_value, provider_id_value in service_refs:
                                osb_services.append((operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, referencia, operacion_legado, uri_value, provider_id_value))
                                print_with_line_number(f"operacion {operacion}")
                                print_with_line_number(f"proxy_ebs1 {proxy_ebs1}")
                                print_with_line_number(f"proxy_ebs2 {proxy_ebs2}")
                                print_with_line_number(f"proxy_ebs3 {proxy_ebs3}")
                                print_with_line_number(f"referencia {referencia}")
                                print_with_line_number(f"operacion_legado {operacion_legado}")
                                print_with_line_number(f"uri_value {uri_value}")
                                print_with_line_number(f"provider_id_value {provider_id_value}")
                                print_with_line_number("")
                                print_with_line_number(f"osb_services: {osb_services}")
                                print_with_line_number("")

                        with open(osb_file_path, 'r', encoding="utf-8") as f:
                            content = f.read()
                            service_name = os.path.splitext(os.path.basename(osb_file_path))[0]
                            print_with_line_number(f"service_name: {service_name}")
                            print_with_line_number("")
                            wsdl_relative_path = extract_wsdl_relative_path(content)
                            print_with_line_number(f"wsdl_relative_path: {wsdl_relative_path}")
                            print_with_line_number("")

                            if wsdl_relative_path:
                                wsdl_path = os.path.join(jdeveloper_projects_dir, wsdl_relative_path + ".WSDL")
                                print_with_line_number(f"wsdl_path: {wsdl_path}")
                                print_with_line_number("")
                                operations = extract_wsdl_operations(wsdl_path)
                                print_with_line_number(f"operations: {operations}")
                                print_with_line_number("")
                                service_refs = extract_uri_and_provider_id_from_bix(osb_file_path)
                                print_with_line_number(f"service_refs: {service_refs}")
                                print_with_line_number("")

                                for uri_value, provider_id_value in service_refs:
                                    osb_services.append((operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, referencia, operacion_legado, uri_value, provider_id_value))
                                    print_with_line_number(f"operacion {operacion}")
                                    print_with_line_number(f"proxy_ebs1 {proxy_ebs1}")
                                    print_with_line_number(f"proxy_ebs2 {proxy_ebs2}")
                                    print_with_line_number(f"proxy_ebs3 {proxy_ebs3}")
                                    print_with_line_number(f"referencia {referencia}")
                                    print_with_line_number(f"operacion_legado {operacion_legado}")
                                    print_with_line_number(f"uri_value {uri_value}")
                                    print_with_line_number(f"provider_id_value {provider_id_value}")
                                    print_with_line_number("")
                                    print_with_line_number(f"osb_services: {osb_services}")
                                    print_with_line_number("")
                    
                    
                    else:
                        osb_services.append((operacion , proxy_ebs1, proxy_ebs2, proxy_ebs3, referencia, operacion_legado, 'N/A', 'N/A'))
                        print_with_line_number(f"NO es ni 'Proxy' ni 'Business': {referencia}")
                        print_with_line_number("")
                        print_with_line_number(f"osb_services: {osb_services}")
                        print_with_line_number("")
            
            else:
                proxy_interno = referencia.split("/")[-1]
                print_with_line_number(f"DATOS {operacion , proxy_ebs1, proxy_ebs2, proxy_interno, referencia, operacion_legado, 'N/A', 'N/A'}")
                osb_services.append((operacion , proxy_ebs1, proxy_ebs2, proxy_interno, referencia, operacion_legado, 'N/A', 'N/A'))
                print_with_line_number(f"Palabra invalida: {referencia}")
                print_with_line_number("")
                print_with_line_number(f"osb_services: {osb_services}")
                print_with_line_number("")
    return osb_services

def extract_osb_services_finals(jdeveloper_projects_dir, services_for_operations):
    osb_services = []
    
    #print_with_line_number("")
    #print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_FINALS*********************************************")
    #print_with_line_number("")
    
    for service_name_principal, proxies_list in services_for_operations.items():
        #print_with_line_number(f" ")
        #print_with_line_number("/////////////")
        #print_with_line_number(f"SERVICIO: {service_name_principal}")
        #print_with_line_number("****************************************************************************************************")
        
        for proxy_dict in proxies_list:
            for operation_name, proxy_business in proxy_dict.items():
                #print_with_line_number("Nombre de operacion:", operation_name)
                #print_with_line_number("Nombre proxy_business:", proxy_business)
                #print_with_line_number()
                
                #print_with_line_number("****************************************************************************************************")
                #print_with_line_number("")
                
                if 'Proxies' in proxy_business:
                    osb_file_path = os.path.join(jdeveloper_projects_dir, proxy_business + ".ProxyService")
                    #print_with_line_number(f"PROXY : {proxy_business}")
                    project_name = extract_project_name_from_proxy(osb_file_path)
                    if project_name is None:
                        continue
    
                    pipeline_path = extract_pipeline_path_from_proxy(osb_file_path, jdeveloper_projects_dir)
                    #print_with_line_number(f"PIPELINE: {pipeline_path}")
                    
                    with open(osb_file_path, 'r', encoding="utf-8") as f:
                        content = f.read()
                        service_name = os.path.splitext(os.path.basename(osb_file_path))[0]
                        wsdl_relative_path = extract_wsdl_relative_path(content)
                        
                        if wsdl_relative_path:
                            wsdl_path = os.path.join(jdeveloper_projects_dir, wsdl_relative_path + ".WSDL")
                            #print_with_line_number("")
                            #print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_FINALS*********************************************")
                            #print_with_line_number(f"WSDL: {wsdl_path}")
                            #print_with_line_number("")
                            operations = extract_wsdl_operations(wsdl_path)
                            #print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_FINALS*********************************************")
                            #print_with_line_number("")
                            #print_with_line_number(f"OPERACION DEL PIPELINE: {operations}")
                            service_for_operations = extract_service_for_operations(pipeline_path, operations)
                            
                            
                            if not service_for_operations:
                                #print_with_line_number("")
                                #print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_FINALS*********************************************")
                                #print_with_line_number(f"OPERACIONES INTERNAS: {service_for_operations}")
                                service_refs = extract_service_refs_from_pipeline(pipeline_path)
                                #print_with_line_number("")
                                #print_with_line_number("*****************************INICIO EXTRACT_OSB_SERVICES_FINALS*********************************************")
                                #print_with_line_number("")
                                #print_with_line_number("Service for operations no devolvió datos. Obteniendo referencias de servicio desde el archivo .pipeline...")
                                #print_with_line_number(f" ")
                                
                                #print_with_line_number("__________________________________________________________________________")
                                #print_with_line_number(f"PROXY ABC: {proxy_business}")
                                #print_with_line_number("__________________________________________________________________________")
                                
                                for service_ref in service_refs:
                                    #print_with_line_number("___________________1________________________")
                                    #print_with_line_number(f"   OPERACION EBS: {service_name}")
                                    #print_with_line_number(f"   OPERACION ABC: {operations[0]} ")
                                    #print_with_line_number(f"   PROXY ABC: {proxy_business}")
                                    #print_with_line_number(f"   REFERENCIAS PL: {service_ref} ")
                                    #print_with_line_number("____________________________________________")
                                    
                                    osb_services.append((service_name, proxy_business, operations[0], service_ref))
                                    #print_with_line_number("SE INVOCA AL BS 1")
                                    extract_osb_businessService(jdeveloper_projects_dir, osb_services)
                                        
                            else:
                                for referencias in service_for_operations:
                                    #print_with_line_number("__________________2__________________________")
                                    #print_with_line_number(f"   OPERACION EBS: {service_name}")
                                    #print_with_line_number(f"   PROXY ABC: {proxy_business}")
                                    #print_with_line_number(f"   REFERENCIAS PL: {referencias} ")
                                    #print_with_line_number("____________________________________________")
                                    
                                    osb_services.append((service_name, proxy_business, operations[0], referencias))
                                    #print_with_line_number("SE INVOCA AL BS 2")
                                    extract_osb_businessService(jdeveloper_projects_dir, osb_services)
                                
                elif 'BusinessServices' in proxy_business:
                    osb_file_path = os.path.join(jdeveloper_projects_dir, proxy_business + ".BusinessService")
                    #print_with_line_number("")
                    #print_with_line_number("/////////////")
                    #print_with_line_number(f"BUSINESS SERVICE : {proxy_business}")
                    project_name = extract_project_name_from_business(osb_file_path)
                    if project_name is None:
                        continue
    
                    with open(osb_file_path, 'r', encoding="utf-8") as f:
                        content = f.read()
                        service_name = os.path.splitext(os.path.basename(osb_file_path))[0]
                        wsdl_relative_path = extract_wsdl_relative_path(content)
                        
                        if wsdl_relative_path:
                            wsdl_path = os.path.join(jdeveloper_projects_dir, wsdl_relative_path + ".WSDL")
                            #print_with_line_number(f"WSDL: {wsdl_path}")
                            operations = extract_wsdl_operations(wsdl_path)
                            #print_with_line_number(f"OPERACIONES WSDL: {operations}")
                            service_refs = extract_uri_and_provider_id_from_bix(osb_file_path)
                            #print_with_line_number("Service for operations no devolvió datos. Obteniendo referencias de servicio desde el archivo .pipeline...")
                            #print_with_line_number(f" ")
                            ##print_with_line_number("Referencias de servicio encontradas:", service_refs)
                            
                            for uri_value, provider_id_value in service_refs:
                                #print_with_line_number(f"SERVICE REFS BUSINESS: {uri_value} , {provider_id_value} ")
                                osb_services.append((service_name, uri_value, provider_id_value))
                        else:
                            service_refs = extract_uri_and_provider_id_from_bix(osb_file_path)
                            #print_with_line_number("__________________________________________________________________________")
                            #print_with_line_number(f"BUSINESS ABC: {proxy_business}")
                            #print_with_line_number("__________________________________________________________________________")
                            
                            for uri_value, provider_id_value in service_refs:
                                print_with_line_number("____________________________________________")
                                print_with_line_number(f"   OPERACION EBS: {service_name}")
                                print_with_line_number(f"   URI: {uri_value}")
                                print_with_line_number(f"   TIPO: {provider_id_value}")
                                print_with_line_number("____________________________________________")
                                
                            osb_services.append((service_name,  uri_value, provider_id_value))
                    #print_with_line_number("**************************FIN DEL BUSINESS SERVICE*********************************")  
                else:
                    print_with_line_number("NADA") 
                #print_with_line_number(f"OSB SERVICES APPEND: {osb_services} ") 
    #print_with_line_number("")
    #print_with_line_number("*****************************FIN EXTRACT_OSB_SERVICES_FINALS*********************************************")
    #print_with_line_number("")    
    return osb_services
    
def count_total_references(references):
    return len(references)

def devolver_ruta_wsdl_proxy(proxy_path):
    try:
        with open(proxy_path, 'r', encoding="utf-8") as f:
            content = f.read()
            start = content.find('<con:wsdl ref="') + len('<con:wsdl ref="')
            end = content.find('"', start)
            wsdl_ref = content[start:end]
            #print_with_line_number(f"wsdl_ref: {wsdl_ref}") 
            return wsdl_ref
    except FileNotFoundError:
        #print_with_line_number(f"El archivo {proxy_path} no existe.")
        return None

def extract_project_name_from_proxy(proxy_path):
    try:
        with open(proxy_path, 'r', encoding="utf-8") as f:
            content = f.read()
            start = content.find('<con:wsdl ref="') + len('<con:wsdl ref="')
            end = content.find('"', start)
            wsdl_ref = content[start:end]
            return wsdl_ref.split("/")[0]
    except FileNotFoundError:
        #print_with_line_number(f"El archivo {proxy_path} no existe.")
        return None
        
def extract_project_name_from_business(business_path):
    try:
        with open(business_path, 'r', encoding="utf-8") as f:
            content = f.read()
            start = content.find('<con:wsdl ref="') + len('<con:wsdl ref="')
            end = content.find('"', start)
            wsdl_ref = content[start:end]
            return wsdl_ref.split("/")[0]
    except FileNotFoundError:
        #print_with_line_number(f"El archivo {business_path} no existe.")
        return None

def extract_project_name_from_business_tuxedo(business_path):
    try:
        with open(business_path, 'r', encoding="utf-8") as f_bix:
            bix_content = f_bix.read()
            start_bix = bix_content.find('<con:endpointConfig>') + len('<con:endpointConfig>')
            end_bix = bix_content.find('</con:endpointConfig>', start_bix)
            endpoint_config_section = bix_content[start_bix:end_bix]

            start_provider_id = endpoint_config_section.find('<tran:provider-id>') + len('<tran:provider-id>')
            end_provider_id = endpoint_config_section.find('</tran:provider-id>', start_provider_id)
            provider_id = endpoint_config_section[start_provider_id:end_provider_id].strip()
            
            return provider_id
    except FileNotFoundError:
        #print_with_line_number(f"El archivo {business_path} no existe.")
        return None

def extract_uri_and_provider_id_from_bix(bix_path):
    lista_uri_provider = []
    with open(bix_path, 'r', encoding="utf-8") as f:
        content = f.read()
        # Buscar el valor dentro de las etiquetas <env:value>
        uri_match = re.search(r'<env:value>(.*?)</env:value>', content, re.DOTALL)
        
        #print_with_line_number(f"MATCH: {uri_match}")
        if uri_match:
            uri_value = uri_match.group(1)
        else:
            uri_value = None

        #print_with_line_number(f"URI VALUE: {uri_value}")
        # Buscar el valor dentro de las etiquetas <tran:provider-id>
        provider_id_match = re.search(r'<tran:provider-id>(.*?)</tran:provider-id>', content, re.DOTALL)
        #print_with_line_number(f"PROVIDER_ID: {provider_id_match}")
        if provider_id_match:
            provider_id_value = provider_id_match.group(1)
        else:
            provider_id_value = None
        
        #print_with_line_number(f"PROVIDER_ID_VALUE: {provider_id_value}")
        lista_uri_provider.append((uri_value, provider_id_value))
        return lista_uri_provider

def has_http_provider_id(xml_content):
    root = ET.fromstring(xml_content)
    namespaces = {'tran': 'http://www.bea.com/wli/sb/transports'}
    provider_id_element = root.find(".//tran:provider-id", namespaces)
    return provider_id_element is not None and provider_id_element.text == 'http'

def extract_service_url(xml_content):
    root = ET.fromstring(xml_content)
    tran_namespace = {'tran': 'http://www.bea.com/wli/sb/transports', 'env': 'http://www.bea.com/wli/config/env'}
    uri_element = root.find(".//tran:URI/env:value", namespaces=tran_namespace)
    if uri_element is not None:
        return uri_element.text
    return ''

def extract_wsdl_relative_path(xml_content):
    root = ET.fromstring(xml_content)
    namespaces = {'con': 'http://www.bea.com/wli/sb/services/bindings/config'}
    namespaces_pipeline = {'con': 'http://www.bea.com/wli/sb/pipeline/config'}
    wsdl_ref_element = root.find(".//con:wsdl", namespaces)
    wsdl_ref_element_pipeline = root.find(".//con:wsdl", namespaces_pipeline)
    if wsdl_ref_element is not None:
        wsdl_relative_path = wsdl_ref_element.attrib.get('ref', '')
        return wsdl_relative_path
    elif wsdl_ref_element_pipeline is not None:
        wsdl_relative_path = wsdl_ref_element_pipeline.attrib.get('ref', '')
        return wsdl_relative_path
    return ''

def extract_wsdl_operations(wsdl_path):
    operations = set()  # Utilizamos un conjunto en lugar de una lista
    if wsdl_path.endswith('.WSDL') and os.path.isfile(wsdl_path):
        with open(wsdl_path, 'r', encoding="utf-8") as f:
            wsdl_content = f.read()
            # Buscamos todas las coincidencias de "<operation name=" seguidas por el nombre de la operación
            operation_names = re.findall(r'operation name="([^"]+)', wsdl_content)
            for operation_name in operation_names:
                operations.add(operation_name)  # Agregamos el nombre de la operación al conjunto
    return list(operations)  # Convertimos el conjunto de vuelta a lista antes de devolverlo
  
  
def extract_pipeline_path_from_proxy(proxy_path, jdeveloper_projects_dir):
    try:
        with open(proxy_path, 'r', encoding="utf-8") as f:
            content = f.read()
            start = content.find('<ser:invoke ref="') + len('<ser:invoke ref="')
            end = content.find('"', start)
            pipeline_ref = content[start:end]
            pipeline_path = os.path.join(jdeveloper_projects_dir, pipeline_ref + ".pipeline")
            return pipeline_path
    except FileNotFoundError:
        print(f"El archivo {proxy_path} no pudo ser encontrado.")
        return None  # O puedes lanzar otra excepción, dependiendo del flujo de tu programa.
        
def extract_uri_from_bix(bix_path):
    with open(bix_path, 'r', encoding="utf-8") as f:
        content = f.read()
        # Utilizamos una expresión regular para encontrar el valor dentro de las etiquetas <env:value>
        match = re.search(r'<env:value>(.*?)</env:value>', content, re.DOTALL)
        print_with_line_number(f"MATCH: {match}")
        if match:
            uri_value = match.group(1)  # Obtenemos el valor capturado por la expresión regular
            return uri_value
        else:
            print_with_line_number("No se encontró ninguna URI en el archivo .BusinessService.")
            return None
        
        print_with_line_number(f"uri_value: {uri_value}")
            
def extract_provider_id_from_bix(bix_path):
    with open(bix_path, 'r', encoding="utf-8") as f:
        content = f.read()
        # Buscar el valor dentro de las etiquetas <tran:provider-id>
        provider_id_match = re.search(r'<tran:provider-id>(.*?)</tran:provider-id>', content, re.DOTALL)
        if provider_id_match:
            provider_id_value = provider_id_match.group(1)
        else:
            provider_id_value = None

        return provider_id_value

def definir_operaciones_internas_pipeline(pipeline_path):
    service_refs = set()
    services_for_operations = {}
    #print_with_line_number("ENTRO A OPERACIONES INTERNAS PIPELINE")
    try:
        with open(pipeline_path, 'r', encoding="utf-8") as f:
            pipeline_content = f.read()
            root = ET.fromstring(pipeline_content)
            
            ns_stage_transform_config   = {'con1': 'http://www.bea.com/wli/sb/stages/transform/config'}
            ns_stage_publish_config     = {'con1': 'http://www.bea.com/wli/sb/stages/publish/config'}
            ns_stage_routing_config     = {'con1': 'http://www.bea.com/wli/sb/stages/routing/config'}
            ns_stage_config             = {'con1':'http://www.bea.com/wli/sb/stages/config'}
            
            ns_stage_pipeline_config    = {'con': 'http://www.bea.com/wli/sb/pipeline/config',
                                        'con1': 'http://www.bea.com/wli/sb/stages/routing/config',
                                        'con2': 'http://www.bea.com/wli/sb/stages/config',
                                        'con3': 'http://www.bea.com/wli/sb/stages/transform/config',
                                        'ref': 'http://www.bea.com/wli/sb/reference',
                                        'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
            
            ns                           = {'con': 'http://www.example.com',
                                            'con4': 'http://www.bea.com/wli/sb/stages/routing/config',
                                            'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
            
            ws_callouts = root.findall(".//con1:wsCallout", namespaces=ns_stage_transform_config)
            #print_with_line_number(f"ws_callouts: {ws_callouts}")
            
            ws_callouts2 = root.findall(".//con1:wsCallout", namespaces=ns_stage_config)
            
            java_callouts = root.findall(".//con1:javaCallout", namespaces=ns_stage_transform_config)
            #print_with_line_number(f"java_callouts: {java_callouts}")
            routes = root.findall(".//con1:route", namespaces=ns_stage_publish_config)
            #print_with_line_number(f"routes: {routes}")
            routes2 = root.findall(".//con1:route", namespaces=ns_stage_routing_config)
            #print_with_line_number(f"routes2: {routes2}")
            flow_elements = root.findall(".//con:flow", ns_stage_pipeline_config)
            print_with_line_number(f"flow_elements: {flow_elements}")
            print_with_line_number("")
            
            for java_callout in java_callouts:
                method_element = java_callout.find(".//con1:method", namespaces=ns_stage_transform_config)
                if method_element is not None:
                    method_text = method_element.text
                    operation_name = method_text.split('(')[0].split()[-1]
                    service_element = java_callout.find(".//con1:archive", namespaces=ns_stage_transform_config)
                    if service_element is not None:
                        service_ref = service_element.attrib.get('ref', '')
                        service_refs.add(service_ref)
                        
                        # Verificar si la operación ya existe en el diccionario
                        new_operation_name = operation_name
                        version = 2
                        while (new_operation_name in services_for_operations and services_for_operations[new_operation_name] != service_ref):
                            new_operation_name = f"{operation_name}v{version}"
                            version += 1  # Incrementa la versión si ya existe

                        # Asignar el service_ref con el nuevo nombre de operación
                        services_for_operations[new_operation_name] = service_ref
                        
                        print_with_line_number(f"service_ref: {service_ref} - operation_name: {new_operation_name}")
            
            for ws_callout in ws_callouts:
                service_element = ws_callout.find(".//con1:service", namespaces=ns_stage_transform_config)
                operation_element = ws_callout.find(".//con1:operation", namespaces=ns_stage_transform_config)
                if service_element is not None and operation_element is not None:
                    service_ref = service_element.attrib.get('ref', '')
                    operation_name = operation_element.text
                    service_refs.add(service_ref)
                    
                    # Verificar si la operación ya existe en el diccionario
                    new_operation_name = operation_name
                    version = 2
                    while (new_operation_name in services_for_operations and services_for_operations[new_operation_name] != service_ref):
                        new_operation_name = f"{operation_name}v{version}"
                        version += 1  # Incrementa la versión si ya existe

                    # Asignar el service_ref con el nuevo nombre de operación
                    services_for_operations[new_operation_name] = service_ref
                    
                    print_with_line_number(f"service_ref: {service_ref} - operation_name: {new_operation_name}")
            
            for element in root.iter():
                if element.tag.endswith('wsCallout'):
                    service_element = element.find(".//con1:service", namespaces=ns_stage_transform_config)
                    operation_element = element.find(".//con1:operation", namespaces=ns_stage_transform_config)
                    if service_element is not None and operation_element is not None:
                        service_ref = service_element.attrib.get('ref', '')
                        operation_name = operation_element.text
                        service_refs.add(service_ref)
                        
                        # Verificar si la operación ya existe en el diccionario
                        new_operation_name = operation_name
                        version = 2
                        while (new_operation_name in services_for_operations and services_for_operations[new_operation_name] != service_ref):
                            new_operation_name = f"{operation_name}v{version}"
                            version += 1  # Incrementa la versión si ya existe

                        # Asignar el service_ref con el nuevo nombre de operación
                        services_for_operations[new_operation_name] = service_ref
                        
                        print_with_line_number(f"service_ref: {service_ref} - operation_name: {new_operation_name}")
                      
                        
            #2 Forma de encontrar ws_callouts:
            
            for ws_callout in ws_callouts2:
                service_element = ws_callout.find(".//con1:service", namespaces=ns_stage_config)
                operation_element = ws_callout.find(".//con1:operation", namespaces=ns_stage_config)
                if service_element is not None and operation_element is not None:
                    service_ref = service_element.attrib.get('ref', '')
                    operation_name = operation_element.text
                    service_refs.add(service_ref)
                    
                    # Verificar si la operación ya existe en el diccionario
                    new_operation_name = operation_name
                    version = 2
                    while (new_operation_name in services_for_operations and services_for_operations[new_operation_name] != service_ref):
                        new_operation_name = f"{operation_name}v{version}"
                        version += 1  # Incrementa la versión si ya existe

                    # Asignar el service_ref con el nuevo nombre de operación
                    services_for_operations[new_operation_name] = service_ref
                    
                    print_with_line_number(f"service_ref: {service_ref} - operation_name: {new_operation_name}")
            
            for element in root.iter():
                if element.tag.endswith('wsCallout'):
                    service_element = element.find(".//con1:service", namespaces=ns_stage_config)
                    operation_element = element.find(".//con1:operation", namespaces=ns_stage_config)
                    if service_element is not None and operation_element is not None:
                        service_ref = service_element.attrib.get('ref', '')
                        operation_name = operation_element.text
                        service_refs.add(service_ref)
                        
                        # Verificar si la operación ya existe en el diccionario
                        new_operation_name = operation_name
                        version = 2
                        while (new_operation_name in services_for_operations and services_for_operations[new_operation_name] != service_ref):
                            new_operation_name = f"{operation_name}v{version}"
                            version += 1  # Incrementa la versión si ya existe

                        # Asignar el service_ref con el nuevo nombre de operación
                        services_for_operations[new_operation_name] = service_ref
                        
                        print_with_line_number(f"service_ref: {service_ref} - operation_name: {new_operation_name}")
                        
            for route in routes:
                service_element = route.find(".//con1:service", namespaces=ns_stage_publish_config)
                operation_element = route.find(".//con1:operation", namespaces=ns_stage_publish_config)
                if service_element is not None and operation_element is not None:
                    service_ref = service_element.attrib.get('ref', '')
                    operation_name = operation_element.text
                    service_refs.add(service_ref)
                    
                    # Verificar si la operación ya existe en el diccionario
                    new_operation_name = operation_name
                    version = 2
                    while (new_operation_name in services_for_operations and services_for_operations[new_operation_name] != service_ref):
                        new_operation_name = f"{operation_name}v{version}"
                        version += 1  # Incrementa la versión si ya existe

                    # Asignar el service_ref con el nuevo nombre de operación
                    services_for_operations[new_operation_name] = service_ref
                    
                    print_with_line_number(f"service_ref: {service_ref} - operation_name: {new_operation_name}")
            
            #2 Forma de encontrar routes2:
            
            ns_con2 = {'con2': 'http://www.bea.com/wli/sb/stages/routing/config'}

            # Encuentra todos los elementos 'con2:route' dentro de 'con:flow'
            route_elements = root.findall(".//con2:route", namespaces=ns_con2)
            print_with_line_number(f"route_elements final : {route_elements}")

            # Itera sobre cada elemento 'con2:route' encontrado
            for route in route_elements:
                # Encuentra el elemento 'con2:service' dentro de 'con2:route'
                service_element = route.find(".//con2:service", namespaces=ns_con2)
                
                print_with_line_number(f"route_elements final : {service_element}")
                
                # Encuentra el elemento 'con2:operation' dentro de 'con2:route'
                operation_element = route.find(".//con2:operation", namespaces=ns_con2)
                
                # Verifica si ambos elementos 'con2:service' y 'con2:operation' existen
                if service_element is not None and operation_element is not None:
                    # Obtén el valor del atributo 'ref' de 'con2:service'
                    service_ref = service_element.attrib.get('ref', '')
                    
                    # Obtén el texto dentro de 'con2:operation'
                    operation_name = operation_element.text
                    
                    # Agrega el servicio y la operación al diccionario 'services_for_operations'
                    service_refs.add(service_ref)
                    
                    # Verificar si la operación ya existe en el diccionario
                    new_operation_name = operation_name
                    version = 2
                    while (new_operation_name in services_for_operations and services_for_operations[new_operation_name] != service_ref):
                        new_operation_name = f"{operation_name}v{version}"
                        version += 1  # Incrementa la versión si ya existe

                    # Asignar el service_ref con el nuevo nombre de operación
                    services_for_operations[new_operation_name] = service_ref
                    
                    print_with_line_number(f"service_ref: {service_ref} - operation_name: {new_operation_name}")
                            
             
             # Itera sobre cada elemento <con:flow> encontrado
            for flow_element in flow_elements:
                # Encuentra todos los elementos <con1:service> dentro de <con:flow>
                service_elements = flow_element.findall(".//con1:service[@xsi:type='ref:BusinessServiceRef']", ns_stage_pipeline_config)
                
                # Si no se encuentra ningún servicio dentro del flujo, salta al siguiente flujo
                if not service_elements:
                    continue
                
                # Itera sobre cada elemento <con1:service> encontrado dentro de <con:flow>
                for service_element in service_elements:
                    # Accede al atributo 'ref' del elemento <con1:service>
                    service_ref = service_element.attrib.get('ref', '')

                    # Encuentra todos los elementos <con1:operation> dentro de <con:flow>
                    operation_elements = flow_element.findall(".//con1:operation", ns_stage_pipeline_config)

                    # Si no se encuentra ningún elemento <con1:operation>, establece un valor predeterminado
                    if not operation_elements:
                        operation_name = service_ref.split('/')[-1]
                    else:
                        # Obtiene el texto del primer elemento <con1:operation>, que es el nombre de la operación
                        operation_element = operation_elements[0]
                        operation_name = operation_element.text.strip()

                    # Verificar si la operación ya existe en el diccionario
                    new_operation_name = operation_name
                    version = 2
                    while (new_operation_name in services_for_operations and services_for_operations[new_operation_name] != service_ref):
                        new_operation_name = f"{operation_name}v{version}"
                        version += 1  # Incrementa la versión si ya existe

                    # Asignar el service_ref con el nuevo nombre de operación
                    services_for_operations[new_operation_name] = service_ref
                    
                    print_with_line_number(f"service_ref: {service_ref} - operation_name: {new_operation_name}")
            
            print_with_line_number(f"service_refs: {service_refs}")
            print_with_line_number(f"Flow Elements Services: {services_for_operations}")

                   

        return services_for_operations
    except FileNotFoundError:
        print(f"El archivo {pipeline_path} no pudo ser encontrado.")

def extract_service_for_operations2(pipeline_path,operations):
    service_refs = set()
    services_for_operations = {}
    #print_with_line_number("ENTRO A OPERACIONES INTERNAS PIPELINE")
    
    with open(pipeline_path, 'r', encoding="utf-8") as f:
        pipeline_content = f.read()
        root = ET.fromstring(pipeline_content)
        
        ns_stage_transform_config   = {'con1': 'http://www.bea.com/wli/sb/stages/transform/config'}
        ns_stage_publish_config     = {'con1': 'http://www.bea.com/wli/sb/stages/publish/config'}
        ns_stage_routing_config     = {'con1': 'http://www.bea.com/wli/sb/stages/routing/config'}
        ns_stage_config             = {'con1':'http://www.bea.com/wli/sb/stages/config'}
        
        ns_stage_pipeline_config    = {'con': 'http://www.bea.com/wli/sb/pipeline/config',
                                    'con1': 'http://www.bea.com/wli/sb/stages/routing/config',
                                    'con2': 'http://www.bea.com/wli/sb/stages/config',
                                    'con3': 'http://www.bea.com/wli/sb/stages/transform/config',
                                    'ref': 'http://www.bea.com/wli/sb/reference',
                                    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
        
        ns                           = {'con': 'http://www.example.com',
                                        'con4': 'http://www.bea.com/wli/sb/stages/routing/config',
                                        'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
        
        ws_callouts = root.findall(".//con1:wsCallout", namespaces=ns_stage_transform_config)
        #print_with_line_number(f"ws_callouts: {ws_callouts}")
        java_callouts = root.findall(".//con1:javaCallout", namespaces=ns_stage_transform_config)
        #print_with_line_number(f"java_callouts: {java_callouts}")
        routes = root.findall(".//con1:route", namespaces=ns_stage_publish_config)
        #print_with_line_number(f"routes: {routes}")
        routes2 = root.findall(".//con1:route", namespaces=ns_stage_routing_config)
        #print_with_line_number(f"routes2: {routes2}")
        flow_elements = root.findall(".//con:flow", ns_stage_pipeline_config)
        print_with_line_number(f"flow_elements: {flow_elements}")
        print_with_line_number("")
        
        for java_callout in java_callouts:
            method_element = java_callout.find(".//con1:method", namespaces=ns_stage_transform_config)
            if method_element is not None:
                method_text = method_element.text
                operation_name = method_text.split('(')[0].split()[-1]
                service_element = java_callout.find(".//con1:archive", namespaces=ns_stage_transform_config)
                if service_element is not None:
                    service_ref = service_element.attrib.get('ref', '')
                    service_refs.add(service_ref)
                    services_for_operations[operation_name] = service_ref
                    #print_with_line_number(f"services_for_operations java_callouts: {services_for_operations}")
        
        for ws_callout in ws_callouts:
            service_element = ws_callout.find(".//con1:service", namespaces=ns_stage_transform_config)
            operation_element = ws_callout.find(".//con1:operation", namespaces=ns_stage_transform_config)
            if service_element is not None and operation_element is not None:
                service_ref = service_element.attrib.get('ref', '')
                operation_name = operation_element.text
                service_refs.add(service_ref)
                services_for_operations[operation_name] = service_ref
                #print_with_line_number(f"services_for_operations ws_callouts: {services_for_operations}")
        
        for element in root.iter():
            if element.tag.endswith('wsCallout'):
                service_element = element.find(".//con1:service", namespaces=ns_stage_transform_config)
                operation_element = element.find(".//con1:operation", namespaces=ns_stage_transform_config)
                if service_element is not None and operation_element is not None:
                    service_ref = service_element.attrib.get('ref', '')
                    operation_name = operation_element.text
                    service_refs.add(service_ref)
                    services_for_operations[operation_name] = service_ref
                    #print_with_line_number(f"services_for_operations iter: {services_for_operations}")
        
        for route in routes:
            service_element = route.find(".//con1:service", namespaces=ns_stage_publish_config)
            operation_element = route.find(".//con1:operation", namespaces=ns_stage_publish_config)
            if service_element is not None and operation_element is not None:
                service_ref = service_element.attrib.get('ref', '')
                operation_name = operation_element.text
                service_refs.add(service_ref)
                services_for_operations[operation_name] = service_ref
                #print_with_line_number(f"services_for_operations routes: {services_for_operations}")
        
        for route in routes2:
            service_element = route.find(" .//con1:service", namespaces=ns_stage_routing_config)
            operation_element = route.find(" .//con1:operation", namespaces=ns_stage_routing_config)
            if service_element is not None and operation_element is not None:
                service_ref = service_element.attrib.get('ref', '')
                operation_name = operation_element.text
                service_refs.add(service_ref)
                services_for_operations[operation_name] = service_ref
                #print_with_line_number(f"services_for_operations routes2: {services_for_operations}")
                
         
         # Itera sobre cada elemento <con:flow> encontrado
        for flow_element in flow_elements:
            # Encuentra todos los elementos <con1:service> dentro de <con:flow>
            service_elements = flow_element.findall(".//con1:service[@xsi:type='ref:BusinessServiceRef']", ns_stage_pipeline_config)
            
            # Si no se encuentra ningún servicio dentro del flujo, salta al siguiente flujo
            if not service_elements:
                continue
            
            # Itera sobre cada elemento <con1:service> encontrado dentro de <con:flow>
            for service_element in service_elements:
                # Accede al atributo 'ref' del elemento <con1:service>
                service_ref = service_element.attrib.get('ref', '')

                # Encuentra todos los elementos <con1:operation> dentro de <con:flow>
                operation_elements = flow_element.findall(".//con1:operation", ns_stage_pipeline_config)

                # Si no se encuentra ningún elemento <con1:operation>, establece un valor predeterminado
                if not operation_elements:
                    operation_name = service_ref.split('/')[-1]
                else:
                    # Obtiene el texto del primer elemento <con1:operation>, que es el nombre de la operación
                    operation_element = operation_elements[0]
                    operation_name = operation_element.text.strip()

                # Agrega la relación entre el nombre de la operación y la referencia del servicio al diccionario services_for_operations
                services_for_operations[operation_name] = service_ref

        print_with_line_number(f"Flow Elements Services: {services_for_operations}")

               

    return services_for_operations


def extract_service_refs_from_pipeline(pipeline_path):
    service_refs = set()  
    try:
        with open(pipeline_path, 'r', encoding="utf-8") as f:
            pipeline_content = f.read()
            root = ET.fromstring(pipeline_content)
            ns = {'con3': 'http://www.bea.com/wli/sb/stages/transform/config',
                  'con2': 'http://www.bea.com/wli/sb/stages/transform/config',
                  'con4': 'http://www.bea.com/wli/sb/stages/publish/config',
                  'con1': 'http://www.bea.com/wli/sb/stages/routing/config'}
            ws_callouts = root.findall(".//con3:wsCallout", namespaces=ns)
            java_callouts = root.findall(".//con2:javaCallout", namespaces=ns)
            routes = root.findall(".//con4:route", namespaces=ns)
            routes2 = root.findall(".//con1:route", namespaces=ns)
            for java_callout in java_callouts:
                archive_element = java_callout.find(".//con2:archive", namespaces=ns)
                if archive_element is not None:
                    archive_ref = archive_element.attrib.get('ref', '')
                    service_refs.add(archive_ref) 
            for ws_callout in ws_callouts:
                service_element = ws_callout.find(".//con3:service", namespaces=ns)
                if service_element is not None:
                    service_ref = service_element.attrib.get('ref', '')
                    service_refs.add(service_ref)
            
            for element in root.iter():
                if element.tag.endswith('wsCallout'):
                    service_element = element.find(".//service")
                    if service_element is not None:
                        service_ref = service_element.attrib.get('ref', '')
                        service_refs.add(service_ref)
            
            
            for route in routes:
                service_element = route.find(".//con4:service", namespaces=ns)
                if service_element is not None:
                    service_ref = service_element.attrib.get('ref', '')
                    service_refs.add(service_ref)
            for route in routes2:
                service_element = route.find(".//con1:service", namespaces=ns)
                if service_element is not None:
                    service_ref = service_element.attrib.get('ref', '')
                    service_refs.add(service_ref)
        return list(service_refs)
    except FileNotFoundError:
        print(f"El archivo {pipeline_path} no se encontró.")
        return []
    except Exception as e:
        print(f"Ocurrió un error al procesar el archivo {pipeline_path}: {e}")
        return []

def extract_service_for_operations(pipeline_path, operations):
    services_for_operations = {}
    print_with_line_number("")
    print_with_line_number("***************************** INICIO EXTRACT SERVICE OPERATIONS*********************************************")
    if pipeline_path.endswith('.pipeline') and os.path.isfile(pipeline_path):
        print_with_line_number(f"pipeline_path: {pipeline_path}")
        with open(pipeline_path, 'r', encoding="utf-8") as f:
            pipeline_content = f.read()
            
            print_with_line_number(pipeline_content)  # Imprime los primeros 500 caracteres
            root = ET.fromstring(pipeline_content)
            namespaces = {'con': 'http://www.bea.com/wli/sb/pipeline/config', 
                          'con1': 'http://www.bea.com/wli/sb/stages/routing/config',
                          'con2': 'http://www.bea.com/wli/sb/stages/config',
                          'con3': 'http://www.bea.com/wli/sb/stages/transform/config',
                          'con4': 'http://www.bea.com/wli/sb/stages/publish/config',                                                          
                          'ref': 'http://www.bea.com/wli/sb/reference',
                          'xsi': 'http://www.w3.org/2001/XMLSchema-instance'} 
                          

            print_with_line_number(f"LEYENDO ROOT: {root}")
            # Parsea el archivo .pipeline
            tree = ET.parse(pipeline_path)
            root = tree.getroot()
            root2 = ET.fromstring(pipeline_content)
            
            flow_elements = root.findall(".//con:flow", namespaces)

            
            for flow_element in flow_elements:
                
                service_elements = flow_element.findall(".//con1:service[@xsi:type='ref:BusinessServiceRef']", namespaces)
                proxy_elements = flow_element.findall(".//con1:service[@xsi:type='ref:ProxyRef']", namespaces)
                
                                                                                          
                for service_element in service_elements:
                                                                          
                    service_ref = service_element.attrib.get('ref', '')
                    
                                                                                         
                    operation_elements = flow_element.findall(".//con1:operation", namespaces)
                    for operation_element in operation_elements:
                        operation_name = operation_element.text.strip()
                        services_for_operations[operation_name] = (service_ref)
                        print_with_line_number("flow_element")
                        print_with_line_number(f"Operation Name: {operation_name}")
                        print_with_line_number("")
                
                for proxy_element in proxy_elements:
                    service_ref = proxy_element.attrib.get('ref', '')
                    operation_elements = flow_element.findall(".//con1:operation", namespaces)
                    for operation_element in operation_elements:
                                                                                                           
                        operation_name = operation_element.text.strip()
                                                                                                                                                  
                        services_for_operations[operation_name] = service_ref
                                                                                
                        print_with_line_number("flow_element")
                        print_with_line_number(f"Operation Name: {operation_name}")
                        print_with_line_number("")
                
            branch_elements = root.findall(".//con:branch", namespaces)
            if branch_elements:
                for branch_element in branch_elements:
                    print_with_line_number("")
                    operation_name = branch_element.attrib.get('name', '')
                    print_with_line_number("")
                    print_with_line_number(f"Operation Name Branch Elements: {operation_name}")
                    if operation_name in operations:
                        service_element = branch_element.find(".//con1:service", namespaces)
  
                        if service_element is not None:
                            service_ref = service_element.attrib.get('ref', '')
                            services_for_operations[operation_name] = service_ref
                            print_with_line_number("branch_elements")
                            print_with_line_number(f"Operation Name: {operation_name}, Service Ref: {service_ref}")
                            print_with_line_number("")
                        else:

                            # Si service_element es None, buscar el elemento <con:request> dentro de branch_element
                            request_element = branch_element.find(".//con:request", namespaces)
                            if request_element is not None:
                                request_value = request_element.text
                                print("El valor del elemento <con:request> dentro de branch_element es:", request_value)
                                
                                
                                # Utilizamos XPath para encontrar los elementos 'con:pipeline' con el atributo 'name' igual a 'request_value'
                                pipelines = root.findall(".//con:pipeline[@name='" + request_value + "']", namespaces)

                                # Imprimimos los elementos encontrados (si los hay)
                                for pipeline in pipelines:
                                    print("Se encontró un pipeline con name igual a '{}':".format(request_value))
                                    #print(ET.tostring(pipeline, encoding='unicode'))
                                    
                                    ns_stage_transform_config   = {'con1': 'http://www.bea.com/wli/sb/stages/transform/config'}
                                    ns_stage_publish_config     = {'con1': 'http://www.bea.com/wli/sb/stages/publish/config'}
                                    ns_stage_routing_config     = {'con1': 'http://www.bea.com/wli/sb/stages/routing/config'}
                                    ns_stage_config             = {'con1':'http://www.bea.com/wli/sb/stages/config'}
                                    
                                    ns_stage_pipeline_config    = {'con': 'http://www.bea.com/wli/sb/pipeline/config',
                                                                'con1': 'http://www.bea.com/wli/sb/stages/routing/config',
                                                                'con2': 'http://www.bea.com/wli/sb/stages/config',
                                                                'con3': 'http://www.bea.com/wli/sb/stages/transform/config',
                                                                'ref': 'http://www.bea.com/wli/sb/reference',
                                                                'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
                                    
                                    ns                           = {'con': 'http://www.example.com',
                                                                    'con4': 'http://www.bea.com/wli/sb/stages/routing/config',
                                                                    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
                                    

                                    ws_callouts = pipeline.findall(".//con1:wsCallout", namespaces=ns_stage_transform_config)
                                    #print_with_line_number(f"ws_callouts: {ws_callouts}")
                                    java_callouts = pipeline.findall(".//con1:javaCallout", namespaces=ns_stage_transform_config)
                                    #print_with_line_number(f"java_callouts: {java_callouts}")
                                    routes = pipeline.findall(".//con1:route", namespaces=ns_stage_publish_config)
                                    #print_with_line_number(f"routes: {routes}")
                                    routes2 = pipeline.findall(".//con1:route", namespaces=ns_stage_routing_config)
                                    #print_with_line_number(f"routes2: {routes2}")
                                    flow_elements = pipeline.findall(".//con:flow", ns_stage_pipeline_config)
                                    print_with_line_number(f"flow_elements: {flow_elements}")
                                    print_with_line_number("")
                                    
                                    for java_callout in java_callouts:
                                        method_element = java_callout.find(".//con1:method", namespaces=ns_stage_transform_config)
                                        if method_element is not None:
                                            method_text = method_element.text
                                            service_element = java_callout.find(".//con1:archive", namespaces=ns_stage_transform_config)
                                            if service_element is not None:
                                                service_ref = service_element.attrib.get('ref', '')
                                                services_for_operations[operation_name] = service_ref
                                                print_with_line_number(f"services_for_operations java_callouts: {services_for_operations}")
                                    
                                    for ws_callout in ws_callouts:
                                        service_element = ws_callout.find(".//con1:service", namespaces=ns_stage_transform_config)
                                        operation_element = ws_callout.find(".//con1:operation", namespaces=ns_stage_transform_config)
                                        if service_element is not None and operation_element is not None:
                                            service_ref = service_element.attrib.get('ref', '')
                                            services_for_operations[operation_name] = service_ref
                                            print_with_line_number(f"services_for_operations ws_callouts: {services_for_operations}")
                                    
                                    
                                    for route in routes:
                                        service_element = route.find(".//con1:service", namespaces=ns_stage_publish_config)
                                        operation_element = route.find(".//con1:operation", namespaces=ns_stage_publish_config)
                                        if service_element is not None and operation_element is not None:
                                            service_ref = service_element.attrib.get('ref', '')
                                            services_for_operations[operation_name] = service_ref
                                            print_with_line_number(f"services_for_operations routes: {services_for_operations}")
                                    
                                    for route in routes2:
                                        service_element = route.find(" .//con1:service", namespaces=ns_stage_routing_config)
                                        operation_element = route.find(" .//con1:operation", namespaces=ns_stage_routing_config)
                                        if service_element is not None and operation_element is not None:
                                            service_ref = service_element.attrib.get('ref', '')
                                            services_for_operations[operation_name] = service_ref
                                            print_with_line_number(f"services_for_operations routes2: {services_for_operations}")
                                            
                                     
                                     # Itera sobre cada elemento <con:flow> encontrado
                                    for flow_element in flow_elements:
                                        # Encuentra todos los elementos <con1:service> dentro de <con:flow>
                                        service_elements = flow_element.findall(".//con1:service[@xsi:type='ref:BusinessServiceRef']", ns_stage_pipeline_config)
                                        
                                        # Si no se encuentra ningún servicio dentro del flujo, salta al siguiente flujo
                                        if not service_elements:
                                            continue
                                        
                                        # Itera sobre cada elemento <con1:service> encontrado dentro de <con:flow>
                                        for service_element in service_elements:
                                            # Accede al atributo 'ref' del elemento <con1:service>
                                            service_ref = service_element.attrib.get('ref', '')

                                            # Encuentra todos los elementos <con1:operation> dentro de <con:flow>
                                            operation_elements = flow_element.findall(".//con1:operation", ns_stage_pipeline_config)


                                            operation_element = operation_elements[0]

                                            # Agrega la relación entre el nombre de la operación y la referencia del servicio al diccionario services_for_operations
                                            services_for_operations[operation_name] = service_ref
                                                    

            
            else:                
                route_elements = root.findall(".//con:route-node", namespaces)
                for route_element in route_elements:
                    operation_element = route_element.find(".//con1:operation", namespaces)
                    if operation_element is not None:
                        operation_name = operation_element.text.strip()  
                        if operation_name in operations:
                            service_element = route_element.find(".//con1:service", namespaces)
                            if service_element is not None:
                                service_ref = service_element.attrib.get('ref', '')
                                
                                # Verificar si la operación ya existe en el diccionario
                                new_operation_name = operation_name
                                version = 2
                                while (new_operation_name in services_for_operations and services_for_operations[new_operation_name] != service_ref):
                                    new_operation_name = f"{operation_name}v{version}"
                                    version += 1  # Incrementa la versión si ya existe

                                # Asignar el service_ref con el nuevo nombre de operación
                                services_for_operations[new_operation_name] = service_ref
                                
                                
                                print_with_line_number("route_elements")
                                print_with_line_number(f"Operation Name: {operation_name}, Service Ref: {service_ref}")
                                print_with_line_number("")
                                 
                # Encuentra todos los elementos <wsCallout> sin importar el prefijo del namespace
                callout_elements = [element for element in root.iter() if element.tag.endswith('wsCallout')]
                
                # Itera sobre cada elemento <wsCallout> encontrado
                for callout_element in callout_elements:
                    operation_name = ""
                    service_ref = ""
                    operation_element = callout_element.find(".//con3:operation", namespaces)
                    if operation_element is not None:
                        operation_name = operation_element.text.strip()
                    service_element = callout_element.find(".//con3:service", namespaces)
                    if service_element is not None:
                        service_ref = service_element.attrib.get('ref', '')
                    if operation_name and service_ref:
                        
                        # Verificar si la operación ya existe en el diccionario
                        new_operation_name = operation_name
                        version = 2
                        while (new_operation_name in services_for_operations and services_for_operations[new_operation_name] != service_ref):
                            new_operation_name = f"{operation_name}v{version}"
                            version += 1  # Incrementa la versión si ya existe

                        # Asignar el service_ref con el nuevo nombre de operación
                        services_for_operations[new_operation_name] = service_ref
                        print_with_line_number("callout_element")
                        print_with_line_number(f"Operation Name: {operation_name}, Service Ref: {service_ref}")
                        print_with_line_number("")
                        
                
                # Encuentro el nombre de la operación y el servicio con un filtro más específico por 'varName'
                validacion_service_node = True
                validacion_assign_node = True
                service_node = root.findall(".//con4:service", namespaces={"con4": "http://www.bea.com/wli/sb/stages/routing/config"})
                if service_node:
                    service_ref = service_node[0].attrib['ref']
                else:
                    validacion_service_node = False
                    print_with_line_number("No se encontró el nodo con la operación")

                # Filtramos por varName="NOMBRE_SERVICIO_TUXEDO" para obtener la expresión correcta
                assign_node = root.findall(".//con1:assign[@varName='NOMBRE_SERVICIO_TUXEDO']", namespaces={"con1": "http://www.bea.com/wli/sb/stages/transform/config"})
                if assign_node:
                    operation_name = assign_node[0].find(".//con2:xqueryText", namespaces={"con2": "http://www.bea.com/wli/sb/stages/config"}).text.strip()
                    operation_name = operation_name.replace(" ", "")
                    operation_name = operation_name.replace("'", "")
                    validacion_assign_node = True
                else:
                    validacion_assign_node = False
                    print_with_line_number("No se encontró el nodo assign con varName='NOMBRE_SERVICIO_TUXEDO'")
                    
                    assign_node = root.findall(".//con1:operation", namespaces={"con1": "http://www.bea.com/wli/sb/stages/routing/config"})
                    if assign_node:
                        operation_name = assign_node[0].text.strip()
                        validacion_assign_node = True
               
                # Asigno al diccionario
                if validacion_service_node and not validacion_assign_node:
                    operation_name = service_ref.split("/")[-1]
                    print_with_line_number(f"Operation Name: {operation_name}, Service Ref: {service_ref}")
                    
                    # Verificar si la operación ya existe en el diccionario
                    new_operation_name = operation_name
                    version = 2
                    while (new_operation_name in services_for_operations and services_for_operations[new_operation_name] != service_ref):
                        new_operation_name = f"{operation_name}v{version}"
                        version += 1  # Incrementa la versión si ya existe

                    # Asignar el service_ref con el nuevo nombre de operación
                    services_for_operations[new_operation_name] = service_ref
                    
                # Asigno al diccionario
                if validacion_service_node and validacion_assign_node:
                    print_with_line_number(f"Operation Name: {operation_name}, Service Ref: {service_ref}")
                    
                    # Verificar si la operación ya existe en el diccionario
                    new_operation_name = operation_name
                    version = 2
                    while (new_operation_name in services_for_operations and services_for_operations[new_operation_name] != service_ref):
                        new_operation_name = f"{operation_name}v{version}"
                        version += 1  # Incrementa la versión si ya existe

                    # Asignar el service_ref con el nuevo nombre de operación
                    services_for_operations[new_operation_name] = service_ref
                                
    print_with_line_number(f"SERVICES FOR: {services_for_operations}")
    print_with_line_number("***************************** FIN EXTRACT SERVICE OPERATIONS*********************************************")
    print_with_line_number("")
    return services_for_operations


def extract_service_for_operations_audibpel(pipeline_path, operations):
    services_for_operations = {}
    seguir = True
    print_with_line_number("")
    print_with_line_number("***************************** INICIO EXTRACT SERVICE OPERATIONS*********************************************")
        
    if pipeline_path.endswith('.pipeline') and os.path.isfile(pipeline_path):
        print_with_line_number(f"pipeline_path: {pipeline_path}")
        with open(pipeline_path, 'r', encoding="utf-8") as f:
            pipeline_content = f.read()
            root = ET.fromstring(pipeline_content)
            namespaces = {'con': 'http://www.bea.com/wli/sb/pipeline/config', 
                          'con1': 'http://www.bea.com/wli/sb/stages/routing/config',
                          'con2': 'http://www.bea.com/wli/sb/stages/config',
                          'con3': 'http://www.bea.com/wli/sb/stages/transform/config',
                          'con4': 'http://www.bea.com/wli/sb/stages/publish/config',
                          'ref': 'http://www.bea.com/wli/sb/reference',
                          'xsi': 'http://www.w3.org/2001/XMLSchema-instance'} 
                          

            print_with_line_number(f"LEYENDO ROOT OPERATIONS AUDIBPEL: {root}")
            # Parsea el archivo .pipeline
            tree = ET.parse(pipeline_path)
            root = tree.getroot()

            branch_elements = root.findall(".//con:branch", namespaces)
            if branch_elements:
                for branch_element in branch_elements:
                    print_with_line_number("")
                    operation_name = branch_element.attrib.get('name', '')
                    print_with_line_number("")
                    print_with_line_number(f"Operation Name Branch Elements: {operation_name}")
                    if operation_name in operations:
                        service_element = branch_element.find(".//con1:service", namespaces)
                        print_with_line_number(f"service_element: {service_element}")
                        
                                    
                        if service_element is not None:                            
                            #Consulta audibpel:
                            print_with_line_number("buscar_definicion_audibpel")
                            nombre_audibpel = buscar_definicion_audibpel(branch_element,operation_name,namespaces,root)
                            print_with_line_number(f"nombre_audibpel: {nombre_audibpel}")
                            
                            service_ref = service_element.attrib.get('ref', '')
                            services_for_operations.setdefault(operation_name, []).append((service_ref, nombre_audibpel))
                            print_with_line_number("branch_elements")
                            print_with_line_number(f"Operation Name: {operation_name}, Service Ref: {service_ref}, nombre_audibpel: {nombre_audibpel}")
                            print_with_line_number("")
                            print_with_line_number(services_for_operations)
                            print_with_line_number("")
                            seguir = False
                            continue
                        else:
                            seguir = True
                            #Consulta audibpel:
                            print_with_line_number("buscar_definicion_audibpel")
                            nombre_audibpel = buscar_definicion_audibpel(branch_element,operation_name,namespaces,root)
                            print_with_line_number(f"nombre_audibpel: {nombre_audibpel}")
                            
                            # Si service_element es None, buscar el elemento <con:request> dentro de branch_element
                            request_element = branch_element.find(".//con:request", namespaces)
                            print_with_line_number(f"request_element: {request_element}")
                            if request_element is not None:
                                request_value = request_element.text
                                print("El valor del elemento <con:request> dentro de branch_element es:", request_value)
                                
                                
                                # Utilizamos XPath para encontrar los elementos 'con:pipeline' con el atributo 'name' igual a 'request_value'
                                pipelines = root.findall(".//con:pipeline[@name='" + request_value + "']", namespaces)

                                # Imprimimos los elementos encontrados (si los hay)
                                for pipeline in pipelines:
                                    print("Se encontró un pipeline con name igual a '{}':".format(request_value))
                                    #print(ET.tostring(pipeline, encoding='unicode'))
                                    
                                    ns_stage_transform_config   = {'con1': 'http://www.bea.com/wli/sb/stages/transform/config'}
                                    ns_stage_publish_config     = {'con1': 'http://www.bea.com/wli/sb/stages/publish/config'}
                                    ns_stage_routing_config     = {'con1': 'http://www.bea.com/wli/sb/stages/routing/config'}
                                    ns_stage_config             = {'con1':'http://www.bea.com/wli/sb/stages/config'}
                                    
                                    ns_stage_pipeline_config    = {'con': 'http://www.bea.com/wli/sb/pipeline/config',
                                                                'con1': 'http://www.bea.com/wli/sb/stages/routing/config',
                                                                'con2': 'http://www.bea.com/wli/sb/stages/config',
                                                                'con3': 'http://www.bea.com/wli/sb/stages/transform/config',
                                                                'ref': 'http://www.bea.com/wli/sb/reference',
                                                                'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
                                    
                                    ns                           = {'con': 'http://www.example.com',
                                                                    'con4': 'http://www.bea.com/wli/sb/stages/routing/config',
                                                                    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
                                    

                                    ws_callouts = pipeline.findall(".//con1:wsCallout", namespaces=ns_stage_transform_config)
                                    #print_with_line_number(f"ws_callouts: {ws_callouts}")
                                    java_callouts = pipeline.findall(".//con1:javaCallout", namespaces=ns_stage_transform_config)
                                    #print_with_line_number(f"java_callouts: {java_callouts}")
                                    routes = pipeline.findall(".//con1:route", namespaces=ns_stage_publish_config)
                                    #print_with_line_number(f"routes: {routes}")
                                    routes2 = pipeline.findall(".//con1:route", namespaces=ns_stage_routing_config)
                                    #print_with_line_number(f"routes2: {routes2}")
                                    flow_elements = pipeline.findall(".//con:flow", ns_stage_pipeline_config)
                                    #print_with_line_number(f"flow_elements: {flow_elements}")
                                    print_with_line_number("")
                                    
                                    for ws_callout in ws_callouts:
                                        service_element = ws_callout.find(".//con1:service", namespaces=ns_stage_transform_config)
                                        operation_element = ws_callout.find(".//con1:operation", namespaces=ns_stage_transform_config)
                                        if service_element is not None and operation_element is not None:
                                            service_ref = service_element.attrib.get('ref', '')
                                            services_for_operations.setdefault(operation_name, []).append((service_ref, nombre_audibpel))
                                            print_with_line_number(f"services_for_operations ws_callouts: {services_for_operations}")
                                            seguir = False
                                            continue
                                    
                                    
                                    for java_callout in java_callouts:
                                        method_element = java_callout.find(".//con1:method", namespaces=ns_stage_transform_config)
                                        if method_element is not None:
                                            method_text = method_element.text
                                            service_element = java_callout.find(".//con1:archive", namespaces=ns_stage_transform_config)
                                            if service_element is not None:
                                                service_ref = service_element.attrib.get('ref', '')
                                                services_for_operations.setdefault(operation_name, []).append((service_ref, nombre_audibpel))
                                                print_with_line_number(f"services_for_operations java_callouts: {services_for_operations}")
                                                seguir = False
                                                continue

                                    for route in routes:
                                        service_element = route.find(".//con1:service", namespaces=ns_stage_publish_config)
                                        operation_element = route.find(".//con1:operation", namespaces=ns_stage_publish_config)
                                        if service_element is not None and operation_element is not None:
                                            service_ref = service_element.attrib.get('ref', '')
                                            services_for_operations.setdefault(operation_name, []).append((service_ref, nombre_audibpel))
                                            print_with_line_number(f"services_for_operations routes: {services_for_operations}")
                                            seguir = False
                                            continue
                                    
                                    for route in routes2:
                                        service_element = route.find(" .//con1:service", namespaces=ns_stage_routing_config)
                                        operation_element = route.find(" .//con1:operation", namespaces=ns_stage_routing_config)
                                        if service_element is not None and operation_element is not None:
                                            service_ref = service_element.attrib.get('ref', '')
                                            services_for_operations.setdefault(operation_name, []).append((service_ref, nombre_audibpel))
                                            print_with_line_number(f"services_for_operations routes2: {services_for_operations}")
                                            seguir = False
                                            continue
                                            
                                     
                                     # Itera sobre cada elemento <con:flow> encontrado
                                    for flow_element in flow_elements:
                                        # Encuentra todos los elementos <con1:service> dentro de <con:flow>
                                        service_elements = flow_element.findall(".//con1:service[@xsi:type='ref:BusinessServiceRef']", ns_stage_pipeline_config)
                                        
                                        # Si no se encuentra ningún servicio dentro del flujo, salta al siguiente flujo
                                        if not service_elements:
                                            seguir = False
                                            continue
                                        
                                        # Itera sobre cada elemento <con1:service> encontrado dentro de <con:flow>
                                        for service_element in service_elements:
                                            # Accede al atributo 'ref' del elemento <con1:service>
                                            service_ref = service_element.attrib.get('ref', '')

                                            # Encuentra todos los elementos <con1:operation> dentro de <con:flow>
                                            operation_elements = flow_element.findall(".//con1:operation", ns_stage_pipeline_config)


                                            operation_element = operation_elements[0]

                                            # Agrega la relación entre el nombre de la operación y la referencia del servicio al diccionario services_for_operations
                                            services_for_operations.setdefault(operation_name, []).append((service_ref, nombre_audibpel))
                                            seguir = False
                                            continue
                                                    
                            print_with_line_number(services_for_operations)
                            print_with_line_number("")




            if seguir:
                flow_elements = root.findall(".//con:flow", namespaces)

                
                for flow_element in flow_elements:
                    
                    service_elements = flow_element.findall(".//con1:service[@xsi:type='ref:BusinessServiceRef']", namespaces)
                    proxy_elements = flow_element.findall(".//con1:service[@xsi:type='ref:ProxyRef']", namespaces)
                    
                    for service_element in service_elements:
                        service_ref = service_element.attrib.get('ref', '')
                        operation_elements = flow_element.findall(".//con1:operation", namespaces)
                        for operation_element in operation_elements:
                            operation_name = operation_element.text.strip()
                            print_with_line_number(f"Operation Name: {operation_name}")
                            print_with_line_number(f"len(operations): {len(operations)}")
                            
                            if len(operations) == 1:
                                operation_name = operations[0]
                                
                            print_with_line_number(f"Operation Name: {operation_name}")
                            
                            if operation_name in operations:
                                #Consulta audibpel:
                                print_with_line_number("buscar_definicion_audibpel")
                                nombre_audibpel = buscar_definicion_audibpel(flow_element,operation_name,namespaces,root)
                                print_with_line_number(f"nombre_audibpel: {nombre_audibpel}")
                                services_for_operations.setdefault(operation_name, []).append((service_ref, nombre_audibpel))
                                print_with_line_number("flow_element")
                                print_with_line_number(f"Operation Name: {operation_name}")
                                print_with_line_number("")
                                seguir = False
                                continue
                    
                    for proxy_element in proxy_elements:
                        service_ref = proxy_element.attrib.get('ref', '')
                        operation_elements = flow_element.findall(".//con1:operation", namespaces)
                        for operation_element in operation_elements:
                            
                            operation_name = operation_element.text.strip()
                            print_with_line_number(f"Operation Name: {operation_name}")
                            print_with_line_number(f"len(operations): {len(operations)}")
                            
                            if len(operations) == 1:
                                operation_name = operations[0]
                                
                            print_with_line_number(f"Operation Name: {operation_name}")
                            
                            if operation_name in operations:
                                #Consulta audibpel:
                                print_with_line_number("buscar_definicion_audibpel")
                                nombre_audibpel = buscar_definicion_audibpel(flow_element,operation_name,namespaces,root)
                                print_with_line_number(f"nombre_audibpel: {nombre_audibpel}")
                                services_for_operations.setdefault(operation_name, []).append((service_ref, nombre_audibpel))
                                print_with_line_number("flow_element")
                                print_with_line_number(f"Operation Name: {operation_name}")
                                print_with_line_number("")
                                seguir = False
                                continue
                            
                
            if seguir:               
                route_elements = root.findall(".//con:route-node", namespaces)
                for route_element in route_elements:
                    operation_element = route_element.find(".//con1:operation", namespaces)
                    if operation_element is not None:
                        operation_name = operation_element.text.strip()  
                        if operation_name in operations:
                            service_element = route_element.find(".//con1:service", namespaces)
                            if service_element is not None:
                                service_ref = service_element.attrib.get('ref', '')
                                services_for_operations.setdefault(operation_name, []).append((service_ref, 'N/A'))
                                print_with_line_number("route_elements")
                                print_with_line_number(f"Operation Name: {operation_name}, Service Ref: {service_ref}")
                                print_with_line_number("")
                                seguir = False
                                continue
                                
                # Encuentra todos los elementos <wsCallout> sin importar el prefijo del namespace
                callout_elements = [element for element in root.iter() if element.tag.endswith('wsCallout')]
                
                # Itera sobre cada elemento <wsCallout> encontrado
                for callout_element in callout_elements:
                    operation_name = ""
                    service_ref = ""
                    operation_element = callout_element.find(".//con3:operation", namespaces)
                    if operation_element is not None:
                        operation_name = operation_element.text.strip()
                    service_element = callout_element.find(".//con3:service", namespaces)
                    if service_element is not None:
                        service_ref = service_element.attrib.get('ref', '')
                    if operation_name and service_ref:
                        services_for_operations.setdefault(operation_name, []).append((service_ref, 'N/A'))
                        print_with_line_number("callout_element")
                        print_with_line_number(f"Operation Name: {operation_name}, Service Ref: {service_ref}")
                        print_with_line_number("")
                        seguir = False
                        continue
                                
    print_with_line_number(f"SERVICES FOR: {services_for_operations}")
    print_with_line_number("***************************** FIN EXTRACT SERVICE OPERATIONS*********************************************")
    print_with_line_number("")
    return services_for_operations

def buscar_definicion_audibpel(branch_element, operation_name, namespaces, root):
    response_element = branch_element.find(".//con:response", namespaces)
    valor_nombre_flujo= operation_name
    if response_element is not None:
        response_value = response_element.text
        print_with_line_number(f"El valor del elemento <con:response> dentro de branch_element es: {response_value}")

        pipelines = root.findall(".//con:pipeline[@name='" + response_value + "']", namespaces)

        for pipeline in pipelines:
            print("Se encontró un pipeline con name igual a '{}':".format(response_value))
            
            service_elements = pipeline.findall(".//con2:xqueryTransform", namespaces)
            print_with_line_number(f"service_elements: {service_elements}")

            for service_element in service_elements:
            
                param_element = service_element.find(".//con2:param[@name='nombreFlujo']", namespaces)
                print_with_line_number(f"param_element: {param_element}")

                if param_element is not None:
                    valor_nombre_flujo = param_element.find("./con2:path", namespaces).text
                    print_with_line_number(valor_nombre_flujo)
                    
                    valor_nombre_flujo = valor_nombre_flujo.replace('"', '')
                    
                    valor_nombre_flujo = valor_nombre_flujo.replace("'", "")
                    
                    valor_nombre_flujo = valor_nombre_flujo.replace(',', '')

                    valor_nombre_flujo = valor_nombre_flujo.replace('fn:concat', '')
                    
                    valor_nombre_flujo = valor_nombre_flujo.replace('concat', '')
                    
                    valor_nombre_flujo = valor_nombre_flujo.replace('data', '')
                    
                    valor_nombre_flujo = valor_nombre_flujo.replace('fn:data', '')
                    
                    valor_nombre_flujo = valor_nombre_flujo.replace('(', '')
                    
                    valor_nombre_flujo = valor_nombre_flujo.replace(')', '')

                    variables_a_reemplazar = ['$operacionExp', '$operacionAbc', '$operacionEXP', '$operacionABC', '$operation']
                    for variable in variables_a_reemplazar:
                        valor_nombre_flujo = valor_nombre_flujo.replace(variable, operation_name)
            
    print_with_line_number(valor_nombre_flujo)
    return valor_nombre_flujo
# Función para autenticar con Google Sheets
def authenticate_google_sheets():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    gc = gspread.authorize(credentials)
    return gc

def write_to_google_sheets(data):
    gc = authenticate_google_sheets()
    workbook = gc.open("BCS_InventarioServicios_Otorgamiento [Kevin]")
    worksheet = workbook.worksheet("Copia de Pruebas")

    # Prepara los datos para la escritura
    rows_to_write = []
    for row_data in data:
        rows_to_write.append(row_data)

    # Escribe en lotes
    batch_size = 1000
    for i in range(0, len(rows_to_write), batch_size):
        batch = rows_to_write[i:i+batch_size]
        try:
            worksheet.append_rows(batch)
            print_with_line_number(f"Se han agregado {len(batch)} filas a la hoja de cálculo.")
        except gspread.exceptions.APIError as e:
            print_with_line_number(f"Error al agregar filas: {e}")
            print_with_line_number("Deteniendo la escritura de datos en Google Sheets.")
            break
        time.sleep(1)

    print_with_line_number("Proceso de escritura de datos en Google Sheets finalizado.")

# Función principal
def main():
    jdeveloper_projects_dir = "C:/Users/ktorres/Desktop/BCS/BUS/Otorgamiento_QA"
    
    services_with_data = extract_osb_services_with_http_provider_id(jdeveloper_projects_dir)
    
    print_with_line_number("DEF MAIN")

    data_for_sheet = []
    
    print_with_line_number(f" COMPLETOOOOOOOOOO: {services_with_data}")
    
    
    data_for_sheet.append(["#", "Nombre Servicio", "Operacion", "Proyecto EXP", "End Point SOAP DEV / Precertificación","Audibpel EXP", "Ruta EBS", "Servicio EBS 1","Servicio EBS 2","Servicio EBS 3","Proxy ABC", "Proyecto ABC", "Nombre Business", "Operacion Business", "Url Business", "Tipo Business"])
    write_to_google_sheets(data_for_sheet)
    data_for_sheet = []
        
    print_with_line_number("____________VALIDACION_________________")
    print_with_line_number("")
    #print_with_line_number(f" REGISTROS: {registros}")
    print_with_line_number("")
    print_with_line_number("")
    print_with_line_number("__________________________________________________________________________")

    services_with_data = [ast.literal_eval(data_str) for data_str in services_with_data]
     
        
    for index,service_name,operacion_abc,project_name,service_url,nombre_flujo_audibpel_exp,ruta_proxy_ebs,proxy_ebs1,proxy_ebs2,proxy_ebs3,proxy_abc,ruta_business,legado_business,business_service,url_business,tipo_business  in services_with_data:
        try:
            index = index
            service_name = service_name
            operacion_abc = operacion_abc
            project_name = project_name
            service_url = service_url
            nombre_flujo_audibpel_exp = nombre_flujo_audibpel_exp                                                     
            ruta_proxy_ebs = ruta_proxy_ebs
            proxy_ebs1 = proxy_ebs1
            proxy_ebs2 = proxy_ebs2
            proxy_ebs3 = proxy_ebs3
            proxy_abc = proxy_abc
            ruta_business = ruta_business
            legado_business = legado_business
            business_service = business_service
            url_business = url_business
            tipo_business = tipo_business
            data_for_sheet.append([index,service_name,operacion_abc,project_name,service_url,nombre_flujo_audibpel_exp,ruta_proxy_ebs,proxy_ebs1,proxy_ebs2,proxy_ebs3,proxy_abc,ruta_business,legado_business,business_service,url_business,tipo_business])
        except Exception as e:
            logging.error(f"Error al procesar datos para la hoja de cálculo: {e}")
            print_with_line_number(f"Error al procesar datos para la hoja de cálculo: {e}")

    
    #Escribir datos en la hoja de Google Sheets
    write_to_google_sheets(data_for_sheet)

    #print_with_line_number("Datos escritos en Google Sheets con éxito.")

if __name__ == "__main__":
    main()
