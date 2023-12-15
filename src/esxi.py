##################################################################################################
############## TP sur ESXI                                         ###############################
############## Virtualisation                                      ###############################
############## ANZIE SEVERIN BRADLEY                               ###############################
############## Classe ESXI (envoie des instructions a l'esxi)      ###############################
##################################################################################################

import json
import os
from sdk import create_vm
from sdk.case import switch_case
import argparse

def add_dict_to_namespace(namespace, input_dict):
    """Ajouter dynaiquement des champs a un dictionaire"""
    for key, value in input_dict.items():
        setattr(namespace, key, value)

class ESXI:
    def __init__(self, config_path, command=None, count = 1):
        self.config_path = config_path
        self.command = command
        self.count = count
        self.run()
    
    def run(self):
        # Vérifier si le fichier de configuration existe
        config_file = os.path.join(os.getcwd(), "config", self.config_path)
        if not os.path.exists(config_file):
            print(f"Erreur: Le fichier de configuration {self.config_path} n'existe pas.")
            return

        # Charger le contenu du fichier de configuration JSON
        with open(config_file, 'r') as file:
            config_data = json.load(file)
        
        # charger le fichier contenant les parametres de connexion
        with open(os.path.join(os.getcwd(), "config", "auth.json"), 'r') as file:
            instance_config_data = json.load(file)

        # Récupérer le champ "host" du fichier JSON
        if self.command in config_data:
            commandConf = config_data[self.command]
            auth=instance_config_data["serviceInstance"]
            args = argparse.Namespace()
            args.host = auth["host"]
            args.port = auth["port"]
            args.user = auth["user"]
            args.password = auth["password"]
            args.disable_ssl_verification = auth["disable_ssl_verification"]

            #ajouter les champs de connexion aux arguments
            add_dict_to_namespace(args, commandConf)

            #recherche et execution de la commande souhaitée
            i = 1
            while(i <= int(self.count)):
                args.count = i
                switch_case(command=self.command, args=args)
                i += 1
        else:
            print(f"Aucun champ {self.command} trouvé dans le fichier de configuration.")
