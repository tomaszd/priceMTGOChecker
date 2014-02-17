from django.db import models

# Create your models here.
#witam
from django.db import models


# class Card(models.Model):
#     question_text = models.CharField(max_length=200,)
#     pub_date = models.DateTimeField('date published')


class Color(models.Model):
    colors_choices=(('WHITE','w'),
                    ('BLUE','u'),
                    ('GREEN','g'),
                    ('RED','r'),
                    ('BLACK','b'),
                    ('COLORLESS','0'),
                    ('MULTICOLOR','mc'))
    color = models.CharField(max_length=20, choices=colors_choices)