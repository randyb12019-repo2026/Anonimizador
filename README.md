# 🔒 Anonimizador Local de Datos Personales (PII)

## Descripción

Este proyecto implementa una solución de anonimización de datos personales utilizando Inteligencia Artificial ejecutada completamente en local mediante Ollama y el modelo Qwen3:4B.

Su objetivo es identificar y proteger información sensible contenida en textos como correos electrónicos, tickets de soporte, formularios o documentación interna antes de que estos sean procesados por sistemas externos.

La aplicación detecta automáticamente datos personales y los sustituye por etiquetas estandarizadas, permitiendo preservar la privacidad de la información y reducir riesgos asociados al tratamiento de datos sensibles.

## Problema que resuelve

Cada vez más organizaciones utilizan herramientas de Inteligencia Artificial para analizar y procesar información textual. Sin embargo, muchos de esos documentos contienen datos personales cuya exposición puede suponer riesgos de privacidad o incumplimientos normativos.

Este proyecto aborda ese problema mediante una capa de anonimización previa que permite eliminar información sensible antes de utilizar servicios de IA o compartir documentos con terceros.

## Características principales

* Ejecución 100% local mediante Ollama.
* Sin dependencias de APIs externas de pago.
* Detección automática de información personal.
* Sustitución de datos sensibles por etiquetas normalizadas.
* Interfaz web desarrollada con Streamlit.
* Visualización de entidades detectadas.
* Descarga del texto anonimizado.
* Salidas estructuradas validadas mediante Pydantic.

## Datos detectados

Actualmente la aplicación es capaz de identificar:

* Nombres y apellidos
* Correos electrónicos
* Números de teléfono
* DNI
* Direcciones
* IBAN
* Tarjetas bancarias

Los datos detectados son reemplazados por etiquetas como:

```text
[NOMBRE]
[EMAIL]
[TELEFONO]
[DNI]
[DIRECCION]
[IBAN]
[TARJETA]
```

## Arquitectura de la solución

La aplicación sigue un enfoque de dos etapas:

### 1. Detección

El modelo de lenguaje identifica entidades sensibles presentes en el texto y devuelve una respuesta estructurada.

### 2. Anonimización

La lógica desarrollada en Python sustituye cada entidad detectada por una etiqueta correspondiente.

Este enfoque permite:

* Mayor control sobre el proceso.
* Resultados reproducibles.
* Facilidad de auditoría.
* Menor riesgo de que información sensible permanezca en el texto final.

## Tecnologías utilizadas

* Python
* Streamlit
* Ollama
* Qwen3:4B
* Pydantic
* Pandas

## Estructura del proyecto

```text
.
├── app.py
├── anonimizador.py
├── ejemplo.txt
├── enunciado_anonimizador.md
├── requirements.txt
└── README.md
```

## Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd <nombre-del-repositorio>
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Descargar el modelo

```bash
ollama pull qwen3:4b
```

### 4. Ejecutar la aplicación

```bash
streamlit run app.py
```

## Ejemplo de funcionamiento

### Texto original

```text
Mi nombre es Juan Pérez.
Mi correo es juan.perez@gmail.com.
Mi teléfono es 612345678.
```

### Texto anonimizado

```text
Mi nombre es [NOMBRE].
Mi correo es [EMAIL].
Mi teléfono es [TELEFONO].
```

## Posibles mejoras futuras

* Soporte para documentos PDF y Word.
* Procesamiento masivo de archivos.
* Exportación de informes de anonimización.
* Detección multilingüe.
* Incorporación de métricas de confianza.
* Integración con flujos empresariales de tratamiento documental.

## Autor

Proyecto desarrollado como parte de un portfolio de proyectos de Inteligencia Artificial y Procesamiento de Lenguaje Natural (NLP), enfocado en privacidad, protección de datos y uso de modelos de lenguaje ejecutados localmente.
