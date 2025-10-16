import os, json, random
from flask import Flask, render_template, request, make_response, g
from markupsafe import Markup, escape
from jinja2 import Environment, FileSystemLoader, select_autoescape, StrictUndefined

app = Flask(__name__)

@app.context_processor
def inject_meta():
    return {"meta": {"release": os.getenv("RELEASE_SHA", "")}}

# Toggle: Seguro por padrão (sem SSTI). Ativar em execuções de CTF.
CHALLENGE_MODE = os.getenv("CHALLENGE_MODE", "on").lower() in ("1", "true", "on", "yes", "y", "sim")

# Ambiente Jinja SEGURO: StrictUndefined evita "pescaria" silenciosa de variáveis
jinja_safe = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(["html", "xml"]),
    undefined=StrictUndefined,
)

# Ambiente Jinja INSEGURO (para o CTF), só habilitado se CHALLENGE_MODE=on
jinja_ctf = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(["html", "xml"]),
)

def naive_sanitize(s: str) -> str:
    # Sanitização *ingênua* apenas para dificultar payloads triviais.
    # NÃO confie nisso para segurança real.
    return s.replace("{%", "").replace("%}", "")

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
    # Contexto mínimo; sem chaves de SMTP/API (removidas do compose)
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

    # Decoys opcionais para sessões de CTF (sem segredos reais)
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
            secure=False,  # definir true se for HTTPS
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
    # epitaph_template = (
    #     request.form.get("epitaph_template")
    #     or request.form.get("epitafio")
    #     or "— Descanse em paz —"
    # )
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
    epitaph = Markup(epitaph_safe_text)  # renderiza como texto literal
    hint = "<!-- modo seguro: nenhum template é avaliado -->"

    # Caminho CTF: avalia template controlado pelo usuário com contexto
    if CHALLENGE_MODE:
        try:
            rendered = jinja_ctf.from_string(naive_sanitize(epitaph_template)).render(**ctx)
            # epitaph = Markup(rendered)  # entrega exatamente o que foi renderizado
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
