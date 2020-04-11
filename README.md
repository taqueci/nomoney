*Read this in other languages: [日本語](README.ja.md)*

# NoMoney

NoMoney is a simple household account book (for my wife).
This application is implemented by Django.

The way of booking is based on double-entry bookkeeping system.

![Screenshot](money/static/money/img/screenshots/report-lg-en.png)

## Requirements

* Python 3.7+
* Django 3.0
* PostgreSQL 9.5+

## Installation

### Database

Prepare database for NoMoney.

### NoMoney

1. Clone or copy files of NoMoney.
2. Change directory to NoMoney directory and
execute `pip3 install -r requirements.txt` to install necessary libraries.
3. Modify `config/settings.py` according to your environment.
4. Execute `python3 manage.py migrate` to migrate.
5. Execute `django-admin compilemessages` to compile .po file.

### Web server

Configure web server.

See [Deploying Django](https://docs.djangoproject.com/en/3.0/howto/deployment/).

## Usage

### Account setting

First, add accounts.
Open administraton page and add accounts as the following:

| Name           | Account   |
|----------------|-----------|
| Salary         | Income    |
| Cash           | Asset     |
| Credit card    | Liability |
| Foods          | Expense   |
| Clothes/Beauty | Expense   |
| ...            | ...       |

### Journal

In order to book giving and taking of money,
open "New Journal" on the right side of the page.

### Report

If you want to know the summary, open "Reports" page.

## License

[MIT](LICENSE)

## Author

Takeshi Nakamura
