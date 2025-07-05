
# ⚡ GitHub Webhook Event Tracker

A sleek full-stack project that captures GitHub activity (Push, Pull Request, Merge) in real-time using webhooks, stores it in MongoDB, and displays it with a 🔥 hot UI.

## 🧠 What It Does

Whenever you:
- Push code
- Open a pull request
- Merge a branch

GitHub sends a webhook ➡️ Our Flask API processes the event ➡️ Stores it in MongoDB ➡️ React frontend fetches and displays it every 15 seconds.

---

## 🧱 Project Structure

```

📦 github-event-tracker/
├── backend/
│   ├── app.py              # Flask API to handle webhooks and fetch events
│   ├── .env                # MongoDB URI goes here
│   ├── requirements.txt    # Python dependencies
│   ├── package.json        # If using concurrently or dev dependencies
│   └── ...
│
├── frontend/
│   ├── src/
│   │   └── App.jsx         # Core UI logic
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   └── ...
│
└── README.md               # You're reading it.

````

---

## 🛠️ Tech Stack

- **Frontend:** React + TailwindCSS + Vite
- **Backend:** Flask + PyMongo
- **Database:** MongoDB

---

## ⚙️ How to Run It Locally

### 1. 🧩 Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate   # On Windows use venv\Scripts\activate
pip install -r requirements.txt

# Create your .env file
echo "MONGO_URI=your_mongodb_uri_here" > .env

# Run the Flask server
python app.py
````

### 2. 🎨 Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Your React app will run on [http://localhost:5173](http://localhost:5173), and the backend on [http://localhost:5000](http://localhost:5000).

---

## 🪝 Setting Up GitHub Webhook

1. Go to your GitHub repo (e.g., `action-repo`)
2. Go to **Settings > Webhooks > Add webhook**
3. Payload URL:
   `http://localhost:5000/webhook`
4. Content type: `application/json`
5. Events: Select `Just the push and pull_request events`
6. Save

✅ Now GitHub events will start flowing into your app!

---

## 🧾 Example Event Formats

* 🟢 **Push:**
  `"Travis pushed to staging on 1st April 2021 - 9:30 PM UTC"`

* 🟡 **Pull Request:**
  `"Travis submitted a pull request from staging to master on 1st April 2021 - 9:00 AM UTC"`

* 🔴 **Merge:**
  `"Travis merged branch dev to master on 2nd April 2021 - 12:00 PM UTC"`

---

## 🚀 Bonus Touches

* ✅ Handles duplicate events (GitHub sometimes retries!)
* ✅ Graceful error handling for bad payloads
* ✅ Beautiful, dark-themed UI with animations
* ✅ Auto-refresh every 15 seconds
* ✅ Clear structure for maintainability

---

## 📌 Tips

* Use [ngrok](https://ngrok.com/) or [LocalTunnel](https://theboroer.github.io/localtunnel-www/) to test GitHub webhooks locally.
* Want brownie points? Handle the `merge` event via `pull_request.closed` + `merged: true` – already implemented 😉

---

## 🤝 Let's Connect

If you found this interesting, feel free to fork, star ⭐, or reach out!

> Built with ❤️, Flask, and React.

