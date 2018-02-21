# Server Setup

This document has describes how to set up and operate web application
(which we'll call "the appserver" from now on) that provides SHARED's
public services.

Most of these steps are only required when setting up a completely new
appserver. If you just need to restart a server that's already been
configured, skip to **[Running the Server](#running-the-server)**.


## Overview

The appserver runs best on Linux; it has been tested with Ubuntu and
CentOS, but any system providing a web server and Python 3.6 support
will probably work.

It uses a few open-source components:

- [Apache][apache] is a web server. It efficiently serves static files
  and handles the actual network connections from users (as
  a [reverse proxy][reverse-proxy]), including HTTPS support. Besides
  some configuration, Apache requires no custom code.
- [Gunicorn][gunicorn] is a Python "application server". It mediates
  between the Apache server and the SHARED logic, managing startup and
  concurrency. Besides some configuration, Gunicorn requires no custom
  code.
- [Django][django] is a web application framework. The logic of
  application (i.e. most of the code in this repo) uses Django.

[django]: https://www.djangoproject.com/
[gunicorn]: http://gunicorn.org/
[apache]: https://httpd.apache.org/
[reverse-proxy]: https://en.wikipedia.org/wiki/Reverse_proxy


## Installing Python 3.6

The SHARED server requires Python 3.6 (it makes use of
the [secrets module][secrets-mod] for enhanced security), which must
be built from scratch for the LTS version of Ubuntu.

[secrets-mod]: https://docs.python.org/3/library/secrets.html

The steps for building Python 3.6 are:

```shell
# Install pre-requisites
apt-get update && apt-get install -y \
    build-essential \
    libbz2-dev \
    libgdbm-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    wget \
    zlib1g-dev

# Fetch and unpack the Python source code
wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tar.xz && \
     tar xf Python-3.6.4.tar.xz

# Configure and build the Python interpreter (takes ~10 minutes)
./configure --enable-optimizations && \
    make -j 8 && \
    make altinstall
```

Python 3.6 should now be installed as `python3.6` (which prevents it
from clobbering any previously-installed versions of Python).


## Getting the Appserver Code

Clone the latest copy of the `shared-server` source code. This will
create the "app directory", which contains the app's code and
Gunicorn configuration.

```
git clone git@github.com:hcv-shared/shared-server.git
```


## Configuring Apache

To configure the Apache, copy the `shared.conf` file from the
appserver's root directory to the Apache server's configuration
directory (which is usually something like `/etc/httpd/conf.d`, but
might vary depending on which distribution of Linux you're using, or
how you installed Apache).

You may have to [restart apache][so-restart-apache] for the
changes to take effect.

[so-restart-apache]: https://stackoverflow.com/questions/8270108/how-to-reload-apache-configuration-for-a-site-without-restarting-apache

Our IT department manages all our TLS certificates, so they'll add
some configuration files to the `httpd` directory and you shouldn't
have to worry about them.


## Set up a Python Virtual Environment Installing Dependencies

The appserver's dependencies should be installed in
a [virtual environment][virtualenv-doc] to isolate it from any other
Python projects that might be running on the same host.

[virtualenv-doc]: https://docs.python.org/3/tutorial/venv.html

In the appserver's directory:

```shell
# Create the virtual environment
python3.6 -m venv venv

# Activate the virtual environment
# From this point forward, your shell will use the version  of
# Python installed in this directory
source ./venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```


## Setting Up the App Directory

These steps should be performed **when the server is first set up on a
new host**, after getting the appserver code.

1.  Create the keyfile (or copy it from a previous host). It should
    look like this:

    ```shell
    export SHARED_SERVER_SECRET_KEY='a long random string'
    export SHARED_SERVER_HMAC_KEY='a different long random string'
    ```

    You can use the [`make_dev_keys.py`](../make_dev_keys.py) script in
    the appserver's root directory to generate a new keyfile.

    Changing these keys will invalidate all logged-in Admin sessions
    (so administrators will have to log in again) and secure submission
    links (so links will have to be re-issued), respectively.

1.  If it doesn't already exist, create a directory called `tmpdata` at
    the root of the app directory. This is where users' submitted data
    will be stored.

1.  Make sure the database is up-to-date:

    ```shell
    source ./venv/bin/activate
    python manage.py migrate
    ```

<a name="running-the-server">

## Running the Server

This should be performed to **start or re-start** the appserver (e.g:
when the host server is re-booted).

If new static content (HTML, CSS, or JavaScript; Images; PDF
documents, etc.) have been added, they should be collected and copied
to a directory called `static` in the Apache server's web-root (the
directory that Apache serves static files from, usually
`/var/www/html/`).

```shell
# Gather static files into one directory (called `to_webroot`)
python manage.py collectstatic
cp -R to_webroot/* /var/www/html/static/
```

The command for starting the server is:

```shell
(source keys ;
 source ./venv/bin/activate ;
 gunicorn -c gunicorn_settings.py shared_server.wsgi)
```

This stores the secret keys as environment variables, activates the
virtual environment, and starts Gunicorn. This process should be run
in the background (by appending `&` to the command) or run in a
detachable terminal emulator like `screen` or `tmux`.

The application server should now be internally accessible on port
8000, and the public-facing Apache server should be directing traffic
to it.
