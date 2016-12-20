from datetime import datetime

class User:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.first_name = kwargs.get('first_name')
        self.middle_name = kwargs.get('middle_name')
        self.last_name = kwargs.get('last_name')
        self.roles = kwargs.get('roles')
        self.polynomial_coef = kwargs.get('polynomial_coef')


class Category:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.allowed_roles = kwargs.get('allowed_roles')


class Note:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.author_id = kwargs.get('author_id')
        self.category_id = kwargs.get('category_id')
        self.title = kwargs.get('title')
        self.text = kwargs.get('text')


class SecurityLog:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.date_created = kwargs.get('date_created')
        self.user_id = kwargs.get('user_id')
        self.event_type = kwargs.get('event_type')
        self.is_safe = kwargs.get('is_safe')
        self.metadata = kwargs.get('metadata')
