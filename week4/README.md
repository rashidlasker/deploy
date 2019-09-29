Assignment 3: Templates, Templates, Templates!
========

This week you'll be writing templates for the models you created last week. You have free reign in deciding which templates your app requires. We are looking for functionality where users can see a list of items and be able to click on an item and see details about it.

For example, if your project is a recipe sharing app and you have `User`, `Recipe`, and `Comment` models, you could create detail views and templates for `User` and `Recipe`. `Comment` might not need its own view/template because the view for `Recipe` could also show all associated `Comment`s. You would also need to create a view and corresponding template that lists `Recipe`s.

Templates in Django
----

Django Templates are basically HTML files that have variables supplied by the corresponding Django view. For example, consider this example polls app.

In `views.py`, we call `render(request, <path_to_template>, <context_dictionary>)`.

`polls/views.py¶`
```
from django.shortcuts import get_object_or_404, render

from .models import Question
# ...
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
```

`context_dictionary` contains variables that your template can use to populate information. In this example, a `Question` model instance is passed to the template where it is used to display information in the template.

`polls/templates/polls/detail.html¶`
```
<h1>{{ question.question_text }}</h1>
<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }}</li>
{% endfor %}
</ul>
```

For more guidance on writing Django apps, we highly recommend going through this tutorial:
https://docs.djangoproject.com/en/2.2/intro/tutorial01/

What to turn in
---------------

The only thing we should need to do to test your project is clone your repository, git check out the appropriate commit/release, make a db folder, and run `docker-compose up`. We should not have to debug issues, change your code etc.

For this project, we just expect your project to have a home listing page of your items that we can click into and view item details. Please send us a link to your Git repo and tell us the URLs to visit to see your templates.

Finally, we strongly encourage you to take time to demo in the office hours or check-ins. We want to make sure not only you are writing code that works but also code that is of best practices.
