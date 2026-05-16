# LOL Skin Gacha Collector
LoL Skin Gacha Collector is a fun web app where you can collect League of Legends skins. You can try your luck in the Gacha to get new skins, earn gold by clicking in the Forge, and build your own skin collection. You can also search for other players to see what skins they have and show off your own profile.

## Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/cleofejianjoshua/lol-skin-collector.git
cd lol-skin-collector
```

---

### 2. Setup Python backend

```
cd backend
python -m venv venv
```

#### Activate virtual environment

**Windows:**

```
venv\Scripts\activate
```

**Mac/Linux:**

```
source venv/bin/activate
```

#### Install dependencies

```
pip install -r requirements.txt
```

---


### 3. Start Flask backend

```
cd backend
python run.py
```

Backend runs at:
http://127.0.0.1:5000

---

### 4. Setup Vue frontend

Open a new terminal:

```
cd frontend
npm install
npm run dev
```

Frontend runs at:
http://localhost:5173

---

### 5. Use the app

Open the Vue URL in your browser.
