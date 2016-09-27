# alexandria
##### The first iteration - with Python, Flask, and MySQL

## Setting up your development environment

`http://flask.pocoo.org/docs/0.11/installation/`


## Setting up MYSQL locally for Ubuntu
    Install MySQL server
    `sudo apt-get update`
    `sudo apt-get install mysql-server`

    Set up MYSQL
    `/usr/bin/mysql_secure_installation`

    Start MYSQL
    `sudo service mysql start`

    Enter shell
    `/usr/bin/mysql -u root -p`

    Set password if you want

    If you want to launch at reboot
    `sudo /usr/sbin/update-rc.d mysql defaults`

    Running sql scripts in the mysql shell
    `mysql> source file_name` or
    `mysql> \. file_name`

## Accessing the Compute Engine and SQL Database
Credentials to log in to Google Cloud Platform:
```
GCP Credentials:
Username: hackstar1675@gcplab.me
Password: **********
```
Go to the compute engine and click the button that says "SSH". Now you are in the Compute Engine.
To connect to the database:
```
mysql -u root -p --host 104.155.149.246
```
You will be prompted for a password.

URI is ```mysql://root:hackathonmans@104.197.221.85/alexandria_db```
