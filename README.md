Django JanySON
==============

[![Build Status](https://travis-ci.org/un-def/django-janyson.svg?branch=master)](https://travis-ci.org/un-def/django-janyson)
[![Coverage Status](https://coveralls.io/repos/github/un-def/django-janyson/badge.svg?branch=master)](https://coveralls.io/github/un-def/django-janyson?branch=master)
[![PyPI version](https://badge.fury.io/py/django-janyson.svg)](https://pypi.python.org/pypi/django-janyson/)
[![PyPI license](https://img.shields.io/pypi/l/django-janyson.svg?maxAge=3600)](https://raw.githubusercontent.com/un-def/django-janyson/master/LICENSE)

Store additional model fields as JSON object in PostgreSQL's `jsonb` field and work with them as regular model fields. Need new boolean/text/foreign key/many-to-many/etc. field? Just add the decorator with the field description to your model. It's all! No more annoying migrations.


### Installation

* Install the package using `pip install django-janyson`.
* Add `janyson` to `INSTALLED_APPS` setting (optional).


### Requirements

* Python 2.7+ or 3.4+
* Django 1.9+ with psycopg2
* [six](https://pypi.python.org/pypi/six)


### Example

```python
from django.db import models

from janyson.decorators import add_fields
from janyson.fields import JanySONField


class Tag(models.Model):

    name = models.CharField(max_length=16)

    def __str__(self):
        return "[Tag: {}]".format(self.name)


extra_fields = {
    'desc': {'type': 'str'},
    'qty': {'type': 'num', 'default': 0, 'use_default': True},
    'avail': {'type': 'nullbool', 'use_default': True},
    'main_tag': {'type': 'fk', 'model': Tag},
    'tags': {'type': 'm2m', 'model': 'demo_app.Tag'},
}

common_options = {
    'use_default': False,
    'dir_hide': True,
}

@add_fields(extra_fields, field_options=common_options, janyson_field='extra')
class Item(models.Model):

    name = models.CharField(max_length=64)
    extra = JanySONField(verbose_name='janyson field', default=dict,
                         blank=True, null=True)

    def __str__(self):
        return "[Item: {}]".format(self.name)
```

```python
>>> from demo_app.models import Tag, Item

>>> Tag.objects.create(name='tag1')
>>> Tag.objects.create(name='tag2')
>>> item = Item(name='test')

>>> item
<Item: [Item: test]>
>>> item.desc
AttributeError: 'Item' object has no attribute 'desc'
>>> item.qty
0
>>> print(item.avail)
None
>>> item.tags
AttributeError: 'Item' object has no attribute 'tags'

>>> tags = Tag.objects.all()
>>> item.desc = 'description'
>>> item.qty = 100
>>> item.avail = True
>>> item.tags = tags
>>> item.save()

>>> del item
>>> item = Item.objects.get(name='test')
>>> item.desc
'description'
>>> item.qty
100
>>> item.avail
True
>>> item.tags
[<Tag: [Tag: tag1]>, <Tag: [Tag: tag1]>, <Tag: [Tag: tag2]>]
```

### Tests

`$ python runtests.py [-d TESTDBNAME] [-h HOSTNAME] [-p PORT] [-U USERNAME] [-P PASSWORD] [-w]`

Run `python runtests.py --help` for additional info.

Test with multiple Python versions and measure code coverage (using [tox](https://pypi.python.org/pypi/tox) and [coverage.py](https://pypi.python.org/pypi/coverage)):

```
$ pip install -r requirements_dev.txt
$ ./runtests.sh [TOX_OPTIONS] [-- RUNTESTS_OPTIONS]
```

Example:

`$ ./runtests.sh -e py27,py35 -- -h 127.0.0.1 -p 5432 -U testuser -w`


### Documentation

Coming soon.
