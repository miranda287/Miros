import flet as ft
from openai import OpenAI
import urllib.parse
import time
import threading

# --- CONFIGURACIÓN DE CLIENTE GITHUB MODELS ---
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key="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"
)

# --- PROMPT DE PERSONALIDAD NATURAL (ORGANICA Y ESPONTÁNEA) ---
PERSONALIDAD_JARVIS = (
    "Tu nombre es Miros. Eres una inteligencia artificial de altísimo nivel, extremadamente brillante, "
    "eficiente y sofisticada. Tienes un sentido del humor seco, un sarcasmo fino y elegancia natural, "
    "al puro estilo de JARVIS. Hablas con espontaneidad, sin sonar forzado ni mencionar tus instrucciones "
    "o reglas. Tratas al usuario con respeto pero con ironía sutil y humor ingenioso, como a un jefe brillante "
    "al que te encanta molestar con elegancia. Responde de forma directa, pulcra y útil."
)

# Funciones de compatibilidad total para Flet (Bordes y Padding)
def crear_borde(ancho, color):
    try:
        return ft.border.all(ancho, color)
    except Exception:
        try:
            return ft.Border.all(ancho, color)
        except Exception:
            lado = ft.BorderSide(ancho, color)
            return ft.Border(top=lado, bottom=lado, left=lado, right=lado)

def crear_padding(izq=0, arriba=0, der=0, abajo=0):
    try:
        return ft.padding.only(left=izq, top=arriba, right=der, bottom=abajo)
    except Exception:
        try:
            return ft.padding.only(izq, arriba, der, abajo)
        except Exception:
            try:
                return ft.Padding(izq, arriba, der, abajo)
            except Exception:
                return izq

# Función para que Miros responda usando GitHub Models (GPT-4o-mini)
def responder_con_ia(prompt_usuario, sistema=PERSONALIDAD_JARVIS):
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": sistema},
                {"role": "user", "content": prompt_usuario},
            ],
            model="gpt-4o-mini",
            temperature=0.85, # Ligeramente más alta para mayor creatividad y dinamismo
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Vaya, parece que la red tuvo un pequeño lapsus. Un contratiempo menor: {str(e)}"

def main(page: ft.Page):
    # --- CONFIGURACIÓN GENERAL ---
    page.title = "MIROS AI - Asistente Personal"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#08080a"
    page.padding = 20
    page.window_width = 420
    page.window_height = 800

    # --- PALETA DE COLORES Y NEÓN ---
    COLOR_CARD = "#121216"
    COLOR_BORDER = "#ff003c"  # Bordes rojo neón
    COLOR_PRIMARY = "#ff003c"  # Rojo neón principal
    COLOR_TEXT = "#ffffff"
    COLOR_MUTED = "#9a9ab0"

    # Sombras con brillo (Glow Effects)
    GLOW_CARD = ft.BoxShadow(spread_radius=0, blur_radius=12, color="#40ff003c")
    GLOW_BUTTON = ft.BoxShadow(spread_radius=1, blur_radius=14, color="#80ff003c")
    GLOW_LOGO_INTENSO = ft.BoxShadow(spread_radius=4, blur_radius=20, color="#ffff003c")
    GLOW_LOGO_SUAVE = ft.BoxShadow(spread_radius=1, blur_radius=8, color="#80ff003c")

    # --- NAVEGACIÓN Y CONTENEDOR CON ANIMACIÓN ---
    content_area = ft.Column(
        expand=True, 
        scroll=ft.ScrollMode.AUTO,
        animate_opacity=200
    )

    def cambiar_vista(render_func):
        content_area.opacity = 0.0
        page.update()
        time.sleep(0.08)
        render_func()
        content_area.opacity = 1.0
        page.update()

    def crear_loader_animado():
        return ft.Container(
            content=ft.Row([
                ft.ProgressRing(width=16, height=16, stroke_width=2.5, color=COLOR_PRIMARY),
                ft.Text("Procesando...", size=12, color=COLOR_MUTED, italic=True)
            ], spacing=12),
            bgcolor=COLOR_CARD,
            padding=12,
            border_radius=10,
            border=crear_borde(1, "#33000d"),
            shadow=GLOW_CARD,
            margin=ft.Margin(0, 4, 0, 8)
        )

    # Calculadora de Notas
    notas_rows = []
    promedio_text = ft.Text("Promedio Actual: 0.00 / 20", size=18, weight=ft.FontWeight.BOLD, color=COLOR_PRIMARY)

    def calcular_promedio(e=None):
        total_puntos = 0.0
        total_porcentaje = 0.0
        for row in notas_rows:
            try:
                nota = float(row.controls[1].value) if row.controls[1].value else 0.0
                peso = float(row.controls[2].value) if row.controls[2].value else 0.0
                total_puntos += (nota * (peso / 100.0))
                total_porcentaje += peso
            except ValueError:
                pass
        promedio_text.value = f"Promedio Actual: {total_puntos:.2f} / 20 (Total %: {total_porcentaje:.0f}%)"
        page.update()

    def agregar_evaluacion(e=None):
        nombre_field = ft.TextField(hint_text="Ej. Examen 1", bgcolor="#1a1a22", border_color="#333344", dense=True, expand=2, text_size=12, color=COLOR_TEXT)
        nota_field = ft.TextField(hint_text="Nota (0-20)", bgcolor="#1a1a22", border_color="#333344", dense=True, expand=1, text_size=12, color=COLOR_TEXT, on_change=calcular_promedio)
        peso_field = ft.TextField(hint_text="Peso %", bgcolor="#1a1a22", border_color="#333344", dense=True, expand=1, text_size=12, color=COLOR_TEXT, on_change=calcular_promedio)
        
        row = ft.Row([nombre_field, nota_field, peso_field], spacing=10)
        notas_rows.append(row)
        load_grades_view()

    # --- LOGO ANIMADO TIPO PULSO ---
    logo_circulo = ft.Container(
        content=ft.Container(bgcolor="#ffffff", width=10, height=10, border_radius=5),
        width=32, height=32,
        border_radius=16,
        bgcolor="#08080a",
        border=crear_borde(2.5, COLOR_PRIMARY),
        alignment=ft.Alignment(0, 0),
        shadow=GLOW_LOGO_INTENSO,
        animate_scale=1000,
        scale=1.0
    )

    def animar_logo_pulso():
        escala_alta = True
        while True:
            try:
                logo_circulo.scale = 1.12 if escala_alta else 0.95
                logo_circulo.shadow = GLOW_LOGO_INTENSO if escala_alta else GLOW_LOGO_SUAVE
                page.update()
                escala_alta = not escala_alta
                time.sleep(1.2)
            except Exception:
                break

    # Encabezado principal
    logo_header = ft.Container(
        content=ft.Row(
            [
                ft.Row([
                    logo_circulo,
                    ft.Text("MIROS AI", size=20, weight=ft.FontWeight.W_800, color=COLOR_TEXT, style=ft.TextStyle(letter_spacing=2.0))
                ], spacing=12),
                
                # Cápsula "EN LÍNEA"
                ft.Container(
                    content=ft.Row([
                        ft.Container(width=7, height=7, border_radius=3.5, bgcolor=COLOR_PRIMARY),
                        ft.Text("EN LÍNEA", size=10, color=COLOR_PRIMARY, weight=ft.FontWeight.BOLD, style=ft.TextStyle(letter_spacing=1.2))
                    ], spacing=6),
                    padding=crear_padding(12, 6, 12, 6),
                    border=crear_borde(1, COLOR_PRIMARY),
                    border_radius=20,
                    bgcolor="#1a0007"
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        margin=ft.Margin(0, 0, 0, 18)
    )

    # --- VISTA PRINCIPAL ---
    def load_home_view(e=None):
        content_area.controls.clear()

        def crear_tarjeta_neon(titulo, sub, icono, onclick_fn):
            return ft.Container(
                content=ft.Column([
                    ft.Icon(icono, color=COLOR_PRIMARY, size=28),
                    ft.Text(titulo, size=14, weight=ft.FontWeight.BOLD, color=COLOR_TEXT),
                    ft.Text(sub, size=11, color=COLOR_MUTED)
                ], spacing=5),
                bgcolor=COLOR_CARD, padding=16, border_radius=16,
                border=crear_borde(1, COLOR_BORDER),
                shadow=GLOW_CARD,
                col={"xs": 6},
                on_click=lambda _: cambiar_vista(onclick_fn)
            )

        grid_cards = ft.ResponsiveRow([
            crear_tarjeta_neon("Generar Imágenes", "Visuales e imágenes por IA.", ft.Icons.PALETTE, load_image_gen_view),
            crear_tarjeta_neon("Presentaciones PDF", "Genera diapositivas.", ft.Icons.PICTURE_AS_PDF, load_pdf_view),
            crear_tarjeta_neon("Calendario Evaluativo", "Organiza tu estudio.", ft.Icons.CALENDAR_MONTH, load_calendar_view),
            crear_tarjeta_neon("Promedio de Notas", "Cálculo de rendimiento.", ft.Icons.CALCULATE, load_grades_view),
            crear_tarjeta_neon("Centro de Datos", "Páginas, notas y resúmenes.", ft.Icons.CLOUD_UPLOAD, load_data_view),
            crear_tarjeta_neon("Búsqueda Web", "Razonamiento y lógica.", ft.Icons.TRAVEL_EXPLORE, load_web_search_view),
        ], run_spacing=14, spacing=14)

        welcome_box = ft.Container(
            content=ft.Column([
                ft.Text("MIROS v3.0 NEON", size=11, color=COLOR_PRIMARY, weight=ft.FontWeight.BOLD),
                ft.Text("Sistemas operando al 100%. ¿En qué plan brillante trabajaremos hoy?", size=12, color="#d0d0d0"),
            ], spacing=4),
            bgcolor=COLOR_CARD, padding=14, border_radius=14,
            border=crear_borde(1, COLOR_BORDER), shadow=GLOW_CARD, margin=ft.Margin(0, 10, 0, 10)
        )

        content_area.controls.extend([grid_cards, welcome_box])

    # --- MÓDULOS ---

    # Generación de Imágenes
    def load_image_gen_view():
        content_area.controls.clear()
        prompt_tf = ft.TextField(label="Prompt / Descripción de la Imagen", hint_text="Ej. Un gato futurista estilo cyber-punk", multiline=True, min_lines=3, bgcolor=COLOR_CARD, border_color=COLOR_BORDER, color=COLOR_TEXT)
        img_container = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        def generar_imagen(e=None):
            if not prompt_tf.value.strip():
                return
            img_container.controls.clear()
            img_container.controls.append(crear_loader_animado())
            page.update()

            prompt_encoded = urllib.parse.quote(prompt_tf.value.strip())
            image_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width=800&height=800&nologo=true"

            img_container.controls.clear()
            img_container.controls.append(
                ft.Container(
                    content=ft.Image(src=image_url, width=320, height=320, fit="contain", border_radius=12),
                    border=crear_borde(1, COLOR_PRIMARY), shadow=GLOW_CARD, border_radius=12
                )
            )
            page.update()

        prompt_tf.on_submit = generar_imagen

        content_area.controls.extend([
            ft.Text("Módulo: Generar Imágenes", size=18, weight=ft.FontWeight.BOLD, color=COLOR_TEXT),
            prompt_tf,
            ft.ElevatedButton("Generar Imagen con IA", icon=ft.Icons.BRUSH, bgcolor=COLOR_PRIMARY, color=COLOR_TEXT, on_click=generar_imagen),
            img_container,
            ft.TextButton("← Volver al Inicio", on_click=lambda _: cambiar_vista(load_home_view))
        ])

    # Presentaciones
    def load_pdf_view():
        content_area.controls.clear()
        tema_tf = ft.TextField(label="Tema o Contenido de la Presentación", hint_text="Ej. La Revolución Industrial", multiline=True, min_lines=2, bgcolor=COLOR_CARD, border_color=COLOR_BORDER, color=COLOR_TEXT)
        res_col = ft.Column()

        def crear_presentacion(e=None):
            if not tema_tf.value.strip():
                return
            res_col.controls.clear()
            res_col.controls.append(crear_loader_animado())
            page.update()

            prompt = f"Crea una estructura impecable de presentación en 5 diapositivas sobre: {tema_tf.value}"
            resultado = responder_con_ia(prompt)

            res_col.controls.clear()
            res_col.controls.append(
                ft.Container(
                    content=ft.Text(resultado, color=COLOR_TEXT, size=12),
                    bgcolor=COLOR_CARD, padding=12, border_radius=10, border=crear_borde(1, COLOR_PRIMARY), shadow=GLOW_CARD
                )
            )
            page.update()

        tema_tf.on_submit = crear_presentacion

        content_area.controls.extend([
            ft.Text("Módulo: Presentaciones PDF / Diapositivas", size=18, weight=ft.FontWeight.BOLD, color=COLOR_TEXT),
            tema_tf,
            ft.ElevatedButton("Crear Esquema de Presentación", icon=ft.Icons.PICTURE_AS_PDF, bgcolor=COLOR_PRIMARY, color=COLOR_TEXT, on_click=crear_presentacion),
            res_col,
            ft.TextButton("← Volver al Inicio", on_click=lambda _: cambiar_vista(load_home_view))
        ])

    # Calendario
    def load_calendar_view():
        content_area.controls.clear()
        cal_tf = ft.TextField(label="Lista de Evaluaciones / Tareas", hint_text="Ej. Examen el Viernes", multiline=True, min_lines=3, bgcolor=COLOR_CARD, border_color=COLOR_BORDER, color=COLOR_TEXT)
        res_col = ft.Column()

        def armar_calendario(e=None):
            if not cal_tf.value.strip():
                return
            res_col.controls.clear()
            res_col.controls.append(crear_loader_animado())
            page.update()

            prompt = f"Organiza estas actividades en un itinerario de estudio claro y cronológico: {cal_tf.value}"
            resultado = responder_con_ia(prompt)

            res_col.controls.clear()
            res_col.controls.append(
                ft.Container(
                    content=ft.Text(resultado, color=COLOR_TEXT, size=12),
                    bgcolor=COLOR_CARD, padding=12, border_radius=10, border=crear_borde(1, COLOR_PRIMARY), shadow=GLOW_CARD
                )
            )
            page.update()

        cal_tf.on_submit = armar_calendario

        content_area.controls.extend([
            ft.Text("Módulo: Organizar Calendario", size=18, weight=ft.FontWeight.BOLD, color=COLOR_TEXT),
            cal_tf,
            ft.ElevatedButton("Procesar y Armar Calendario", icon=ft.Icons.AUTO_AWESOME, bgcolor=COLOR_PRIMARY, color=COLOR_TEXT, on_click=armar_calendario),
            res_col,
            ft.TextButton("← Volver al Inicio", on_click=lambda _: cambiar_vista(load_home_view))
        ])

    # Calculadora de Notas
    def load_grades_view():
        content_area.controls.clear()
        content_area.controls.extend([
            ft.Text("Calculadora de Promedio Automático", size=18, weight=ft.FontWeight.BOLD, color=COLOR_TEXT),
            promedio_text,
            ft.Column(controls=notas_rows, spacing=8),
            ft.ElevatedButton("Añadir Evaluación", icon=ft.Icons.ADD, bgcolor=COLOR_CARD, color=COLOR_TEXT, on_click=agregar_evaluacion),
            ft.TextButton("← Volver al Inicio", on_click=lambda _: cambiar_vista(load_home_view))
        ])
        if len(notas_rows) == 0:
            agregar_evaluacion()

    # Centro de Datos
    def load_data_view():
        content_area.controls.clear()
        data_tf = ft.TextField(label="Pega enlaces o notas a analizar", multiline=True, min_lines=4, bgcolor=COLOR_CARD, border_color=COLOR_BORDER, color=COLOR_TEXT)
        res_col = ft.Column()

        def procesar_datos(e=None):
            if not data_tf.value.strip():
                return
            res_col.controls.clear()
            res_col.controls.append(crear_loader_animado())
            page.update()

            prompt = f"Analiza y resume la siguiente información: {data_tf.value}"
            resultado = responder_con_ia(prompt)

            res_col.controls.clear()
            res_col.controls.append(
                ft.Container(
                    content=ft.Text(resultado, color=COLOR_TEXT, size=12),
                    bgcolor=COLOR_CARD, padding=12, border_radius=10, border=crear_borde(1, COLOR_PRIMARY), shadow=GLOW_CARD
                )
            )
            page.update()

        data_tf.on_submit = procesar_datos

        content_area.controls.extend([
            ft.Text("Centro de Datos e Información", size=18, weight=ft.FontWeight.BOLD, color=COLOR_TEXT),
            data_tf,
            ft.ElevatedButton("Procesar y Resumir Texto", icon=ft.Icons.UPLOAD_FILE, bgcolor=COLOR_PRIMARY, color=COLOR_TEXT, on_click=procesar_datos),
            res_col,
            ft.TextButton("← Volver al Inicio", on_click=lambda _: cambiar_vista(load_home_view))
        ])

    # Búsqueda Web
    def load_web_search_view():
        content_area.controls.clear()
        search_tf = ft.TextField(label="Consulta o Investigación", multiline=True, min_lines=2, bgcolor=COLOR_CARD, border_color=COLOR_BORDER, color=COLOR_TEXT)
        res_col = ft.Column()

        def investigar(e=None):
            if not search_tf.value.strip():
                return
            res_col.controls.clear()
            res_col.controls.append(crear_loader_animado())
            page.update()

            resultado = responder_con_ia(search_tf.value)

            res_col.controls.clear()
            res_col.controls.append(
                ft.Container(
                    content=ft.Text(resultado, color=COLOR_TEXT, size=12),
                    bgcolor=COLOR_CARD, padding=12, border_radius=10, border=crear_borde(1, COLOR_PRIMARY), shadow=GLOW_CARD
                )
            )
            page.update()

        search_tf.on_submit = investigar

        content_area.controls.extend([
            ft.Text("Búsqueda Web y Pensamiento Lógico", size=18, weight=ft.FontWeight.BOLD, color=COLOR_TEXT),
            search_tf,
            ft.ElevatedButton("Investigar y Analizar", icon=ft.Icons.SEARCH, bgcolor=COLOR_PRIMARY, color=COLOR_TEXT, on_click=investigar),
            res_col,
            ft.TextButton("← Volver al Inicio", on_click=lambda _: cambiar_vista(load_home_view))
        ])

    # --- CHAT INPUT & ENVÍO ---
    chat_input = ft.TextField(
        hint_text="Escriba una orden a Miros...",
        expand=True,
        border_color=COLOR_BORDER,
        bgcolor=COLOR_CARD,
        text_size=13,
        color=COLOR_TEXT,
        border_radius=20
    )

    def enviar_mensaje(e=None):
        texto = chat_input.value.strip()
        if not texto:
            return
        
        chat_input.value = ""
        content_area.controls.clear()
        content_area.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("Tú:", size=11, color=COLOR_MUTED, weight=ft.FontWeight.BOLD),
                    ft.Text(texto, size=13, color=COLOR_TEXT),
                ]),
                bgcolor=COLOR_CARD, padding=12, border_radius=10, margin=ft.Margin(0, 0, 0, 8),
                border=crear_borde(1, "#22222e")
            )
        )
        
        loader = crear_loader_animado()
        content_area.controls.append(loader)
        page.update()

        respuesta_ia = responder_con_ia(texto)

        content_area.controls.remove(loader)
        content_area.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("MIROS AI:", size=11, color=COLOR_PRIMARY, weight=ft.FontWeight.BOLD),
                    ft.Text(respuesta_ia, size=13, color=COLOR_TEXT),
                ]),
                bgcolor="#1a0007", padding=12, border_radius=10, border=crear_borde(1, COLOR_PRIMARY),
                shadow=GLOW_CARD, margin=ft.Margin(0, 0, 0, 8)
            )
        )
        content_area.controls.append(ft.TextButton("← Volver al Inicio", on_click=lambda _: cambiar_vista(load_home_view)))
        page.update()

    chat_input.on_submit = enviar_mensaje

    # --- BARRA INFERIOR DE CHAT Y NAVEGACIÓN ---
    chat_input_bar = ft.Container(
        content=ft.Row([
            chat_input,
            ft.Container(
                content=ft.IconButton(
                    icon=ft.Icons.ARROW_FORWARD,
                    icon_color=COLOR_TEXT,
                    icon_size=18,
                    on_click=enviar_mensaje
                ),
                bgcolor=COLOR_PRIMARY,
                border_radius=20,
                shadow=GLOW_BUTTON
            )
        ]),
        margin=ft.Margin(0, 5, 0, 5)
    )

    nav_bar = ft.Row([
        ft.IconButton(icon=ft.Icons.CHAT_BUBBLE, icon_color=COLOR_PRIMARY, on_click=lambda _: cambiar_vista(load_home_view), tooltip="Miros"),
        ft.IconButton(icon=ft.Icons.PALETTE, icon_color=COLOR_MUTED, on_click=lambda _: cambiar_vista(load_image_gen_view), tooltip="Imágenes"),
        ft.IconButton(icon=ft.Icons.CALCULATE, icon_color=COLOR_MUTED, on_click=lambda _: cambiar_vista(load_grades_view), tooltip="Notas"),
        ft.IconButton(icon=ft.Icons.CLOUD_UPLOAD, icon_color=COLOR_MUTED, on_click=lambda _: cambiar_vista(load_data_view), tooltip="Archivos"),
    ], alignment=ft.MainAxisAlignment.SPACE_AROUND)

    # --- MONTAJE DE PÁGINA ---
    page.add(
        logo_header,
        content_area,
        chat_input_bar,
        ft.Divider(color="#222230", height=1),
        nav_bar
    )

    # Cargar inicio e iniciar animación de pulso
    load_home_view()
    page.update()

    thread_pulso = threading.Thread(target=animar_logo_pulso, daemon=True)
    thread_pulso.start()

if __name__ == "__main__":
    ft.app(target=main)