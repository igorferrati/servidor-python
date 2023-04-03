import subprocess as sub

sub.run(["gunicorn", "-b", "0.0.0.0:8000", "wsgi:app"])

sub.run(["nginx", "-g", "daemon off;"])