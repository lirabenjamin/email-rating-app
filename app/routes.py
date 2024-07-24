from flask import render_template, request, redirect, url_for, session, current_app as app, jsonify
import json
import random
import logging
from bson import ObjectId

# Load emails
with open('instance/emails.json', 'r') as f:
    emails = json.load(f)

# Track rated emails
rated_emails = {ra: [] for ra in ['RA1', 'RA2', 'RA3', 'RA4', 'RA5', 'RA6', 'RA7', 'RA8', 'RA9', 'RA10']}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ra_name = request.form['ra_name']
        session['ra_name'] = ra_name
        return redirect(url_for('rate_email'))
    return render_template('index.html')

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
            }

            # Save responses to MongoDB
            result = app.db.responses.insert_one(responses)
            rated_emails[ra_name].append(email_id)
        except Exception as e:
            logging.error(f"Error saving to database: {e}")
            return jsonify(error="An error occurred while saving your response. Please try again."), 500

    available_emails = [email for email in emails if email['id'] not in rated_emails[ra_name]]
    if not available_emails:
        rated_emails[ra_name] = []
        available_emails = emails

    email_to_rate = random.choice(available_emails)
    return render_template('rating.html', email=email_to_rate)

@app.route('/responses', methods=['GET'])
def get_responses():
    try:
        responses = app.db.responses.find()
        response_list = []
        for response in responses:
            response['_id'] = str(response['_id'])  # Convert ObjectId to string
            response_list.append(response)
        return jsonify(response_list)
    except Exception as e:
        logging.error(f"Error retrieving responses: {e}")
        return jsonify(error="An error occurred while retrieving responses."), 500
