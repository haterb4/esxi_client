># avant toute chose cd src 
# create vm:
    python app.py -c vmconfig.json -cm [commande a executer] -n [nombre repetitions]

## exemple:
    python app.py -c vmconfig.json -cm createVMFromOVA -n 1

# les commandes possibles sont dans src/config/vmconfig.json:
    - createNewVM: creer une vm
    - createVMFromISO: creer une vm a partir d'u iso v1
    - createVMFromISO2: creer une vm a partir d'u iso v2
    - createVMFromOVA: creer une vm a partir d'un ova
    - cloneVM: clonner une vm
    - destroyVM: supprimmer une vm
    - getAllVM: lister toutes les vm
    - rebootVM: redemarer une vm

# veuillez a bien modifier les valeurs necessaire dans le fichier de configuration