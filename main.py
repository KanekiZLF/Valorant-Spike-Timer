# Instale as bibliotecas antes de rodar:
# pip install pygame
# pip install pillow
# pip install keyboard

import pygame
import sys
import keyboard
from PIL import Image
import math
import tkinter as tk
from tkinter import Entry, Label, Button
import webbrowser
import ctypes

# Esconde a janela principal do Tkinter
root = tk.Tk()
root.withdraw()

# --- Configurações Iniciais ---
pygame.init()

# Definir a tela
WIDTH, HEIGHT = 450, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Valorant Spike Timer")

# Cores
WHITE = (255, 255, 255)
DARK_GRAY = (40, 40, 40)
DARKER_GRAY = (25, 25, 25)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Constantes do Temporizador
SPIKE_TIME = 45.0
DEFUSE_TIME = 7.0
TRANSITION_TIME = 10.0

# Variável de teste para adiantar o tempo da spike
TIME_OFFSET = 0.0

# Variáveis de Jogo
timer_active = False
start_time = 0.0
remaining_time = SPIKE_TIME
configured_key = 'f1'
setting_mode = False
custom_spike_time = 0.0

# Variável para o checkbox
blinking_enabled = True # Piscar ativado por padrão

# --- Carregar e Converter a Imagem da Spike ---
try:
    pil_image = Image.open('spike.webp').convert('RGBA')
    pygame_image = pygame.image.fromstring(pil_image.tobytes(), pil_image.size, pil_image.mode)
    spike_size = (200, 200)
    pygame_image = pygame.transform.scale(pygame_image, spike_size)
except Exception as e:
    print(f"Erro ao carregar a imagem da spike: {e}")
    sys.exit()

# --- Fontes ---
font_time = pygame.font.Font(None, 100)
font_button = pygame.font.Font(None, 24)
font_message = pygame.font.Font(None, 30)

# --- Botões ---
config_button_rect = pygame.Rect(10, 10, 150, 30)
about_button_rect = pygame.Rect(WIDTH - 160, 10, 150, 30)
start_stop_button_rect = pygame.Rect(10, HEIGHT - 40, 150, 30)
set_time_button_rect = pygame.Rect(WIDTH - 160, HEIGHT - 40, 150, 30)
checkbox_rect = pygame.Rect(WIDTH - 140, 50, 20, 20)
checkbox_text_pos = (WIDTH - 115, 60)

def draw_buttons():
    # CORREÇÃO: Declara a variável globalmente dentro da função
    global blinking_enabled

    pygame.draw.rect(screen, DARK_GRAY, config_button_rect, border_radius=5)
    text = font_button.render("Configurar Tecla", True, WHITE)
    text_rect = text.get_rect(center=config_button_rect.center)
    screen.blit(text, text_rect)

    pygame.draw.rect(screen, DARK_GRAY, about_button_rect, border_radius=5)
    text = font_button.render("Sobre", True, WHITE)
    text_rect = text.get_rect(center=about_button_rect.center)
    screen.blit(text, text_rect)
    
    pygame.draw.rect(screen, DARK_GRAY, start_stop_button_rect, border_radius=5)
    text_start_stop = "Parar" if timer_active else "Iniciar"
    text = font_button.render(text_start_stop, True, WHITE)
    text_rect = text.get_rect(center=start_stop_button_rect.center)
    screen.blit(text, text_rect)
    
    pygame.draw.rect(screen, DARK_GRAY, set_time_button_rect, border_radius=5)
    text = font_button.render("Definir Tempo", True, WHITE)
    text_rect = text.get_rect(center=set_time_button_rect.center)
    screen.blit(text, text_rect)
    
    pygame.draw.rect(screen, DARK_GRAY, checkbox_rect, border_radius=3)
    if blinking_enabled:
        pygame.draw.rect(screen, GREEN, checkbox_rect.inflate(-4, -4), border_radius=2)
    
    text = font_button.render("Piscar", True, WHITE)
    text_rect = text.get_rect(midleft=(checkbox_text_pos))
    screen.blit(text, text_rect)

def toggle_timer(e=None):
    global timer_active, start_time, remaining_time, setting_mode, custom_spike_time

    if setting_mode:
        return
    
    if not timer_active:
        timer_active = True
        start_time = pygame.time.get_ticks() - (TIME_OFFSET * 1000)
        print("Temporizador iniciado!")
    else:
        timer_active = False
        remaining_time = custom_spike_time if custom_spike_time > 0 else SPIKE_TIME
        print("Temporizador resetado instantaneamente.")

def draw_timer():
    global remaining_time, timer_active, start_time, custom_spike_time
    
    if setting_mode:
        return
    
    start_time_value = custom_spike_time if custom_spike_time > 0 else SPIKE_TIME

    if not timer_active:
        remaining_time = start_time_value
    else:
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        remaining_time = max(0, start_time_value - elapsed_time)
        if remaining_time == 0:
            timer_active = False

    display_time = int(remaining_time)
    text_time = font_time.render(f"{display_time:02d}", True, WHITE)
    text_rect = text_time.get_rect(center=(WIDTH // 2, 120))
    screen.blit(text_time, text_rect)

    blink_speed = 0
    spike_color = WHITE
    if remaining_time > TRANSITION_TIME:
        spike_color = GREEN
        blink_speed = 1.5  
    elif remaining_time > 0:
        if remaining_time >= DEFUSE_TIME:
            lerp_value = 1 - ((remaining_time - DEFUSE_TIME) / (TRANSITION_TIME - DEFUSE_TIME))
            spike_color = (
                int(GREEN[0] * (1 - lerp_value) + RED[0] * lerp_value),
                int(GREEN[1] * (1 - lerp_value) + RED[1] * lerp_value),
                int(GREEN[2] * (1 - lerp_value) + RED[2] * lerp_value)
            )
        else:
            spike_color = RED
            
        lerp_value_blink = 1 - (remaining_time / TRANSITION_TIME)
        start_blink_speed = 1.5
        end_blink_speed = 0.2
        blink_speed = start_blink_speed + (end_blink_speed - start_blink_speed) * lerp_value_blink
    else:
        spike_color = RED
        blink_speed = 0.2
        remaining_time = 0

    current_time = pygame.time.get_ticks() / 1000.0
    
    spike_surface = pygame_image.copy()
    spike_surface.fill(spike_color, special_flags=pygame.BLEND_RGBA_MULT)
    
    if timer_active and blinking_enabled:
        alpha_factor = (math.sin(current_time * (2 * math.pi / blink_speed)) + 1) / 2.0
        alpha = int(255 * alpha_factor)
        spike_surface.set_alpha(alpha)
    else:
        spike_surface.set_alpha(255)

    screen.blit(spike_surface, spike_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))

def show_about_window():
    about_win = tk.Toplevel(root)
    about_win.title("Sobre o Desenvolvedor")
    win_width = 350
    win_height = 150
    try:
        class RECT(ctypes.Structure):
            _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long), ("right", ctypes.c_long), ("bottom", ctypes.c_long),]
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        rect = RECT()
        ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
        pygame_win_x, pygame_win_y = rect.left, rect.top
    except Exception as e:
        print(f"Erro ao obter a posição da janela do Pygame: {e}")
        pygame_win_x, pygame_win_y = 0, 0
    x = pygame_win_x + (WIDTH / 2) - (win_width / 2)
    y = pygame_win_y + (HEIGHT / 2) - (win_height / 2)
    about_win.geometry(f'{win_width}x{win_height}+{int(x)}+{int(y)}')
    about_win.configure(bg="#252525")
    about_win.resizable(False, False)
    tk.Label(about_win, text="Desenvolvido por: Luiz F. R. Pimentel", bg="#252525", fg="white", font=("Arial", 12)).pack(pady=(10, 0))
    tk.Label(about_win, text="Versão: 1.0", bg="#252525", fg="white", font=("Arial", 12)).pack(pady=(5, 0))
    link_label = tk.Label(about_win, text="Conheça o desenvolvedor", bg="#252525", fg="#00BFFF", cursor="hand2", font=("Arial", 12, "underline"))
    link_label.pack(pady=(10, 0))
    link_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/KanekiZLF"))
    close_button = tk.Button(about_win, text="Fechar", command=about_win.destroy, bg="#404040", fg="white", bd=0, relief="flat", font=("Arial", 10))
    close_button.pack(pady=(10, 0))
    about_win.grab_set()
    about_win.wait_window()

def get_spike_time_input():
    global custom_spike_time
    input_win = tk.Toplevel(root)
    input_win.title("Definir Tempo")
    win_width, win_height = 250, 100
    try:
        class RECT(ctypes.Structure):
            _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long), ("right", ctypes.c_long), ("bottom", ctypes.c_long),]
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        rect = RECT()
        ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
        pygame_win_x, pygame_win_y = rect.left, rect.top
    except Exception:
        pygame_win_x, pygame_win_y = 0, 0
    x = pygame_win_x + (WIDTH / 2) - (win_width / 2)
    y = pygame_win_y + (HEIGHT / 2) - (win_height / 2)
    input_win.geometry(f'{win_width}x{win_height}+{int(x)}+{int(y)}')
    input_win.configure(bg="#252525")
    input_win.resizable(False, False)
    Label(input_win, text="Tempo da Spike (segundos):", bg="#252525", fg="white", font=("Arial", 10)).pack(pady=(5,0))
    entry_field = Entry(input_win, width=10)
    entry_field.insert(0, str(int(custom_spike_time if custom_spike_time > 0 else SPIKE_TIME)))
    entry_field.pack(pady=(5,0))
    def on_set(event=None):
        global custom_spike_time
        try:
            new_time = float(entry_field.get())
            if new_time > 0:
                custom_spike_time = new_time
                print(f"Tempo da Spike definido para: {custom_spike_time} segundos.")
            else:
                custom_spike_time = 0.0
                print("Tempo inválido. Usando o padrão de 45 segundos.")
        except ValueError:
            custom_spike_time = 0.0
            print("Entrada inválida. Usando o padrão de 45 segundos.")
        input_win.destroy()
    Button(input_win, text="OK", command=on_set, bg="#404040", fg="white", bd=0, relief="flat", font=("Arial", 10)).pack(pady=(5,0))
    entry_field.bind("<Return>", on_set)
    entry_field.focus_set()
    input_win.grab_set()
    input_win.wait_window()

# --- Loop Principal ---
running = True
clock = pygame.time.Clock()
keyboard.on_press_key(configured_key, toggle_timer)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if config_button_rect.collidepoint(event.pos):
                print("Modo de configuração ativado. Pressione a nova tecla...")
                setting_mode = True
                timer_active = False
                keyboard.unhook_all()
            if about_button_rect.collidepoint(event.pos):
                show_about_window()
            if start_stop_button_rect.collidepoint(event.pos):
                toggle_timer()
            if set_time_button_rect.collidepoint(event.pos):
                get_spike_time_input()
            
            if checkbox_rect.collidepoint(event.pos):
                blinking_enabled = not blinking_enabled
                print(f"Piscar está agora: {'Ativado' if blinking_enabled else 'Desativado'}")

        if setting_mode and event.type == pygame.KEYDOWN:
            new_key = keyboard.get_hotkey_name()
            if new_key:
                print(f"Tecla de atalho definida para: {new_key}")
                configured_key = new_key
                setting_mode = False
                keyboard.on_press_key(configured_key, toggle_timer)

    screen.fill(DARKER_GRAY)
    draw_buttons()
    draw_timer()
    if setting_mode:
        message = "Pressione a nova tecla de atalho..."
        message_text = font_message.render(message, True, WHITE)
        message_rect = message_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(message_text, message_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()