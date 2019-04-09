
#!/usr/local/bin/python
# -*- coding: utf-8 -*-


from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

# Create your models here.
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


class Product(models.Model):
    """
    """

    name = models.CharField(verbose_name=_("Nombre"), max_length=50)
    priority = models.PositiveIntegerField(verbose_name=_('Prioridad'), validators=[MaxValueValidator(3), MinValueValidator(1)])
    entry_date = models.DateTimeField(verbose_name=_("Fecha de Entrada"), auto_now_add=True)
    exit_date = models.DateTimeField(verbose_name=_("Fecha de Entrada"))
    sla = models.FileField(verbose_name=_('Service Level Agreement'))
    #client = models.CharField(verbose_name=_("Cliente"), max_length=50)
    humidity = models.PositiveIntegerField(verbose_name=_('Humedad'), null=True)
    temperature = models.IntegerField(verbose_name=_('Temperatura'), null=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        db_table = 'product'


class Container(models.Model):
    """
    """

    room = models.ForeignKey(Room, verbose_name=_('Sala'), on_delete=models.PROTECT, related_name='container_room')
    product = models.ForeignKey(Product, verbose_name=_('Producto'), on_delete=models.PROTECT, related_name='container_product')

    class Meta:
        verbose_name = 'Contenedor'
        verbose_name_plural = 'Contenedores'
        db_table = 'container'


class MoveTask(models.Model):
    """
    """

    container = models.ForeignKey(Container, verbose_name=_('Contenedor'), on_delete=models.PROTECT, related_name='move_task_container')
    origin = models.ForeignKey(Room, verbose_name=_('Sala'), null=True, on_delete=models.SET_NULL, related_name='origin_room')
    destination = models.ForeignKey(Room, verbose_name=_('Sala'), null=True, on_delete=models.SET_NULL, related_name='destination_room')
    worker = models.ForeignKey(User, verbose_name=_('Trabajador'), null=True, on_delete=models.SET_NULL, related_name='move_task_worker')

    class Meta:
        verbose_name = 'Tarea de Movimiento'
        verbose_name_plural = 'Tareas de Movimiento'
        db_table = 'move_task'


class MaintenanceTask(models.Model):
    """
    """

    room = models.ForeignKey(Room, verbose_name=_('Sala'), null=True, on_delete=models.SET_NULL, related_name='maintenance_task_room')
    machine = models.CharField(verbose_name=_("Máquina"), max_length=50)
    worker = models.ForeignKey(User, verbose_name=_('Trabajador'), null=True, on_delete=models.SET_NULL, related_name='maintenance_task_worker')

    class Meta:
        verbose_name = 'Tarea de Mantenimiento'
        verbose_name_plural = 'Tareas de Mantenimiento'
        db_table = 'maintenance_task'




#
