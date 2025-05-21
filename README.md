# Code Sharing Application

A Django-based web application designed for developers to share, organize, and manage code snippets efficiently.

## Features

* **User Authentication**: Secure login and registration system.
* **Code Snippet Management**: Users can create, edit, and delete their code snippets.
* **Syntax Highlighting**: Supports multiple programming languages for better readability.
* **Search Functionality**: Easily search through saved snippets.
* **Responsive Design**: Accessible on both desktop and mobile devices.

## Technologies Used

* **Backend**: Django (Python)
* **Frontend**: HTML, CSS, JavaScript
* **Database**: SQLite (default)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/SulemanMughal/code-sharing.git
   cd code-sharing
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations:

   ```bash
   python manage.py migrate
   ```

4. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

5. Run the development server:

   ```bash
   python manage.py runserver
   ```

6. Access the application at `http://127.0.0.1:8000/`.

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.
