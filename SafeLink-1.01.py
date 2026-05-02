import json
import os
import threading
import sys
from pathlib import Path
from tkinter import PhotoImage, messagebox

import customtkinter as ctk
import requests
from PIL import Image


API_URL = "https://www.virustotal.com/vtapi/v2/url/report"
APP_TITLE = "SafeLink 1.0.1"
CONFIG_FILENAME = "config.json"

COLORS = {
    "app_bg": "#050000",
    "header_bg": "#170606",
    "panel_bg": "#100303",
    "field_bg": "#060000",
    "border": "#7f1d1d",
    "border_strong": "#b91c1c",
    "accent": "#dc2626",
    "accent_hover": "#b91c1c",
    "text": "#fee2e2",
    "muted": "#fca5a5",
    "soft": "#fecaca",
    "status_bg": "#230909",
}


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def check_website(api_key, url):
    params = {
        "apikey": api_key,
        "resource": url,
        "allinfo": "false",
    }
    response = requests.get(API_URL, params=params, timeout=20)
    response.raise_for_status()
    return response.json()


def evaluate_site(result):
    if "positives" not in result:
        return "Aucune information disponible"

    positives = result.get("positives", 0)
    total = result.get("total", 0)

    if positives > 0:
        return f"Risque détecté ({positives}/{total} détections)"

    return f"Fiable ({positives}/{total} détections)"


def get_config_path():
    if sys.platform.startswith("win"):
        base_dir = Path(os.getenv("APPDATA", Path.home()))
    else:
        base_dir = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config"))

    return base_dir / "SafeLink" / CONFIG_FILENAME


def load_config():
    config_path = get_config_path()
    if not config_path.exists():
        return {}

    try:
        return json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def save_config(config):
    config_path = get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")


def delete_config():
    config_path = get_config_path()
    try:
        config_path.unlink()
    except FileNotFoundError:
        pass
    except OSError:
        pass


class SafeLinkApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)
        self.geometry("920x660")
        self.minsize(820, 600)
        self.configure(fg_color=COLORS["app_bg"])

        self._checking = False
        self.logo_image = None
        self.logo_title_image = None
        self.logo_small_image = None
        self.logo_button_image = None
        self.window_icon_image = None
        self.remember_api_var = ctk.BooleanVar(value=False)

        self._set_icon()
        self._build_layout()

    def _set_icon(self):
        for image_path in self._asset_candidates("safelink-logo.png"):
            if image_path.exists():
                try:
                    self.window_icon_image = PhotoImage(file=str(image_path))
                    self.iconphoto(True, self.window_icon_image)
                    break
                except Exception:
                    pass

        for icon_path in self._asset_candidates("safelink-logo.ico") + self._asset_candidates("logo.ico"):
            if icon_path.exists():
                try:
                    self.iconbitmap(str(icon_path))
                    return
                except Exception:
                    pass

    def _asset_candidates(self, filename):
        app_dir = Path(__file__).resolve().parent
        cwd = Path.cwd()
        bundle_dir = Path(getattr(sys, "_MEIPASS", app_dir))

        return [
            app_dir / "assets" / filename,
            app_dir / filename,
            cwd / "assets" / filename,
            cwd / filename,
            bundle_dir / "assets" / filename,
            bundle_dir / filename,
        ]

    def _load_logo_image(self, size):
        logo_paths = (
            self._asset_candidates("safelink-logo-mark.png")
            + self._asset_candidates("safelink-logo.png")
        )

        for logo_path in logo_paths:
            if logo_path.exists():
                try:
                    image = Image.open(logo_path).copy()
                    return ctk.CTkImage(light_image=image, dark_image=image, size=size)
                except Exception:
                    pass

        return None

    def _build_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        header = ctk.CTkFrame(
            self,
            fg_color=COLORS["header_bg"],
            border_color=COLORS["border"],
            border_width=1,
            corner_radius=8,
        )
        header.grid(row=0, column=0, sticky="ew", padx=28, pady=(24, 16))
        header.grid_columnconfigure(2, weight=1)

        self.logo_image = self._load_logo_image((58, 58))
        self.logo_title_image = self._load_logo_image((42, 42))
        self.logo_small_image = self._load_logo_image((24, 24))
        self.logo_button_image = self._load_logo_image((20, 20))

        logo_label = ctk.CTkLabel(
            header,
            text="",
            image=self.logo_image,
            width=64,
            height=64,
            fg_color="transparent",
            corner_radius=8,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS["accent"],
        )
        logo_label.grid(row=0, column=0, rowspan=2, sticky="w", padx=(16, 0), pady=14)

        accent_bar = ctk.CTkFrame(header, fg_color=COLORS["accent"], width=5, corner_radius=4)
        accent_bar.grid(row=0, column=1, rowspan=2, sticky="nsw", padx=(14, 0), pady=16)

        title_group = ctk.CTkFrame(header, fg_color="transparent")
        title_group.grid(row=0, column=2, sticky="w", padx=(16, 0), pady=(14, 0))

        title_logo = ctk.CTkLabel(
            title_group,
            text="",
            image=self.logo_title_image,
            width=46,
            height=46,
            fg_color="transparent",
        )
        title_logo.grid(row=0, column=0, sticky="w", padx=(0, 10))

        title = ctk.CTkLabel(
            title_group,
            text="SafeLink",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=COLORS["text"],
        )
        title.grid(row=0, column=1, sticky="w")

        version_badge = ctk.CTkLabel(
            header,
            text="1.0.1",
            width=58,
            height=24,
            fg_color="#2a0909",
            corner_radius=12,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS["soft"],
        )
        version_badge.grid(row=0, column=3, sticky="e", padx=(12, 16), pady=(18, 0))

        subtitle = ctk.CTkLabel(
            header,
            text="Vérification d'URLs avec VirusTotal",
            font=ctk.CTkFont(size=15),
            text_color=COLORS["muted"],
        )
        subtitle.grid(row=1, column=2, sticky="w", padx=(16, 0), pady=(0, 16))

        status_badge = ctk.CTkFrame(
            header,
            fg_color=COLORS["status_bg"],
            border_color=COLORS["border"],
            border_width=1,
            corner_radius=16,
        )
        status_badge.grid(row=1, column=3, sticky="e", padx=16, pady=(0, 16))

        self.status_label = ctk.CTkLabel(
            status_badge,
            text="Prêt",
            image=self.logo_button_image,
            compound="left",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COLORS["accent"],
        )
        self.status_label.grid(row=0, column=0, padx=12, pady=5)

        divider = ctk.CTkFrame(self, fg_color="#3f0a0a", height=1)
        divider.grid(row=1, column=0, sticky="ew", padx=28, pady=(0, 18))

        content = ctk.CTkFrame(self, fg_color="transparent")
        content.grid(row=2, column=0, sticky="nsew", padx=28, pady=(0, 24))
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=1)

        input_panel = ctk.CTkFrame(
            content,
            fg_color=COLORS["panel_bg"],
            border_color=COLORS["border"],
            border_width=1,
            corner_radius=8,
        )
        input_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        input_panel.grid_columnconfigure(0, weight=1)
        input_panel.grid_rowconfigure(5, weight=1)

        ctk.CTkLabel(
            input_panel,
            text="Analyse",
            image=self.logo_small_image,
            compound="left",
            font=ctk.CTkFont(size=19, weight="bold"),
            text_color=COLORS["text"],
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(20, 4))

        ctk.CTkLabel(
            input_panel,
            text="Clé API VirusTotal",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COLORS["soft"],
        ).grid(row=1, column=0, sticky="w", padx=20, pady=(12, 8))

        self.entry_api_key = ctk.CTkEntry(
            input_panel,
            height=42,
            show="*",
            placeholder_text="Collez votre clé API",
            fg_color=COLORS["field_bg"],
            border_color=COLORS["border_strong"],
            text_color=COLORS["text"],
            placeholder_text_color="#991b1b",
            corner_radius=6,
        )
        self.entry_api_key.grid(row=2, column=0, sticky="ew", padx=20)

        self.remember_api_checkbox = ctk.CTkCheckBox(
            input_panel,
            text="Mémoriser la clé API localement",
            variable=self.remember_api_var,
            command=self.on_remember_api_toggle,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            border_color=COLORS["border"],
            checkmark_color="#fff1f2",
            text_color=COLORS["soft"],
        )
        self.remember_api_checkbox.grid(row=3, column=0, sticky="w", padx=20, pady=(12, 0))

        ctk.CTkLabel(
            input_panel,
            text="URLs à vérifier",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COLORS["soft"],
        ).grid(row=4, column=0, sticky="w", padx=20, pady=(18, 8))

        self.entry_urls = ctk.CTkTextbox(
            input_panel,
            height=270,
            fg_color=COLORS["field_bg"],
            border_color=COLORS["border_strong"],
            border_width=1,
            text_color=COLORS["text"],
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["accent_hover"],
            corner_radius=6,
        )
        self.entry_urls.grid(row=5, column=0, sticky="nsew", padx=20)

        actions = ctk.CTkFrame(input_panel, fg_color="transparent")
        actions.grid(row=6, column=0, sticky="ew", padx=20, pady=20)
        actions.grid_columnconfigure(0, weight=1)

        self.check_button = ctk.CTkButton(
            actions,
            text="Vérifier",
            height=44,
            command=self.on_check_button_click,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            text_color="#fff1f2",
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=6,
        )
        self.check_button.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        clear_button = ctk.CTkButton(
            actions,
            text="Effacer",
            width=104,
            height=44,
            command=self.clear_inputs,
            fg_color=COLORS["field_bg"],
            hover_color="#1f0707",
            text_color=COLORS["soft"],
            border_width=1,
            border_color=COLORS["border"],
            corner_radius=6,
        )
        clear_button.grid(row=0, column=1)

        result_panel = ctk.CTkFrame(
            content,
            fg_color=COLORS["panel_bg"],
            border_color=COLORS["border"],
            border_width=1,
            corner_radius=8,
        )
        result_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        result_panel.grid_columnconfigure(0, weight=1)
        result_panel.grid_rowconfigure(1, weight=1)

        result_header = ctk.CTkFrame(result_panel, fg_color="transparent")
        result_header.grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 8))
        result_header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            result_header,
            text="Résultats",
            image=self.logo_small_image,
            compound="left",
            font=ctk.CTkFont(size=19, weight="bold"),
            text_color=COLORS["text"],
        ).grid(row=0, column=0, sticky="w")

        copy_button = ctk.CTkButton(
            result_header,
            text="Copier",
            width=92,
            height=32,
            command=self.copy_results,
            fg_color=COLORS["field_bg"],
            hover_color="#1f0707",
            text_color=COLORS["soft"],
            border_width=1,
            border_color=COLORS["border"],
            corner_radius=6,
        )
        copy_button.grid(row=0, column=1, sticky="e")

        self.result_box = ctk.CTkTextbox(
            result_panel,
            fg_color=COLORS["field_bg"],
            border_color=COLORS["border_strong"],
            border_width=1,
            text_color=COLORS["soft"],
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["accent_hover"],
            corner_radius=6,
        )
        self.result_box.grid(row=1, column=0, sticky="nsew", padx=18)
        self.result_box.insert("1.0", "Les résultats apparaîtront ici après la vérification.")
        self.result_box.configure(state="disabled")

        self.progress_bar = ctk.CTkProgressBar(
            result_panel,
            height=8,
            fg_color="#250909",
            progress_color=COLORS["accent"],
        )
        self.progress_bar.grid(row=2, column=0, sticky="ew", padx=18, pady=18)
        self.progress_bar.set(0)
        self.load_saved_api_key()

    def on_check_button_click(self):
        if self._checking:
            return

        api_key = self.entry_api_key.get().strip()
        urls = [
            url.strip()
            for url in self.entry_urls.get("1.0", "end").splitlines()
            if url.strip()
        ]

        if not api_key:
            messagebox.showerror("Erreur", "Veuillez saisir votre clé API.")
            return

        if not urls:
            messagebox.showerror("Erreur", "Veuillez saisir au moins une URL.")
            return

        self.persist_api_key(api_key)

        self._checking = True
        self.check_button.configure(state="disabled", text="Vérification...")
        self.status_label.configure(text="Analyse en cours", text_color="#f87171")
        self.progress_bar.set(0)
        self._set_results("Analyse en cours...\n")

        thread = threading.Thread(
            target=self._run_checks,
            args=(api_key, urls),
            daemon=True,
        )
        thread.start()

    def _run_checks(self, api_key, urls):
        results = []
        total_urls = len(urls)

        for index, url in enumerate(urls, start=1):
            try:
                result = check_website(api_key, url)
                evaluation = evaluate_site(result)
                results.append(f"{url}\n  {evaluation}")
            except requests.RequestException as error:
                results.append(f"{url}\n  Erreur réseau: {error}")
            except ValueError:
                results.append(f"{url}\n  Réponse serveur invalide")

            progress = index / total_urls
            self.after(0, self._set_progress, progress, f"{index}/{total_urls} analyse(s)")

        self.after(0, self._finish_checks, results)

    def _set_progress(self, progress, status):
        self.progress_bar.set(progress)
        self.status_label.configure(text=status, text_color="#f87171")

    def _finish_checks(self, results):
        self._checking = False
        self.check_button.configure(state="normal", text="Vérifier")
        self.status_label.configure(text="Terminé", text_color="#ef4444")
        self._set_results("\n\n".join(results))

    def _set_results(self, text):
        self.result_box.configure(state="normal")
        self.result_box.delete("1.0", "end")
        self.result_box.insert("1.0", text)
        self.result_box.configure(state="disabled")

    def clear_inputs(self):
        if self._checking:
            return

        self.entry_urls.delete("1.0", "end")
        self._set_results("Les résultats apparaîtront ici après la vérification.")
        self.progress_bar.set(0)
        self.status_label.configure(text="Prêt", text_color="#ef4444")

    def load_saved_api_key(self):
        config = load_config()
        api_key = config.get("api_key", "")
        remember_api = bool(config.get("remember_api", False) and api_key)

        if api_key:
            self.entry_api_key.insert(0, api_key)

        self.remember_api_var.set(remember_api)

    def persist_api_key(self, api_key):
        if self.remember_api_var.get():
            save_config({"remember_api": True, "api_key": api_key})
        else:
            delete_config()

    def on_remember_api_toggle(self):
        if self.remember_api_var.get():
            api_key = self.entry_api_key.get().strip()
            if api_key:
                save_config({"remember_api": True, "api_key": api_key})
            return

        delete_config()
        self.status_label.configure(text="Clé API oubliée", text_color="#ef4444")

    def copy_results(self):
        results = self.result_box.get("1.0", "end").strip()
        if not results:
            return

        self.clipboard_clear()
        self.clipboard_append(results)
        self.status_label.configure(text="Résultats copiés", text_color="#ef4444")


if __name__ == "__main__":
    app = SafeLinkApp()
    app.mainloop()
