# Nur CRM

**Nur CRM** is a web application designed to help businesses manage their clients, track product sales, and calculate profits efficiently. It leverages Django's powerful features and offers a user-friendly interface for seamless business management.

## Features

- **User Authentication**: Custom login and signup functionality with email-based authentication.
- **Client Management**: Add, view, and manage client details.
- **Product Management**: Track products, prices, stock, and sales.
- **Profit Calculation**: Automatically calculate benefits based on sales data.
- **Email Notifications**: Send emails to users upon registration or during specific actions (e.g., password reset).
- **Password Management**: Custom password reset functionality with permissions and email validation.

## Technologies Used

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS (customized templates)
- **Database**: PostgreSQL
- **Email**: Django's `send_mail` for email notifications

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/siddikmeo7/NurCRM.git
   cd nur-crm
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser for accessing the admin panel:

   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:

   ```bash
   python manage.py runserver
   ```

7. Open the application in your browser:

   ```
   http://127.0.0.1:8000/
   ```

## Usage

- Access the admin panel to manage the application: `http://127.0.0.1:8000/admin/`
- Register a new user or log in with an existing account.
- Navigate through the dashboard to add clients, manage products, and track profits.

## Project Structure

```
NurCRM/
├── accounts/          # Custom user authentication and management
├── products/          # Product management app
├── clients/           # Client management app
├── templates/         # HTML templates
├── static/            # Static files (CSS, JS, images)
├── Nur/               # Main project configuration
└── requirements.txt   # Project dependencies
```

## Key Code Examples

### Custom Login View

```python
class LoginView(DjangoLoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')
```

### Custom Password Reset

```python
class CustomPasswordResetView(PermissionRequiredMixin, DjangoPasswordResetView):
    permission_required = 'auth.change_user'
    def form_valid(self, form):
        email = form.cleaned_data["email"]
        users = form.get_users(email)
        user = users.first()
        if user:
            if user.last_password_reset and (now() - user.last_password_reset).total_seconds() < 3600:
                return HttpResponseForbidden("A password reset email has already been sent. Please try again later.")
            user.last_password_reset = now()
            user.save()
        return super().form_valid(form)
```

## Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request.

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For inquiries or support, please contact **Abubakr Khusainov** at `your-email@example.com`.
