"""
Beyond Nen Fishing - app de pesca com preview em tempo real e pausa segura.
Windows 10/11 + Roblox.

Instalar:
  py -m pip install opencv-python mss numpy pyautogui keyboard pillow

Executar:
  py beyond_nen_app.py

F6 iniciar/pausar | F7 parar | F8 mostrar/ocultar preview | slot da vara configurável
"""

import time
import logging
import threading
import queue
import tkinter as tk
from tkinter import ttk
import ctypes
from ctypes import wintypes

import cv2
import mss
import numpy as np
import pyautogui
import keyboard
from PIL import Image, ImageTk

# Captura e preview independentes da automação
PREVIEW_FPS = 10
SCAN_INTERVAL = 0.035
LOST_SECONDS = 2.0
BITE_TIMEOUT = 50
MAX_RECOVERIES = 3  # Mantido apenas como referência histórica; não limita mais as tentativas.
RECOVERY_UNEQUIP_DELAY = 0.45
RECOVERY_EQUIP_DELAY = 0.85
CAST_DELAY = 0.35
AFTER_CATCH = 1.0
DEADBAND = 3

logging.basicConfig(
    filename="beyond_nen_fishing.log",
    filemode="a",
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
LOGGER = logging.getLogger("BeyondNenFishing")

# Região inicial do minigame em porcentagem da tela.
# Ajustável na própria interface.
DEFAULT_ROI = (0.08, 0.68, 0.84, 0.22)

INPUT_MOUSE = 0
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG), ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD), ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD), ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class INPUT_UNION(ctypes.Union):
    _fields_ = [("mi", MOUSEINPUT)]

class INPUT(ctypes.Structure):
    _fields_ = [("type", wintypes.DWORD), ("union", INPUT_UNION)]

def send_mouse(flag):
    extra = ctypes.c_ulong(0)
    mi = MOUSEINPUT(0, 0, 0, flag, 0, ctypes.pointer(extra))
    inp = INPUT(INPUT_MOUSE, INPUT_UNION(mi=mi))
    ctypes.windll.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))

def mouse_down():
    send_mouse(MOUSEEVENTF_LEFTDOWN)

def mouse_up():
    send_mouse(MOUSEEVENTF_LEFTUP)

def roblox_is_foreground():
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    title = ctypes.create_unicode_buffer(512)
    ctypes.windll.user32.GetWindowTextW(hwnd, title, 512)
    return "roblox" in title.value.lower()

def components(mask, min_area=20):
    n, labels, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    result = []
    for i in range(1, n):
        x, y, w, h, area = stats[i]
        if area >= min_area:
            result.append((int(x), int(y), int(w), int(h), int(area)))
    return result

def get_roi(frame, roi):
    H, W = frame.shape[:2]
    x, y, w, h = roi
    x1 = max(0, min(W - 1, int(x * W)))
    y1 = max(0, min(H - 1, int(y * H)))
    x2 = max(x1 + 1, min(W, int((x + w) * W)))
    y2 = max(y1 + 1, min(H, int((y + h) * H)))
    return frame[y1:y2, x1:x2], (x1, y1, x2-x1, y2-y1)

def detect_bar(frame, roi):
    """
    Detecta a faixa laranja móvel e o marcador branco móvel.
    A borda branca fixa do trilho é descartada pela área do componente:
    no layout de referência, o marcador tem área branca maior que as bordas.
    """
    crop, origin = get_roi(frame, roi)
    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    rh, rw = crop.shape[:2]

    # O alvo do minigame é um retângulo dourado/alaranjado.
    # A restrição de proporção elimina a barra de progresso inferior,
    # que é muito mais comprida e poderia ser escolhida por engano.
    yellow = cv2.inRange(
        hsv, np.array([8, 55, 85], dtype=np.uint8),
        np.array([43, 255, 255], dtype=np.uint8)
    )
    yellow = cv2.morphologyEx(
        yellow, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8)
    )

    targets = []
    for x, y, w, h, area in components(yellow, 65):
        aspect = w / max(h, 1)
        if (
            9 <= w <= rw * 0.18
            and 7 <= h <= rh * 0.75
            and 1.4 <= aspect <= 4.2
            and area >= 65
        ):
            targets.append((x, y, w, h, area))

    if not targets:
        return None, crop, origin, None

    # Escolhe o alvo de formato retangular com maior área.
    targets.sort(key=lambda a: a[4], reverse=True)
    tx, ty, tw, th, _ = targets[0]
    target_cy = ty + th / 2

    # O marcador branco é estreito e alto. As bordas fixas do trilho
    # também são brancas, mas seus componentes costumam ter área menor.
    white = cv2.inRange(
        hsv, np.array([0, 0, 190], dtype=np.uint8),
        np.array([179, 95, 255], dtype=np.uint8)
    )
    white = cv2.morphologyEx(
        white, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8)
    )

    sliders = []
    for x, y, w, h, area in components(white, 12):
        cy = y + h / 2
        if (
            3 <= w <= 40
            and h >= th * 0.70
            and h <= rh * 0.90
            and abs(cy - target_cy) <= max(8, th * 0.30)
        ):
            sliders.append((x, y, w, h, area))

    if not sliders:
        return None, crop, origin, (tx, ty, tw, th, None)

    # Seleciona o componente mais sólido: evita confundir a moldura
    # vertical esquerda/direita do trilho com a barrinha que se move.
    sliders.sort(key=lambda a: (a[4], a[3], a[2]), reverse=True)
    sx, sy, sw, sh, _ = sliders[0]

    det = {
        "slider_left": sx,
        "slider_right": sx + sw,
        "slider_center": sx + sw / 2,
        "slider_width": sw,
        "target_left": tx,
        "target_right": tx + tw,
        "target_center": tx + tw / 2,
        "target_width": tw,
    }
    raw = (tx, ty, tw, th, sx, sy, sw, sh)
    return det, crop, origin, raw

class FishingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Beyond Nen Fishing")
        self.root.geometry("920x760")
        self.root.minsize(760, 650)
        self.root.configure(bg="#171a21")

        self.running = False
        self.closed = False
        self.preview_on = True
        self.mouse_held = False
        self.status = "Captura ao vivo iniciando…"
        self.roi = list(DEFAULT_ROI)
        self.slot_key = "1"
        self.events = queue.Queue()
        self.latest_frame = None
        self.latest_info = "Aguardando captura…"
        self.lock = threading.Lock()
        self.photo = None
        self.worker = threading.Thread(target=self.capture_and_farm_loop, daemon=True)
        LOGGER.info("Aplicativo iniciado. Slot da vara: %s", self.slot_key)
        self.worker.start()

        self.build_ui()
        keyboard.add_hotkey("F6", lambda: self.events.put("toggle"))
        keyboard.add_hotkey("F7", lambda: self.events.put("stop"))
        keyboard.add_hotkey("F8", lambda: self.events.put("preview"))
        self.root.after(80, self.tick)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def build_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10), padding=8)
        style.configure("TLabel", background="#171a21", foreground="#e8eaf0",
                        font=("Segoe UI", 10))
        style.configure("Small.TLabel", background="#171a21", foreground="#aeb6c5",
                        font=("Segoe UI", 9))
        outer = tk.Frame(self.root, bg="#171a21", padx=16, pady=14)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="BEYOND NEN  /  PESCA AUTOMÁTICA",
                  font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(outer, text="A prévia agora captura a tela continuamente, mesmo com a farm pausada.",
                  style="Small.TLabel").pack(anchor="w", pady=(3, 12))

        bar = tk.Frame(outer, bg="#252b38", padx=10, pady=9)
        bar.pack(fill="x")
        ttk.Button(bar, text="▶ Iniciar / pausar (F6)",
                   command=lambda: self.events.put("toggle")).pack(side="left", padx=4)
        ttk.Button(bar, text="■ Parar (F7)",
                   command=lambda: self.events.put("stop")).pack(side="left", padx=4)
        ttk.Button(bar, text="Prévia (F8)",
                   command=lambda: self.events.put("preview")).pack(side="left", padx=4)

        statusbox = tk.Frame(outer, bg="#252b38", padx=11, pady=9)
        statusbox.pack(fill="x", pady=10)
        ttk.Label(statusbox, text="STATUS", style="Small.TLabel").pack(anchor="w")
        self.status_var = tk.StringVar(value=self.status)
        tk.Label(statusbox, textvariable=self.status_var, bg="#252b38", fg="#f4d27a",
                 font=("Segoe UI", 10, "bold"), anchor="w", justify="left",
                 wraplength=850).pack(fill="x", pady=(3, 0))

        slotbox = tk.Frame(outer, bg="#252b38", padx=10, pady=8)
        slotbox.pack(fill="x", pady=(0, 10))
        ttk.Label(slotbox, text="SLOT DA VARA (1 A 9)", style="Small.TLabel").pack(side="left")
        self.slot_var = tk.StringVar(value=self.slot_key)
        slot_spin = ttk.Spinbox(slotbox, from_=1, to=9, width=5, textvariable=self.slot_var,
                                justify="center", command=self.update_slot)
        slot_spin.pack(side="left", padx=(10, 8))
        slot_spin.bind("<KeyRelease>", lambda _e: self.update_slot())
        slot_spin.bind("<FocusOut>", lambda _e: self.update_slot())
        ttk.Label(slotbox, text="Usado para desequipar e reequipar a vara em uma recuperação automática.",
                  style="Small.TLabel").pack(side="left")

        ttk.Label(outer, text="CAPTURA AO VIVO — retângulo vermelho = área analisada",
                  style="Small.TLabel").pack(anchor="w", pady=(3, 5))
        self.preview = tk.Label(outer, bg="#080a0e", fg="#aeb6c5",
                                text="Capturando tela…", font=("Segoe UI", 10))
        self.preview.pack(fill="both", expand=True)

        settings = tk.Frame(outer, bg="#252b38", padx=10, pady=9)
        settings.pack(fill="x", pady=(10, 0))
        ttk.Label(settings, text="ÁREA DO MINIGAME",
                  style="Small.TLabel").pack(anchor="w", pady=(0, 7))
        actions = tk.Frame(settings, bg="#252b38")
        actions.pack(fill="x")
        ttk.Button(actions, text="▧ Selecionar área na tela",
                   command=self.start_area_selection).pack(side="left", padx=(0, 8))
        ttk.Button(actions, text="Restaurar área padrão",
                   command=self.reset_roi).pack(side="left")
        self.area_var = tk.StringVar(value="Área padrão: X 8% • Y 68% • L 84% • A 22%")
        tk.Label(settings, textvariable=self.area_var, bg="#252b38", fg="#f4d27a",
                 font=("Segoe UI", 9), anchor="w").pack(fill="x", pady=(7, 0))
        ttk.Label(outer, text="F6 iniciar/pausar • F7 parar • F8 prévia • Selecione com o mouse a região que contém a barra de pesca.",
                  style="Small.TLabel").pack(anchor="w", pady=(8, 0))

    def update_slot(self):
        try:
            value = int(self.slot_var.get())
            if 1 <= value <= 9:
                self.slot_key = str(value)
        except (ValueError, tk.TclError):
            pass

    def recover_fishing(self, reason):
        """Solta o mouse, alterna o slot da vara e prepara um novo lançamento."""
        LOGGER.warning("Iniciando recuperação da pesca: %s", reason)
        self.release()
        self.status = f"Recuperação automática: {reason} — desequipando a vara (slot {self.slot_key})…"
        pyautogui.press(self.slot_key)
        time.sleep(RECOVERY_UNEQUIP_DELAY)
        pyautogui.press(self.slot_key)
        self.status = f"Recuperação automática: vara reequipada no slot {self.slot_key}; preparando novo lançamento…"
        time.sleep(RECOVERY_EQUIP_DELAY)
        LOGGER.info("Recuperação da vara concluída.")

    def start_area_selection(self):
        if self.running:
            self.status = "Pause a farm (F6) antes de selecionar a área."
            return
        self.status = "Seleção de área: arraste um retângulo em volta da barra do minigame."
        self.root.withdraw()
        self.root.after(300, self.open_selection_overlay)

    def open_selection_overlay(self):
        try:
            with mss.mss() as sct:
                mon = sct.monitors[1]
                shot = np.array(sct.grab(mon))
            frame = cv2.cvtColor(shot, cv2.COLOR_BGRA2RGB)
            screen_h, screen_w = frame.shape[:2]

            overlay = tk.Toplevel(self.root)
            overlay.overrideredirect(True)
            overlay.attributes("-topmost", True)
            overlay.geometry(f"{screen_w}x{screen_h}+0+0")
            overlay.configure(bg="black")

            # Escala a captura para caber no canvas mantendo proporção.
            canvas = tk.Canvas(overlay, width=screen_w, height=screen_h,
                               highlightthickness=0, cursor="crosshair")
            canvas.pack(fill="both", expand=True)
            photo = ImageTk.PhotoImage(Image.fromarray(frame))
            canvas.create_image(0, 0, image=photo, anchor="nw")
            canvas.image = photo
            canvas.create_rectangle(12, 12, 650, 58, fill="#111827",
                                    outline="#f4d27a", width=2)
            canvas.create_text(24, 22, anchor="nw",
                               text="ARRASTE PARA SELECIONAR A ÁREA DO MINIGAME",
                               fill="white", font=("Segoe UI", 14, "bold"))
            canvas.create_text(24, 42, anchor="nw",
                               text="Enter: confirmar • Esc: cancelar",
                               fill="#f4d27a", font=("Segoe UI", 10))

            state = {"x0": None, "y0": None, "rect": None}

            def on_down(event):
                state["x0"], state["y0"] = event.x, event.y
                if state["rect"] is not None:
                    canvas.delete(state["rect"])
                state["rect"] = canvas.create_rectangle(
                    event.x, event.y, event.x, event.y,
                    outline="#00ff66", width=3, fill="#00ff66", stipple="gray25")

            def on_move(event):
                if state["x0"] is not None and state["rect"] is not None:
                    canvas.coords(state["rect"], state["x0"], state["y0"], event.x, event.y)

            def finish_selection(event=None):
                if state["x0"] is None or state["rect"] is None:
                    return
                ex = event.x if event is not None else canvas.winfo_pointerx() - overlay.winfo_rootx()
                ey = event.y if event is not None else canvas.winfo_pointery() - overlay.winfo_rooty()
                x1, x2 = sorted((state["x0"], ex))
                y1, y2 = sorted((state["y0"], ey))
                x1, x2 = max(0, min(screen_w, x1)), max(0, min(screen_w, x2))
                y1, y2 = max(0, min(screen_h, y1)), max(0, min(screen_h, y2))
                if x2 - x1 < 30 or y2 - y1 < 20:
                    self.status = "Área muito pequena. Selecione uma região maior."
                    return
                self.roi = [x1/screen_w, y1/screen_h,
                            (x2-x1)/screen_w, (y2-y1)/screen_h]
                self.area_var.set(
                    f"Área selecionada: X {x1} • Y {y1} • L {x2-x1} • A {y2-y1}"
                )
                self.status = "Área selecionada! A prévia destacará a região em vermelho."
                overlay.destroy()
                self.root.deiconify()
                self.root.lift()

            def cancel(_event=None):
                overlay.destroy()
                self.root.deiconify()
                self.root.lift()
                self.status = "Seleção cancelada; área anterior mantida."

            canvas.bind("<ButtonPress-1>", on_down)
            canvas.bind("<B1-Motion>", on_move)
            canvas.bind("<ButtonRelease-1>", finish_selection)
            overlay.bind("<Escape>", cancel)
            overlay.bind("<Return>", finish_selection)
            overlay.focus_force()
            self._selection_overlay = overlay
        except Exception as exc:
            self.root.deiconify()
            self.status = f"Não foi possível abrir a seleção: {exc}"

    def reset_roi(self):
        self.roi = list(DEFAULT_ROI)
        self.area_var.set("Área padrão: X 8% • Y 68% • L 84% • A 22%")
        self.status = "Área padrão restaurada."

    def release(self):
        mouse_up()
        self.mouse_held = False

    def toggle(self):
        self.running = not self.running
        LOGGER.info("F6: farm %s pelo usuário.", "iniciada" if self.running else "pausada")
        if not self.running:
            self.release()
            self.status = "Farm pausada."
        else:
            self.status = "Farm ativa — clique no Roblox para deixá-lo em primeiro plano."

    def stop(self):
        LOGGER.info("F7: parada solicitada pelo usuário.")
        self.running = False
        self.release()
        self.status = "Parada. Botão esquerdo solto."

    def capture_and_farm_loop(self):
        cast_time = 0.0
        next_cast_at = 0.0
        last_seen = 0.0
        in_game = False
        candidate_frames = 0
        recovery_count = 0
        consecutive_errors = 0
        next_preview = 0.0
        previous_target_center = None
        previous_target_time = None
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            while not self.closed:
                try:
                    # Sempre captura, mesmo quando running=False.
                    shot = np.array(sct.grab(monitor))
                    frame = cv2.cvtColor(shot, cv2.COLOR_BGRA2BGR)
                    now = time.monotonic()
                    roi_snapshot = tuple(self.roi)
                    det, crop, origin, raw = detect_bar(frame, roi_snapshot)

                    if now >= next_preview:
                        preview_frame = frame.copy()
                        ox, oy, ow, oh = origin
                        cv2.rectangle(preview_frame, (ox, oy), (ox+ow, oy+oh), (0, 0, 255), 3)
                        if raw:
                            tx, ty, tw, th = raw[:4]
                            cv2.rectangle(preview_frame, (ox+tx, oy+ty),
                                          (ox+tx+tw, oy+ty+th), (0, 220, 255), 2)
                            if len(raw) == 8 and raw[4] is not None:
                                _, _, _, _, sx, sy, sw, sh = raw
                                cv2.rectangle(preview_frame, (ox+sx, oy+sy),
                                              (ox+sx+sw, oy+sy+sh), (255, 255, 255), 2)
                        with self.lock:
                            self.latest_frame = preview_frame
                            self.latest_info = f"Tela {frame.shape[1]}x{frame.shape[0]} | ROI {ox},{oy},{ow},{oh}"
                        next_preview = now + 1.0 / PREVIEW_FPS

                    if not self.running:
                        if self.mouse_held:
                            self.release()
                        cast_time = 0
                        next_cast_at = 0.0
                        in_game = False
                        previous_target_center = None
                        previous_target_time = None
                        candidate_frames = 0
                        time.sleep(0.04)
                        continue

                    if not roblox_is_foreground():
                        if self.mouse_held:
                            self.release()
                        self.status = "Aguardando Roblox em primeiro plano (Alt+Tab). Prévia continua ao vivo."
                        time.sleep(SCAN_INTERVAL)
                        continue

                    if not in_game and cast_time == 0 and now >= next_cast_at:
                        pyautogui.click(button="left")
                        cast_time = now
                        self.status = "Vara lançada — aguardando minigame…"

                    if det:
                        candidate_frames += 1
                        if candidate_frames < 4 and not in_game:
                            self.status = f"Verificando minigame… ({candidate_frames}/4)"
                        else:
                            in_game = True
                            recovery_count = 0
                            consecutive_errors = 0
                            last_seen = now
                            pos = det["slider_center"]
                            target_center = det["target_center"]

                            # Estima a direção/velocidade do alvo laranja para
                            # compensar deslocamentos durante o ciclo de captura.
                            target_velocity = 0.0
                            if previous_target_center is not None and previous_target_time is not None:
                                dt = max(0.001, now - previous_target_time)
                                target_velocity = (target_center - previous_target_center) / dt
                                target_velocity = max(-500.0, min(500.0, target_velocity))
                            previous_target_center = target_center
                            previous_target_time = now

                            # Pequena previsão (80 ms) reduz atraso na perseguição
                            # quando o alvo laranja está andando pela barra.
                            aim_center = target_center + target_velocity * 0.08
                            switch_margin = max(3.0, det["target_width"] * 0.10)
                            error = aim_center - pos

                            # Controle com histerese: alterna entre segurar (avança)
                            # e soltar (volta), mirando o centro do alvo móvel.
                            # Não mantém o clique indefinidamente ao entrar no alvo.
                            if self.mouse_held:
                                if error < -switch_margin:
                                    self.release()
                                    state = "SOLTO / voltando"
                                else:
                                    state = "SEGURANDO / avançando"
                            else:
                                if error > switch_margin:
                                    mouse_down()
                                    self.mouse_held = True
                                    state = "SEGURANDO / avançando"
                                else:
                                    state = "SOLTO / voltando"

                            self.status = (
                                f"Minigame confirmado | {state} | "
                                f"barra {pos:.1f} | alvo {target_center:.1f} | "
                                f"erro {error:+.1f}px"
                            )
                    else:
                        candidate_frames = 0
                        # Se perder o reconhecimento por um quadro, solta o mouse
                        # imediatamente. Isso evita ficar segurando às cegas.
                        if in_game and self.mouse_held:
                            self.release()
                            self.status = "Alvo temporariamente não detectado — soltando para evitar travamento…"
                        if in_game and now-last_seen > LOST_SECONDS:
                            self.release()
                            in_game = False
                            cast_time = 0
                            next_cast_at = now + AFTER_CATCH
                            previous_target_center = None
                            previous_target_time = None
                            self.status = (
                                "Minigame concluído — aguardando para lançar a próxima vara…"
                            )
                        elif not in_game and cast_time and now-cast_time > BITE_TIMEOUT:
                            cast_time = 0
                            recovery_count += 1
                            self.recover_fishing(
                                f"minigame não apareceu no tempo limite (tentativa {recovery_count})"
                            )
                            in_game = False
                            candidate_frames = 0
                            previous_target_center = None
                            previous_target_time = None
                            # Backoff progressivo: evita relançamentos rápidos se o jogo não responder.
                            retry_delay = min(30.0, 2.0 ** min(recovery_count, 5))
                            next_cast_at = time.monotonic() + retry_delay
                            LOGGER.warning(
                                "Nova tentativa de lançamento agendada em %.1f segundos.",
                                retry_delay,
                            )
                            self.status = (
                                f"Recuperação {recovery_count} concluída — nova tentativa em "
                                f"{retry_delay:.0f}s…"
                            )

                    time.sleep(SCAN_INTERVAL)
                except Exception as exc:
                    # Erro temporário: solta o mouse, guarda e ree equipa a vara
                    # pelo slot configurado, sem gerar cliques de lançamento.
                    self.release()
                    consecutive_errors += 1
                    LOGGER.exception(
                        "Erro durante a pesca (sequência: %s); iniciando recuperação da vara.",
                        consecutive_errors,
                    )
                    cast_time = 0
                    in_game = False
                    candidate_frames = 0
                    recovery_count = 0
                    previous_target_center = None
                    previous_target_time = None
                    try:
                        self.recover_fishing(f"erro temporário ({exc})")
                        retry_delay = min(60.0, 2.0 ** min(consecutive_errors, 6))
                        next_cast_at = time.monotonic() + retry_delay
                        self.status = (
                            f"Vara guardada e reequipada no slot {self.slot_key}. "
                            f"Retomando em {retry_delay:.0f}s…"
                        )
                    except Exception as recovery_exc:
                        LOGGER.exception("Falha ao guardar/reequipar a vara: %s", recovery_exc)
                        retry_delay = min(60.0, 2.0 ** min(consecutive_errors, 6))
                        next_cast_at = time.monotonic() + retry_delay
                        self.status = (
                            f"Não consegui alternar o slot {self.slot_key}; "
                            f"nova tentativa em {retry_delay:.0f}s: {recovery_exc}"
                        )
                    time.sleep(0.2)

    def tick(self):
        while True:
            try:
                action = self.events.get_nowait()
            except queue.Empty:
                break
            if action == "toggle":
                self.toggle()
            elif action == "stop":
                self.stop()
            elif action == "preview":
                self.preview_on = not self.preview_on
                self.status = "Prévia ligada." if self.preview_on else "Prévia desligada."
        self.status_var.set(self.status)
        if self.preview_on:
            with self.lock:
                frame = None if self.latest_frame is None else self.latest_frame.copy()
                info = self.latest_info
            if frame is not None:
                h, w = frame.shape[:2]
                maxw, maxh = 860, 390
                scale = min(maxw/w, maxh/h)
                resized = cv2.resize(frame, (int(w*scale), int(h*scale)))
                rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
                self.photo = ImageTk.PhotoImage(Image.fromarray(rgb))
                self.preview.configure(image=self.photo, text="")
                self.root.title("Beyond Nen Fishing — " + info)
        else:
            self.preview.configure(image="", text="Prévia desligada (F8)")
        self.root.after(80, self.tick)

    def close(self):
        self.running = False
        self.closed = True
        self.release()
        try:
            keyboard.unhook_all_hotkeys()
        except Exception:
            pass
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    FishingApp(root)
    root.mainloop()