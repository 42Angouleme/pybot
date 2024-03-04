from functools import wraps
import sys

def _must_not(module, lang):
    return f"Le module {module} est déjà démarré." if lang == "fr" else f"{module} module has already been started."

def _must(module, lang):
    return f"Le module {module} doit être démarré avant ce module." if lang == "fr" else f"{module} module must be started before this module."

msg = {
    'fr': {
        "has_conversation": "Une autre discussion est actuellement en cours.",
        "no_conversation": "Aucune conversation n'a été commencé avec le robot.",
        "no_AI": _must("IA", "fr"),
        "has_AI": _must_not("IA", "fr"),
        "no_webapp": _must("application web", "fr"),
        "has_window": _must_not("fenêtre", "fr"),
        "no_camera": _must("caméra", "fr"),
        "has_camera": _must_not("camera", "fr"),
        "no_user": _must("utilisateur", "fr"),
        "has_user": _must_not("utilisateur", "fr"),
        "is_empty": lambda str: f"{str} est vide (=None).",
    },
    'en': {
        "has_conversation": "Another discussion is currently underway.",
        "no_conversation": "No conversation has been started with the robot.",
        "no_AI": _must("AI", "en"),
        "has_AI": _must_not("AI", "en"),
        "no_webapp": _must("Webapp", "en"),
        "has_window": _must_not("Window", "en"),
        "no_camera": _must("Camera", "en"),
        "has_camera": _must_not("Camera", "en"),
        "no_user": _must("User", "en"),
        "has_user": _must_not("User", "en"),
        "is_empty": lambda str: f"{str} is empty (=None).",
    }
}

def err(msg: str, lang: str = "fr"):
    if (lang.lower() == "fr") :
        print(f"\033[91mErreur: {msg}\033[00m", file=sys.stderr)
    elif (lang.lower() == "en") :
        print(f"\033[91mError: {msg}\033[00m", file=sys.stderr)
    return True

def warn(msg: str, lang: str = "fr"):
    if (lang.lower() == "fr") :
        print(f"\033[33mAttention: {msg}\033[00m", file=sys.stderr)
    elif (lang.lower() == "en") :
        print(f"\033[33mWarning: {msg}\033[00m", file=sys.stderr)
    return False

def _get_decorator(error_condition, err_msg_key, logger=err):
    def lang_decorator(lang):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if (error_condition(self) and logger(msg[lang][err_msg_key], lang)):
                    return
                return func(self, *args, **kwargs)
            return wrapper
        return decorator
    return lang_decorator

def no_conversation(lang):
    return _get_decorator(error_condition = lambda self: self._Robot__chatGPT is not None, err_msg_key = "has_conversation")(lang)

def conversation(lang):
    return _get_decorator(error_condition = lambda self: self._Robot__chatgpt is None, err_msg_key = "no_conversation")(lang)

def AI(lang):
    return _get_decorator(error_condition = lambda self: self.AI is None, err_msg_key = "has_AI")(lang)

def no_AI(lang):
    return _get_decorator(error_condition = lambda self: self.AI is not None, err_msg_key = "no_AI")(lang)

def window(lang):
    return _get_decorator(error_condition = lambda self: self.window is None or self.fenetre._get_surface() is None, err_msg_key = "no_window", logger=warn)(lang)

def no_window(lang):
    return _get_decorator(error_condition = lambda self: self.window is not None, err_msg_key = "has_window")(lang)

def webapp(lang):
    return _get_decorator(error_condition = lambda self: self._Robot__webapp is None, err_msg_key = "no_webapp")(lang)

def warn_webapp(lang):
    return _get_decorator(error_condition = lambda self: self._Robot__webapp is None, err_msg_key = "no_webapp", logger=warn)(lang)

def camera(lang):
    return _get_decorator(error_condition = lambda self: self.camera is None, err_msg_key = "no_camera")(lang)

def no_camera(lang):
    return _get_decorator(error_condition = lambda self: self.camera is not None, err_msg_key = "has_camera")(lang)

def no_user(lang):
    return _get_decorator(error_condition = lambda self: self.user is not None, err_msg_key = "has_user")(lang)

def user(lang):
    return _get_decorator(error_condition = lambda self: self.user is None, err_msg_key = "no_user")(lang)
