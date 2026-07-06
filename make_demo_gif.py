import asyncio
import io
import subprocess
import time
import sys
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright

OUTPUT_DIR = Path("docs")
OUTPUT_DIR.mkdir(exist_ok=True)

def start_streamlit():
    proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(6)
    return proc

async def capture_gif():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        await page.goto("http://localhost:8501", wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)

        async def shot():
            data = await page.screenshot()
            return Image.open(io.BytesIO(data))

        frames = []

        # 1 — App vacia
        frames.append(await shot())

        texto = (
            "Buenos dias, me llamo Maria Garcia Lopez. "
            "Mi DNI es 12345678A y mi telefono es +34 600 123 456. "
            "Vivo en Calle Mayor 15, 28001 Madrid. "
            "Mi email es maria.garcia@gmail.com "
            "y mi IBAN es ES12 3456 7890 1234 5678 9012."
        )

        # 2-6 — Tipeo del texto en partes
        partes = [
            "Buenos dias, me llamo Maria Garcia Lopez. ",
            "Mi DNI es 12345678A y mi telefono es +34 600 123 456. ",
            "Vivo en Calle Mayor 15, 28001 Madrid. ",
            "Mi email es maria.garcia@gmail.com ",
            "y mi IBAN es ES12 3456 7890 1234 5678 9012.",
        ]
        textarea = page.locator("textarea")
        await textarea.click()
        for parte in partes:
            await textarea.type(parte, delay=12)
            frames.append(await shot())

        # 7 — Pausa breve antes del clic
        await page.wait_for_timeout(600)
        frames.append(await shot())

        # 8 — Click en boton Anonimizar
        await page.locator("button:has-text('Anonimizar')").click()
        await page.wait_for_timeout(300)
        frames.append(await shot())

        # 9 — Esperar a que termine el procesamiento
        # Esperar a que aparezca el texto anonimizado
        resultado = page.locator("text=Texto anonimizado")
        try:
            await resultado.wait_for(state="visible", timeout=180000)
        except:
            pass
        await page.wait_for_timeout(1500)
        frames.append(await shot())

        # 10 — Scroll hasta el final para ver tabla de entidades
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(500)
        frames.append(await shot())

        await browser.close()

        # Mostrar cada frame el tiempo suficiente para verse bien
        durations = [
            2000,   # 1: app vacia
            200,    # 2: typing parte 1
            200,    # 3: typing parte 2
            200,    # 4: typing parte 3
            200,    # 5: typing parte 4
            200,    # 6: typing parte 5
            1000,   # 7: pausa pre-click
            500,    # 8: click
            5000,   # 9: resultado visible
            4000,   # 10: scroll + tabla
        ]
        out_path = OUTPUT_DIR / "demo.gif"
        frames[0].save(
            out_path,
            save_all=True,
            append_images=frames[1:],
            duration=durations,
            loop=0,
            optimize=False,
        )
        print(f"GIF creado: {out_path}")
        return out_path

async def main():
    print("Iniciando Streamlit...")
    proc = start_streamlit()
    try:
        await capture_gif()
    finally:
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    asyncio.run(main())
