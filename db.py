import sqlite3
from rag_store import add_document

conn = sqlite3.connect("emails.db")
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS emails(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email_id TEXT UNIQUE,
    sender TEXT,
    receiver TEXT,
    subject TEXT,
    body TEXT,
    status TEXT
)""")
cur.execute("""CREATE TABLE IF NOT EXISTS replies(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email_id TEXT,
    draft TEXT,
    critique TEXT,
    status TEXT
)""")
conn.commit()

def save_email(email_id, sender, receiver, subject, body):
    cur.execute("INSERT OR IGNORE INTO emails(email_id, sender, receiver, subject, body, status) VALUES (?,?,?,?,?,?)",
                (email_id, sender, receiver, subject, body, "received"))
    conn.commit()
    add_document(f"email-{email_id}", body, {"type": "email", "sender": sender, "subject": subject})
