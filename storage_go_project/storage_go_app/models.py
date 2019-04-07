
#!/usr/local/bin/python
# -*- coding: utf-8 -*-


from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

# Create your models here.

"""
class Worker(models.Model):

    user =
"""

class Entity(models.Model):
    """
    """

    STATUS = (("Pendiente", "Pendiente"), ("En Proceso", "En Proceso"), ("Terminada", "Terminada"))
    status = models.CharField(verbose_name=_("Estado"), max_length=10, choices=STATUS, default='Pendiente')
    priority = models.PositiveIntegerField(verbose_name=_('Prioridad'), validators=[MaxValueValidator(3), MinValueValidator(1)])
    work = models.ForeignKey(User, verbose_name=_('Trabajador'), null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class Room(models.Model):
    """
    """

    STATUS = (("Abierta", "Abierta"), ("Cerrada", "Cerrada"))
    status = models.CharField(verbose_name=_("Estado"), max_length=7, choices=STATUS, default='Cerrada')
    name = models.CharField(verbose_name=_("Nombre"), max_length=50)
    humidity = models.PositiveIntegerField(verbose_name=_('Humedad'), null=True)
    temperature = models.IntegerField(verbose_name=_('Temperatura'), null=True)

    class Meta:
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'
        db_table = 'room'

    def __unicode__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)


class Product(Entity):
    """
    """

    STATUS = (("Pendiente", "Pendiente"), ("En Proceso", "En Proceso"), ("Terminada", "Terminada"))
    status = models.CharField(verbose_name=_("Estado"), max_length=10, choices=STATUS, default='Pendiente')
    priority = models.PositiveIntegerField(verbose_name=_('Prioridad'), validators=[MaxValueValidator(3), MinValueValidator(1)])
    #containers = models.
    entry_date = models.DateTimeField(verbose_name=_("Fecha de Entrada"), auto_now_add=True)
    exit_date = models.DateTimeField(verbose_name=_("Fecha de Entrada"))
    sla = models.FileField(verbose_name=_('Service Level Agreement'))
    #client = models.CharField(verbose_name=_("Cliente"), max_length=50)
    #humidity = models.PositiveIntegerField(verbose_name=_('Humedad'), null=True)
    #temperature = models.IntegerField(verbose_name=_('Temperatura'), null=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        db_table = 'product'


class Container(models.Model):
    """
    """

    #code = models.CharField(verbose_name=_("Nombre"), max_length=50)
    room = models.ForeignKey(Room, verbose_name=_('Sala'), on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, verbose_name=_('Producto'), on_delete=models.models.SET_NULL)

    class Meta:
        verbose_name = 'Contenedor'
        verbose_name_plural = 'Contenedores'
        db_table = 'container'


class MoveTask(Entity):
    """
    """

    container = models.ForeignKey(Container)
    #origin
    #destination

    class Meta:
        verbose_name = 'Tarea de Movimiento'
        verbose_name_plural = 'Tareas de Movimiento'
        db_table = 'move_task'


class MaintenanceTask(Entity):
    """
    """

    #place
    #machine

    class Meta:
        verbose_name = 'Tarea de Mantenimiento'
        verbose_name_plural = 'Tareas de Mantenimiento'
        db_table = 'maintenance_task'




#
