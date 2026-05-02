# SafeLink

<p align="center">
  <img src="assets/safelink-logo.svg" alt="Logo SafeLink" width="150">
</p>

SafeLink est une application de bureau qui vérifie la réputation d'URLs avec l'API VirusTotal. Elle permet d'analyser plusieurs liens à la fois et d'afficher les résultats directement dans l'interface.

Dépôt GitHub : <https://github.com/AnARCHIS12/Safelink>

## Fonctionnalités

- Interface moderne en CustomTkinter.
- Design rouge/noir avec logo intégré.
- Vérification de plusieurs URLs en une seule analyse.
- Résultats affichés dans l'application.
- Barre de progression et statut d'analyse.
- Bouton pour copier les résultats.
- Bouton pour effacer la saisie.
- Mémorisation locale optionnelle de la clé API.

## Prérequis

- Python 3.x.
- Une clé API VirusTotal.
- Les dépendances Python :

```bash
pip install requests customtkinter pillow
```

## Obtenir une clé API VirusTotal

1. Rendez-vous sur [virustotal.com](https://www.virustotal.com/).
2. Créez un compte ou connectez-vous.
3. Ouvrez votre espace utilisateur.
4. Copiez votre clé dans la section API Key.
5. Collez cette clé dans SafeLink.

## Utilisation

Lancez la version 1.0.1 :

```bash
python SafeLink-1.01.py
```

Ensuite :

1. Collez votre clé API VirusTotal.
2. Saisissez une URL par ligne.
3. Cliquez sur **Vérifier**.
4. Consultez ou copiez les résultats.

Si vous cochez **Mémoriser la clé API localement**, SafeLink garde la clé dans le fichier de configuration utilisateur afin de la recharger au prochain lancement.

## GitHub Pages

Une page de présentation est prête dans `docs/`.

Pour l'activer sur GitHub :

1. Ouvrez les paramètres du dépôt.
2. Allez dans **Pages**.
3. Choisissez la branche principale.
4. Sélectionnez le dossier `/docs`.
5. Enregistrez.

La page contient une section **Téléchargements** qui pointe vers la dernière release GitHub :

- Windows : `SafeLink-windows-x64.exe`
- Debian/Ubuntu : `safelink_amd64.deb`
- Fedora : `safelink-fedora-x86_64.rpm`

## Releases automatiques

Le workflow `.github/workflows/release.yml` compile SafeLink et crée une release GitHub.

Il se lance :

- automatiquement quand vous poussez un tag `v*`, par exemple `v1.0.1` ;
- manuellement depuis l'onglet **Actions** avec un numéro de version.

Exemple :

```bash
git tag v1.0.1
git push origin v1.0.1
```

La release contient :

- un exécutable Windows `.exe` ;
- un paquet Debian/Ubuntu `.deb` ;
- un paquet Fedora `.rpm`.

## Fichiers du logo

Le logo est disponible dans `assets/` :

- `assets/safelink-logo.svg` : source vectorielle pour le README.
- `assets/safelink-logo.png` : version carrée du logo.
- `assets/safelink-logo-mark.png` : version transparente utilisée dans l'interface.
- `assets/safelink-logo.ico` : icône utilisée par la fenêtre.

## Note

SafeLink utilise l'API publique VirusTotal v2. Les limites d'utilisation dépendent de votre compte VirusTotal.
