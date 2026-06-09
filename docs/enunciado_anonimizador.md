# 🔒 Proyecto: Anonimizador de datos personales (PII)

## El caso
Una empresa quiere pasar textos (emails de clientes, tickets, historiales) por una
herramienta de IA en la nube, pero **mandar datos personales a un servidor externo
viola el RGPD**. La solución: un anonimizador que corre **100% en local** y tacha los
datos personales ANTES de que el texto salga de la máquina.

Aquí es donde brilla un modelo pequeño local: **gratis, rápido y privado**.

## Qué vas a construir
Una pequeña web local (Streamlit) donde pegas un texto y te devuelve:
- el texto con los datos personales tachados (`[NOMBRE]`, `[EMAIL]`, `[TELEFONO]`…)
- una tabla con todo lo que se ha detectado
- un botón para descargar el resultado

Todo hablando con **Ollama en local** (`qwen3:4b`). Sin API de pago.

## La idea clave (no te la saltes)
**No** le pidas al modelo que reescriba el texto. Hazlo en dos pasos:
1. **El modelo DETECTA** → devuelve una *lista estructurada* de datos personales
   (tipo + fragmento exacto). Usa `format=` con un modelo Pydantic.
2. **Tu código TACHA** → sustituye cada fragmento por su etiqueta.

¿Por qué así? Porque **garantizas** que el dato desaparece (no dependes de que el
modelo no se deje ninguno al reescribir) y puedes **auditar** qué se quitó.

## Pasos sugeridos
1. Define con Pydantic la salida: una lista de entidades `{tipo, texto}`, donde `tipo`
   es un `Literal[...]` con las categorías (NOMBRE, EMAIL, TELEFONO, DNI, DIRECCION,
   IBAN, TARJETA). El `Literal` evita que el modelo se invente categorías.
2. `detectar(texto)` → llama a Ollama con `format=schema` + un *system prompt* que
   explique la tarea. Devuelve el objeto validado.
3. `anonimizar(texto, deteccion)` → en Python, reemplaza cada `texto` por `[TIPO]`.
4. Móntalo en una web con Streamlit: `text_area` + botón + resultado + tabla.

> Consejo: separa la **lógica** (un archivo) de la **web** (otro). Más limpio y te deja
> probar la lógica sin levantar la web.

## Datos de prueba
Tienes `ejemplo.txt` con varios datos personales mezclados (nombre, email, teléfono,
dirección, DNI, IBAN). Empieza por ahí.

## Antes de empezar
```bash
pip install -r requirements.txt
```
Arrancar la web:  `streamlit run app.py`

## Está "hecho" cuando…
- Pegas el ejemplo y los datos personales salen tachados.
- La tabla muestra qué se detectó y de qué tipo.
- Puedes descargar el texto limpio.