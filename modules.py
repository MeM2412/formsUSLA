# Import the database function needed to update the status
from db_logic import update_gadget_status

def handle_give_gadget(uid):
    """Callback function to convert Numpy ID and save gadget status."""
    # Convert the Numpy ID to a standard Python integer so PostgreSQL accepts it
    clean_id = int(uid)
    update_gadget_status(clean_id, True)