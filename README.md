


SafeLink
Description
SafeLink est une application de vérification de sites Web qui utilise l'API de VirusTotal pour analyser la sécurité des URL. L'application propose une interface graphique conviviale permettant de saisir des URL et de vérifier leur statut de sécurité.

Fonctionnalités
Vérification de plusieurs URL simultanément.
Évaluation de la sécurité des sites avec des résultats clairs.
Choix de plusieurs thèmes personnalisés, y compris Anarchiste, Neutre, Manga, et plus.
Interface graphique moderne avec un design coloré.
Exécutable
Un fichier exécutable (SafeLink.exe) est disponible pour une utilisation facile sans nécessiter Python ou d'autres installations.

Prérequis
Clé API VirusTotal (voir section "Obtenir une clé API" ci-dessous)
Installation
Clonez le dépôt ou téléchargez le code source.
Si vous utilisez l'exécutable, passez cette étape. Sinon, assurez-vous d'avoir Python 3.x installé sur votre machine.
Si vous utilisez le code source, installez les dépendances requises :
bash
Copier le code
pip install requests
Obtenir une clé API VirusTotal
Rendez-vous sur VirusTotal.
Créez un compte et activez-le via l'email de confirmation.
Connectez-vous et accédez à votre clé API dans votre profil.
Utilisation
Exécutez l'application avec la commande :
bash
Copier le code
python safe_link.py
Ou, si vous utilisez l'exécutable, double-cliquez sur SafeLink.exe.
Saisissez votre clé API dans le champ approprié.
Entrez les URL à vérifier (une par ligne).
Cliquez sur "Vérifier" pour lancer l'analyse.
Thèmes Disponibles
Anarchiste : Rouge et noir
Neutre : Couleurs standard
Manga : Couleurs vives
VirusTotal : Thème sombre
Cyberpunk : Thème futuriste
Dark Mode : Mode sombre
Communiste : Rouge et jaune
Call of Duty : Thème militaire
Battlefield : Thème de guerre
Dépannage
Si vous rencontrez des erreurs lors de l'exécution, assurez-vous que votre clé API est valide.
Vérifiez votre connexion Internet pour l'accès à l'API VirusTotal.
Contribution
Les contributions sont les bienvenues ! N'hésitez pas à soumettre des problèmes ou des pull requests pour améliorer l'application.

License
Ce projet est sous la licence MIT. Voir le fichier LICENSE pour plus de détails.