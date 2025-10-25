import os
import asyncio
import email
from imapclient import IMAPClient
from dotenv import load_dotenv

from workflows import build_agent  
from rag_store import add_document  

load_dotenv()

EMAIL_ADDR = "safeernawaz649@gmail.com"
EMAIL_PASS = os.getenv("APP_PASSWORD")
IMAP_SERVER = "imap.gmail.com"

# -------- Helpers --------
def get_email_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode(errors="ignore")
    else:
        return msg.get_payload(decode=True).decode(errors="ignore")
    return ""

def save_reply(subject, reply):
    with open("replies.txt", "a", encoding="utf-8") as f:
        f.write(f"Subject: {subject}\nReply: {reply}\n{'-'*40}\n")

# -------- Email handler --------
async def handle_email(msgid, data, client):
    msg = email.message_from_bytes(data[b"RFC822"])
    subject = msg["Subject"] or "(No Subject)"
    body = get_email_body(msg)

    print(f"\n📧 Processing email: {subject}")

    # Run workflow
    # reply = await run_workflow(subject, body)
    reply = await build_agent()

    # Save to disk (persistence)
    save_reply(subject, reply)

    # Store in RAG for future context
    add_document(f"Subject: {subject}\nBody: {body}\nReply: {reply}")

    print(f"✅ Reply generated for {subject}:\n{reply}\n")

# -------- Main loop --------
async def main():
    with IMAPClient(IMAP_SERVER) as client:
        client.login(EMAIL_ADDR, EMAIL_PASS)
        client.select_folder("INBOX")

        print("📨 Email agent started...")

        while True:
            print("🔍 Checking for unseen messages...")
            messages = client.search(["UNSEEN"])
            print(messages)
            if messages:
                response = client.fetch(messages, ["RFC822"])
                tasks = [
                    asyncio.create_task(handle_email(msgid, data, client))
                    for msgid, data in response.items()
                ]
                await asyncio.gather(*tasks)

            await asyncio.sleep(15)  # check every 15s

if __name__ == "__main__":
    asyncio.run(main())

