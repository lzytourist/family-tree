# Family Tree
<em>Know Your Roots</em>

## Setup
- Clone `git@github.com:lzytourist/family-tree.git`
- Install requirements from `requirements.txt` or use <code>pipenv</code> to install dependencies.
- Create a MySQL database named `family_db`
- Run migrations `python manage.py migrate`
- Run development server `python manage.py runserver`
- Register your account `http://127.0.0.1:8000/register/`

### Populate database with dummy data using the generator
- Open python shell `python manage.py shell`
- Import `data_generator.py` using `from FamilyBranch.data_generator import PersonFactory`
- Import `User` model `from django.contrib.auth.models import User`
- Get your registered user `user = User.objects.get(email=registration_email)`
- Generate data `data = PersonFactory(user=user, depth=5)`.

## `main` branch is under development and `v1` contains a working solution.
https://github.com/lzytourist/family-tree/tree/v1
