
#!/usr/local/bin/python
# -*- coding: utf-8 -*-


from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

# Custom fields
class IntegerRangeField(models.IntegerField):
    """
    """

    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


# Extending Django Models
class CustomPermission(models.Model):
    """
    """

    #group
    #user

    PERMISSION_TYPE = (('Modelo', 'Modelo'), ('Objeto', 'Objeto'), ('Atributo', 'Atributo'))
    type = models.CharField(verbose_name=_('Tipo'), max_length=10, choices=PERMISSION_TYPE, default=1)
    ACTION_TYPE = (('Ver', 'Ver'), ('Crear', 'Crear'), ('Modificar', 'Modificar'), ('Borrar','Borrar'))
    action = models.CharField(verbose_name=_('Acción'), max_length=10, choices=ACTION_TYPE, default=1)

    #module = models.CharField(verbose_name=_('Módulo'), max_length=50)
    model = models.CharField(verbose_name=_('Modelo'), max_length=50, null=True)
    object = models.CharField(verbose_name=_('Objeto'), max_length=50, null=True)
    attribute = models.CharField(verbose_name=_('Attributo'), max_length=50, null=True)


    class Meta:
        verbose_name = _("Permiso Personalizado")
        verbose_name_plural = _("Permisos Personalizados")
        #default_permissions = ()

    def __str__(self):
        return self.type + ' | ' + self.action + ' | ' + self.module + ' | ' + self.model + ' | ' + self.object + ' | ' + self.attribute

    def __unicode__(self):
        return self.type + ' | ' + self.action + ' | ' + self.module + ' | ' + self.model + ' | ' + self.object + ' | ' + self.attribute


# Create your models here.
"""
class Transports
"""


class Room(models.Model):
    """
    """

    STATUS = (("Abierta", "Abierta"), ("Cerrada", "Cerrada"))
    status = models.CharField(verbose_name=_("Estado"), max_length=7, choices=STATUS, default='Cerrada')
    name = models.CharField(verbose_name=_("Nombre"), max_length=50)
    humidity = models.PositiveIntegerField(verbose_name=_('Humedad'), default=23)
    temperature = models.IntegerField(verbose_name=_('Temperatura'), default=23)
    max_containers = models.PositiveIntegerField(verbose_name=_('Capacidad Máxima'), default=4)

    class Meta:
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'
        db_table = 'room'

    def meta(self):
        return self._meta

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class RoomMap(models.Model):
    """
    """

    STATUS = (("Disponible", "Disponible"), ("Ocupado", "Ocupado"))
    status = models.CharField(verbose_name=_("Estado"), max_length=10, choices=STATUS, default='Disponible')
    room = models.ForeignKey(Room, verbose_name=_('Mapa'), on_delete=models.CASCADE, related_name='room_map')
    x = models.PositiveIntegerField(verbose_name=_('Eje X'))
    y = models.PositiveIntegerField(verbose_name=_('Eje Y'))

    class Meta:
        verbose_name = 'Mapa de Sala'
        verbose_name_plural = 'Mapas de Sala'
        db_table = 'room_map'

    def __unicode__(self):
        return 'X: ' + str(self.x) + ' Y: ' + str(self.y) #self.name

    def __str__(self):
        return 'X: ' + str(self.x) + ' Y: ' + str(self.y) #self.name


class Product(models.Model):
    """
    """

    name = models.CharField(verbose_name=_("Nombre"), max_length=50)
    priority = models.PositiveIntegerField(verbose_name=_('Prioridad'), validators=[MaxValueValidator(3), MinValueValidator(1)])
    entry_date = models.DateTimeField(verbose_name=_("Fecha de Entrada"))
    exit_date = models.DateTimeField(verbose_name=_("Fecha de Entrada"))
    sla = models.FileField(verbose_name=_('Service Level Agreement'))
    min_humidity = models.PositiveIntegerField(verbose_name=_('Hum. Mínima'), default=23)
    max_humidity = models.PositiveIntegerField(verbose_name=_('Hum. Máxima'), default=23)
    max_temperature = models.IntegerField(verbose_name=_('Temp. mínima'), default=23)
    max_temperature = models.IntegerField(verbose_name=_('Temp. Máxima'), default=23)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        db_table = 'product'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Container(models.Model):
    """
    """

    #room = models.ForeignKey(Room, verbose_name=_('Sala'), on_delete=models.PROTECT, related_name='container_room')
    product = models.ForeignKey(Product, verbose_name=_('Producto'), on_delete=models.PROTECT, related_name='container_product')
    #room_map = models.OneToOneField(RoomMap, verbose_name=_('Ubicacion'), on_delete=models.CASCADE, related_name='container_roommap', default=1)

    class Meta:
        verbose_name = 'Contenedor'
        verbose_name_plural = 'Contenedores'
        db_table = 'container'

    def __unicode__(self):
        return str(self.id)# + ', sala: ' + str(self.room) + ' | ' +  'producto: ' + str(self.product)

    def __str__(self):
        return str(self.id)# + ', sala: ' + str(self.room) + ' | ' +  'producto: ' + str(self.product)


class MoveTask(models.Model):
    """
    """

    container = models.ForeignKey(Container, verbose_name=_('Contenedor'), on_delete=models.CASCADE, related_name='move_task_container')
    origin = models.ForeignKey(Room, verbose_name=_('Sala origen'), null=True, on_delete=models.SET_NULL, related_name='origin_room')
    destination = models.ForeignKey(Room, verbose_name=_('Sala destino'), null=True, on_delete=models.SET_NULL, related_name='destination_room')
    worker = models.ForeignKey(User, verbose_name=_('Trabajador'), null=True, on_delete=models.SET_NULL, related_name='move_task_worker')

    class Meta:
        verbose_name = 'Tarea de Movimiento'
        verbose_name_plural = 'Tareas de Movimiento'
        db_table = 'move_task'

    def __unicode__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)


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

    def __unicode__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)




#
