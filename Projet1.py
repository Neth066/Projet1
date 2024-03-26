
# Ce 
import argparse
import requests


def lister_parties(idul, jeton):
    url = "https://pax.ulaval.ca/quixo/api/h24/parties/"
    response = requests.get(url, auth=(idul, jeton))
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401 or response.status_code == 406:
        return response.json()
    else:
        return {"error": "Unknown error occurred."}

def récupérer_partie(id_partie, idul, jeton):
    url = f"https://pax.ulaval.ca/quixo/api/h24/partie/{id_partie}/"
    response = requests.get(url, auth=(idul, jeton))
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to retrieve game."}

def débuter_partie(idul, jeton):
    url = "https://pax.ulaval.ca/quixo/api/h24/partie/"
    response = requests.post(url, auth=(idul, jeton))
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to start new game."}

def jouer_coup(id_partie, type_coup, position, idul, jeton):
    url = "https://pax.ulaval.ca/quixo/api/h24/jouer/"
    data = {"id": id_partie, "type": type_coup, "pos": position}
    response = requests.put(url, json=data, auth=(idul, jeton))
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to make move."}


def formater_légende(joueurs):
    return f"Légende: X={joueurs[0]}, O={joueurs[1]}"

def formater_plateau(plateau):
    horizontal_line = "---|---|---|---|---|\n"
    board_str = horizontal_line
    for i, row in enumerate(plateau):
        board_str += f"{i+1} | {' | '.join(row)} |\n"
        board_str += horizontal_line if i < 4 else "--|---|---|---|---\n"
    board_str += "  | 1   2   3   4   5\n"
    return board_str

def formater_jeu(joueurs, plateau):
    return f"{formater_légende(joueurs)}\n{formater_plateau(plateau)}"

def formater_les_parties(parties):
    formatted_parties = []
    for partie in parties:
        gagnant_str = f", gagnant: {partie['gagnant']}" if partie['gagnant'] else ""
        formatted_parties.append(f"{partie['id']} : {partie['date']}, {partie['joueurs'][0]} vs {partie['joueurs'][1]}{gagnant_str}")
    return "\n".join(formatted_parties)

def récupérer_le_coup():
    origine_str = input("Donnez la position d'origine du bloc (x,y) : ")
    direction = input("Quelle direction voulez-vous insérer? ('haut', 'bas', 'gauche', 'droite') : ")
    origine = list(map(int, origine_str.split(',')))
    return origine, direction

def analyser_commande():
    parser = argparse.ArgumentParser()
    parser.add_argument("idul", type=str, help="IDUL du joueur")
    return parser.parse_args()

# Test des fonctions
if __name__ == "__main__":
    # Test des fonctions formater_légende et formater_plateau
    joueurs = ["josmi42", "automate"]
    plateau = [
        [" ", " ", "X", " ", " "],
        [" ", " ", " ", " ", " "],
        [" ", " ", " ", " ", "O"],
        [" ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " "],
    ]
    print(formater_légende(joueurs))
    print(formater_plateau(plateau))

    # Test de la fonction formater_jeu
    print(formater_jeu(joueurs, plateau))

    # Test de la fonction formater_les_parties
    parties = [
        {
            "id": "121684ab-6e52-4f81-b278-65d88e4a0535",
            "date": "2024-01-22 21:35:24",
            "joueurs": ["josmi42", "robot-2"],
            "gagnant": None,
        },
        {
            "id": "2acc319d-102a-4908-b03a-fa028ae089fa",
            "date": "2024-01-10 23:17:01",
            "joueurs": ["josmi42", "robot-1"],
            'gagnant': "josmi42",
        },
    ]
    print(formater_les_parties(parties))

    # Test de la fonction récupérer_le_coup
    origine, direction = récupérer_le_coup()
    print(origine)
    print(direction)

    # Test de la fonction analyser_commande
    args = analyser_commande()
    print(args.idul)

