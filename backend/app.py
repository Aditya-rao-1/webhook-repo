import os
from flask import Flask, request, jsonify
from pymongo import MongoClient, DESCENDING
from dotenv import load_dotenv
from datetime import datetime
from flask_cors import CORS

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise RuntimeError("MONGO_URI not set in .env")

client = MongoClient(MONGO_URI)
db = client.github_events  # database
events_collection = db.events  # collection


# --- Helper Function for Formatting ---
def format_event(event_data):
    """
    Takes a raw event document from MongoDB and formats it into a human-readable string.
    This function is now protected by a try-except block to handle any potential data errors gracefully.
    """
    try:
        author = event_data['author']
        action = event_data['action']
        from_branch = event_data.get('from_branch', '')
        to_branch = event_data.get('to_branch', '')
        
        raw_timestamp = event_data.get('timestamp')
        if not raw_timestamp:
            return "Event with missing timestamp"

        # CORRECTED TIMESTAMP HANDLING:
        # This handles both ISO formats from GitHub:
        # 1. 'YYYY-MM-DDTHH:MM:SSZ' (from pull requests)
        # 2. 'YYYY-MM-DDTHH:MM:SS+OFFSET' (from pushes)
        # We replace 'Z' with '+00:00' to make it compatible with fromisoformat().
        parsed_time = datetime.fromisoformat(raw_timestamp.replace('Z', '+00:00'))
        
        # Format the datetime object into the desired string format.
        timestamp = parsed_time.strftime("%d %B %Y - %I:%M %p UTC")

        if action == 'PUSH':
            return f"{author} pushed to {to_branch} on {timestamp}"
        elif action == 'PULL_REQUEST':
            return f"{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}"
        elif action == 'MERGE':
            return f"{author} merged branch {from_branch} to {to_branch} on {timestamp}"
        
        return f"Unknown action: {action} by {author}"

    except (ValueError, KeyError) as e:
        # This robust error handling prevents the UI from crashing if one event is malformed.
        print(f"Error formatting event: {e}. Data: {event_data}")
        return f"Could not display event due to a data error: {event_data.get('request_id', 'Unknown ID')}"

# --- API Endpoints ---

@app.route('/webhook', methods=['POST'])
def github_webhook():
    """Receives, processes, and stores webhook events from GitHub."""
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')
    
    event_doc = None

    if event_type == 'push':
        # Add a check to handle events without a head_commit (e.g., creating/deleting a branch).
        if not data.get('head_commit'):
            return jsonify({'status': 'ignored, no head_commit'}), 200

        pusher = data['pusher']['name']
        to_branch = data['ref'].split('/')[-1]
        commit_hash = data['after']
        timestamp = data['head_commit']['timestamp']

        event_doc = {
            'request_id': commit_hash,
            'author': pusher,
            'action': 'PUSH',
            'from_branch': '', # Push event doesn't have a 'from_branch'
            'to_branch': to_branch,
            'timestamp': timestamp,
        }

    elif event_type == 'pull_request':
        action = data.get('action')
        pr_data = data.get('pull_request', {})
        
        if action == 'opened':
            event_doc = {
                'request_id': str(pr_data['id']),
                'author': pr_data['user']['login'],
                'action': 'PULL_REQUEST',
                'from_branch': pr_data['head']['ref'],
                'to_branch': pr_data['base']['ref'],
                'timestamp': pr_data['created_at'],
            }
        # This handles the "Merge" action (Brownie Points!)
        elif action == 'closed' and pr_data.get('merged'):
            event_doc = {
                'request_id': str(pr_data['id']),
                'author': pr_data.get('merged_by', {}).get('login', 'Unknown'),
                'action': 'MERGE',
                'from_branch': pr_data['head']['ref'],
                'to_branch': pr_data['base']['ref'],
                'timestamp': pr_data['merged_at'],
            }

    if event_doc:
        # This check prevents storing duplicate events, which GitHub can sometimes send.
        if not events_collection.find_one({'request_id': event_doc['request_id'], 'action': event_doc['action']}):
            events_collection.insert_one(event_doc)
            print(f"Stored event: {event_doc['action']} by {event_doc['author']}")
        else:
            print(f"Duplicate event ignored: {event_doc['action']} {event_doc['request_id']}")

    return jsonify({'status': 'success'}), 200


# --- API Endpoint for Frontend ---
@app.route('/api/events', methods=['GET'])
def get_events():
    try:
        raw_events = list(events_collection.find().sort('timestamp', DESCENDING).limit(20))
        formatted = [format_event(e) for e in raw_events]
        return jsonify(formatted)
    except Exception as e:
        print("Error fetching events:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
