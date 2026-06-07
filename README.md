AI Anti-Spam Email Classifier

Description

This project automatically analyzes incoming Gmail messages and classifies them by communication intent.

The system can:

* read emails from Gmail via Gmail API;
* classify messages into categories;
* generate statistics on incoming emails;
* apply automated actions depending on the category.

Categories

* spam
* promo
* newsletter
* personal
* important
* routine_question

Architecture

Gmail API → Email Extraction → Intent Classification → Statistics and Actions

Examples of actions:

* spam → archive
* newsletter → label
* important → notification
* routine_question → auto-reply

Technologies

* Python
* Gmail API
* OAuth 2.0
* Rule-based NLP

Running the Project

1. Run authentication:

python auth.py

2. Start email processing:

python read_emails.py

Example Output

Тема: Оповещение системы безопасности
Категория: important

Тема: IT-магистратура онлайн
Категория: promo

Статистика:

important: 4
promo: 3
personal: 3

important: 4
promo: 3
personal: 3
