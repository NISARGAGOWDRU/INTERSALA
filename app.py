from flask import Flask, request, jsonify
import psycopg2
from config import DATABASE

app = Flask(__name__)

def get_db_connection():
    """Connect to the PostgreSQL database."""
    conn = psycopg2.connect(
        dbname=DATABASE['dbname'],
        user=DATABASE['user'],
        password=DATABASE['password'],
        host=DATABASE['host'],
        port=DATABASE['port']
    )
    return conn

@app.route('/')
def home():
    """Home route to check if the Flask app is running."""
    return "Flask app is running!"

@app.route('/user/profile', methods=['POST'])
def save_user_profile():
    """Save user profile data to the database."""
    # Step 1: Get the JSON data from the request
    data = request.json
    
    # Step 2: Validate the input data
    required_fields = ['name', 'skills', 'experience_level', 'preferences']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        # Step 3: Extract the user profile data from JSON
        name = data['name']
        skills = ','.join(data['skills'])  # Convert skills list to a comma-separated string
        experience_level = data['experience_level']
        desired_roles = ','.join(data['preferences']['desired_roles'])  # Convert to comma-separated string
        locations = ','.join(data['preferences']['locations'])  # Convert to comma-separated string
        job_type = data['preferences']['job_type']

        # Step 4: Connect to PostgreSQL
        conn = get_db_connection()
        cursor = conn.cursor()

        # Step 5: Insert data into the users table
        query = """
        INSERT INTO users (name, skills, experience_level, desired_roles, locations, job_type)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, skills, experience_level, desired_roles, locations, job_type))

        # Step 6: Commit the transaction and close the connection
        conn.commit()
        cursor.close()
        conn.close()

        # Step 7: Return success response
        return jsonify({'message': 'User profile saved successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
