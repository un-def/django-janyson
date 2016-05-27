Django JanySON
==============

Store additional model fields as JSON object in PostgreSQL's `jsonb` field and work with them as regular model fields. Need new boolean/text/foreign key/many-to-many/etc. field? Just add the decorator with the field description to your model. It's all! No more annoying migrations.


### Installation

* Install the package using `pip install django-janyson`.
* Add `janyson` to `INSTALLED_APPS` setting.


### Requirements

* Python 2 or 3 (tested with 2.7+ and 3.3+)
* Django 1.9+ with psycopg2
* six


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

`python runtests.py [-d TESTDBNAME] [-h HOSTNAME] [-p PORT] [-U USERNAME] [-P PASSWORD]`

Run `python runtests.py --help` for additional info.


### Documentation

Coming soon.
