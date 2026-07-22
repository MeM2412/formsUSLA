import psycopg2
from psycopg2 import IntegrityError
import os
from dotenv import load_dotenv

# This function reads the .env file and loads the variables into the environment
load_dotenv()

def get_db_connection():
    """Establish a connection to the PostgreSQL database."""
    # Fetch the exact variable name you used in your .env file
    db_url = os.environ.get("DB_URL")
    
    if not db_url:
        raise ValueError("No DB_URL found. Please check your .env file.")
        
    conn = psycopg2.connect(db_url)
    return conn

def insert_submission(first_name, middle_name, last_name, phone, email, privacy_accepted):
    """
    Inserts a new form submission into the database.
    Enforces the 'one response per user' rule by catching IntegrityErrors.
    """
    # Safety check for the required privacy policy
    if not privacy_accepted:
        return {"success": False, "message": "Privacy policy must be accepted."}

    conn = get_db_connection()
    cur = conn.cursor()
    
    insert_query = """
        INSERT INTO event_submissions 
        (first_name, middle_name, last_name, phone, email, privacy_policy_accepted)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
    """
    
    try:
        # Execute the query with parameterized inputs to prevent SQL injection
        cur.execute(insert_query, (first_name, middle_name, last_name, phone, email, privacy_accepted))
        submission_id = cur.fetchone()[0]
        conn.commit()
        
        return {"success": True, "id": submission_id, "message": "Submission successful!"}
        
    except IntegrityError:
        # This catches the UNIQUE constraint failures for phone and email
        conn.rollback()
        return {"success": False, "message": "A submission with this email or phone number already exists."}
        
    except Exception as e:
        conn.rollback()
        return {"success": False, "message": f"An unexpected error occurred: {str(e)}"}
        
    finally:
        cur.close()
        conn.close()

def get_all_submissions():
    """
    Fetches all event submissions from the database.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Retrieve all data ordered by the newest submissions first
    query = """
        SELECT id, first_name, middle_name, last_name, phone, email, created_at, gadget_given
        FROM event_submissions 
        ORDER BY created_at DESC;
    """
    
    try:
        cur.execute(query)
        rows = cur.fetchall()
        # Fetch the column names to use as headers in our dashboard
        columns = [desc[0] for desc in cur.description]
        return {"success": True, "data": rows, "columns": columns}
        
    except Exception as e:
        return {"success": False, "message": f"Failed to fetch data: {str(e)}"}
        
    finally:
        cur.close()
        conn.close()


def update_gadget_status(user_id, status):
    """Updates the gadget_given boolean for a specific user."""
    try:
        conn = psycopg2.connect(os.environ.get("DB_URL"))
        cur = conn.cursor()
        
        # %s prevents SQL injection attacks
        cur.execute(
            "UPDATE event_submission SET gadget_given = %s WHERE id = %s",
            (status, user_id)
        )
        
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Database error: {e}")
        return False