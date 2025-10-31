import csv
import json
import random
from pathlib import Path

VOCAB_FILE = Path("vocabulario.csv")
WEIGHTS_FILE = Path("weights.json")

vocab = []
with open(VOCAB_FILE, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f, delimiter=";")
    for row in reader:
        vocab.append({"english": row["english"], "spanish": row["spanish"]})

if WEIGHTS_FILE.exists():
    with open(WEIGHTS_FILE, "r", encoding="utf-8") as f:
        stats = json.load(f)
else:
    stats = {}

for entry in vocab:
    word = entry["english"]
    if word not in stats:
        stats[word] = {"seen": 0, "success": 0}

def get_weight(word_data):
    seen = word_data.get("seen", 0)
    success = word_data.get("success", 0)
    if seen == 0:
        return 1.0
    accuracy = success / seen
    return max(0.1, 1.0 - accuracy)

def choose_word():
    words = [entry["english"] for entry in vocab]
    weights = [get_weight(stats[w]) for w in words]
    total = sum(weights)
    probs = [w / total for w in weights]
    chosen = random.choices(words, probs)[0]
    translation = next(entry["spanish"] for entry in vocab if entry["english"] == chosen)
    return chosen, translation

def save_stats():
    with open(WEIGHTS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)


print("\n=== Quiz de vocabulario ===")
print("Pulsa Ctrl+C para salir.\n")

try: 
    while True:
        word, translation = choose_word()
        print(f"\n▶️ {word}")
        input("Pulsa [Enter] para ver la traducción... ")
        print(f"\n🗣️ {translation}")

        ans = input("\n¿La sabías? (y/n): ").strip().lower()
        while ans not in ["y", "n"]:
            ans = input("Por favor, escribe 'y' o 'n': ").strip().lower()

        stats[word]["seen"] += 1
        if ans == "y":
            stats[word]["success"] += 1

        seen = stats[word]["seen"]
        success = stats[word]["success"]
        accuracy = success / seen if seen > 0 else 0

        print(f"Estadísticas de '{word}':")
        print(f"     → Veces vistas: {seen}")
        print(f"     → Aciertos: {success}")
        print(f"     → Precisión: {accuracy:.1%}")

        save_stats()

except KeyboardInterrupt:
    print("\n\nProgreso guardado.")
    save_stats()
