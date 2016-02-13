pysenteishon
===============

Control your presentations with the swipe of your finger!

Install
========

From PyPi
----------

::

   pip install pysenteishon
   pysenteishon

From GitHub
-------------

::

   git clone https://github.com/edvm/pysenteishon
   cd pysenteishon
   python pysenteishon/src/app.py

Usage
=====

After running the app:

- Make sure you allow access to port 5000 in your firewall settings.

- Open your presentation PDF on your computer and leave it open (MAKE
  SURE the program that is running your presentation has FOCUS).

- Open a web browser with your cellphone and point it to your laptop
  ip address port 5000, for example: http://192.168.0.11:5000

- Swipe on your touchscreen and start your talk! :D

Options
========

::

   usage: app.py [-h] [-p PORT] [-a user password]

   optional arguments:
     -h, --help            show this help message and exit
     -p PORT, --port PORT  Listen on port
     -a user password, --auth user password
                           Basic auth
