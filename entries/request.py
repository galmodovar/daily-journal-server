import sqlite3
import json
from models import Entry, Mood


def get_all_entries():
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.date,
            a.concept,
            a.entry,
            a.mood_id,
            b.mood
        FROM journalentry a
        JOIN mood b
            ON b.id = a.mood_id
        """)

        # Initialize an empty list to hold all entry representations
        entries = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an entry instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            entry = Entry(row['id'], row['date'], row['concept'],
                          row['entry'], row['mood_id'])
            
            mood = Mood(row['mood_id'], row['mood'])

            entry.mood = mood.__dict__

            entries.append(entry.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(entries)

# Function with a single parameter


def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.date,
            a.concept,
            a.entry,
            a.mood_id
        FROM journalentry a
        WHERE a.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an entry instance from the current row
        entry = Entry(data['id'], data['date'], data['concept'],
                      data['entry'], data['mood_id'])

        return json.dumps(entry.__dict__)


def delete_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM journalentry
        WHERE id = ?
        """, (id, ))

def search_entries(searchTerms):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(f"""
        SELECT
            a.id,
            a.date,
            a.concept,
            a.entry,
            a.mood_id
        FROM JournalEntry a
        WHERE a.entry LIKE "%{searchTerms}%"
        """)

        dataset = db_cursor.fetchall()

        entries = []

        for row in dataset:
            entry = Entry(row['id'], row['date'], row['concept'], row['entry'], row['mood_id'])

            entries.append(entry.__dict__)
        
        return json.dumps(entries)

# Function to create animal
def create_entry(new_entry):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO journalentry
            ( date, concept, entry, mood_id )
        VALUES
            ( ?, ?, ?, ? )
        """, (new_entry['date'], new_entry['concept'],
              new_entry['entry'], new_entry['moodId'] ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_entry['id'] = id

# Function to update entry
def update_entry(id, new_entry):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE journalentry
            SET
                date = ?,
                concept = ?,
                entry = ?,
                mood_id = ?
        WHERE id = ?
        """, (new_entry['date'], new_entry['concept'],
              new_entry['entry'], new_entry['mood_id'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
