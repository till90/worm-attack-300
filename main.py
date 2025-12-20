#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from flask import Flask, jsonify, make_response, render_template_string, request
from werkzeug.exceptions import HTTPException

SERVICE_NAME_SLUG = "worms-mini"
PAGE_TITLE = "Mini Worms – Local Duel"
PAGE_H1 = "Mini Worms"
PAGE_SUBTITLE = "Lokales 2-Spieler-Duell im Browser (abwechselnde Züge)."
LANDING_URL = "https://data-tales.dev/"
COOKBOOK_URL = "https://data-tales.dev/cookbook/"
PLZ_URL = "https://plz.data-tales.dev/"

VERSION = os.environ.get("SERVICE_VERSION", "1.0.0")

app = Flask(__name__)
app.config.update(
    ENV="production",
    DEBUG=False,
    TESTING=False,
    PROPAGATE_EXCEPTIONS=False,
    TEMPLATES_AUTO_RELOAD=False,
)


HTML = r"""<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="{{ page_subtitle }}" />
  <meta name="theme-color" content="#0b0f19" />
  <title>{{ page_title }}</title>

  <style>
    :root{
      --bg: #0b0f19;
      --bg2:#0f172a;
      --card:#111a2e;
      --text:#e6eaf2;
      --muted:#a8b3cf;
      --border: rgba(255,255,255,.10);
      --shadow: 0 18px 60px rgba(0,0,0,.35);
      --primary:#6ea8fe;
      --primary2:#8bd4ff;
      --focus: rgba(110,168,254,.45);

      --radius: 18px;
      --container: 1100px;
      --gap: 18px;

      --font: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji","Segoe UI Emoji";
    }

    [data-theme="light"]{
      --bg:#f6f7fb;
      --bg2:#ffffff;
      --card:#ffffff;
      --text:#111827;
      --muted:#4b5563;
      --border: rgba(17,24,39,.12);
      --shadow: 0 18px 60px rgba(17,24,39,.10);
      --primary:#2563eb;
      --primary2:#0ea5e9;
      --focus: rgba(37,99,235,.25);
    }

    *{box-sizing:border-box}
    html,body{height:100%}
    body{
      margin:0;
      font-family:var(--font);
      background: radial-gradient(1200px 800px at 20% -10%, rgba(110,168,254,.25), transparent 55%),
                  radial-gradient(1000px 700px at 110% 10%, rgba(139,212,255,.20), transparent 55%),
                  linear-gradient(180deg, var(--bg), var(--bg2));
      color:var(--text);
    }

    .container{
      max-width:var(--container);
      margin:0 auto;
      padding:0 18px;
    }

    .skip-link{
      position:absolute; left:-999px; top:10px;
      background:var(--card); color:var(--text);
      padding:10px 12px; border-radius:10px;
      border:1px solid var(--border);
    }
    .skip-link:focus{left:10px; outline:2px solid var(--focus)}

    .site-header{
      position:sticky; top:0; z-index:20;
      backdrop-filter: blur(10px);
      background: rgba(10, 14, 24, .55);
      border-bottom:1px solid var(--border);
    }
    [data-theme="light"] .site-header{ background: rgba(246,247,251,.75); }

    .header-inner{
      display:flex; align-items:center; justify-content:space-between;
      padding:14px 0;
      gap:14px;
    }
    .brand{display:flex; align-items:center; gap:10px; text-decoration:none; color:var(--text); font-weight:700}
    .brand-mark{
      width:14px; height:14px; border-radius:6px;
      background: linear-gradient(135deg, var(--primary), var(--primary2));
      box-shadow: 0 10px 25px rgba(110,168,254,.25);
    }
    .nav{display:flex; gap:16px; flex-wrap:wrap}
    .nav a{color:var(--muted); text-decoration:none; font-weight:600}
    .nav a:hover{color:var(--text)}
    .header-actions{display:flex; gap:10px; align-items:center}

    .btn{
      display:inline-flex; align-items:center; justify-content:center;
      gap:8px;
      padding:10px 14px;
      border-radius:12px;
      border:1px solid transparent;
      text-decoration:none;
      font-weight:700;
      color:var(--text);
      background: transparent;
      cursor:pointer;
      user-select:none;
      -webkit-tap-highlight-color: transparent;
    }
    .btn:focus{outline:2px solid var(--focus); outline-offset:2px}
    .btn-primary{
      border-color: transparent;
      background: linear-gradient(135deg, var(--primary), var(--primary2));
      color: #0b0f19;
    }
    [data-theme="light"] .btn-primary{ color:#ffffff; }
    .btn-secondary{ background: rgba(255,255,255,.06); }
    [data-theme="light"] .btn-secondary{ background: rgba(17,24,39,.04); }
    .btn-ghost{ background: transparent; }
    .btn:hover{transform: translateY(-1px)}
    .btn:active{transform:none}

    .sr-only{
      position:absolute; width:1px; height:1px; padding:0; margin:-1px;
      overflow:hidden; clip:rect(0,0,0,0); border:0;
    }

    .section{padding:42px 0}
    .kicker{
      margin:0 0 10px;
      display:inline-block;
      font-weight:800;
      letter-spacing:.08em;
      text-transform:uppercase;
      color:var(--muted);
      font-size:12px;
    }
    h1{margin:0 0 12px; font-size:42px; line-height:1.1}
    @media (max-width: 520px){ h1{font-size:34px} }
    .lead{margin:0 0 18px; color:var(--muted); font-size:16px; line-height:1.6}

    .card{
      border:1px solid var(--border);
      border-radius: var(--radius);
      background: rgba(255,255,255,.04);
      padding:16px;
      box-shadow: var(--shadow);
    }
    [data-theme="light"] .card{ background: rgba(255,255,255,.92); }

    .tag{
      font-size:12px;
      font-weight:800;
      color: var(--muted);
      border:1px solid var(--border);
      background: rgba(255,255,255,.03);
      padding:6px 8px;
      border-radius:999px;
      display:inline-flex;
      align-items:center;
      gap:8px;
      white-space:nowrap;
    }
    [data-theme="light"] .tag{ background: rgba(17,24,39,.02); }

    .muted{color:var(--muted); line-height:1.6; margin:0}

    /* --- Minimal Ergänzungen für das Game (ohne Look-Wechsel) --- */
    .game-wrap{display:grid; gap: var(--gap); margin-top: 14px}
    .game-card{padding:18px}
    .hud{
      display:flex; align-items:center; justify-content:space-between;
      gap:12px; flex-wrap:wrap;
      margin-bottom: 10px;
    }
    .hud-left{display:flex; flex-direction:column; gap:8px}
    .hud-row{display:flex; gap:10px; flex-wrap:wrap; align-items:center}
    .hud-mini{font-weight:650; color:var(--muted); font-size:13px}

    .hp-row{
      display:grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin: 8px 0 14px;
    }
    @media (max-width: 640px){
      .hp-row{grid-template-columns:1fr}
    }
    .hp{
      border:1px solid var(--border);
      border-radius: 14px;
      padding:10px 12px;
      background: rgba(255,255,255,.03);
    }
    [data-theme="light"] .hp{ background: rgba(17,24,39,.02); }
    .hp-top{display:flex; justify-content:space-between; align-items:center; gap:10px; margin-bottom:8px}
    .hp-name{font-weight:900}
    .hp-val{font-weight:800; color:var(--muted)}
    .hp-bar{
      height: 10px;
      border-radius: 999px;
      border: 1px solid var(--border);
      overflow:hidden;
      background: rgba(255,255,255,.03);
    }
    [data-theme="light"] .hp-bar{ background: rgba(17,24,39,.02); }
    .hp-fill{
      height: 100%;
      width: 100%;
      border-radius: 999px;
      background: linear-gradient(135deg, var(--primary), var(--primary2));
      transform-origin: left center;
      transform: scaleX(1);
    }

    .canvas-wrap{
      position: relative;
      border-radius: var(--radius);
      overflow:hidden;
      border: 1px solid var(--border);
      background: rgba(255,255,255,.02);
    }
    [data-theme="light"] .canvas-wrap{ background: rgba(17,24,39,.02); }

    canvas{
      display:block;
      width:100%;
      height: 480px;
    }
    @media (max-width: 640px){
      canvas{ height: 420px; }
    }
    @media (max-width: 420px){
      canvas{ height: 380px; }
    }

    .fallback{
      position:absolute;
      inset: 12px;
      display:flex;
      flex-direction:column;
      gap:10px;
      justify-content:center;
      align-items:flex-start;
      background: rgba(17,26,46,.92);
      backdrop-filter: blur(10px);
      padding: 14px;
    }
    [data-theme="light"] .fallback{
      background: rgba(255,255,255,.96);
    }
    .fallback h3{margin:0; font-size:16px}
    .fallback p{margin:0; color:var(--muted)}
    .fallback code{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
      font-size: 12px;
      color: var(--text);
      background: rgba(255,255,255,.04);
      border: 1px solid var(--border);
      padding: 2px 6px;
      border-radius: 8px;
    }

    .game-foot{
      margin-top: 12px;
      display:flex;
      flex-direction:column;
      gap:6px;
    }

    .toast{
      position: fixed;
      left: 50%;
      bottom: 18px;
      transform: translateX(-50%);
      max-width: min(720px, calc(100vw - 24px));
      padding: 12px 14px;
      border-radius: 14px;
      border: 1px solid var(--border);
      background: rgba(17,26,46,.92);
      backdrop-filter: blur(10px);
      box-shadow: var(--shadow);
      color: var(--text);
      font-weight: 750;
      opacity: 0;
      pointer-events: none;
      transition: opacity .18s ease, transform .18s ease;
      z-index: 80;
      will-change: opacity, transform;
    }
    [data-theme="light"] .toast{ background: rgba(255,255,255,.96); }
    .toast.show{
      opacity: 1;
      transform: translateX(-50%) translateY(-2px);
    }
  </style>
</head>

<body>
  <a class="skip-link" href="#main">Zum Inhalt springen</a>

  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="{{ landing_url }}" aria-label="Zur Landing Page">
        <span class="brand-mark" aria-hidden="true"></span>
        <span class="brand-text">data-tales.dev</span>
      </a>

      <div class="nav-dropdown" data-dropdown>
          <button class="btn btn-ghost nav-dropbtn"
                  type="button"
                  aria-haspopup="true"
                  aria-expanded="false"
                  aria-controls="servicesMenu">
            Dienste <span class="nav-caret" aria-hidden="true">▾</span>
          </button>

          <div id="servicesMenu" class="card nav-menu" role="menu" hidden>
            <a role="menuitem" href="https://flybi-demo.data-tales.dev/">Flybi Dashboard Demo</a>
            <a role="menuitem" href="https://wms-wfs-sources.data-tales.dev/">WMS/WFS Server Viewer</a>
            <a role="menuitem" href="https://tree-locator.data-tales.dev/">Tree Locator</a>
            <a role="menuitem" href="https://plz.data-tales.dev/">PLZ → Koordinaten</a>
            <a role="menuitem" href="https://paw-wiki.data-tales.dev/">Paw Patrole Wiki</a>
            <a role="menuitem" href="https://paw-quiz.data-tales.dev/">Paw Patrole Quiz</a>
            <a role="menuitem" href="https://hp-quiz.data-tales.dev/">Harry Potter Quiz</a>
            <a role="menuitem" href="https://worm-attack-3000.data-tales.dev/">Wurm Attacke 3000</a>
          </div>
      </div>

      <div class="header-actions">
        <div class="header-note" aria-label="Feedback Kontakt">
          <span class="header-note__label">Änderung / Kritik:</span>
          <a class="header-note__mail" href="mailto:info@data-tales.dev">info@data-tales.dev</a>
        </div>

        
        <button class="btn btn-ghost" id="themeToggle" type="button" aria-label="Theme umschalten">
          <span aria-hidden="true" id="themeIcon">☾</span>
          <span class="sr-only">Theme umschalten</span>
        </button>
      </div>
    </div>
  </header>

  <main id="main">
    <section class="section">
      <div class="container">
        <p class="kicker">{{ service_name_slug }}</p>
        <h1>{{ page_h1 }}</h1>
        <p class="lead">{{ page_subtitle }}</p>

        <div class="game-wrap">
          <div class="card game-card">
            <div class="hud" role="region" aria-label="Spielstatus">
              <div class="hud-left">
                <div class="hud-row">
                  <span class="tag" id="turnTag">Lade Spiel…</span>
                  <span class="tag" id="windTag">Wind: —</span>
                  <span class="tag" id="weaponTag">Waffe: —</span>
                </div>
                <div class="hud-mini" id="aimTag">Angle: — · Power: —</div>
              </div>
              <div class="hud-row">
                <button class="btn btn-secondary" id="restartBtn" type="button">Neustart</button>
              </div>
            </div>

            <div class="hp-row" aria-label="Healthbars">
              <div class="hp" aria-label="Player 1 Health">
                <div class="hp-top">
                  <div class="hp-name" id="p1Name">Player 1</div>
                  <div class="hp-val" id="p1HpText">100</div>
                </div>
                <div class="hp-bar" aria-hidden="true">
                  <div class="hp-fill" id="p1HpFill"></div>
                </div>
              </div>
              <div class="hp" aria-label="Player 2 Health">
                <div class="hp-top">
                  <div class="hp-name" id="p2Name">Player 2</div>
                  <div class="hp-val" id="p2HpText">100</div>
                </div>
                <div class="hp-bar" aria-hidden="true">
                  <div class="hp-fill" id="p2HpFill"></div>
                </div>
              </div>
            </div>

            <div class="canvas-wrap">
              <canvas id="gameCanvas" aria-label="Mini Worms Spielfeld"></canvas>

              <div id="fallback" class="card fallback" role="alert">
                <h3>Spiel konnte nicht initialisiert werden</h3>
                <p class="muted">
                  Bitte prüfe, ob dein Browser <code>&lt;canvas&gt;</code> und JavaScript unterstützt.
                  Du kannst die Seite neu laden oder einen anderen Browser verwenden.
                </p>
              </div>

              <noscript>
                <div class="card fallback" role="alert">
                  <h3>JavaScript ist deaktiviert</h3>
                  <p class="muted">Dieses Mini-Game benötigt JavaScript für Rendering und Eingabe.</p>
                </div>
              </noscript>
            </div>

            <div class="game-foot muted" aria-label="Steuerung">
              <div><strong>Steuerung (immer nur der aktive Spieler):</strong></div>
              <div>Angle: <strong>↑/↓</strong> oder <strong>W/S</strong> · Schießen: <strong>Space</strong>/<strong>Enter</strong> (halten zum Aufladen)</div>
              <div>Waffen: <strong>1</strong> Bazooka · <strong>2</strong> Granate · <strong>3</strong> Banane · Restart: <strong>R</strong> oder Button</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>

  <div class="toast" id="toast" aria-live="polite"></div>

  <script>
    (function(){
    const dd = document.querySelector('[data-dropdown]');
    if(!dd) return;

    const btn = dd.querySelector('.nav-dropbtn');
    const menu = dd.querySelector('.nav-menu');

    function setOpen(isOpen){
      btn.setAttribute('aria-expanded', String(isOpen));
      if(isOpen){
        menu.hidden = false;
        dd.classList.add('open');
      }else{
        menu.hidden = true;
        dd.classList.remove('open');
      }
    }

    btn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      const isOpen = btn.getAttribute('aria-expanded') === 'true';
      setOpen(!isOpen);
    });

    document.addEventListener('click', (e) => {
      if(!dd.contains(e.target)) setOpen(false);
    });

    document.addEventListener('keydown', (e) => {
      if(e.key === 'Escape') setOpen(false);
    });

    // Wenn per Tab aus dem Dropdown rausnavigiert wird: schließen
    dd.addEventListener('focusout', () => {
      requestAnimationFrame(() => {
        if(!dd.contains(document.activeElement)) setOpen(false);
      });
    });

    // Initial geschlossen
    setOpen(false);
  })();
  (function(){
    "use strict";

    var $ = function(sel){ return document.querySelector(sel); };

    var fallback = $("#fallback");
    var toastEl = $("#toast");
    var themeToggle = $("#themeToggle");

    function safeText(el, txt){
      if(!el) return;
      el.textContent = String(txt);
    }

    function showFallback(title, msg){
      if(!fallback) return;
      fallback.style.display = "flex";
      var h = fallback.querySelector("h3");
      var p = fallback.querySelector("p");
      if(h) h.textContent = title || "Fehler";
      if(p) p.textContent = msg || "Unbekannter Fehler.";
    }

    function hideFallback(){
      if(!fallback) return;
      fallback.style.display = "none";
    }

    function showToast(msg){
      try{
        safeText(toastEl, msg);
        toastEl.classList.add("show");
        window.clearTimeout(showToast._t);
        showToast._t = window.setTimeout(function(){
          toastEl.classList.remove("show");
        }, 1600);
      }catch(_e){}
    }

    function setTheme(theme){
      var root = document.documentElement;
      var icon = themeToggle ? themeToggle.querySelector('span[aria-hidden="true"]') : null;

      if(theme === "light"){
        root.setAttribute("data-theme", "light");
        if(icon) icon.textContent = "☀";
      }else{
        root.removeAttribute("data-theme");
        if(icon) icon.textContent = "☾";
      }
    }

    function loadTheme(){
      var t = null;
      try{ t = localStorage.getItem("theme"); }catch(_e){}
      setTheme(t === "light" ? "light" : "dark");
    }

    function toggleTheme(){
      var isLight = document.documentElement.getAttribute("data-theme") === "light";
      var next = isLight ? "dark" : "light";
      try{ localStorage.setItem("theme", next); }catch(_e){}
      setTheme(next);
      if(Game && Game.refreshPalette) Game.refreshPalette();
    }

    loadTheme();
    if(themeToggle){
      themeToggle.addEventListener("click", toggleTheme);
    }

    function cssVar(name){
      return window.getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    }

    function clamp(v, a, b){
      return Math.max(a, Math.min(b, v));
    }

    function lerp(a, b, t){
      return a + (b - a) * t;
    }

    function hexToRgb(hex){
      var h = (hex || "").trim();
      if(!h) return {r:255,g:255,b:255};
      if(h.indexOf("#") === 0) h = h.slice(1);
      if(h.length === 3){
        h = h[0]+h[0]+h[1]+h[1]+h[2]+h[2];
      }
      var n = parseInt(h, 16);
      if(!isFinite(n)) return {r:255,g:255,b:255};
      return { r: (n >> 16) & 255, g: (n >> 8) & 255, b: n & 255 };
    }

    function rgba(rgb, a){
      return "rgba(" + rgb.r + "," + rgb.g + "," + rgb.b + "," + a + ")";
    }

    function nowMs(){ return performance && performance.now ? performance.now() : Date.now(); }

    var turnTag = $("#turnTag");
    var windTag = $("#windTag");
    var weaponTag = $("#weaponTag");
    var aimTag = $("#aimTag");

    var p1HpText = $("#p1HpText");
    var p2HpText = $("#p2HpText");
    var p1HpFill = $("#p1HpFill");
    var p2HpFill = $("#p2HpFill");

    var restartBtn = $("#restartBtn");
    var canvas = $("#gameCanvas");
    if(!canvas){
      showFallback("Canvas fehlt", "Das Spielfeld-Element wurde nicht gefunden.");
      return;
    }

    var ctx = null;
    try{
      ctx = canvas.getContext("2d", { alpha: true });
    }catch(_e){
      ctx = null;
    }
    if(!ctx){
      showFallback("Canvas nicht verfügbar", "Dein Browser unterstützt das Rendering nicht.");
      return;
    }

    var Game = {};
    var state = null;

    var KEYS = {
      UP: ["ArrowUp", "KeyW"],
      DOWN: ["ArrowDown", "KeyS"],
      LEFT: ["ArrowLeft", "KeyA"],
      RIGHT: ["ArrowRight", "KeyD"],
      FIRE: ["Space", "Enter", "NumpadEnter"],
      W1: ["Digit1"],
      W2: ["Digit2"],
      W3: ["Digit3"],
      RESTART: ["KeyR"]
    };

    function keyIn(code, arr){
      for(var i=0;i<arr.length;i++) if(code === arr[i]) return true;
      return false;
    }

    var palette = {
      primary: hexToRgb("#6ea8fe"),
      primary2: hexToRgb("#8bd4ff"),
      text: "#e6eaf2",
      border: "rgba(255,255,255,.10)"
    };

    function refreshPalette(){
      try{
        palette.primary = hexToRgb(cssVar("--primary"));
        palette.primary2 = hexToRgb(cssVar("--primary2"));
        palette.text = cssVar("--text") || palette.text;
        palette.border = cssVar("--border") || palette.border;
      }catch(_e){}
    }

    function setCanvasSize(){
      var dpr = window.devicePixelRatio || 1;
      var rect = canvas.getBoundingClientRect();
      var w = Math.max(320, Math.floor(rect.width));
      var h = Math.max(320, Math.floor(rect.height));
      canvas.width = Math.floor(w * dpr);
      canvas.height = Math.floor(h * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      return { w: w, h: h };
    }

    function makeTerrain(n){
      var arr = new Array(n);
      var seedA = Math.random() * 1000;
      var seedB = Math.random() * 1000;

      function smoothNoise(t, seed){
        var x = t * 6.0 + seed;
        var s = Math.sin(x) * 0.5 + Math.sin(x*0.37) * 0.3 + Math.sin(x*1.73) * 0.2;
        return s;
      }

      for(var i=0;i<n;i++){
        var t = i / (n - 1);
        var n1 = smoothNoise(t, seedA);
        var n2 = smoothNoise(t, seedB) * 0.6;
        var v = (n1 + n2);
        v = (v + 1.2) / 2.4; // approx 0..1
        v = clamp(v, 0.0, 1.0);
        arr[i] = v;
      }

      // gentle edges: avoid very low/high at extremes
      for(var j=0;j<n;j++){
        var t2 = j / (n - 1);
        var edge = Math.sin(Math.PI * t2);
        arr[j] = lerp(0.55, arr[j], clamp(edge, 0.15, 1.0));
      }
      return arr;
    }

    function terrainYAt(x){
      var w = state.view.w;
      var h = state.view.h;
      var n = state.terrain.length;
      if(w <= 1) return h * 0.75;

      var fx = clamp(x / w, 0, 1);
      var idx = fx * (n - 1);
      var i0 = Math.floor(idx);
      var i1 = Math.min(n - 1, i0 + 1);
      var t = idx - i0;

      var base = lerp(state.terrain[i0], state.terrain[i1], t);
      var minY = h * 0.42;
      var maxY = h * 0.84;
      var y = lerp(maxY, minY, base); // lower value => lower terrain? invert for feel
      return y;
    }

    function applyCrater(cx, cy, r){
      var w = state.view.w;
      var h = state.view.h;
      var n = state.terrain.length;

      var fx0 = clamp((cx - r) / w, 0, 1);
      var fx1 = clamp((cx + r) / w, 0, 1);
      var i0 = Math.floor(fx0 * (n - 1));
      var i1 = Math.ceil(fx1 * (n - 1));

      for(var i=i0; i<=i1; i++){
        var fx = i / (n - 1);
        var x = fx * w;
        var dx = x - cx;
        var adx = Math.abs(dx);
        if(adx > r) continue;

        var depth = Math.sqrt(Math.max(0, r*r - dx*dx));
        var cutY = cy + depth;
        cutY = clamp(cutY, 0, h + 200);

        var curY = terrainYAt(x);

        // If crater would push the surface downward, increase the terrain value locally.
        if(cutY > curY){
          var delta = cutY - curY;          // pixels down
          var denom = Math.max(1, (h * 0.42)); // normalize
          var bump = clamp(delta / denom, 0, 0.45);

          // convert pixel-down into smaller "base" value (since y = lerp(maxY, minY, base))
          // pushing surface down => increase y => decrease base
          state.terrain[i] = clamp(state.terrain[i] - bump, 0.0, 1.0);
        }
      }
    }

    function dist(ax, ay, bx, by){
      var dx = ax - bx, dy = ay - by;
      return Math.sqrt(dx*dx + dy*dy);
    }

    function explosion(cx, cy, radius, maxDmg, crater){
      if(crater) applyCrater(cx, cy, radius);

      var hits = [];
      for(var p=0;p<state.players.length;p++){
        var pl = state.players[p];
        if(!pl.alive) continue;

        var px = pl.x * state.view.w;
        var py = pl.y;

        var d = dist(cx, cy, px, py);
        if(d <= radius + pl.r){
          var t = clamp(d / radius, 0, 1);
          var dmg = Math.round(maxDmg * (1 - t));
          dmg = clamp(dmg, 0, maxDmg);
          if(dmg > 0){
            pl.hp = clamp(pl.hp - dmg, 0, 100);
            hits.push({ id: pl.id, dmg: dmg });
          }
        }
      }

      state.fx.explosion = {
        x: cx, y: cy,
        r: radius,
        started: nowMs(),
        dur: 360
      };

      // Trigger falling if ground changed under worms
      for(var p2=0;p2<state.players.length;p2++){
        var pl2 = state.players[p2];
        if(!pl2.alive) continue;
        pl2.falling = true;
      }

      return hits;
    }

    function allPlayersStable(){
      for(var i=0;i<state.players.length;i++){
        var pl = state.players[i];
        if(!pl.alive) continue;
        if(pl.falling) return false;
      }
      return true;
    }

    function checkGameOver(){
      var alive = state.players.filter(function(p){ return p.hp > 0; });
      if(alive.length <= 1){
        state.phase = "gameover";
        state.inputLocked = true;
        var winner = alive.length === 1 ? alive[0] : null;
        state.winner = winner ? winner.id : 0;
        showToast(winner ? ("Game Over: " + winner.name + " gewinnt!") : "Game Over: Unentschieden");
        return true;
      }
      return false;
    }

    var WEAPONS = {
      bazooka: { key:"bazooka", name:"Bazooka", projR: 3.5, radius: 26, maxDmg: 55, fuse: 0.0, bounce: 0 },
      grenade: { key:"grenade", name:"Granate", projR: 4.2, radius: 34, maxDmg: 65, fuse: 2.6, bounce: 2 },
      banana:  { key:"banana",  name:"Banane",  projR: 4.6, radius: 46, maxDmg: 85, fuse: 0.0, bounce: 0 }
    };

    function weaponBySlot(slot){
      if(slot === 1) return WEAPONS.bazooka;
      if(slot === 2) return WEAPONS.grenade;
      return WEAPONS.banana;
    }

    function setWeapon(slot){
      state.weaponSlot = clamp(slot, 1, 3);
      state.weapon = weaponBySlot(state.weaponSlot);
      safeText(weaponTag, "Waffe: " + state.weapon.name);
    }

    function newTurn(){
      state.active = 1 - state.active;
      state.angleDeg = 45;
      state.power = 62;
      state.inputLocked = false;
      state.phase = "aim";
      state.projectile = null;
      state.pendingSwitch = false;
      state.postShotHold = 0;

      state.wind = (Math.random() * 2 - 1) * 55; // px/s^2
      updateHud();
    }

    function startGame(){
      refreshPalette();

      state = {
        view: setCanvasSize(),
        terrainN: 620,
        terrain: makeTerrain(620),
        players: [
          { id: 1, name: "Player 1", x: 0.18, y: 0, r: 12, hp: 100, vy: 0, falling: false, alive: true },
          { id: 2, name: "Player 2", x: 0.82, y: 0, r: 12, hp: 100, vy: 0, falling: false, alive: true }
        ],
        active: 0,
        angleDeg: 45,
        power: 62,
        weaponSlot: 1,
        weapon: WEAPONS.bazooka,
        wind: 0,
        gravity: 420,
        projectile: null,
        phase: "aim",
        inputLocked: false,
        fx: { explosion: null },
        pendingSwitch: false,
        postShotHold: 0,
        winner: 0,
        isCharging: false,
        _lastAimToast: 0
      };

      // place worms on ground
      for(var i=0;i<state.players.length;i++){
        var pl = state.players[i];
        var px = pl.x * state.view.w;
        pl.y = terrainYAt(px) - pl.r - 1;
        pl.vy = 0;
        pl.falling = false;
        pl.alive = true;
        pl.hp = 100;
      }

      state.active = 0;
      state.wind = (Math.random() * 2 - 1) * 55;
      setWeapon(1);

      state.phase = "aim";
      state.inputLocked = false;
      state.projectile = null;

      hideFallback();
      updateHud();
      showToast("Player 1 am Zug");
    }

    function updateHud(){
      if(!state) return;

      var p1 = state.players[0];
      var p2 = state.players[1];

      safeText(p1HpText, String(Math.round(p1.hp)));
      safeText(p2HpText, String(Math.round(p2.hp)));

      var p1Scale = clamp(p1.hp / 100, 0, 1);
      var p2Scale = clamp(p2.hp / 100, 0, 1);

      if(p1HpFill) p1HpFill.style.transform = "scaleX(" + p1Scale.toFixed(3) + ")";
      if(p2HpFill) p2HpFill.style.transform = "scaleX(" + p2Scale.toFixed(3) + ")";

      var activeId = state.players[state.active].id;
      safeText(turnTag, "Player " + activeId + " am Zug");

      var w = Math.round(Math.abs(state.wind));
      var dir = state.wind < -1 ? "←" : (state.wind > 1 ? "→" : "·");
      safeText(windTag, "Wind: " + dir + " " + w);

      safeText(weaponTag, "Waffe: " + state.weapon.name);

      safeText(aimTag, "Angle: " + Math.round(state.angleDeg) + "° · Power: " + Math.round(state.power));
    }

    function fire(){
      if(state.inputLocked) return;
      if(state.phase !== "aim") return;

      var shooter = state.players[state.active];
      if(shooter.hp <= 0) return;

      state.inputLocked = true;
      state.phase = "projectile";

      var w = state.view.w;
      var h = state.view.h;

      var sx = shooter.x * w;
      var sy = shooter.y - shooter.r * 0.15;

      var dir = (shooter.id === 1) ? 1 : -1;

      var angleDeg = state.angleDeg;
      if(dir === -1) angleDeg = 180 - angleDeg;
      var angleRad = (angleDeg * Math.PI / 180);
      var speed = 120 + (state.power / 100) * 520;

      var vx = Math.cos(angleRad) * speed;
      var vy = -Math.sin(angleRad) * speed;

      state.projectile = {
        x: sx + dir * (shooter.r + 2),
        y: sy - shooter.r * 0.1,
        vx: vx,
        vy: vy,
        r: state.weapon.projR,
        age: 0,
        bounces: 0,
        fuse: state.weapon.fuse,
        exploded: false,
        owner: shooter.id
      };
    }

    function endShotAndSwitch(msg){
      state.projectile = null;
      state.phase = "post";
      state.pendingSwitch = true;
      state.postShotHold = 0;
      if(msg) showToast(msg);
    }

    function impactExplode(cx, cy){
      var wpn = state.weapon;
      var hits = explosion(cx, cy, wpn.radius, wpn.maxDmg, true);

      if(hits.length){
        var txt = hits.map(function(h){ return "P" + h.id + " -" + h.dmg; }).join(" · ");
        showToast("Treffer! " + txt);
      }else{
        showToast("Boom!");
      }

      if(checkGameOver()) return;

      endShotAndSwitch(null);
    }

    function projectileCollidesWorm(px, py){
      for(var i=0;i<state.players.length;i++){
        var pl = state.players[i];
        if(pl.hp <= 0) continue;
        var wx = pl.x * state.view.w;
        var wy = pl.y;
        if(dist(px, py, wx, wy) <= pl.r + (state.projectile ? state.projectile.r : 3)){
          return { pl: pl, x: wx, y: wy };
        }
      }
      return null;
    }

    function updateWormPhysics(dt){
      var w = state.view.w;
      for(var i=0;i<state.players.length;i++){
        var pl = state.players[i];
        if(pl.hp <= 0){
          pl.alive = false;
          continue;
        }
        pl.alive = true;

        var px = pl.x * w;
        var gy = terrainYAt(px) - pl.r - 1;

        // If worm is above ground -> fall
        if(pl.y < gy - 0.5){
          pl.falling = true;
        }

        if(pl.falling){
          pl.vy += state.gravity * dt;
          pl.y += pl.vy * dt;

          var gy2 = terrainYAt(px) - pl.r - 1;
          if(pl.y >= gy2){
            pl.y = gy2;
            pl.vy = 0;
            pl.falling = false;
          }
        }else{
          // keep pinned to ground if terrain rises slightly
          pl.y = terrainYAt(px) - pl.r - 1;
          pl.vy = 0;
        }

        // out of bounds (optional "fall out")
        if(pl.y > state.view.h + 80){
          pl.hp = 0;
          pl.alive = false;
        }
      }
    }

    function updateProjectile(dt){
      var p = state.projectile;
      if(!p) return;

      var w = state.view.w;
      var h = state.view.h;

      var steps = 4; // reduce tunneling
      var sub = dt / steps;

      for(var s=0; s<steps; s++){
        p.age += sub;

        // fuse for grenade
        if(state.weapon.key === "grenade" && p.fuse > 0 && p.age >= p.fuse){
          impactExplode(p.x, p.y);
          return;
        }

        // integrate
        p.vx += state.wind * sub;
        p.vy += state.gravity * sub;
        p.x += p.vx * sub;
        p.y += p.vy * sub;

        // worm collision
        var hit = projectileCollidesWorm(p.x, p.y);
        if(hit){
          impactExplode(p.x, p.y);
          return;
        }

        // bounds
        if(p.x < -80 || p.x > w + 80 || p.y > h + 120 || p.y < -160){
          endShotAndSwitch("Verfehlt.");
          return;
        }

        // terrain collision
        var gy = terrainYAt(p.x);
        if(p.y + p.r >= gy){
          if(state.weapon.key === "grenade" && p.bounces < state.weapon.bounce){
            // bounce with simple normal from slope
            var eps = 6;
            var gyL = terrainYAt(p.x - eps);
            var gyR = terrainYAt(p.x + eps);
            var dx = 2*eps;
            var dy = gyR - gyL;
            // tangent (dx, dy) => normal (-dy, dx)
            var nx = -dy;
            var ny = dx;
            var nlen = Math.sqrt(nx*nx + ny*ny) || 1;
            nx /= nlen; ny /= nlen;

            // reflect v around normal
            var dot = p.vx * nx + p.vy * ny;
            p.vx = p.vx - 2 * dot * nx;
            p.vy = p.vy - 2 * dot * ny;

            // restitution + friction
            p.vx *= 0.62;
            p.vy *= 0.55;

            // reposition above ground
            p.y = gy - p.r - 1;

            p.bounces += 1;
            if(p.bounces >= state.weapon.bounce){
              // let it still fly until fuse expires
            }
          }else{
            impactExplode(p.x, gy - 1);
            return;
          }
        }
      }
    }

    function updatePost(dt){
      // Let worms settle a bit before switching
      state.postShotHold += dt;

      updateWormPhysics(dt);

      if(checkGameOver()) return;

      if(state.postShotHold > 0.25 && allPlayersStable()){
        newTurn();
        showToast("Player " + state.players[state.active].id + " am Zug");
      }else if(state.postShotHold > 2.25){
        // hard timeout to avoid getting stuck
        newTurn();
        showToast("Player " + state.players[state.active].id + " am Zug");
      }
    }

    function update(dt){
      if(!state) return;

      if(state.phase === "aim"){
        if(state.isCharging){
          state.power = clamp(state.power + 45 * dt, 10, 100);
        }
        updateWormPhysics(dt);
      }else if(state.phase === "projectile"){
        updateProjectile(dt);
        updateWormPhysics(dt);
      }else if(state.phase === "post"){
        updatePost(dt);
      }else if(state.phase === "gameover"){
        updateWormPhysics(dt);
      }

      // explosion fx auto-clear
      if(state.fx.explosion){
        var t = nowMs() - state.fx.explosion.started;
        if(t > state.fx.explosion.dur){
          state.fx.explosion = null;
        }
      }

      updateHud();
    }

    function drawTerrain(){
      var w = state.view.w;
      var h = state.view.h;

      var c1 = palette.primary;
      var c2 = palette.primary2;

      ctx.beginPath();
      ctx.moveTo(0, h);
      ctx.lineTo(0, terrainYAt(0));

      var step = Math.max(2, Math.floor(w / 220));
      for(var x=0; x<=w; x+=step){
        ctx.lineTo(x, terrainYAt(x));
      }
      ctx.lineTo(w, terrainYAt(w));
      ctx.lineTo(w, h);
      ctx.closePath();

      var grad = ctx.createLinearGradient(0, h*0.4, 0, h);
      grad.addColorStop(0, rgba(c1, 0.14));
      grad.addColorStop(1, rgba(c2, 0.10));
      ctx.fillStyle = grad;
      ctx.fill();

      // outline
      ctx.beginPath();
      ctx.moveTo(0, terrainYAt(0));
      for(var xx=0; xx<=w; xx+=step){
        ctx.lineTo(xx, terrainYAt(xx));
      }
      ctx.strokeStyle = rgba(c1, 0.22);
      ctx.lineWidth = 2;
      ctx.stroke();
    }

    function drawWorm(pl){
      var w = state.view.w;
      var px = pl.x * w;
      var py = pl.y;

      var col = (pl.id === 1) ? palette.primary : palette.primary2;

      ctx.beginPath();
      ctx.arc(px, py, pl.r, 0, Math.PI*2);
      ctx.fillStyle = rgba(col, 0.92);
      ctx.fill();

      ctx.lineWidth = 2;
      ctx.strokeStyle = rgba(col, 0.30);
      ctx.stroke();

      // active marker
      if(state.phase !== "gameover" && state.players[state.active].id === pl.id){
        ctx.beginPath();
        ctx.arc(px, py - pl.r - 10, 5, 0, Math.PI*2);
        ctx.fillStyle = rgba(col, 0.75);
        ctx.fill();
      }
    }

    function drawProjectile(){
      var p = state.projectile;
      if(!p) return;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI*2);
      ctx.fillStyle = rgba(palette.primary, 0.35);
      ctx.fill();

      ctx.lineWidth = 2;
      ctx.strokeStyle = rgba(palette.primary2, 0.35);
      ctx.stroke();
    }

    function drawExplosionFx(){
      var fx = state.fx.explosion;
      if(!fx) return;

      var t = clamp((nowMs() - fx.started) / fx.dur, 0, 1);
      var r = lerp(6, fx.r, t);
      var a = lerp(0.42, 0.0, t);

      ctx.beginPath();
      ctx.arc(fx.x, fx.y, r, 0, Math.PI*2);
      ctx.fillStyle = rgba(palette.primary2, a);
      ctx.fill();

      ctx.beginPath();
      ctx.arc(fx.x, fx.y, r * 0.72, 0, Math.PI*2);
      ctx.fillStyle = rgba(palette.primary, a * 0.9);
      ctx.fill();
    }

    function drawAimPreview(){
      if(state.inputLocked) return;
      if(state.phase !== "aim") return;

      var shooter = state.players[state.active];
      if(!shooter || shooter.hp <= 0) return;

      var w = state.view.w;

      var dir = (shooter.id === 1) ? 1 : -1;
      var angleDeg = state.angleDeg;
      if(dir === -1) angleDeg = 180 - angleDeg;
      var angle = angleDeg * Math.PI / 180;
      var speed = 120 + (state.power / 100) * 520;

      var x = shooter.x * w + dir * (shooter.r + 2);
      var y = shooter.y - shooter.r * 0.15;

      var vx = Math.cos(angle) * speed;
      var vy = -Math.sin(angle) * speed;

      var points = 26;
      var stepT = 0.10;
      var px = x, py = y, pvx = vx, pvy = vy;

      ctx.save();
      ctx.lineWidth = 0;
      for(var i=0;i<points;i++){
        pvx += state.wind * stepT;
        pvy += state.gravity * stepT;
        px += pvx * stepT;
        py += pvy * stepT;

        if(px < -40 || px > state.view.w + 40 || py > state.view.h + 40) break;

        var gy = terrainYAt(px);
        if(py >= gy) break;

        ctx.beginPath();
        ctx.arc(px, py, 2.1, 0, Math.PI*2);
        ctx.fillStyle = rgba((shooter.id === 1) ? palette.primary : palette.primary2, 0.55);
        ctx.fill();
      }
      ctx.restore();

      // aim line
      var ax = x;
      var ay = y;
      var lx = ax + Math.cos(angle) * 34 * dir;
      var ly = ay - Math.sin(angle) * 34;

      ctx.beginPath();
      ctx.moveTo(ax, ay);
      ctx.lineTo(lx, ly);
      ctx.strokeStyle = rgba((shooter.id === 1) ? palette.primary : palette.primary2, 0.55);
      ctx.lineWidth = 3;
      ctx.stroke();
    }

    function drawGameOverOverlay(){
      if(state.phase !== "gameover") return;

      var w = state.view.w;
      var h = state.view.h;

      ctx.save();
      ctx.fillStyle = "rgba(0,0,0,0.25)";
      ctx.fillRect(0, 0, w, h);

      var text = "Game Over";
      var sub = (state.winner === 1) ? "Player 1 gewinnt" : (state.winner === 2 ? "Player 2 gewinnt" : "Unentschieden");

      ctx.fillStyle = palette.text;
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.font = "800 32px " + cssVar("--font");
      ctx.fillText(text, w/2, h*0.44);
      ctx.font = "700 16px " + cssVar("--font");
      ctx.fillText(sub + " · Restart: R", w/2, h*0.52);
      ctx.restore();
    }

    function render(){
      if(!state) return;

      var w = state.view.w;
      var h = state.view.h;

      // clear
      ctx.clearRect(0, 0, w, h);

      // subtle canvas haze
      var g = ctx.createLinearGradient(0, 0, 0, h);
      g.addColorStop(0, rgba(palette.primary, 0.08));
      g.addColorStop(1, rgba(palette.primary2, 0.05));
      ctx.fillStyle = g;
      ctx.fillRect(0, 0, w, h);

      drawTerrain();
      drawAimPreview();

      for(var i=0;i<state.players.length;i++){
        drawWorm(state.players[i]);
      }

      drawProjectile();
      drawExplosionFx();
      drawGameOverOverlay();
    }

    var lastT = nowMs();
    function loop(){
      var t = nowMs();
      var dt = (t - lastT) / 1000;
      lastT = t;
      dt = clamp(dt, 0, 0.033);

      update(dt);
      render();

      requestAnimationFrame(loop);
    }

    function preventScrollKeys(e){
      // prevent scroll for game keys
      var code = e.code;
      if(
        keyIn(code, KEYS.UP) || keyIn(code, KEYS.DOWN) ||
        keyIn(code, KEYS.LEFT) || keyIn(code, KEYS.RIGHT) ||
        keyIn(code, KEYS.FIRE)
      ){
        e.preventDefault();
      }
    }

    function onKeyDown(e){
      preventScrollKeys(e);
      if(!state) return;

      var code = e.code;

      if(keyIn(code, KEYS.RESTART)){
        startGame();
        return;
      }

      if(state.phase === "gameover"){
        return;
      }

      if(keyIn(code, KEYS.W1)) { setWeapon(1); return; }
      if(keyIn(code, KEYS.W2)) { setWeapon(2); return; }
      if(keyIn(code, KEYS.W3)) { setWeapon(3); return; }

      if(state.inputLocked) return;
      if(state.phase !== "aim") return;

      if(keyIn(code, KEYS.UP)){
        state.angleDeg = clamp(state.angleDeg + 2, 10, 80);
        return;
      }
      if(keyIn(code, KEYS.DOWN)){
        state.angleDeg = clamp(state.angleDeg - 2, 10, 80);
        return;
      }
      if(keyIn(code, KEYS.RIGHT)){
        state.power = clamp(state.power + 3, 10, 100);
        return;
      }
      if(keyIn(code, KEYS.LEFT)){
        state.power = clamp(state.power - 3, 10, 100);
        return;
      }
       if(keyIn(code, KEYS.FIRE)){
        if(!state.isCharging){
          state.isCharging = true;
          state.power = 10;
        }
        return;
      }
    }

    function onKeyUp(e){
      if(!state || state.inputLocked || state.phase !== "aim") return;
      var code = e.code;
      if(keyIn(code, KEYS.FIRE)){
        if(state.isCharging){
          state.isCharging = false;
          fire();
        }
      }
    }

    var resizeTimer = 0;
    function onResize(){
      window.clearTimeout(resizeTimer);
      resizeTimer = window.setTimeout(function(){
        if(!state) return;
        // safest: restart on resize to keep terrain + physics consistent
        startGame();
        showToast("Neu gestartet (Resize).");
      }, 200);
    }

    if(restartBtn){
      restartBtn.addEventListener("click", function(){
        startGame();
      });
    }

    // Boot
    try{
      refreshPalette();
      startGame();
      window.addEventListener("keydown", onKeyDown, { passive: false });
      window.addEventListener("keyup", onKeyUp, { passive: false });
      window.addEventListener("resize", onResize);
      requestAnimationFrame(loop);
    }catch(_err){
      showFallback("Spiel konnte nicht gestartet werden", "Bitte Seite neu laden.");
    }

    Game.refreshPalette = refreshPalette;
    hideFallback();
  })();
  </script>
</body>
</html>
"""


def _security_headers(resp):
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    resp.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    resp.headers.setdefault("Cross-Origin-Opener-Policy", "same-origin")
    resp.headers.setdefault("Cross-Origin-Resource-Policy", "same-origin")
    resp.headers.setdefault("Permissions-Policy", "interest-cohort=()")

    # CSP: inline CSS/JS required by spec (single-file HTML)
    resp.headers.setdefault(
        "Content-Security-Policy",
        "default-src 'self'; "
        "base-uri 'self'; "
        "object-src 'none'; "
        "frame-ancestors 'none'; "
        "img-src 'self' data:; "
        "style-src 'self' 'unsafe-inline'; "
        "script-src 'self' 'unsafe-inline'; "
        "connect-src 'self';",
    )
    return resp


@app.after_request
def add_headers(resp):
    _security_headers(resp)
    path = request.path or "/"
    if path == "/":
        resp.headers["Cache-Control"] = "no-store"
    elif path.startswith("/api/"):
        resp.headers["Cache-Control"] = "no-store"
        resp.headers.setdefault("Content-Type", "application/json; charset=utf-8")
    return resp


@app.get("/")
def index():
    html = render_template_string(
        HTML,
        service_name_slug=SERVICE_NAME_SLUG,
        page_title=PAGE_TITLE,
        page_h1=PAGE_H1,
        page_subtitle=PAGE_SUBTITLE,
        landing_url=LANDING_URL,
        cookbook_url=COOKBOOK_URL,
        plz_url=PLZ_URL,
        version=VERSION,
    )
    resp = make_response(html, 200)
    resp.headers["Content-Type"] = "text/html; charset=utf-8"
    return resp


@app.get("/api/health")
def health():
    return jsonify(ok=True)


@app.get("/api/meta")
def meta():
    return jsonify(ok=True, service=SERVICE_NAME_SLUG, version=VERSION)


def _render_error_page(status_code: int, title: str, message: str):
    tmpl = r"""<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="theme-color" content="#0b0f19" />
  <title>{{ title }}</title>
  <style>
    :root{
      --bg: #0b0f19; --bg2:#0f172a; --card:#111a2e; --text:#e6eaf2; --muted:#a8b3cf;
      --border: rgba(255,255,255,.10); --shadow: 0 18px 60px rgba(0,0,0,.35);
      --primary:#6ea8fe; --primary2:#8bd4ff; --focus: rgba(110,168,254,.45);
      --radius: 18px; --container: 1100px; --gap: 18px;
      --font: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji","Segoe UI Emoji";
    }
    [data-theme="light"]{
      --bg:#f6f7fb; --bg2:#ffffff; --card:#ffffff; --text:#111827; --muted:#4b5563;
      --border: rgba(17,24,39,.12); --shadow: 0 18px 60px rgba(17,24,39,.10);
      --primary:#2563eb; --primary2:#0ea5e9; --focus: rgba(37,99,235,.25);
    }
    *{box-sizing:border-box}
    body{
      margin:0; font-family:var(--font);
      background: radial-gradient(1200px 800px at 20% -10%, rgba(110,168,254,.25), transparent 55%),
                  radial-gradient(1000px 700px at 110% 10%, rgba(139,212,255,.20), transparent 55%),
                  linear-gradient(180deg, var(--bg), var(--bg2));
      color:var(--text);
      min-height:100vh;
      display:flex; align-items:center; justify-content:center;
      padding: 28px 18px;
    }
    .container{max-width:var(--container); width:100%}
    .card{
      border:1px solid var(--border);
      border-radius: var(--radius);
      background: rgba(255,255,255,.04);
      padding:18px;
      box-shadow: var(--shadow);
    }
    [data-theme="light"] .card{ background: rgba(255,255,255,.92); }
    h1{margin:0 0 10px; font-size:22px}
    p{margin:0 0 14px; color:var(--muted); line-height:1.6}
    .btn{
      display:inline-flex; align-items:center; justify-content:center;
      padding:10px 14px; border-radius:12px;
      border:1px solid transparent;
      text-decoration:none; font-weight:800;
      color: #0b0f19;
      background: linear-gradient(135deg, var(--primary), var(--primary2));
    }
    [data-theme="light"] .btn{ color:#ffffff; }
  </style>
</head>
<body>
  <div class="container">
    <div class="card">
      <h1>{{ title }}</h1>
      <p>{{ message }}</p>
      <a class="btn" href="/">Zurück zum Spiel</a>
    </div>
  </div>
</body>
</html>"""
    html = render_template_string(tmpl, title=title, message=message)
    resp = make_response(html, status_code)
    resp.headers["Content-Type"] = "text/html; charset=utf-8"
    resp.headers["Cache-Control"] = "no-store"
    return resp


@app.errorhandler(404)
def not_found(_e):
    if (request.path or "").startswith("/api/"):
        return jsonify(ok=False, error="not_found"), 404
    return _render_error_page(404, "Seite nicht gefunden", "Die angeforderte Seite existiert nicht.")


@app.errorhandler(500)
def server_error(_e):
    if (request.path or "").startswith("/api/"):
        return jsonify(ok=False, error="server_error"), 500
    return _render_error_page(500, "Serverfehler", "Ein unerwarteter Fehler ist aufgetreten.")


@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
    # Avoid leaking details
    if (request.path or "").startswith("/api/"):
        return jsonify(ok=False, error="server_error"), 500
    return _render_error_page(500, "Serverfehler", "Ein unerwarteter Fehler ist aufgetreten.")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, debug=False)
