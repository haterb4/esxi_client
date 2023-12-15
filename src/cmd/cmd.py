import argparse

def parse_arguments():
    # ArgumentParser
    parser = argparse.ArgumentParser(description='Script de configuration ESXi.')

    # le fichier de configuration
    parser.add_argument('-c', '--config', type=str, required=True, help='Chemin vers le fichier de configuration JSON')

    # commande a executer
    parser.add_argument('-cm', '--command', type=str, required=True, help='Commande a executer')

    parser.add_argument('-n', '--number', type=str, required=True, help='nombre de repetitions de la commande')

    # Analyser les arguments de la ligne de commande
    args = parser.parse_args()
    return args