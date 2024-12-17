import logging

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(message)s')

def handle_db_exception(e, context):
    logging.error(f"Database error occurred while {context}: {e}")  # Logs an ERROR

