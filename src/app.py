import secrets
import string
import tkinter as tk
from tkinter import ttk, messagebox

# Symbols allowed in passwords
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.?/"

# -----------------------------
# Password generation function
# -----------------------------
def generate_password(length, upper, lower, digits, symbols, avoid_ambiguous):
    # Enforce minimum length
    if length < 8:
        raise ValueError("Minimum recommandé : 8 caractères")

    # Characters that are hard to distinguish visually
    ambiguous = set("O0Il1")
    pools = []

    # Character sets
    U = string.ascii_uppercase
    L = string.ascii_lowercase
    D = string.digits
    S = SYMBOLS

    # Remove ambiguous characters if option is enabled
    if avoid_ambiguous:
        U = "".join(c for c in U if c not in ambiguous)
        L = "".join(c for c in L if c not in ambiguous)
        D = "".join(c for c in D if c not in ambiguous)

    # Build the character pools based on user choices
    if upper: pools.append(U)
    if lower: pools.append(L)
    if digits: pools.append(D)
    if symbols: pools.append(S)

    # At least one type must be selected
    if not pools:
        raise ValueError("Choisis au moins un type de caractères")

    # Combine all selected characters
    all_chars = "".join(pools)

    # Ensure at least one character from each selected type
    password = [secrets.choice(pool) for pool in pools]

    # Fill the rest of the password
    while len(password) < length:
        password.append(secrets.choice(all_chars))

    # Shuffle the password for randomness
    secrets.SystemRandom().shuffle(password)

    return "".join(password)


# -----------------------------
# Password strength estimator
# -----------------------------
def strength(pw):
    score = 0

    # Length-based scoring
    if len(pw) >= 8: score += 1
    if len(pw) >= 12: score += 1
    if len(pw) >= 16: score += 1

    # Diversity-based scoring
    score += any(c.isupper() for c in pw)
    score += any(c.islower() for c in pw)
    score += any(c.isdigit() for c in pw)
    score += any(c in SYMBOLS for c in pw)

    # Final strength label
    if score <= 3: return "Faible"
    if score <= 5: return "Moyen"
    return "Fort"


# -----------------------------
# GUI Application (Tkinter)
# -----------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Password Generator")
        self.resizable(False, False)
        self.configure(padx=16, pady=16)

        # Variables linked to the UI
        self.length = tk.StringVar(value="16")
        self.upper = tk.BooleanVar(value=True)
        self.lower = tk.BooleanVar(value=True)
        self.digits = tk.BooleanVar(value=True)
        self.symbols = tk.BooleanVar(value=True)
        self.ambiguous = tk.BooleanVar(value=True)

        self.password = tk.StringVar()
        self.strength = tk.StringVar(value="—")

        # Build the interface
        self.build_ui()

    # Create the UI layout
    def build_ui(self):
        ttk.Label(
            self, 
            text="Générateur de mot de passe", 
            font=("Helvetica", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=10)

        # Password length input
        ttk.Label(self, text="Longueur").grid(row=1, column=0, sticky="w")
        ttk.Entry(self, textvariable=self.length, width=6).grid(row=1, column=1, sticky="w")

        # Options checkboxes
        ttk.Checkbutton(self, text="Majuscules", variable=self.upper).grid(row=2, column=0, sticky="w")
        ttk.Checkbutton(self, text="Minuscules", variable=self.lower).grid(row=3, column=0, sticky="w")
        ttk.Checkbutton(self, text="Chiffres", variable=self.digits).grid(row=4, column=0, sticky="w")
        ttk.Checkbutton(self, text="Symboles", variable=self.symbols).grid(row=5, column=0, sticky="w")
        ttk.Checkbutton(self, text="Éviter caractères ambigus", variable=self.ambiguous).grid(row=6, column=0, sticky="w")

        # Output field
        ttk.Entry(self, textvariable=self.password, width=32).grid(row=7, column=0, columnspan=2, pady=10)

        # Strength label
        ttk.Label(self, text="Force:").grid(row=8, column=0, sticky="w")
        ttk.Label(self, textvariable=self.strength, font=("Helvetica", 11, "bold")).grid(row=8, column=1, sticky="w")

        # Buttons
        ttk.Button(self, text="Générer", command=self.on_generate).grid(row=9, column=0, pady=10)
        ttk.Button(self, text="Copier", command=self.on_copy).grid(row=9, column=1, pady=10)

    # Generate password when button is clicked
    def on_generate(self):
        try:
            length = int(self.length.get())

            pw = generate_password(
                length,
                self.upper.get(),
                self.lower.get(),
                self.digits.get(),
                self.symbols.get(),
                self.ambiguous.get()
            )

            self.password.set(pw)
            self.strength.set(strength(pw))

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    # Copy password to clipboard
    def on_copy(self):
        pw = self.password.get()
        if not pw:
            return

        self.clipboard_clear()
        self.clipboard_append(pw)
        self.update()

        messagebox.showinfo("Copié", "Mot de passe copié 📋")


# -----------------------------
# Program entry point
# -----------------------------
def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
