# Oh chat!
An interactive web based chat application designed for all devices.
Here is the working version of the app [Oh Chat](https://oh-chat.herokuapp.com)

## Requirements:
1. Linux based virtual machine. You can learn the installation of the virtual machine using [Vagrant](https://www.vagrantup.com/) and [Virtual box](https://www.virtualbox.org/wiki/Downloads) [here](http://www.bogotobogo.com/DevOps/Vagrant/Vagrant_VirtualBox.php).
2. Download and install [git](https://git-scm.com/downloads)

## How to run the **Oh Chat** app.
1. Open git bash.
2. Using the command `cd [DIRECTORY NAME]` go to the directory where your **vagrantfile** exists.
3. Install the virtual machine by using the command `vagrant up`.
4. After the succesfull installation of the Linux OS. Run the command `vagrant ssh` to start the virtual machine.
5. Now use the command `cd [VAGRANT SHARED DIRECTORY]` to enter into your vagrant shared directory. Your shared directory is located at `/vagrant`
6. Enter the directory **Oh-Chat** by using the command `cd Oh-Chat`
7. Create a virtual environment by using the command `virtualenv -p python3 venv --always-copy` OR `virtualenv -p python3 venv` (which ever works for you).
8. Activate the virtual environment by using the command `source venv/bin/activate`.
9. Install the extensions from the requirements.txt file by using the command `pip install -r requirements.txt`
10. Now run the app with the command `python manage.py`
11. Open your browser and go to the url `localhost:5000`.
12. Enjoy Chatting!

### Note:
This app does not use any kind of databases.
Python data structures are used to perform the database task.
