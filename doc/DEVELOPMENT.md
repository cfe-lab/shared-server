# Setting up a development server

1. Make sure you have Python 3.6 installed (see `SETUP.md` for
   instructions on how to build it).

1. Clone the latest copy of the code:
   ```shell
    git clone git@github.com:hcv-shared/shared-server.git
   ```

1. Create a virtualenvironment and install dependencies:
   ```shell
   cd shared-server
   make venv
   ```

1. Modify the settings file (`shared_server/settings.py`) to allow lax
   security; this is fine for development, but we want the secure
   options by default. The following settings should be changed for
   development:

   ```python
   CSRF_COOKIE_SECURE = False
   CSRF_COOKIE_DOMAIN = "127.0.0.1"
   SECURE_HSTS_INCLUDE_SUBDOMAINS = False
   SEUCRE_SSL_REDIRECT = False
   SESSION_COOKIE_SECURE = False

   DEBUG = True
   ```
1. Source or create the `dev_keys` file (or set `SECRET_KEY` and
   `HMAC_KEY` in the settings file).

   ```shell
   python make_def_keys.py > dev_keys
   source dev_keys
   ```

1. Update the database

   ```shell
   python manage.py migrate
   ```

1. Create a temporary data folder (where files submitted by
   collaborators are stored).

   ```shell
   mkdir tmpdata
   ```



You should now be able to start the server with `python manage.py
runserver`, run the tests with `make test`, or run tests and style
checks with `make check`.
