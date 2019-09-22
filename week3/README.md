Assignment 3: Django Models + API
========

In this phase of the project you will build your Django data models
and then build a first version of services for accessing those
models.

Database Design
-------------

You should think about what your data models will be and how they
will relate to each other. For example, if you're building an application
for students to hire tutors, you might have models for users, tutors, tutees,
reviews etc. Users might have a relationships to tutors and tutees (can a user
tutor one subject and receive help in another?). You can also start to spec out
what fields will be in each model (e.g. first name, email address, etc.).

Django
------

The Django documentation is going to be invaluable and essential for
completing this work.

A note on code layout: it should look something like this. This is the same directory structure you get when when you use the standard Django `startproject`, `startapp` commands.


	myapp-microservices/
	├── manage.py
	├── myapp
	│   ├── __init__.py
	│   ├── admin.py
	│   ├── migrations
	│   │   └── __init__.py
	│   ├── models.py
	│   ├── tests.py
	│   └── views.py


It's probably worth your effort to set up the admin interface to make
it easy to update your data. In the real world you wouldn't do this,
but I think it's a reasonable short-cut for a class project. The risk
with this is that it could expose security vulnerabilities, so you
wouldn't really want to put it into production.

Docker Compose
--------------

One other thing to introduce before we start coding is Docker Compose. Compose
is a tool for defining the topology and running multi-container Docker
applications.  With Compose, you use a YAML file called docker-compose.yml to configure your
application’s services.  Recall how we start the 'web' and 'mysql' containers
one by one in the previous project. This approach works fine when we have only
two containers (and the configuration is simple), but it is certainly not scalable.
Using Docker Compose, we will be able to start up our containers using a single
command. Here is a tutorial about how Docker Compose works:

First, install Docker Compose if you haven't already done so. You can check if
you have docker-compose on your machine by typing `docker-compose` in your
terminal.

When you've got Compose installed, go ahead and create a new file, docker-compose.yml, in the project root 
directory (you need to name the file exactly as docker-compose.yml). Docker Compose uses these files, called 
YAML (pronounced "yeah-mull") files, to automatically set up or start a group of containers. This is handy, 
much easier than managing each container individually. You can specify a lot of different options here, 
but for now we're merely going to define our entity service and a network then link it to our mysql database. You 
need to make sure the mysql container we created from last time is started.

You can tell compose to create a new container by giving it a name and an image to use. 
We also define a network name that other services will reference. Here's an example

```YAML
version: "3"
services:

  models:
    image: tp33/django
    volumes:
      - <project_root_dir>:/app
    ports:
      - "8001:8000"
    networks:
      - backend
    command: bash -c "mod_wsgi-express start-server --working-directory <project_root_dir> --reload-on-changes <path_to_wsgi.py>/wsgi.py"

networks:
  backend:
```

Volumes is like the -v tag we use when executing docker run in the previous
project. It mounts the app directory in the container onto the <your_file_path>
directory on the host machine (your Mac/PC). By specifing that, you can code in
your text editor/IDE on your host machine and any change you make will be picked
up by the container. It is handy in terms of the development workflow.

Ports expose the port in your container to the port on your host machine. In
this case, we are exposing port 8000 in the container to port 8001 on your host
machine. By exposing the ports, you can access your Django app in the browser on
your host machine by going to localhost:8001 if you use a native Docker app or
<your_docker_ip>:8001 if you use Docker Machine/Toolbox.

Networks simply links the container to one of the networks specified in the 
compose. All services on the same network are able to communicate and so this 
is how we will isolate our services. 
You can read more about networks in docker compose here: 
https://docs.docker.com/compose/networking/

Command specifies the command that will be run when the container starts up. In
this case it will start the mod_wsgi server.

Now that we've got this, save docker-compose.yml. Having Compose create and run our container is as simple as running

	docker-compose up

In order to stop all the containers running press Ctrl+C and wait for each to finish. 

NOTE: for the command to run successfully, you need to have your mysql
container running (since our containers depend on the database to be up)

	docker-compose rm

will remove all the container instances specified by the docker-compose file.

One other thing about docker compose. If for some reason (run makemigrations/migrate, etc.) you need to attach to a container created by docker compose, instead of using `docker attach <container_name>`(it will hang), use `docker exec -it <container_name> bash`.

You can do a lot more with Docker Compose, including building new images straight from a Dockerfile, configuring ports, and defining shared volumes for containers. These are all things that may be helpful to you later in the course, so keep your compose file updated as you go about your project. There are great examples at https://docs.docker.com/compose/install/ and https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-14-04.

Models
------

The first step is to create your Django models for your project. Generally, there are a few guidelines to consider:

Remember, each model corresponds to a table in your database. Each
model is represented in Django by a Python class. Each row in your
table will correspond to an instance of your model class. Django
will automatically create the database tables you need.

Every model should include a unique id. For example, if your project
has things that can be sold, there'll likely be an Items model that
represents the things to be sold. Each Item should have a unique id
that you can record, for example, when creating the lists of Items a
user has bought or sold. Django's built-in auto primary key works fine
(but be sure to know why it works).

You need to think through the relationships between
models. Continuing the example above, a single user may have bought
many items so there is what is called a "one-to-many" relationship
between Users and Items. On the other hand, if you have a user has
written a Review for an Item, the Review will reference the Item id
being reviewed. There will be exactly one Item that the Review
references. This is known as a "one-to-one" relation.

User and Picture models are generally handled specially in
Django. However, as we'll discuss in later classes, we're not
going to use the Django User class. You can use it as a placeholder,
but know that you'll change it in the next few projects.
Pictures are complicated by the fact that they tend to be large.
For now, I'd just ignore doing anything with pictures.

Model Migrations
----------------

Django includes a feature called database migrations. This is a way for you to automatically keep your database tables/schemas
in sync with what your models.py requires. If your models.py refers to a model named 'Cars' but your database doesn't have a
table for that model, then your application won't work.

The way migrations work is that when you change your models.py, you ALWAYS need to also check-in a migration that will make
the corresponding change to you (and your teammates DB's). You do this with the `python manage.py makemigrations` command.
This will create a Python file in your `migrations/` directory that will, when run, update your DB. 

The second step, is that WHENEVER you start your application, you need to run migrations. You do this with 
`python manage.py migrate`. This will check what the last migration run against your DB is, see if there are newer
migrations in `migrations/`, and run the new ones.

A common mistake is that team member 1 changes their models.py but forgets to make and check in a corresponding migration. 
Then when team member 2 checks out the updated models.py and tries to use it, they get an error because their DB doesn't
have the tables needed. 

You can read more in the Django documentation here https://docs.djangoproject.com/en/2.1/topics/migrations/

Docker
--------

For project 2, try and create a quick and simple pipeline for working with Docker. **An objective for project 2 is to show you that setting up to run code is just as important as writing the code.** Some of the key concepts you may want to look into are

- docker-compose
- docker volumes
- docker port forwarding
- modwsgi --reload-on-change flag

Services
--------

Each API will have its own url for accessing it. These are listed in
your project's `urls.py` file. Each one will specify the view that is to
be invoked to handle that url. They will look something like this:

    /api/v1/users/43 - GET to return info about user 43, POST to update the user's info.
    /api/v1/things/23 - GET to return info about thing 23, POST to update it
    /api/v1/things/create - POST to create a new thing
    /api/v1/things/23/update
    /api/v1/things/23/delete

You'll then create a Django view for each url. The view may handle
both GET and POST requests. You'll need to consult the Django
documentation for how to do this and for how to properly format a json
response from your view.

The APIs should return JSON results. The POST methods should take either form-encoded
sets of key-value parameters (preferred) or JSON encoded values. For example, a result
from looking up a user might look like:

```py
{
    'ok': True,
    'result': {
        'username':     'tpinckney',
        'first_name':   'Tom',
        'last_name':    'Pinckney',
        'date_created': 'Feb 12 2016'
    }
}
```

For testing your APIs, you can use your browser to make sure GET requests behave as expected, but browsers cannot send POST requests if there is no form to submit. I recommend your use `curl` or you can use [Postman](https://www.getpostman.com/) to test your APIs—this is what the graders will be using to test your APIs. Make sure you know the difference between sending parameters in the URL's query string (e.g. for GET requests), and sending parameters in the POST body. It can be easy to mix up the two while using Postman.

Iterative design
----------------

You will not get your services and models exactly right. This is really just the
first draft. As you continue to build higher layers of your app in future
assignments you'll come back and change your models and services.

One important way that Django makes this easy is with database migrations. A
migration in Django is a set of schema changes that are required to move your DB
and app from one version to the next.

When you edit your models.py file(s), your DB will not immediately automatically
reflect the changes. Instead, you'll need to use your Django `manage.py` to
generate a set of SQL commands needed to update your DB to match your new
models. Then you can apply these commands to make them actually take affect.
Django breaks this into two stages so that you can check the commands into git
on your dev machine and then later apply them to many different db's—in
theory you might have many dev db instances, some testing/qa instances and then
prod db instances. See the Django getting started or model documentation for
more on migrations and how to use them.

Fixtures
--------
You can think of
fixtures as initial data provided to an empty database. It’s sometimes (e.g. when
testing, grading) useful to pre-populate your database with hard-coded data when
you’re first setting up an app so that you can use the app directly. To avoid
hard-coding test data everytime you have a clean database, we use Django
fixtures which does the work for you automatically.

Here's a quick introduction of fixture and a tutorial on how to use fixtures to
preload data or export your db:

General steps for creating fixtures:

Dump existing db data to db.json (JSON file name does not matter) using

	python manage.py dumpdata > db.json

See Django documentation for the various options for dumpdata: https://docs.djangoproject.com/en/2.1/ref/django-admin/#dumpdata

This is an example fixture. You can see it is basically Django model instances
serialized into JSON format.

```json
[
  {
    "model": "myapp.person",
    "pk": 1,
    "fields": {
      "first_name": "John",
      "last_name": "Lennon"
    }
  },
  {
    "model": "myapp.person",
    "pk": 2,
    "fields": {
      "first_name": "Paul",
      "last_name": "McCartney"
    }
  }
]
```

To use your fixture to pre-populate a **clean** database instance:

Run command

	python manage.py loaddata db.json

The command will deserialize the models instances and loaded them into your
database.

See Django documentation for the various options for loaddata:
https://docs.djangoproject.com/en/2.1/howto/initial-data/

Initial data should now be in db!

To incorporate fixtures into your project submissions, add some data to your
database and create a fixture before pushing to github and add `python manage.py
loaddata` command to your `docker-compose` command to load the data before
starting your server. This is how we can use every group's app without having to
manually enter data every time.

This should go without saying: make sure everyone in the group can flush their
database and load a fixture. Sometimes, you'll have issues with contenttypes and
permissions creating conflicts. Look into the flags you can use to exclude these
from making it into the fixtures JSON. Ensure that everyone in your group can load
data because that's a good sign that the TA's will be able to as well.

What to turn in
---------------

The only thing we should need to do to test your project is clone your repository, git check out the appropriate commit/release, and run `docker-compose up`. We should not have to debug issues, change your code etc.

Remember not to commit database files (the files in your ~/deploy/db/ dir) or pycache (*.pyc) files to Github. If you have already accidentally done so, figure out how to remove them. You can use a .gitignore to help.


For this project, we just expect your project to have at least two models and HTTP/JSON APIs for creating, reading, updating and deleting entries in those models. Make sure you do not omit error checking.

As a reminder, some things that need to be executed by the docker-compose.yml:

- Run migrate
- Load fixtures
- Start the wsgi server
- (You can do something like `command: bash -c "<command_1> && <command_2> && ..."`)
- Expose ports
- Link to the mysql db container

Also note that you NEED to use relative path for your compose file to work on our machines (we won't have the same absolute path as yours)! Be extremely careful when you set up the relative path.

We highly recommend that you do a final test of your system by checking out and running your code on a clean system and an empty database just like we will test.

Finally, we strongly encourage you to take time to demo in the office hours. We want to make sure not only you are writing code that works but also code that is of best practices.
