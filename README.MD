# 🔐 Secure Port Redirector (via SSLStream)

Ce projet est un redirecteur de flux sécurisé, développé en C#. Il redirige uniquement le trafic d'un port si le client est authentifié à l’aide d’un certificat SSL. Il repose sur l’utilisation de `SSLStream` pour garantir une communication sécurisée entre le client et le serveur.

## ✨ Fonctionnalités

- 🔁 Redirection de flux réseau entre client et serveur.
- 🛡️ Authentification forte via certificats SSL.
- ⚙️ Génération automatique des certificats et configuration.
- 💼 Compatible Windows (avec .NET 8.0).
- 🧪 Build & publish automatisé avec `dotnet`.
- 📦 Client embedded

---

## 🚀 Installation

> 💡 Ce projet a été testé uniquement sous **Windows**. Cependant il est possible d'héberger le serveur sur linux en remplaçant le `<RuntimeIdentifier>win-x64</RuntimeIdentifier>` par `<RuntimeIdentifier>linux-x64</RuntimeIdentifier>` dans `server/server.csproj`

### Prérequis

- une machine sous windows (7, 8.1, 10, 11, serveur, etc) pour générer les executables avec `compile.bat` et héberger le serveur
- PowerShell
- Accès à Internet pour l'installation des composant

### Étapes d'installation automatique

Le script Python fourni installe automatiquement :
- Le SDK .NET 8.0
- 7-Zip (version CLI `7zr.exe` / `7za.exe`)
- OpenSSL Windows (précompilé)
- Génère les certificats client/serveur
- Modifie les fichiers `Program.cs` avec les bons paramètres
- Compile et publie les projets client et serveur

### Exécution du script

## Modifier la configuration dans le fichier **`conf.json`** et spécifiez vos adresse IP et les ports associés

```json
{
  "client": {
    "RemoteIP": "127.0.0.1", // IP du serveur de redirection celui exposé sur internet
    "RemotePort": 50000,     // Port exposé sur internet
    "ListenPort": 443        // Port sur lequel le flux sera dupliqué et auquel vous devez vous connecter (ex: localhost:443)
  },
  "server": {
    "DestinationIP": "127.0.0.1", // IP de l'appareil qui doit recevoir la requête (ex: localhost:445) pour un service qui écoute sur le port 445 de la machine local (peut être une machine sur le même réseau tel qu'un nas).
    "DestinationPort": 445,       // Port sur lequel écoute le service comme spécifié plus haut
    "ListenPort": 50000           // Port d'écoute du redirecteur de flux -> doit être ouvert sur internet !
  }
}

```

## Après avoir modifié la configuration exécutez : `compile.bat`

### > Le serveur de redirection se trouve dans : `./server/bin/Release/net8.0/server.exe`
### > Le client se trouve dans : `./client/bin/Release/net8.0/client.exe`

## 🧪 Exemple d'utilisation
### Une fois les binaires compilés :

### 1. Lance le serveur sur la machine dont le port du redirecteur est exposé:
```./server/bin/Release/net8.0-windows/server.exe```

### 2. Lance le client sur n'importe quelle machine windows :

```./client/bin/Release/net8.0-windows/client.exe```

## Vous pouvez maintenant accèder a votre service via `localhost:<ListenPort>` sur le poste client depuis n'importe où.


## 📝 Licence
### Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus d’informations.

## 🤝 Contributions
#### Les contributions sont les bienvenues ! N’hésitez pas à ouvrir une issue ou une pull request pour améliorer le projet ou ajouter des fonctionnalités.