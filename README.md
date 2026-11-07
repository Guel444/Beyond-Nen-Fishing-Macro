# Beyond Nen Fishing Macro

**An automatic fishing macro for Beyond Nen (Roblox), featuring a live screen preview and safe pause controls.**

[English](#english) | [Português](#português)

---

## English

An automatic fishing application for **Beyond Nen (Roblox)**, with a real-time screen preview and controls to start, pause, and stop the automation.

> Designed for Windows 10/11. Roblox must be open and in the foreground while the automatic fishing loop is running.

### Features

- Automatic fishing loop.
- Real-time screen preview, including while the macro is paused.
- Detection of the minigame's moving white marker and orange target.
- Automatic mouse control to keep the marker over the moving target.
- Select the minigame detection area directly on the screen.
- Restore the default detection area.
- Choose the fishing rod hotbar slot (1–9).
- Automatic recovery attempts if the minigame does not appear or an unexpected error occurs.

### Requirements

- Windows 10 or Windows 11.
- Python 3 installed and available through the `py` command.
- Beyond Nen running in Roblox.

### Installation and usage

1. Download the repository using **Code → Download ZIP**, then extract the folder.
2. Run `Instalar_e_abrir.bat`.
3. Wait for the required Python packages to install.
4. Open Roblox and keep its window in the foreground.
5. Click **Start / Pause** or press **F6**.

You can also install the dependencies and run the app manually:

```bat
py -m pip install opencv-python mss numpy pyautogui keyboard pillow
py beyond_nen_app.py
```

### Controls

| Key | Action |
| --- | --- |
| **F6** | Start or pause automatic fishing |
| **F7** | Stop the macro and release the mouse button |
| **F8** | Show or hide the live preview |

The same controls are available through the app buttons.

### Settings

- **Rod slot:** Select the number key (1–9) assigned to the fishing rod. The same slot is used during automatic recovery attempts.
- **Select minigame area:** Pause the macro, then drag a rectangle around the fishing minigame bar to define the detection area.
- **Restore default area:** Reset the detection area to the app's default region.

### Build an executable

Run `Gerar_EXE.bat`. It installs PyInstaller and attempts to create `BeyondNenFishing.exe` in the `dist` folder.

### Notes

- Detection depends on the position and colors of the minigame elements. Adjust the detection area if needed.
- Roblox must remain in the foreground for the macro to send fishing inputs.
- This repository contains the source code and Windows scripts; it does not include a prebuilt executable.
- Python syntax has been checked. This does not count as a full in-game Roblox test.

---

## Português

Aplicativo de pesca automática para **Beyond Nen (Roblox)**, com prévia da tela em tempo real e controles para iniciar, pausar e interromper a automação.

> Projeto para Windows 10/11. O Roblox precisa estar aberto e em primeiro plano durante a pesca automática.

### Recursos

- Pesca automática em loop.
- Prévia da captura de tela em tempo real, inclusive enquanto a farm está pausada.
- Detecção do marcador branco e do alvo laranja móvel do minigame.
- Controle automático do clique para manter o marcador sobre o alvo.
- Seleção da região do minigame diretamente na tela.
- Restauração da região padrão.
- Escolha do slot da vara (1 a 9).
- Tentativas de recuperação automática quando o minigame não aparece ou ocorre uma falha.

### Requisitos

- Windows 10 ou Windows 11.
- Python 3 instalado e disponível pelo comando `py`.
- Beyond Nen aberto no Roblox.

### Instalação e execução

1. Baixe o repositório pelo botão **Code → Download ZIP** e extraia a pasta.
2. Execute `Instalar_e_abrir.bat`.
3. Aguarde a instalação das dependências.
4. Com o Roblox aberto, deixe a janela do Roblox em primeiro plano.
5. Use o botão **Iniciar / pausar** ou pressione **F6**.

Também é possível instalar manualmente as dependências e executar o aplicativo:

```bat
py -m pip install opencv-python mss numpy pyautogui keyboard pillow
py beyond_nen_app.py
```

### Controles

| Tecla | Ação |
| --- | --- |
| **F6** | Iniciar ou pausar a pesca automática |
| **F7** | Parar a automação e soltar o botão do mouse |
| **F8** | Mostrar ou ocultar a prévia |

Os mesmos comandos estão disponíveis pelos botões da interface.

### Configurações

- **Slot da vara:** escolha o número da tecla (1 a 9) correspondente ao slot em que a vara está equipada. Esse slot é usado também nas tentativas de recuperação automática.
- **Selecionar área na tela:** com a automação pausada, arraste um retângulo ao redor da barra do minigame para definir a região analisada.
- **Restaurar área padrão:** retorna à região inicial configurada no aplicativo.

### Gerar um executável

Execute `Gerar_EXE.bat`. O script instala o PyInstaller e tenta gerar o arquivo `BeyondNenFishing.exe` na pasta `dist`.

### Observações

- A detecção depende da posição e das cores dos elementos do minigame. Se necessário, ajuste a área analisada.
- O Roblox precisa estar em primeiro plano para que os comandos de pesca sejam enviados.
- Este repositório contém o código-fonte e scripts de execução; não inclui um executável pronto.
- A sintaxe do Python foi verificada. Isso não equivale a um teste completo dentro do Roblox.
