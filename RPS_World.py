# ==========================================
# ROCK PAPER SCISSORS FROM AROUND THE WORLD
# ==========================================

import customtkinter as ctk
import random
import itertools
from tkinter import messagebox
from PIL import Image
import pygame
import json

# ----------------
# GAME VARIATIONS
# ----------------

# Dictionary: Each country has a unique set of choices
variations = {
    "🦅 Vanilla 🦅": ["Rock", "Paper", "Scissors"],
    "🫡 American Historical 🫡": ["Ro", "Beau", "Sham"],
    "🌺 Hawaii 🌺": ["Guu", "Paa", "Choki"],
    "🍣 Japan 🍣": ["Kawazu", "Hebi", "Namekuji"],
    "🥠 China 🥠": ["Shi", "Ka", "Bu"],
    "🍛 Korea 🍛": ["Bai", "Bo", "Kai"],
    "🔗 Finland 🔗": ["Kivi", "Paperi", "Sakset"],
    "🥐 France 🥐": ["Pierra", "Papier", "Ciseaux"],
    "🌯 Spain 🌯": ["Piedra", "Papel", "Tijera"]
}

# UI colors
choiceColors = ["#FF008D", "#001EFF", "#8900FF"]

particleColors = {
    "neutral": (255, 255, 0),
    "win": (50, 205, 50),
    "lose": (255, 99, 71)
}

# -------------------
# GAME STATE TRACKER
# -------------------

# Class to store and reset counters for game state
class GameState:
    def __init__(self):
        self.resetAll()
    
    # Reset round scores
    def resetRound(self):
        self.roundScoreUser = 0
        self.roundScoreComputer = 0
    
    # Reset match scores
    def resetMatch(self):
        self.matchScoreUser = 0
        self.matchScoreComputer = 0
        self.matchesPlayed = 0
        self.resetRound()
    
    # Reset all game states
    def resetAll(self):
        self.gamesPlayed = 0
        self.gamesWon = 0
        self.gamesLost = 0
        self.particleColorState = "neutral"
        self.currentItemList = []
        self.resetMatch()

# Instance of GameState
gameState = GameState()

# --------------
# SOUND MANAGER
# --------------

# Class to manage sound effects and background music
class SoundManager:
    pygame.mixer.init()
    
    def __init__(self):
        # Sound effects
        self.sounds = {
            "win": pygame.mixer.Sound("sounds/win.wav"),
            "lose": pygame.mixer.Sound("sounds/lose.wav"),
            "tie": pygame.mixer.Sound("sounds/tie.wav"),
        }
        self.menuVolume = 0.5
        self.lowVolume = 0.05

    # Set menu volume
    def setMenuVolume(self, vol):
        pygame.mixer.music.set_volume(vol)

    # Play sound based on result
    def play(self, result):
        if result in self.sounds:
            self.setMenuVolume(self.lowVolume)
            snd = self.sounds[result]
            snd.play()
            # Restore volume after sound plays
            durationMs = int(snd.get_length() * 1000)
            root.after(durationMs, lambda: self.setMenuVolume(self.menuVolume))

soundManager = SoundManager()

# ----------------
# NEON HAND SIGNS
# ----------------

handSigns = {
    "Rock": ctk.CTkImage(Image.open("images/rock.png"), size=(150, 150)),
    "Paper": ctk.CTkImage(Image.open("images/paper.png"), size=(150, 150)),
    "Scissors": ctk.CTkImage(Image.open("images/scissors.png"), size=(150, 150))
}

# -------------------
# PARTICLE SIMULATION
# -------------------

# Class for a single moving and fading particle
class Particle:
    def __init__(self, canvas, x, y, colorState):
        self.canvas = canvas
        self.x, self.y = x, y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.radius = random.uniform(3, 6)
        self.alpha = 1.0
        self.colorState = colorState
        self.id = None

    # Move, fade, and shrink the particle
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.alpha -= 0.03
        self.radius *= 0.97

    # Draw the particle on the canvas
    def draw(self):
        if self.id:
            self.canvas.delete(self.id)
        r, g, b = particleColors[self.colorState]
        r = int(r * self.alpha + 30 * (1 - self.alpha))
        g = int(g * self.alpha + 30 * (1 - self.alpha))
        b = int(b * self.alpha + 30 * (1 - self.alpha))
        color = f"#{r:02x}{g:02x}{b:02x}"
        size = self.radius * (1 + (1 - self.alpha))
        self.id = self.canvas.create_oval(
            self.x - size, self.y - size, self.x + size, 
            self.y + size, fill=color, outline=""
        )

    # Check if the particle is "dead"
    def isDead(self):
        return self.alpha <= 0 or self.radius <= 0.5

# Class to manage particles
class ParticleSystem:
    def __init__(self, canvas):
        self.canvas = canvas
        self.particles = []

    # Emit a new particle at a random position
    def emit(self, colorState):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        self.particles.append(Particle(self.canvas, random.uniform(0, w), 
                                       random.uniform(0, h), colorState))

    def run(self):
        # Spawn new particles each frame
        for _ in range(8):
            self.emit(gameState.particleColorState)
        # Update and draw each particle
        for p in self.particles[:]:
            p.update()
            if p.isDead():
                if p.id:
                    self.canvas.delete(p.id)
                self.particles.remove(p)
            else:
                p.draw()
        # Schedule the next frame
        self.canvas.after(30, self.run)

# ------------
# GAME LOGIC
# ------------

# Prepare the UI and enable buttons
def startGame():
    gameState.currentItemList = variations[countryVar.get()]
    gameState.resetMatch()
    updateLabels()
    enableChoiceButtons()
    for i, button in enumerate(choiceButtons):
        button.configure(text=gameState.currentItemList[i], fg_color=choiceColors[i])
    welcomeFrame.pack_forget()
    choicesFrame.pack(pady=10)
    scoresFrame.pack(pady=5)
    updateStatus(f"🎮 Playing {countryVar.get()} version! \nMatch 1 - Make your choice.", "#FFD700")

# Reveal computer choice with animation
def revealComputerChoice(playerChoice):
    disableChoiceButtons()
    sequence = gameState.currentItemList[:]
    random.shuffle(sequence)
    animationIndex = [0]

    def animate():
        if animationIndex[0] < len(sequence) * 2:
            move = sequence[animationIndex[0] % len(sequence)]
            updateStatus(f"🤖 Processing (Zeep Zorp) 🤖\n{move}", "#FFD700")
            animationIndex[0] += 1
            root.after(150, animate)
        else:
            playRound(playerChoice)
            # only enable if the game hasn't ended
            if not (gameState.matchScoreUser == 2 or gameState.matchScoreComputer == 2):
                enableChoiceButtons()

    animate()

# Play one round of the game
def playRound(choice):
    compChoice = random.choice(gameState.currentItemList)
    outcomeMap = {
        "tie": {
            "cond": compChoice == choice,
            "msg": f"😐 Tie! 😐\n😐 Computer chose {compChoice} 😐",
            "color": "#FFD700"
        },
        "win": {
            "cond": (choice, compChoice) in [
                (gameState.currentItemList[0], gameState.currentItemList[2]),
                (gameState.currentItemList[1], gameState.currentItemList[0]),
                (gameState.currentItemList[2], gameState.currentItemList[1])
            ],
            "msg": f"🎉 You win this round! 🎉\n🎉 Computer chose {compChoice} 🎉",
            "color": "#32CD32"
        },
        "lose": {
            "cond": True,  # Default case
            "msg": f"💀 You lose this round! 💀\n💀 Computer chose {compChoice} 💀",
            "color": "#FF6347"
        }
    }
    
    # Find and apply matching outcome
    for result, data in outcomeMap.items():
        if data["cond"]:
            if result == "win":
                gameState.roundScoreUser += 1
            elif result == "lose":
                gameState.roundScoreComputer += 1
            updateStatus(data["msg"], data["color"])
            soundManager.play(result)
            gameState.particleColorState = result if result != "tie" else "neutral"
            break

    checkMatchEnd()
    updateLabels()

# Check if the match has ended
def checkMatchEnd():
    if gameState.roundScoreUser == 2 or gameState.roundScoreComputer == 2:
        gameState.matchesPlayed += 1
        matchWinner = "user" if gameState.roundScoreUser > gameState.roundScoreComputer else "comp"
        if matchWinner == "user":
            gameState.matchScoreUser += 1
            messagebox.showinfo("🏆 Match Result", f"🎉 You won Match {gameState.matchesPlayed}! 🎉")
        else:
            gameState.matchScoreComputer += 1
            messagebox.showinfo("😔 Match Result", f"💀 You lost Match {gameState.matchesPlayed}! 💀")

        gameState.resetRound()

        if gameState.matchScoreUser == 2 or gameState.matchScoreComputer == 2:
            checkGameEnd()
        else:
            updateStatus(f"Match {gameState.matchesPlayed + 1} - Make your choice.", "#FFD700")

# Final game winner check
def checkGameEnd():
    gameState.gamesPlayed += 1
    if gameState.matchScoreUser > gameState.matchScoreComputer:
        gameState.gamesWon += 1
        messagebox.showinfo("🏆 Game Result", "🎉 YOU WIN THE GAME! 🎉")
    else:
        gameState.gamesLost += 1
        messagebox.showinfo("😔 Game Result", "💀 You lost the game... 💀")

    disableChoiceButtons()  
    playAgainFrame.place(relx=0.85, rely=0.6, anchor="center")


# -------------------
# GUI UPDATE HELPERS
# -------------------

# Cycle through hand signs
handCycle = itertools.cycle(handSigns.values())
def animateHand(label):
    label.configure(image=next(handCycle))
    root.after(300, animateHand, label)

def updateStatus(msg, color="#FFFFFF"):
    statusLabel.configure(text=msg, text_color=color)

def updateLabels():
    scoreLabel.configure(
        text=f"📊 Round Score 📊\n You: {gameState.roundScoreUser} \nComputer: {gameState.roundScoreComputer}\n\n"
             f"🏆 Match Score 🏆\nYou: {gameState.matchScoreUser} \nComputer: {gameState.matchScoreComputer}"
    )
    gameStatsLabel.configure(
        text=f"\n 📈 Games 📈\n Won: {gameState.gamesWon} \n Lost: {gameState.gamesLost} \n Played: {gameState.gamesPlayed}"
    )

def enableChoiceButtons():
    for button in choiceButtons:
        button.configure(state="normal")

def disableChoiceButtons():
    for button in choiceButtons:
        button.configure(state="disabled")

# Reset everything and return to welcome screen
def playAgain():
    playAgainFrame.place_forget()  # Hide the Play Again/Quit buttons
    choicesFrame.pack_forget()
    scoresFrame.pack_forget()
    welcomeFrame.pack(expand=True)
    gameState.resetAll()
    updateLabels()
    updateStatus("Welcome! Select a country to start.")

# Quit game with goodbye message
def quitGame():
    messagebox.showinfo("Goodbye!", "👋 Thanks for playing! See you next time.")
    root.destroy()

# Show specific rules for the current variation
def showRules():
    items = variations[countryVar.get()]
    rulesText = (
        f"📜 Rules for {countryVar.get()} 📜\n\n"
        f"{items[0]} defeats {items[2]}\n"
        f"{items[1]} defeats {items[0]}\n"
        f"{items[2]} defeats {items[1]}"
    )
    messagebox.showinfo("Game Rules", rulesText)

# -------------------
# DRIVER (GUI SETUP)
# -------------------

# Dark theme, green accents
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
root = ctk.CTk()
root.title("🌎 Rock Paper Scissors Around the World 🌍")
root.geometry("600x800")

# Start BGM
pygame.mixer.music.load("sounds/menu.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Canvas for particles
canvas = ctk.CTkCanvas(root, width=600, height=800, bg="#111111", highlightthickness=0)
canvas.place(x=0, y=0, relwidth=1, relheight=1)

# Animated hand label
handLabel = ctk.CTkLabel(root, text="", image=handSigns["Rock"])
handLabel.pack(pady=20)
animateHand(handLabel)

# Title
ctk.CTkLabel(root, text="🌍 Rock Paper Scissors From Around the World 🌍", 
             font=("Arial Rounded MT Bold", 28), text_color="#FFFFFF").pack(pady=15)

# Status line
statusLabel = ctk.CTkLabel(root, text="Welcome! Select a country to start.", 
                           font=("Arial Rounded MT Bold", 16))
statusLabel.pack(pady=10)

# -------------------
# WELCOME SCREEN
# -------------------

welcomeFrame = ctk.CTkFrame(root, corner_radius=15)
welcomeFrame.pack(expand=True)

countryVar = ctk.StringVar(value="🦅 Vanilla 🦅")
ctk.CTkOptionMenu(welcomeFrame, variable=countryVar, values=list(variations.keys())).pack(pady=10)

# "Show Rules" button
ctk.CTkButton(
    welcomeFrame,
    text="📜 Show Rules 📜", 
    command=showRules,
    fg_color="#1E90FF",
    height=35,
    font=("Arial Rounded MT Bold", 14)
).pack(pady=5)

# General rules
ctk.CTkLabel(welcomeFrame, text="📜 General Rules 📜\n1 Match = Best of 3 Rounds\n1 Game = Best of 3 Matches", 
             font=("Arial", 16), justify="center", wraplength=500).pack(pady=15)

# "Start Game" button
ctk.CTkButton(welcomeFrame, text="🚀 Start Game 🚀", command=startGame, fg_color="#32CD32", 
              height=40, font=("Arial Rounded MT Bold", 16)).pack(pady=15)

# Choice Buttons Frame
choicesFrame = ctk.CTkFrame(root, corner_radius=15)
choiceButtons = [
    ctk.CTkButton(choicesFrame, text="Choice", width=250, height=50, 
                  corner_radius=12, font=("Arial Rounded MT Bold", 16), 
                  command=lambda i=i: revealComputerChoice(gameState.currentItemList[i]),
                  state="disabled", fg_color=choiceColors[i])
    for i in range(3)
]
for button in choiceButtons:
    button.pack(pady=7)

# --- Scores Frame ---
scoresFrame = ctk.CTkFrame(root, corner_radius=15)
scoreLabel = ctk.CTkLabel(scoresFrame, text="", font=("Arial", 15))
scoreLabel.pack()
gameStatsLabel = ctk.CTkLabel(scoresFrame, text="", font=("Arial", 15))
gameStatsLabel.pack(pady=5)

# --- Play Again Frame ---
playAgainFrame = ctk.CTkFrame(root, corner_radius=15)

# Play Again button
playAgainButton = ctk.CTkButton(
    playAgainFrame, 
    text="🔄 Play Again? 🔄", 
    command=playAgain, 
    fg_color="#9370DB", 
    height=40
)
playAgainButton.pack(anchor="w", padx=5, pady=5)

# Quit button
quitButton = ctk.CTkButton(
    playAgainFrame,
    text="❌ Quit ❌",
    command=quitGame,
    fg_color="#FF4500",
    height=40
)
quitButton.pack(anchor="w", padx=5, pady=5)

particleSystem = ParticleSystem(canvas)
particleSystem.run()

updateLabels()
root.mainloop()
