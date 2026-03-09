# Test_PB

# 🧪 Tests UI automatisés — ParaBank
TEST 2
Tests UI automatisés avec **Selenium** et **Behave (BDD)** sur le site de démo
[ParaBank](https://parabank.parasoft.com/parabank/index.htm).

---

## 📋 Features testées

| Feature | Scénarios | Statut |
|---------|-----------|--------|
| 🔐Login | 3 | ✅ |
| 💸Transfer Funds | 4 | ✅ |
| **Total** | **7** | **✅** |

### 🔐 Login
- Connexion avec identifiants valides
- Connexion avec username inexistant
- Connexion avec mot de passe incorrect

### 💸 Transfer Funds
- Transfert valide entre deux comptes
- Transfert avec montant négatif
- Transfert avec montant vide
- Transfert avec caractère non numérique

---

## 📁 Structure du projet
```
Test_PB/
├── .github/
│   └── workflows/
│       └── tests.yml          ← CI/CD GitHub Actions
├── features/
│   ├── login.feature          ← Scénarios login
│   ├── transfer.feature       ← Scénarios transfert
│   └── steps/
│       ├── login_steps.py     ← Steps Selenium login
│       └── transfer_steps.py  ← Steps Selenium transfert
├── environment.py             ← Configuration driver Edge/Chrome
├── generer_rapport.py         ← Génération rapport HTML
├── rapport.json               ← Rapport JSON (généré)
├── rapport.html               ← Rapport HTML (généré)
├── screenshots/               ← Screenshots en cas d'échec
├── .gitattributes
└── README.md
```

---

## 🛠️ Technologies

| Outil | Version | Rôle |
|-------|---------|------|
| Python | 3.14 | Langage |
| Behave | 1.3.3 | Framework BDD |
| Selenium | 4.40.0 | Automatisation navigateur |
| Edge | - | Navigateur local |
| Chrome | - | Navigateur CI/CD |
| GitHub Actions | - | CI/CD |

---

## ⚙️ Installation
```bash
# 1. Cloner le repo
git clone https://github.com/yassminekh/Test_PB.git
cd Test_PB

# 2. Installer les dépendances
pip install behave selenium webdriver-manager
```

---

## ▶️ Lancer les tests
```bash
# Tous les tests
py -m behave --no-capture -v

# Login uniquement
py -m behave features/login.feature --no-capture -v

# Transfert uniquement
py -m behave features/transfer.feature --no-capture -v
```

---

## 📊 Générer le rapport HTML
```bash
# 1. Génère le rapport JSON
py -m behave --format json --outfile rapport.json

# 2. Convertit en HTML
py generer_rapport.py

# 3. Ouvre le rapport
start rapport.html
```

---

## 🔄 CI/CD GitHub Actions

Le workflow se déclenche automatiquement à chaque **push** ou **pull request** sur `main`.
```
Push sur GitHub
      ↓
🔐 Job 1 : Tests Login       (3 scénarios)
      ↓ ✅
💸 Job 2 : Tests Transfert   (4 scénarios)
      ↓ ✅
📊 Job 3 : Rapport Final     (rapport.html)
```

### Télécharger le rapport depuis GitHub Actions
```
GitHub → Actions → dernier run → Artifacts → rapport-html-final
```

---

## 🖥️ Navigateurs supportés

| Environnement | Navigateur | Mode |
|---|---|---|
| Local (Windows) | Microsoft Edge | Visible |
| CI/CD (Ubuntu) | Google Chrome | Headless |

---

## 📸 Screenshots

Les screenshots sont **automatiquement sauvegardés** dans `screenshots/`
uniquement en cas d'échec d'un test.
```
screenshots/
├── login_valide_FAILED.png
├── Connexion_avec_username_inexistant_FAILED.png
└── ...
```

---

## 👤 Compte de test ParaBank

| Champ | Valeur |
|---|---|
| Username | john |
| Password | demo |

> ⚠️ Compte de démo public — peut être réinitialisé par ParaBank à tout moment.