## 🚀 Fonctionnalités
- Calculs en notation polonaise inverse
- Interface utilisateur moderne et intuitive
- Historique des calculs
- Mode de calcul par lots
- Export des résultats
- API RESTful

## 🛠 Prérequis
Pour Docker :
- Docker
- Docker Compose

Pour l'installation standard :
- Python 3.8+
- Node.js 18+
- npm ou yarn
- pip (gestionnaire de paquets Python)

## 🔧 Installation et Démarrage

### Installation Standard

#### Backend
1. Créez un environnement virtuel Python :
```bash
cd backend
python -m venv venv
```

2. Activez l'environnement virtuel :
```bash
# Sur Windows
venv\Scripts\activate
# Sur Unix ou MacOS
source venv/bin/activate
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

4. Lancez le serveur :
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
1. Installez les dépendances :
```bash
cd frontend
npm install
# ou avec yarn
yarn install
```

2. Lancez le serveur de développement :
```bash
npm run dev
# ou avec yarn
yarn dev
```

### Avec Docker Compose (Recommandé)

1. Clonez le dépôt :
```bash
git clone [url-du-repo]
cd reverse-polish-calc
```

2. Lancez l'application avec Docker Compose :
```bash
docker-compose up --build
```

L'application sera accessible aux adresses suivantes :
- Frontend : http://localhost:4040
- Backend API : http://localhost:8000

### Démarrage des Services Séparément avec Docker

Si vous souhaitez démarrer les services séparément :

#### Backend
```bash
cd backend
docker build -t rpn-calculator-backend .
docker run -p 8000:8000 rpn-calculator-backend
```

#### Frontend
```bash
cd frontend
docker build -t rpn-calculator-frontend .
docker run -p 4040:80 rpn-calculator-frontend
```

## 📝 Format d'Expression RPN
Dans la notation polonaise inverse, les opérateurs suivent leurs opérandes. Par exemple :
- `3 4 +` équivaut à `3 + 4`
- `5 3 4 * +` équivaut à `5 + (3 * 4)`
- `10 5 2 * -` équivaut à `10 - (5 * 2)`

## 🔍 Exemples d'Utilisation
1. Calcul Simple :
   - Entrée : `3 4 +`
   - Résultat : `7`

2. Calcul Complexe :
   - Entrée : `5 3 4 * +`
   - Résultat : `17`

## 🛑 Arrêt de l'Application

### Pour Docker Compose
```bash
docker-compose down
```

### Pour l'Installation Standard
1. Backend : Appuyez sur Ctrl+C dans le terminal
2. Frontend : Appuyez sur Ctrl+C dans le terminal
3. Désactivez l'environnement virtuel Python :
```bash
deactivate
```

## 🔐 Variables d'Environnement
L'application utilise les variables d'environnement suivantes :
- `BACKEND_URL` : URL de l'API backend (par défaut : http://localhost:8000)
- `DATABASE_URL` : URL de la base de données

## 📚 Documentation API
La documentation de l'API est disponible à l'adresse :
http://localhost:8000/docs

## ⚠️ Dépannage
Si vous rencontrez des problèmes :

1. Vérifiez que tous les ports requis (8000, 4040) sont disponibles
2. Assurez-vous que toutes les dépendances sont correctement installées
3. Vérifiez les logs pour plus de détails :
   ```bash
   # Pour Docker
   docker-compose logs
   
   # Pour l'installation standard
   # Vérifiez les terminaux où tournent le frontend et le backend
   ```

