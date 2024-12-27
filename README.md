# Custom Authentication and Password Reset in Django

This project demonstrates a custom implementation of Django's authentication system, including login, logout, user signup, and password reset functionalities.

## Features

- **Custom Login**
  - Supports a custom login template.
  - Redirects users to a specific page after successful login.

- **Custom Logout**
  - Redirects users to a custom logout page after logging out.

- **User Signup**
  - Allows new users to sign up using a custom form.
  - Sends a welcome email to the registered email address.

- **Password Reset**
  - Supports email-based password reset.
  - Restricts frequent password reset requests (minimum interval: 1 hour).

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/siddikmeo7/custom-authentication.git
   ```

2. Navigate to the project directory:
   ```bash
   cd custom-authentication
   ```

3. Create a virtual environment and activate it:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Apply migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

8. Access the application at `http://127.0.0.1:8000/`.

## Usage

### Custom Views

#### LoginView
- Template: `registration/login.html`
- Redirects to `home` on successful login.

#### CustomLogoutView
- Redirects to a custom logout page after logout.

#### UserSignupForm
- Template: `registration/signup.html`
- Sends a welcome email upon successful registration.

#### Password Reset Views
- **CustomPasswordResetView**: 
  - Restricts users from requesting a password reset more than once every hour.
- **CustomPasswordResetDoneView**: 
  - Displays a confirmation message after a password reset email is sent.
- **CustomPasswordResetConfirmView**: 
  - Allows users to set a new password using a confirmation link.
- **CustomPasswordResetCompleteView**: 
  - Informs users of a successful password reset.

### Email Configuration

To enable email functionality, configure your email settings in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your_smtp_server'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@example.com'
EMAIL_HOST_PASSWORD = 'your_email_password'
```

### Permission Handling

The password reset functionality requires the `auth.change_user` permission.

## Code Structure

### Views

- **LoginView**: Handles user login.
- **CustomLogoutView**: Handles user logout.
- **UserSignupForm**: Manages user registration.
- **Password Reset Views**: Handle the entire password reset process with customization.

### Forms

- **CustomUserForm**: Define your custom user signup form in `Nur.forms`.

## Example Code Snippet

```python
from django.http import HttpResponseForbidden
from django.utils.timezone import now

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

Contributions are welcome! Please fork this repository and submit a pull request for any changes or enhancements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please reach out to:
- Email: `your_email@example.com`
- GitHub: [yourusername](https://github.com/yourusername)
