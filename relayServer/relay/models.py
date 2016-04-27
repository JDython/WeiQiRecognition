from django.db import models

# Create your models here.


class chess_composition(models.Model):
    id = models.AutoField(primary_key=True)
    time = models.DateTimeField()
    matrix =  models.CharField(max_length=1200)

    class Meta:
        db_table='chess_composition'
        ordering=['-time']
