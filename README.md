# Tissue

A light weight CGI based issue tracker.  Meant to be as minimal as possible in dependencies, memory usage, and feature set.  Its simplicity can be extensible, but in its raw form it's designed to be deployable on hardware with minimal resources available, such as a Rasp Pi.  Not tied to any form of source control, it is developed with its use-case being to compliment cgit instances, but it can be used for anything.

# Minimum Requirements
Python >= 3.6

# Setup
Out of the box, an `nginx.conf` is provided to assist with initial deployment.  It will probably need a few tweaks for whatever environment you're setting up, but by default if you're running a standard nginx instance you should place your Tissue install in `/var/www/tissue` and symlink the provided `nginx.conf` into your `sites-enabled` folder of nginx with a smart name like `tissue.conf`.

Once your nginx configuration is complete, it is recommended to run a uWSGI server with CGI enabled, which may require building it yourself.  Instructions to do that are available [here](http://uwsgi-docs.readthedocs.io/en/latest/CGI.html).  A uwsgi configuration is provided that enables Python based cgi paths. Once you have uWSGI installed with the CGI Plugin you can run tissue simply with

```
sudo -u www-data [path-to-uwsgi] ./uwsgi.ini
```

Alternatively, you may use Apache to deploy with CGI, which is something we at Luna.Red typically don't do because it's Apache.