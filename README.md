# SafeLink

SafeLink est une application qui permet de vérifier la sécurité des sites web via l'API VirusTotal. Vous pouvez vérifier plusieurs sites en même temps et recevoir une évaluation sur la sécurité de chaque URL.

## Fonctionnalités

- Vérification de la sécurité des sites via l'API VirusTotal.
- Interface graphique intuitive et simple.
- Prise en charge de plusieurs thèmes visuels : Anarchiste, Neutre, Manga, VirusTotal, Dark Mode, 

## Installation

### Prérequis

- Python 3.x (si vous exécutez depuis le code source).
- Une clé API VirusTotal (instructions ci-dessous).
- Avoir Requests ( en mode python ) 

### Obtenir une clé API VirusTotal

1. Rendez-vous sur [https://www.virustotal.com/](https://www.virustotal.com/).
2. Créez un compte gratuitement et suivez les étapes de confirmation.
3. Une fois connecté, accédez à votre tableau de bord utilisateur.
4. Dans la section "API Key", copiez votre clé API.
5. Collez cette clé dans l'application lorsque cela vous est demandé.

## Utilisation

### Via l'exécutable

1. Ouvrez le fichier `SafeLink.exe`.
2. Entrez votre clé API VirusTotal dans le champ dédié.
3. Saisissez les URL à vérifier (une par ligne).
4. Cliquez sur "Vérifier" pour obtenir les résultats.

### Via le code source

1. Exécutez le script Python :
   ```bash
   python Safelink.py
## Personnalisation des thèmes

SafeLink permet de choisir parmi différents thèmes visuels :

- **Anarchiste** : Rouge et noir.
- **Neutre** : Couleurs sobres et simples.
- **Manga** : Couleurs douces inspirées des mangas.
- **VirusTotal** : Thème sombre inspiré du site VirusTotal.
- **Cyberpunk** : Couleurs néon avec un style futuriste.
- **Dark Mode** : Thème sombre pour les utilisateurs préférant une interface sombre.

### Contribuer
Les contributions sont les bienvenues ! N'hésitez pas à forker ce projet et à soumettre des pull requests.
