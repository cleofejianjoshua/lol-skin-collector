# LOL Skin Gacha Collector

## Setup Instructions (Using SQLite)

### 1. Clone the repository

```
git clone https://github.com/cleofejianjoshua/lol-skin-collector.git
cd lol-skin-collector
```

---

### 2. Setup Python backend

```
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

### 3. Run migrations

```
python -m flask db upgrade
```

---

### 4. Start Flask backend

```
python microblog.py
```

Backend runs at:
http://127.0.0.1:5000

---

### 5. Setup Vue frontend

Open a new terminal:

```
cd frontend
npm install
npm run dev
```

Frontend runs at:
http://localhost:5173

---

### 6. Use the app

Open the Vue URL in your browser.
