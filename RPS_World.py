import customtkinter as ctk
import random
import itertools
from tkinter import messagebox
from PIL import Image
import pygame
import json

# initialize pygame mixer
# SFX and BGM
pygame.mixer.init()

# ==========================================
# ROCK PAPER SCISSORS FROM AROUND THE WORLD
# ==========================================

# ----------------
# GAME VARIATIONS
# ----------------

VARIATIONS = {
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

CHOICE_COLORS = ["#FF008D", "#001EFF", "#8900FF"]

PARTICLE_COLORS = {
    "neutral": (255, 255, 0),
    "win": (50, 205, 50),
    "lose": (255, 99, 71)
}

# -----------------------
# GAME STATE TRACKER
# -----------------------
class GameState:
    def __init__(self):
        self.resetAll()

    def resetRound(self):
        self.roundScoreUser = 0
        self.roundScoreComputer = 0

    def resetMatch(self):
        self.matchScoreUser = 0
        self.matchScoreComputer = 0
        self.matchesPlayed = 0
        self.resetRound()

    def resetAll(self):
        self.gamesPlayed = 0
        self.gamesWon = 0
        self.gamesLost = 0
        self.particleColorState = "neutral"
        self.currentItemList = []
        self.resetMatch()

gameState = GameState()

# -----------------------
# SOUND MANAGER
# -----------------------
class SoundManager:
    def __init__(self):
        self.sounds = {
            "win": pygame.mixer.Sound("sounds/win.wav"),
            "lose": pygame.mixer.Sound("sounds/lose.wav"),
            "tie": pygame.mixer.Sound("sounds/tie.wav"),
        }
        self.menu_volume = 0.5
        self.low_volume = 0.05

    def set_menu_volume(self, vol):
        pygame.mixer.music.set_volume(vol)

    def play(self, result):
        if result in self.sounds:
            self.set_menu_volume(self.low_volume)
            snd = self.sounds[result]
            snd.play()
            duration_ms = int(snd.get_length() * 1000)
            root.after(duration_ms, lambda: self.set_menu_volume(self.menu_volume))

soundManager = SoundManager()

# -----------------------
# NEON HAND SIGNS
# -----------------------
handSigns = {
    "Rock": ctk.CTkImage(Image.open("images/rock.png"), size=(150, 150)),
    "Paper": ctk.CTkImage(Image.open("images/paper.png"), size=(150, 150)),
    "Scissors": ctk.CTkImage(Image.open("images/scissors.png"), size=(150, 150))
}

# -----------------------
# PARTICLE SYSTEM
# -----------------------
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

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.alpha -= 0.03
        self.radius *= 0.97

    def draw(self):
        if self.id:
            self.canvas.delete(self.id)
        r, g, b = PARTICLE_COLORS[self.colorState]
        r = int(r * self.alpha + 30 * (1 - self.alpha))
        g = int(g * self.alpha + 30 * (1 - self.alpha))
        b = int(b * self.alpha + 30 * (1 - self.alpha))
        color = f"#{r:02x}{g:02x}{b:02x}"
        size = self.radius * (1 + (1 - self.alpha))
        self.id = self.canvas.create_oval(
            self.x - size, self.y - size, self.x + size, 
            self.y + size, fill=color, outline=""
        )

    def isDead(self):
        return self.alpha <= 0 or self.radius <= 0.5

class ParticleSystem:
    def __init__(self, canvas):
        self.canvas = canvas
        self.particles = []

    def emit(self, colorState):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        self.particles.append(Particle(self.canvas, random.uniform(0, w), 
                                       random.uniform(0, h), colorState))

    def run(self):
        for _ in range(8):
            self.emit(gameState.particleColorState)
        for p in self.particles[:]:
            p.update()
            if p.isDead():
                if p.id:
                    self.canvas.delete(p.id)
                self.particles.remove(p)
            else:
                p.draw()
        self.canvas.after(30, self.run)

# -----------------------
# GAME LOGIC
# -----------------------
def startGame():
    gameState.currentItemList = VARIATIONS[countryVar.get()]
    gameState.resetMatch()
    updateLabels()
    enableChoiceButtons()

    for i, button in enumerate(choiceButtons):
        button.configure(text=gameState.currentItemList[i], fg_color=CHOICE_COLORS[i])

    welcomeFrame.pack_forget()
    choicesFrame.pack(pady=10)
    scoresFrame.pack(pady=5)

    updateStatus(f"🎮 Playing {countryVar.get()} version! \nMatch 1 - Make your choice.", "#FFD700")

def revealComputerChoice(playerChoice):
    disableChoiceButtons()
    sequence = gameState.currentItemList[:]
    random.shuffle(sequence)
    animation_index = [0]

    def animate():
        if animation_index[0] < len(sequence) * 2:
            move = sequence[animation_index[0] % len(sequence)]
            updateStatus(f"🤖 Processing (Zeep Zorp) 🤖\n{move}", "#FFD700")
            animation_index[0] += 1
            root.after(150, animate)
        else:
            playRound(playerChoice)
            enableChoiceButtons()

    animate()

def playRound(choice):
    compChoice = random.choice(gameState.currentItemList)

    outcome_map = {
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
            "cond": True,  # default case
            "msg": f"💀 You lose this round! 💀\n💀 Computer chose {compChoice} 💀",
            "color": "#FF6347"
        }
    }

    for result, data in outcome_map.items():
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

def checkMatchEnd():
    if gameState.roundScoreUser == 2 or gameState.roundScoreComputer == 2:
        gameState.matchesPlayed += 1

        match_winner = "user" if gameState.roundScoreUser > gameState.roundScoreComputer else "comp"
        if match_winner == "user":
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

# -----------------------
# GUI UPDATE HELPERS
# -----------------------
hand_cycle = itertools.cycle(handSigns.values())
def animateHand(label):
    label.configure(image=next(hand_cycle))
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

def playAgain():
    playAgainFrame.pack_forget()
    choicesFrame.pack_forget()
    scoresFrame.pack_forget()
    welcomeFrame.pack(expand=True)
    gameState.resetAll()
    updateLabels()
    updateStatus("Welcome! Select a country to start.")

def showRules():
    # Get the current variation's choice list
    items = VARIATIONS[countryVar.get()]
    # Standard RPS rules: 0 beats 2, 1 beats 0, 2 beats 1
    rules_text = (
        f"📜 Rules for {countryVar.get()} 📜\n\n"
        f"{items[0]} defeats {items[2]}\n"
        f"{items[1]} defeats {items[0]}\n"
        f"{items[2]} defeats {items[1]}"
    )
    messagebox.showinfo("Game Rules", rules_text)
    
# -----------------------
# DRIVER (GUI SETUP)
# -----------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
root = ctk.CTk()
root.title("🌎 Rock Paper Scissors Around the World 🌍")
root.geometry("600x800")

pygame.mixer.music.load("sounds/menu.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

canvas = ctk.CTkCanvas(root, width=600, height=800, bg="#111111", highlightthickness=0)
canvas.place(x=0, y=0, relwidth=1, relheight=1)

handLabel = ctk.CTkLabel(root, text="", image=handSigns["Rock"])
handLabel.pack(pady=20)
animateHand(handLabel)

ctk.CTkLabel(root, text="🌍 Rock Paper Scissors From Around the World 🌍", 
             font=("Arial Rounded MT Bold", 28), text_color="#FFFFFF").pack(pady=15)

statusLabel = ctk.CTkLabel(root, text="Welcome! Select a country to start.", 
                           font=("Arial Rounded MT Bold", 16))
statusLabel.pack(pady=10)

welcomeFrame = ctk.CTkFrame(root, corner_radius=15)
welcomeFrame.pack(expand=True)

countryVar = ctk.StringVar(value="🦅 Vanilla 🦅")
ctk.CTkOptionMenu(welcomeFrame, variable=countryVar, values=list(VARIATIONS.keys())).pack(pady=10)
# "Show Rules" button - pops up rules for current selection
ctk.CTkButton(
    welcomeFrame,
    text="📜 Show Rules 📜", 
    command=showRules,
    fg_color="#1E90FF",
    height=35,
    font=("Arial Rounded MT Bold", 14)
).pack(pady=5)
ctk.CTkLabel(welcomeFrame, text="📜 General Rules 📜\n1 Match = Best of 3 Rounds\n1 Game = Best of 3 Matches", 
             font=("Arial", 16), justify="center", wraplength=500).pack(pady=15)
ctk.CTkButton(welcomeFrame, text="🚀 Start Game 🚀", command=startGame, fg_color="#32CD32", 
              height=40, font=("Arial Rounded MT Bold", 16)).pack(pady=15)

choicesFrame = ctk.CTkFrame(root, corner_radius=15)
choiceButtons = [
    ctk.CTkButton(choicesFrame, text="Choice", width=250, height=50, 
                  corner_radius=12, font=("Arial Rounded MT Bold", 16), 
                  command=lambda i=i: revealComputerChoice(gameState.currentItemList[i]),
                  state="disabled", fg_color=CHOICE_COLORS[i])
    for i in range(3)
]
for button in choiceButtons:
    button.pack(pady=7)

scoresFrame = ctk.CTkFrame(root, corner_radius=15)
scoreLabel = ctk.CTkLabel(scoresFrame, text="", font=("Arial", 15))
scoreLabel.pack()
gameStatsLabel = ctk.CTkLabel(scoresFrame, text="", font=("Arial", 15))
gameStatsLabel.pack(pady=5)

playAgainFrame = ctk.CTkFrame(root, corner_radius=15)
playAgainButton = ctk.CTkButton(
    playAgainFrame, 
    text="🔄 Play Again? 🔄", 
    command=playAgain, 
    fg_color="#9370DB", 
    height=40
)
playAgainButton.pack()

particleSystem = ParticleSystem(canvas)
particleSystem.run()

updateLabels()
root.mainloop()
