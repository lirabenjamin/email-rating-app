from flask import render_template, request, redirect, url_for, session, current_app as app, jsonify
import json
import random
import logging
from datetime import datetime
from bson import ObjectId

# Load RA names and questions from files
with open('instance/users.json', 'r') as f:
    ra_names = json.load(f)

with open('instance/questions.json', 'r') as f:
    questions = json.load(f)

# Load emails
with open('instance/emails2.json', 'r') as f:
    emails = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ra_name = request.form['ra_name']
        session['ra_name'] = ra_name
        return redirect(url_for('rate_email'))
    return render_template('index.html', ra_names=ra_names)

@app.route('/rate', methods=['GET', 'POST'])
def rate_email():
    ra_name = session.get('ra_name')
    if not ra_name:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            email_id = int(request.form['email_id'])
            responses = {
                'ra_name': ra_name,
                'email_id': email_id,
                'q1': request.form['q1'],
                'q2': request.form['q2'],
                'q3': request.form['q3'],
                'q4': request.form['q4'],
                'q5': request.form['q5'],
                'q6': request.form['q6'],
                'timestamp': datetime.utcnow()  # Save the current UTC timestamp

            }

            # Save responses to MongoDB
            app.db.responses.insert_one(responses)
        except Exception as e:
            logging.error(f"Error saving to database: {e}")
            return jsonify(error="An error occurred while saving your response. Please try again."), 500

    # Get emails rated by the current RA
    rated_by_ra = app.db.responses.find({'ra_name': ra_name}, {'email_id': 1, '_id': 0})
    rated_email_ids = [email['email_id'] for email in rated_by_ra]

    # Get the count of ratings for each email
    email_rating_counts = app.db.responses.aggregate([
        {'$group': {'_id': '$email_id', 'count': {'$sum': 1}}}
    ])
    email_rating_counts = {item['_id']: item['count'] for item in email_rating_counts}

    # Filter out emails already rated by the current RA
    available_emails = [email for email in emails if email['id'] not in rated_email_ids]

    # Find the minimum number of ratings any available email has received
    min_ratings = min(email_rating_counts.get(email['id'], 0) for email in available_emails)

    # Filter the available emails to those with the minimum number of ratings
    min_rated_emails = [email for email in available_emails if email_rating_counts.get(email['id'], 0) == min_ratings]

    if not min_rated_emails:
        # All emails have been rated by the current RA, reset and start the second pass
        rated_email_ids = []
        min_rated_emails = emails
        min_ratings = min(email_rating_counts.get(email['id'], 0) for email in min_rated_emails)
        min_rated_emails = [email for email in min_rated_emails if email_rating_counts.get(email['id'], 0) == min_ratings]

    # Select a random email from the list of emails with the minimum number of ratings
    email_to_rate = random.choice(min_rated_emails)
    return render_template('rating.html', email=email_to_rate, questions=questions)

@app.route('/responses', methods=['GET'])
def get_responses():
    try:
        responses = app.db.responses.find()
        response_list = []
        for response in responses:
            response['_id'] = str(response['_id'])  # Convert ObjectId to string
            response['timestamp'] = response['timestamp'].isoformat()  # Convert timestamp to string
            response_list.append(response)
        return jsonify(response_list)
    except Exception as e:
        logging.error(f"Error retrieving responses: {e}")
        return jsonify(error="An error occurred while retrieving responses."), 500
