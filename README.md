## Data Visualization Project

To run the flask development environment, you'll need to do some prep work. Sadly, this is pretty much unavoidable without a lot of dredge work that will take time from actual development. We will need to write a script to sort this thing out autmoatically.

First, for the sake of expediency, I am currently providing a VM image containing a working development environment, hosted on Mega at the following link: 

To get Flask up and running, you need to first make sure that all of the dependencies have been met. On a stock Ubuntu 20.04 LTS server, you need to install the following packages: 


```
build-essential
mysql-server
libmysqlclient-dev (Mysql headers)
python3-dev (python headers)
python3-venv (allows us to create virtual environments)
python3-mysqldb (python support for sql)
```



When running the actual webserver, we will also need the following packages:


```
apache2 (webserver)
libapache2-mod-wsgi-py3 (Webserver Gateway Interface for python-based webapps)
```

We will also be using Redis to store user session information in memory. You can find installation instructions at the following address, but I'm planning on adding only the relevant steps here later.

https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04

As usual, all of these can be installed using `apt install`.

After all of the prerequisite packages have been installed, you should go ahead and clone the repo. Inside the root directory of the repo, create a virtual environment. This effectively gives us a stand-alone python distribution, that we can freely modify at a remove from the host environment.

`python3 -m venv venv` - this loads the `venv` module, and creates a folder named `venv` containing the virtual environment.

To enter the virtual environment, run `. venv/bin/activate`, and to exit simply type `deactivate` at any time.

Once you've entered the virtual environment, we will first install the required python packages using `pip install`:

```
flask
Flask-session (needed for session handling)
redis (needed to interface with redis)
wheel (needed to compile some c++ interface code)
mysql-connector-python (MySQL interface)
pymysql
cryptography (used for cryptographic hashing)
sshtunnel (Used to create an SSH tunnel to a set server.)
```

Finally, we need to get the Flask debug server running.

First, go into the virtual environment, and then export a few environment variables. These will tell flask where to start executing the web app, and set it into a verbose, debuggable mode.

```
export FLASK_ENV=development
export FLASK_APP=app
flask run --host=xxx.xxx.xxx.xxx
```

Remember to enter the IP address you want to access the website from. If you're connecting on the machine running the server, use `127.0.0.1`. If you're accessing it from another computer on the LAN, then use 192.168.X.XXX. This should never be exposed directly to the web, as it is not a production capable webserver.

The first step is simply making sure the standard Python extension pack is installed.

Once the extensions are installed and activated, pres Ctrl+Shift+P to open the command Pallete, and type in `Python: Select Interpreter`. 

You will select the option to enter the interpreter path, and navigate to your virtual environment. Simply select the Python interpreter located at /venv/bin/python. Code will then default to this runtime, and use the libraries therein. 

Once this is set up, you can debug the flask app by going into the debug view, selecting `Run and Debug`, and then from the dropdown menu, selecting `Flask`. 

Enter the name of the initial executable, currently `app`, and it will spin up a flask instance.

Code will automatically forward port 5000 through ssh, so you can access the debug server using localhost on your native system.

Includes jQuery and chart.js under the MIT license 
