from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from classifier import classify_email
from collections import Counter
import base64
from email.message import EmailMessage

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

creds = Credentials.from_authorized_user_file(
    'token.json',
    SCOPES
)

service = build('gmail', 'v1', credentials=creds)

def get_or_create_label(service, label_name):
    labels = service.users().labels().list(userId='me').execute().get('labels', [])

    for label in labels:
        if label['name'] == label_name:
            return label['id']

    created = service.users().labels().create(
        userId='me',
        body={
            "name": label_name,
            "labelListVisibility": "labelShow",
            "messageListVisibility": "show"
        }
    ).execute()

    return created['id']

def apply_label(service, msg_id, label_id):
    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={"addLabelIds": [label_id]}
    ).execute()

def archive_email(service, msg_id):
    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={"removeLabelIds": ["INBOX"]}
    ).execute()

def auto_reply(service, msg, subject):
    reply = EmailMessage()
    reply.set_content("Спасибо за ваше письмо. Я скоро отвечу.")

    reply["To"] = msg.get("From", "me")
    reply["Subject"] = "Re: " + subject

    raw = base64.urlsafe_b64encode(reply.as_bytes()).decode()

    service.users().messages().send(
        userId='me',
        body={
            "raw": raw,
            "threadId": msg["threadId"]
        }
    ).execute()

results = service.users().messages().list(
    userId='me',
    q='is:unread',
    maxResults=10
).execute()

messages = results.get('messages', [])

print(f'Найдено писем: {len(messages)}\n')

counter = Counter()

label_map = {
    "spam": "AI-Spam",
    "promo": "AI-Promo",
    "newsletter": "AI-Newsletter",
    "important": "AI-Important",
    "personal": "AI-Personal",
    "routine_question": "AI-Routine"
}

for msg in messages:
    message = service.users().messages().get(
        userId='me',
        id=msg['id'],
        format='full'
    ).execute()

    headers = message['payload']['headers']

    subject = 'Без темы'
    body = ""

    for header in headers:
        if header['name'] == 'Subject':
            subject = header['value']
            break

    parts = message.get("payload", {}).get("parts", [])
    for part in parts:
        if part.get("mimeType") == "text/plain":
            data = part.get("body", {}).get("data")
            if data:
                body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

    category = classify_email(subject + " " + body)

    label_name = label_map.get(category, "AI-Other")
    label_id = get_or_create_label(service, label_name)
    apply_label(service, msg['id'], label_id)

    if category == "spam":
        archive_email(service, msg['id'])

    elif category == "newsletter":
        archive_email(service, msg['id'])

    elif category == "important":
        print("IMPORTANT:", subject)

    elif category == "routine_question":
        auto_reply(service, message, subject)

    print(f"Тема: {subject}")
    print(f"Категория: {category}")
    print("-" * 40)

    counter[category] += 1

print("\nСтатистика:")
for k, v in counter.items():
    print(k, ":", v)