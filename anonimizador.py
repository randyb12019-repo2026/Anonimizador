import importlib
import json
import subprocess
from dataclasses import dataclass
from typing import Literal

try:
    pydantic = importlib.import_module("pydantic")
    BaseModel = pydantic.BaseModel
    Field = pydantic.Field
    _HAS_PYDANTIC = True
except ImportError:
    _HAS_PYDANTIC = False

    def Field(*args, **kwargs):
        return None

    class BaseModel:
        pass


FALLBACK_SCHEMA = {
    "type": "object",
    "properties": {
        "entidades": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "tipo": {
                        "type": "string",
                        "enum": ["NOMBRE", "EMAIL", "TELEFONO", "DNI", "DIRECCION", "IBAN", "TARJETA"],
                    },
                    "texto": {"type": "string"},
                },
                "required": ["tipo", "texto"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["entidades"],
    "additionalProperties": False,
}

try:
    ollama = importlib.import_module("ollama")
    chat = ollama.chat
except (ImportError, ModuleNotFoundError):
    def chat(*, model, messages, format, options=None):
        payload = {
            "model": model,
            "messages": messages,
            "format": format,
            "options": options or {},
        }
        proc = subprocess.run(
            ["ollama", "chat", model, "--json"],
            input=json.dumps(payload).encode("utf-8"),
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(proc.stdout)


if _HAS_PYDANTIC:
    class EntidadPII(BaseModel):
        tipo: Literal["NOMBRE", "EMAIL", "TELEFONO", "DNI", "DIRECCION", "IBAN", "TARJETA"]
        texto: str = Field(description="Fragmento exacto detectado en el texto original")


    class DeteccionPII(BaseModel):
        entidades: list[EntidadPII]
else:
    @dataclass
    class EntidadPII:
        tipo: Literal["NOMBRE", "EMAIL", "TELEFONO", "DNI", "DIRECCION", "IBAN", "TARJETA"]
        texto: str


    @dataclass
    class DeteccionPII:
        entidades: list[EntidadPII]

        @classmethod
        def model_json_schema(cls):
            return FALLBACK_SCHEMA

        @classmethod
        def model_validate(cls, data):
            entidades = [
                EntidadPII(tipo=entidad["tipo"], texto=entidad["texto"])
                for entidad in data.get("entidades", [])
            ]
            return DeteccionPII(entidades=entidades)


SYSTEM_PROMPT = """
Eres un detector de datos personales en español.
Tu tarea es detectar PII en el texto del usuario.

Devuelve SOLO entidades que aparezcan literalmente en el texto.
No inventes datos.
No reescribas el texto.
No expliques nada.

Categorías válidas:
NOMBRE, EMAIL, TELEFONO, DNI, DIRECCION, IBAN, TARJETA.
"""


def detectar(texto: str) -> DeteccionPII:
    schema = DeteccionPII.model_json_schema()

    response = chat(
        model="qwen3:4b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": texto},
        ],
        format=schema,
        options={"temperature": 0},
    )

    contenido = response["message"]["content"]
    data = json.loads(contenido)

    return DeteccionPII.model_validate(data)


def anonimizar(texto: str, deteccion: DeteccionPII) -> str:
    texto_limpio = texto

    entidades_ordenadas = sorted(
        deteccion.entidades,
        key=lambda e: len(e.texto),
        reverse=True
    )

    for entidad in entidades_ordenadas:
        texto_limpio = texto_limpio.replace(entidad.texto, f"[{entidad.tipo}]")

    return texto_limpio