##############################################################################################################
############## TP sur ESXI                                                     ###############################
############## Virtualisation                                                  ###############################
############## ANZIE SEVERIN BRADLEY                                           ###############################
############## Implementation d'un switch case pour executer une commande      ###############################
##############################################################################################################
from sdk import create_vm, getallvms, reboot_vm, destroy_vm, clone_vm, deploy_iso, deploy_iso_v2


def default(args):
    """S'execute par defaut si aucune commande valide n'est fournie"""
    print("default action")
    print(f"argument: {args}")

def switch_case(command, args):
    switch_dict = {
        "createVMFromOVA": create_vm.main,
        "getAllVM": getallvms.main,
        "rebootVM": reboot_vm.main,
        "destroyVM": destroy_vm.main,
        "cloneVM": clone_vm.main,
        "createVMFromISO": deploy_iso.main,
        "createVMFromISO2": deploy_iso_v2.main
    }
    # Utilisation de la méthode get pour obtenir la fonction associée à la clé
    # Si la clé n'est pas trouvée, on utilise la fonction par défaut
    switch_dict.get(command, default)(args)