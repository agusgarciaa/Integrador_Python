from pathlib import Path

import streamlit as st 
import pandas as pd

import src.operaciones.validaciones as va
import src.operaciones.eliminaciones as e
import src.operaciones.actualizaciones as act


def insertar_nuevo_registro(df, archivo_target, separador):
    """
    Crea un formulario dinámico para ingresar un nuevo registro en el dataset activo, 
    validando los campos y guardando los cambios.
    """
    dataset_nombre = Path(archivo_target).parent.name

    st.subheader(f"Insertar registro en: {dataset_nombre.capitalize()}")

    columnas_clave = ['scientificname', 'eventdate', 'country', 'stateprovince', 'locality', 'recordedby', 'individualcount']
    
    campos_formulario = [col for col in df.columns if col.lower() in columnas_clave]

    if not campos_formulario:
        campos_formulario = df.columns.tolist()[:5]

    with st.form(key="formulario_insercion"):
        st.write("Complete los datos del nuevo registro:")
        
        datos_ingresados = {}
        
        for campo in campos_formulario:
            if df[campo].dtype in ['int64', 'float64']:
                datos_ingresados[campo] = st.number_input(f"{campo}:", min_value=0, value=0)
            else:
                datos_ingresados[campo] = st.text_input(f"{campo}:", value="")
        
        boton_enviar = st.form_submit_button(label="Confirmar Inserción")

    if boton_enviar:
        formulario_valido = True
        for campo, valor in datos_ingresados.items():
            if str(valor).strip() == "":
                st.error(f"El campo '{campo}' no puede estar vacío.")
                formulario_valido = False
    
        if not va.validar(**datos_ingresados):
            st.error("La validación de la estructura o consistencia de datos ha fallado.")
            formulario_valido = False

        if formulario_valido:
            try:
                nuevo_registro_df = pd.DataFrame([datos_ingresados])
                df_actualizado = pd.concat([df, nuevo_registro_df], ignore_index=True)
                df_actualizado.to_csv(archivo_target, sep=separador, index=False, encoding='utf-8')
                
                st.success("¡Registro insertado con éxito en el dataset!")
                st.balloons()
                
            except Exception as un_error:
                st.error(f"Error crítico al insertar el registro: {un_error}")


# Ejercicio 4.B - Agustin Garcia
def buscar_registro(df, nombre_dataset):
    """
    Permite buscar un registro por identificador y mostrarlo.
    El resultado queda guardado en session_state para que 4.C lo use.
    Si se ingresa algo vacío o no válido devuelve None
    """

    IDS = {
        "iadiza":      "gbifID",
        "inaturalist": "id",
        "xenocanto":   "id",
    }

    columna_id = IDS.get(nombre_dataset)
    #print(df.columns.tolist())
    if not columna_id or columna_id not in df.columns:
        st.error("No se encontró columna identificadora para este dataset.")
        return

    st.markdown("#### Buscar registro por identificador")
    valor_id = st.text_input(f"Ingresá el ID (Ubicado en {columna_id}):", key="buscar_id")

    if not valor_id:
        st.session_state.registro_encontrado = None # ---> NO ENCONTRÓ
        return

    coincidencias = df[df[columna_id].astype(str) == valor_id.strip()]

    if coincidencias.empty:
        st.warning(f"No se encontró ningún registro con {columna_id} = '{valor_id}'.")
        st.session_state.registro_encontrado = None # ---> NO EXISTE
        return

    registro = coincidencias.iloc[0]
    indice = coincidencias.index[0]

    # Guardar en session_state para que 4.C lo pueda usar
    st.session_state.registro_encontrado = {"indice": indice, "datos": registro.to_dict()}  # ---> USAR

    st.success("Registro encontrado:")
    st.dataframe(registro.to_frame().T, use_container_width=True, hide_index=True)  # Mostrar el registro encontrado


# Función 4.C - Lucía Cipolla
@st.fragment
def editar_registro ():
    """
        Muestra los valores del registro que encontró buscar_registro y permite editarlos
        registro_dicc = st.session_state.registro_encontrado = {"indice": indice, "datos": registro.to_dict()}
        indice es la fila del registro, datos es el registro en formato diccionario con las key siendo los nombres
        de las columnas y los valores siendo la celda de y fila en x columna.
        El session_state.registro_encontrado se actualiza con los datos nuevos
        Se utiliza la función 5.C para aplicar los cambios (como solicita la consigna)
    """
    if "dataset_actual" not in st.session_state or st.session_state.dataset_actual is None or st.session_state.dataset_actual == "":
        st.warning('Seleccione un dataset para modificar')
        return
    archivos = {'iadiza':'occurrence.txt',
                'inaturalist':'observations.csv',
                'xenocanto':'Occurrence.txt'}
    nombre_dataset = st.session_state.dataset_actual
    separador = "\t" if nombre_dataset.lower() == "iadiza" else "," 
    
    nombre_archivo = archivos.get(nombre_dataset.lower())
    ruta_raw = Path('raw_datasets') / nombre_dataset / nombre_archivo
    ruta_processed = Path('processed_datasets') / nombre_dataset / nombre_archivo
    ruta_operations = Path('logs') / 'operations.log'

    if not ruta_processed.is_file():
        st.warning(f'No se encontró el archivo {nombre_archivo}')
        return

    if (st.session_state.registro_encontrado is None):
        st.markdown(""" :blue-background[Seleccione un registro para modificar]""")
        return
    
    registro_dicc = st.session_state.registro_encontrado
    datos_viejos = registro_dicc['datos']
    identificador = str(datos_viejos.get('id','') or datos_viejos.get('gbifID','') or datos_viejos.get('occurrenceID', '')).strip()
    claves = list(datos_viejos.keys())
    st.subheader('Seleccione campos a editar')
    filtro_registros = st.multiselect(label='Campos',options=claves)

    campo = {}

    if (len(filtro_registros)>0):
        if 'tabla_actualizada' in st.session_state:
            st.dataframe(st.session_state.tabla_actualizada, hide_index=True)
            st.success('El archivo se actualizó correctamente')
            del st.session_state['tabla_actualizada']

        with st.form(key='formulario_modificacion'):
            st.subheader('Editar Registro')

            for celda in filtro_registros:
                val = datos_viejos.get(celda)
                valor_seguro = "" if pd.isna(val) else str(val)
                campo[celda] = st.text_input(label=celda, value=valor_seguro, key=f"input_{celda}_{valor_seguro}")

            boton_enviar = st.form_submit_button(label='Enviar',type='primary')

        if (boton_enviar):
            try:
                act.actualizar_multiples_campos(ruta_raw,ruta_processed,ruta_operations,separador,identificador,campo)
                for dato, n_valor in campo.items():
                    registro_dicc['datos'][dato] = n_valor
                st.session_state.registro_encontrado = registro_dicc    # ---> MODIFICADO
                st.cache_data.clear()
                st.session_state.tabla_actualizada = pd.DataFrame([campo])
                for clave_id in ['id', 'gbifID', 'occurrenceID']:
                    if clave_id in campo:
                        st.session_state['buscar_id'] = campo[clave_id]
                st.rerun()
            except Exception as e:
                st.error(f'Error al actualizar {e}')


# Función 4.D - Sofia Martins
def modalidades_eliminacion(ruta_raw, ruta_processed, ruta_operations, delimiter, df): 
    df_vistaprevia = pd.DataFrame()
    
    st.subheader("Seccion para eliminacion de registros")
    modalidad = st.selectbox(
        "Selecione la modalidad de eliminacion",
        ["por identificador unico", "por valor de una columna", "por condicion sobre una columna"]
    )
    
    if modalidad == "por identificador unico":
        id_unico = st.text_input("ingrese el identificador del registro a eliminar")
        
        if id_unico:
            posibles_id = df.filter(items=["id", "gbifID", "ocurrenceID"])
            filtro = (posibles_id.astype(str) == id_unico).any(axis=1)
            df_vistaprevia = df[filtro]
            
    if modalidad == "por valor de una columna":
        columna = st.selectbox("seleccione la columna donde desea eliminar registros", df.columns)
        valores = st.text_input("ingresa los valores a eliminar separados por comas")
        
        if valores: 
            lista = valores.split(",")
            df_vistaprevia = df[df[columna].astype(str).isin(lista)]
            
    if modalidad == "por condicion sobre una columna":
        columna = st.selectbox("seleccione la columna donde desea eliminar registros", df.columns)
        valor = st.text_input("ingresa el valor a comparar")
        condicion = st.selectbox("seleccione la condicion de eliminacion", ["==", ">", "<", ">=", "<=", "!="])
        
        if valor:
            try:
                valor_num = float(valor)
                numero = pd.to_numeric(df[columna], errors='coerce')
                
                if condicion == "==": 
                    df_vistaprevia = df[numero == valor_num]
                elif condicion == ">": 
                    df_vistaprevia = df[numero > valor_num]
                elif condicion == "<": 
                    df_vistaprevia = df[numero < valor_num]
                elif condicion == ">=": 
                    df_vistaprevia = df[numero >= valor_num]
                elif condicion == "<=": 
                    df_vistaprevia = df[numero <= valor_num]
                elif condicion == "!=": 
                    df_vistaprevia = df[numero != valor_num]
                
            except ValueError:
                if condicion == "==": 
                    df_vistaprevia = df[df[columna].astype(str) == valor]
                elif condicion == "!=": 
                    df_vistaprevia = df[df[columna].astype(str) != valor]
                else: 
                    st.error("condicion no valida para valores no numericos")

    if not df_vistaprevia.empty:
        st.subheader("vista previa de los registros que seran eliminados")
        st.dataframe(df_vistaprevia)
        
        if st.button("confirmar la eliminacion"):
            if modalidad == "por identificador unico":
                e.eliminar_por_identificador(ruta_raw, ruta_processed, ruta_operations, id_unico)
                
            elif modalidad == "por valor de una columna":
                e.eliminar_registros_por_valor(ruta_raw, ruta_processed, ruta_operations, columna, lista, delimiter)
                
            elif modalidad == "por condicion sobre una columna":
                e.eliminar_por_condicion(ruta_raw, ruta_processed, ruta_operations, columna, condicion, valor, delimiter)
                
            st.success("se eliminaron los registros")
            st.rerun()