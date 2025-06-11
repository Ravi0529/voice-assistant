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
    "camera": "microsoft.windows.camera:",
}


def handle_utility_task(refined_input: str) -> str:
    """
    Handles utility tasks like opening apps, websites, or performing searches.
    """
    lower_input = refined_input.lower()

    # Match known app names first (camera, calculator, etc.)
    for app_keyword in APP_MAP:
        if app_keyword in lower_input:
            return open_application(app_keyword)

    # YouTube Search
    if "search" in lower_input and "youtube" in lower_input:
        return search_youtube(refined_input)

    # Web Search (e.g., "search Google for...")
    if "search" in lower_input or "google" in lower_input:
        return web_search(refined_input)

    # Direct domain open (e.g., github.com)
    if "open" in lower_input and (".com" in lower_input or "github" in lower_input):
        words = refined_input.split()
        url = None
        for word in words:
            if "github" in word:
                url = "https://github.com"
            elif ".com" in word:
                url = word if word.startswith("http") else f"https://{word}"
            if url:
                webbrowser.open(url)
                return f"Opening {url}"
        return "Couldn't extract a valid URL to open."

    # Default fallback
    return "I'm not sure how to handle this request."


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
