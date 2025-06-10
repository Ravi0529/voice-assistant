import webbrowser
import subprocess
import os
import shutil
import platform

# Map common spoken app names to actual executable names
APP_MAP = {
    "chrome": "chrome.exe",
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "vs code": "code",
    "spotify": "spotify.exe",
    "explorer": "explorer.exe",
}


def handle_utility_task(refined_input: str) -> str:
    """
    Attempts to handle utility tasks like opening applications, searching the web or YouTube.
    """
    lower_input = refined_input.lower()

    if "youtube" in lower_input and "search" in lower_input:
        return search_youtube(refined_input)
    elif "search" in lower_input or "google" in lower_input:
        return web_search(refined_input)
    else:
        return open_application(refined_input)


def open_application(app_name: str) -> str:
    """
    Attempts to open an application by name on any OS.
    Tries to resolve common spoken names to actual executables.
    """
    try:
        app_name = app_name.lower().strip()
        exec_name = APP_MAP.get(app_name, app_name)

        if platform.system() == "Windows":
            try:
                os.startfile(exec_name)
                return f"Opening {app_name}..."
            except FileNotFoundError:
                path = shutil.which(exec_name)
                if path:
                    subprocess.Popen([path])
                    return f"Opening {app_name} using PATH..."
                else:
                    return f"Could not find '{exec_name}' in system PATH."
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", "-a", exec_name])
            return f"Opening {app_name} on macOS..."
        else:
            subprocess.Popen([exec_name])
            return f"Opening {app_name} on Linux..."
    except Exception as e:
        return f"Failed to open {app_name}: {str(e)}"


def clean_query(text: str, keywords: list) -> str:
    """
    Removes known keywords from the text and returns a cleaned query.
    """
    text = text.lower()
    for kw in keywords:
        text = text.replace(kw, "")
    return text.strip()


def search_youtube(query: str) -> str:
    """
    Searches YouTube for the provided query.
    """
    try:
        cleaned = clean_query(query, ["search", "youtube", "on", "for"])
        url = (
            f"https://www.youtube.com/results?search_query={cleaned.replace(' ', '+')}"
        )
        webbrowser.open(url)
        return f"Searching YouTube for: {cleaned}"
    except Exception as e:
        return f"Failed to search YouTube: {str(e)}"


def web_search(query: str) -> str:
    """
    Performs a Google search for the provided query.
    """
    try:
        cleaned = clean_query(query, ["search", "google", "on", "for"])
        url = f"https://www.google.com/search?q={cleaned.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Searching Google for: {cleaned}"
    except Exception as e:
        return f"Failed to perform search: {str(e)}"
