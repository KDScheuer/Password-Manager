# Password Manager

This simple password manager application allows you to securely store and manage your account information with a master password. It uses encryption to protect your usernames and passwords.

## Features
 - Secure Storage: Encrypts and securely stores your account information using Fernet symmetric encryption.
 - User-Friendly Interface: Provides an easy-to-use graphical interface for adding, modifying, and deleting accounts.
 - Master Password: Requires a master password for authentication to access stored passwords.
 - Data Persistence: Saves account information securely, allowing you to access it between sessions.

## Dependencies
 - pip install cryptography

## Running the Password Manager:
 - python3 password_manager.py
 - Follow the On-Screen Prompts:
    - Set your master password on the first run.
    - Log in with your master password on subsequent runs.
    - Add, modify, or delete accounts as needed.
 - Exit the Application
    - Choose the "Exit" option from the main menu to close the application.

## Notes
 - Ensure that you remember your master password. If forgotten, there is no way to recover it.
 - Keep the auth.key file secure, as it is crucial for authenticating your master password.

## Disclaimer
 - This password manager is provided as-is, without any warranties. Use it at your own risk.

Feel free to contribute or report issues on GitHub.
