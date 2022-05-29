Reaper to Tosclib
-------------------

This asks REAPER to execute a few commands via Web Interface.

The commands will get all the Parameters of the Last Touched FX and store them in a .json. Then convert the .json to a .tosc file.


1. Install Reaper, Reapack and SWS Extensions.
2. Add this repo to Reapack: 

.. code-block::

    https://raw.githubusercontent.com/AlbertoV5/ReaperTools/master/index.xml

3. Install all LISZT scripts from AlbertoV5-ReaperTools.
4. Setup Python in Reaper (avoid conda on Windows) and install dependencies.
5. Setup Reaper Web Interface*.
6. Load up a FX and run this script.

.. literalinclude:: 5-reaper-tosclib.py
    :language: python


\*Example of Web Interface settings:

.. image:: ../images/reaper_www_settings.JPG

The only thing you need is the port. If you are running this script from another local machine then change the host to the Reaper machine IP or use the Access URL.

The result will be a template with Faders named as the FX Parameters with OSC messages named after them:

.. image:: ../images/reaper_tosc_demo_output.JPG

Feel free to make your own version of liszt-generate.py to fit your needs.