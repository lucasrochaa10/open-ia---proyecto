import os
import json
import glob
import dotenv
from openai import OpenAI
from datetime import datetime

dotenv.load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def show_context(messages: list):
    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich.text import Text
    except ImportError:
        print("Rich no está instalada. Pídele a tu asistente instalarla con: uv pip install rich  (o)  pip install rich")
        return

    console = Console()
    # Filtra mensajes de system para mostrar solo Usuario/Asistente
    visible = [m for m in messages if m.get("role") in {"user", "assistant"}]
    if not visible:
        console.print(Panel("No hay mensajes en el historial.", title="Historial", border_style="yellow"))
        return

    for msg in visible:
        role = msg.get("role", "")
        content = msg.get("content", "")
        ts = msg.get("ts")
        if role == "user":
            title_text = "Usuario" if not ts else f"Usuario [{ts}]"
            title = Text(title_text, style="bold cyan")
            border = "cyan"
        else:
            title_text = "Asistente" if not ts else f"Asistente [{ts}]"
            title = Text(title_text, style="bold magenta")
            border = "magenta"
        console.print(Panel(content, title=title, border_style=border))

def flush_json_snapshot(messages, path):
    try:
        with open(path, "w", encoding="utf-8") as jf:
            json.dump(messages, jf, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error guardando JSON: {e}")

def append_and_log(messages, role, content, log_file, log_json_path):
    messages.append({"role": role, "content": content, "ts": datetime.now().strftime('%H:%M:%S')})
    who = "Usuario" if role == "user" else "Asistente"
    log_file.write(f"[{datetime.now().strftime('%H:%M:%S')}] {who}: {content}\n")
    log_file.flush()
    flush_json_snapshot(messages, log_json_path)

def list_json_logs():
    return sorted(glob.glob("./logs/*.json"))

def pick_previous_conversation():
    files = list_json_logs()
    if not files:
        print("No hay conversaciones previas. Empezando nuevo chat.")
        return []
    print("Conversaciones disponibles:")
    for i, p in enumerate(files, 1):
        print(f"{i}. {os.path.basename(p)}")
    while True:
        choice = input("Elige número (Enter para cancelar): ").strip()
        if choice == "":
            print("Cancelado. Nuevo chat.")
            return []
        if not choice.isdigit():
            print("Introduce un número válido.")
            continue
        idx = int(choice)
        if 1 <= idx <= len(files):
            sel = files[idx - 1]
            try:
                with open(sel, "r", encoding="utf-8") as jf:
                    data = json.load(jf)
                if isinstance(data, list):
                    print(f"Cargado: {os.path.basename(sel)}")
                    return data
            except Exception as e:
                print(f"No se pudo leer {sel}: {e}")
            print("Archivo inválido. Nuevo chat.")
            return []
        print("Número fuera de rango.")

def startup_menu():
    print("\n=== Inicio ===")
    print("1) Nuevo chat")
    print("2) Continuar chat anterior")
    while True:
        opt = input("Opción (1/2): ").strip()
        if opt == "1":
            return []
        if opt == "2":
            return pick_previous_conversation()
        print("Opción no válida.")

def main():
    # Banner inicial con rich si está disponible
    try:
        from rich.console import Console
        from rich.panel import Panel
        console = Console()
        console.rule("Stateful Chatbot - Completions API")
        console.print("Escribe 'exit' para salir o 'Contexto' para ver el historial", style="bold yellow")
    except Exception:
        print("Stateful Chatbot (Completions API, type 'exit' to quit)")
    
    # Menú inicial
    messages = startup_menu()
    
    model = "gpt-4o-mini"
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    # Agregar mensajes cargados a la conversación
    conversation.extend(messages)
    
    # Preparar carpeta y archivos de log
    os.makedirs("logs", exist_ok=True)
    session_ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
    log_txt_path = f"./logs/log_{session_ts}.txt"
    log_json_path = f"./logs/log_{session_ts}.json"
    log_file = open(log_txt_path, "w", encoding="utf-8")
    
    # Si cargaste historial previo, vuelca al .txt/.json de la NUEVA sesión
    if messages:
        for msg in messages:
            who = "Usuario" if msg.get("role") == "user" else "Asistente"
            log_file.write(f"[{datetime.now().strftime('%H:%M:%S')}] {who}: {msg.get('content','')}\n")
        log_file.flush()
        flush_json_snapshot(conversation, log_json_path)

    try:
        while True:
            user_input = input("You: ")
            if user_input.strip().lower() in {"exit", "quit"}:
                print("Goodbye!")
                break
            if user_input.strip().lower() == "contexto":
                show_context(conversation)
                continue

            append_and_log(conversation, "user", user_input, log_file, log_json_path)
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=conversation
                )
                text = response.choices[0].message.content.strip()
                # Imprimir respuesta con rich si está disponible
                try:
                    console  # type: ignore
                    console.print(Panel(text, title=f"Asistente [{datetime.now().strftime('%H:%M:%S')}]", border_style="magenta"))  # type: ignore
                except Exception:
                    print(f"Bot: {text}")
                append_and_log(conversation, "assistant", text, log_file, log_json_path)
            except Exception as e:
                try:
                    console  # type: ignore
                    console.print(f"Error: {e}", style="bold red")  # type: ignore
                except Exception:
                    print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nGoodbye!")
    finally:
        try:
            log_file.close()
        except Exception:
            pass
        # Mensaje de confirmación (verde si rich está disponible)
        try:
            from rich.console import Console
            console = Console()
            console.print(f"Conversación guardada en:\n  {log_txt_path}\n  {log_json_path}", style="green")
        except Exception:
            print(f"Conversación guardada en:\n  {log_txt_path}\n  {log_json_path}")

if __name__ == "__main__":
    main()
