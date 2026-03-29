LOL Skin Gacha Collector
Setup Instructions
1. Clone the repository

git clone https://github.com/cleofejianjoshua/lol-skin-collector.git
cd yourrepo

2. Setup Python backend

python -m venv venv

Activate virtual environment:

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

Install dependencies:
pip install -r requirements.txt

3. Setup PostgreSQL

Make sure PostgreSQL is installed.

Create database:
createdb microblog

4. Configure environment variables

Copy the example file:
cp .env.example .env

Edit .env and set your PostgreSQL username/password.

5. Run migrations

flask db upgrade

6. Start Flask backend

python microblog.py

Backend runs at:
http://127.0.0.1:5000

7. Setup Vue frontend

Open a new terminal:

cd frontend
npm install
npm run dev

Frontend runs at:
http://localhost:5173

8. Use the app

Open the Vue URL in your browser.
