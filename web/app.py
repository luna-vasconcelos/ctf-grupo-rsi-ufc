import os, json, random
from flask import Flask, render_template, request, make_response, g
from markupsafe import Markup, escape
from jinja2 import Environment, FileSystemLoader, select_autoescape, StrictUndefined
import re

app = Flask(__name__)

@app.context_processor
def inject_meta():
    return {"meta": {"release": os.getenv("RELEASE_SHA", "")}}

# Toggle pro ctf
CHALLENGE_MODE = os.getenv("CHALLENGE_MODE", "on").lower() in ("1", "true", "on", "yes", "y", "sim")

# Ambiente Jinja inseguro
jinja_ctf = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(["html", "xml"]),
)

def sanitize(s: str) -> str:

    blocked = [
        "mro", "subclasses", "bases",
        "read", "write", "eval", "exec",
        "sys", "system",
        "config", "application", "wsgi",
        "request", "self", "builtins",
        "namespace", "joiner","popen",
        "getattr", "getitem", "attr",
    ]
    s = re.sub("(" + "|".join(re.escape(t) for t in blocked) + ")", "", s, flags=re.I)

    return s

# login de usuário mock
def load_user(username: str | None):
    try:
        with open("data/users.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        if username:
            for u in data:
                if u.get("username") == username:
                    return u
        return random.choice(data)
    except Exception:
        # Textos que aparecem para o usuário
        return {"username": "visitante", "email": "visitante@spooku.edu", "plan": "Convidado"}

def build_context(user: dict):
    # Contexto mínimo
    theme = {
        "shapes": ["classic", "obelisk", "cross", "tablet"],
        "materials": ["granite", "marble", "sandstone", "basalt"],
        "ornaments": ["skull", "bat", "cobweb", "rose", "raven"],
        "fonts": ["gothic", "cursive", "runes", "serif"],
    }

    order = (user.get("orders") or [{}])[-1]
    ctx = {"user": user, "order": order, "theme": theme}

    # Valores “meta” opcionais usados em templates/health
    release = os.getenv("RELEASE_SHA", "")
    support = os.getenv("SUPPORT_EMAIL", "suporte@example.com")
    ctx["meta"] = {"release": release, "support": support}

    # Decoys para CTF (sem dados reais)
    if CHALLENGE_MODE:
        ctx["decoys"] = {
            "build": release,
            "contact": support,
        }
    return ctx

@app.before_request
def add_security_headers():
    # Padrões mínimos 
    g.sec_headers = {
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff",
        "Referrer-Policy": "no-referrer",
        "Content-Security-Policy": "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'",
    }

@app.after_request
def apply_security_headers(resp):
    for k, v in getattr(g, "sec_headers", {}).items():
        resp.headers.setdefault(k, v)
    return resp

@app.get("/")
def index():
    username = request.cookies.get("as_user") or request.args.get("as_user")
    user = load_user(username)
    resp = make_response(render_template("index.html", user=user))
    if request.args.get("as_user"):
        resp.set_cookie(
            "as_user",
            request.args["as_user"],
            httponly=True,
            samesite="Lax",
            secure=False,  
            max_age=7 * 24 * 3600,
        )
    return resp

@app.post("/preview")
def preview():
    # Campos do formulário
    inscription = (
        request.form.get("inscription")
        or request.form.get("nome")
        or request.form.get("inscricao")
        or "Em memória"
    )
    epitaph_template = request.form.get("epitaph_template","— Rest in peace —")
    shape = request.form.get("shape", "classic")
    material = request.form.get("material", "granite")
    ornament = request.form.get("ornament", "skull")
    font = request.form.get("font", "gothic")
    born = request.form.get("born", "1900")
    died = request.form.get("died", "2000")

    # Usuário + contexto
    username = request.cookies.get("as_user")
    user = load_user(username)
    ctx = build_context(user)

    # Caminho SEGURO por padrão: trata input como texto (escapado)
    epitaph_safe_text = escape(epitaph_template)
    epitaph = Markup(epitaph_safe_text)  
    hint = "<!-- modo seguro: nenhum template é avaliado -->"

    # Caminho CTF: avalia template controlado pelo usuário com contexto
    if CHALLENGE_MODE:
        try:
            rendered = jinja_ctf.from_string(sanitize(epitaph_template)).render(**ctx)
        except Exception:
            epitaph = Markup(epitaph_safe_text)
            hint = "<!-- erro de renderização; texto em modo seguro -->"

    return render_template(
        "preview.html",
        inscription=inscription,
        epitaph=rendered,
        shape=shape,
        material=material,
        ornament=ornament,
        font=font,
        born=born,
        died=died,
        user=user,
        hint=Markup(hint),
    )

@app.get("/healthz")
def healthz():
    return {"ok": True, "version": os.getenv("RELEASE_SHA", "")}

@app.get("/.well-known/meta")
def meta():
    return {
        "service": "gerador-lapide",
        "release": os.getenv("RELEASE_SHA", ""),
        "support": os.getenv("SUPPORT_EMAIL", "suporte@example.com"),
    }
