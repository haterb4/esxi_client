########################################################################
############## TP sur ESXI           ###################################
############## Virtualisation        ###################################
############## ANZIE SEVERIN BRADLEY ###################################
############## Point d'entrée        ###################################
########################################################################
import sys
from esxi import ESXI
from cmd.cmd import parse_arguments

def main():
    # Recuperation des arguments de la ligne de commande
    args = parse_arguments()

    # Créer une instance de la classe ESXI avec les arguments
    ESXI(config_path=args.config, command=args.command, count = args.number)

if __name__ == "__main__":
    sys.exit(main())