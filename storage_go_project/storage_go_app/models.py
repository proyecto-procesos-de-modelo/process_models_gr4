
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.shortcuts import render, redirect, get_object_or_404

from storage_go_app import procedures as storage_procedures
from storage_go_app.decorators import autoconnect

from decimal import Decimal

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

class ActiveUser(models.Model):

    user = models.ForeignKey(User, verbose_name=_('Usuario Trabajando'), related_name='active_user', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Usuario Activo")
        verbose_name_plural = _("Usuarios Activos")
        db_table = 'active_user'
        default_permissions = ()

    def __str__(self):
        return str(self.user)

    def __unicode__(self):
        return str(self.user)


class CustomPermission(models.Model):
    """
    """

    group = models.ForeignKey(Group, verbose_name=_('Grupo'), on_delete=models.CASCADE, related_name='permission_group', default=1)
    #user
    #PERMISSION_TYPE = (('Modelo', 'Modelo'), ('Objeto', 'Objeto'), ('Atributo', 'Atributo'))
    type = models.CharField(verbose_name=_('Tipo'), max_length=10)
    #ACTION_TYPE = (('Ver', 'Ver'), ('Filtrar', 'Filtrar'), ('Crear', 'Crear'), ('Modificar', 'Modificar'), ('Borrar','Borrar'))
    action = models.CharField(verbose_name=_('Acción'), max_length=10)
    #module = models.CharField(verbose_name=_('Módulo'), max_length=50)
    model = models.CharField(verbose_name=_('Modelo'), max_length=50, null=True, blank=True)
    object = models.CharField(verbose_name=_('Objeto'), max_length=50, null=True, blank=True)
    attribute = models.CharField(verbose_name=_('Atributo'), max_length=50, null=True, blank=True)


    class Meta:
        verbose_name = str(_("Permiso Personalizado"))
        verbose_name_plural = _("Permisos Personalizados")
        db_table = 'custom_permission'
        default_permissions = ()

    def __str__(self):
        return str(self.id) #self.type + ' | ' + self.action + ' | ' + self.model + ' | ' + self.object + ' | ' + self.attribute

    def __unicode__(self):
        return str(self.id) #self.type + ' | ' + self.action + ' | ' + self.model + ' | ' + self.object + ' | ' + self.attribute


# Create your models h
class Statistic(models.Model):
    """
    """

    name = models.CharField(verbose_name=_("Nombre"), max_length=100)
    value = models.CharField(verbose_name=_("Valor"), max_length=100)

    class Meta:
        verbose_name = _("Estadística")
        verbose_name_plural = _("Estadísticas")
        db_table = 'statistic'
        default_permissions = ()

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


@autoconnect
class Room(models.Model):
    """
    """

    STATUS = (("Abierta", "Abierta"), ("Cerrada", "Cerrada"))
    status = models.CharField(verbose_name=_("Estado"), max_length=7, choices=STATUS, default='Cerrada')
    name = models.CharField(verbose_name=_("Nombre"), max_length=50)
    humidity = models.FloatField(verbose_name=_('Humedad'))
    temperature = models.FloatField(verbose_name=_('Temperatura'))
    max_containers = models.PositiveIntegerField(verbose_name=_('Capacidad Máxima'), default=0)

    class Meta:
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'
        db_table = 'room'
        default_permissions = ()

    def meta(self):
        return self._meta

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


@autoconnect
class RoomMap(models.Model):
    """
    """

    STATUS = (("Disponible", "Disponible"), ("Ocupado", "Ocupado"))
    status = models.CharField(verbose_name=_("Estado"), max_length=10, choices=STATUS, default='Disponible')
    room = models.ForeignKey(Room, verbose_name=_('Sala'), on_delete=models.CASCADE, related_name='room_map')
    x = models.PositiveIntegerField(verbose_name=_('Eje X'))
    y = models.PositiveIntegerField(verbose_name=_('Eje Y'))

    class Meta:
        verbose_name = 'Mapa de Sala'
        verbose_name_plural = 'Mapas de Sala'
        db_table = 'room_map'
        default_permissions = ()

    def __unicode__(self):
        return str(self.room) + ' - (X: ' + str(self.x) + ' Y: ' + str(self.y) + ')'

    def __str__(self):
        return str(self.room) + ' - (X: ' + str(self.x) + ' Y: ' + str(self.y) + ')'

    def save(self, *args, **kwargs):
        """
        """

        #print("custom room map save function")

        room = get_object_or_404(Room, id=self.room.id)
        Room.objects.filter(id=room.id).update(max_containers=room.max_containers+1)

        super(RoomMap, self).save(*args, **kwargs)


@autoconnect
class Product(models.Model):
    """
    """

    name = models.CharField(verbose_name=_("Nombre"), max_length=50)
    entry_date = models.DateField(verbose_name=_("Fecha de Entrada"), auto_now_add=True)
    exit_date = models.DateField(verbose_name=_("Fecha de Salida"))
    min_humidity = models.FloatField(verbose_name=_('Hum. Mínima'))
    max_humidity = models.FloatField(verbose_name=_('Hum. Máxima'))
    min_temperature = models.FloatField(verbose_name=_('Temp. Mínima'))
    max_temperature = models.FloatField(verbose_name=_('Temp. Máxima'))
    num_containers = models.PositiveIntegerField(verbose_name=_('Nº Contenedores'), default=1)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        db_table = 'product'
        default_permissions = ()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


@autoconnect
class Container(models.Model):
    """
    """

    product = models.ForeignKey(Product, verbose_name=_('Producto'), on_delete=models.CASCADE, related_name='container_product')
    room_map = models.ForeignKey(RoomMap, verbose_name=_('Ubicacion'), on_delete=models.CASCADE, related_name='container_roommap')

    class Meta:
        verbose_name = 'Contenedor'
        verbose_name_plural = 'Contenedores'
        db_table = 'container'
        default_permissions = ()


    def __unicode__(self):
        return str('ID: ') + str(self.id) + ' | ' + str(self.product) + ' | ' +  str(self.room_map)

    def __str__(self):
        return str('ID: ') + str(self.id) + ' | ' + str(self.product) + ' | ' +  str(self.room_map)

    def save(self, *args, **kwargs):
        """
        """
        print("custom save container function")
        print(self)
        print(self.room_map)

        room_map = get_object_or_404(RoomMap, id=self.room_map.id)
        room_map.status = 'Ocupado'
        room_map.save()

        super(Container, self).save(*args, **kwargs)

    @receiver(signals.post_save, sender=Product)
    def createContainers(sender, instance, created, **kwargs):
        """
        filter on reception room
        """

        print("automatically create container ")

        if created:
            for container in range(instance.num_containers):

                destination = RoomMap.objects.filter(room_id=34, status='Disponible').order_by('id').first()

                container = Container.objects.create(
                    product_id=instance.id,
                    room_map=destination
                )


@autoconnect
class MoveTask(models.Model):
    """
    """

    STATUS = (("Completada", "Completada"), ("Pendiente", "Pendiente"))
    status = models.CharField(verbose_name=_("Estado"), max_length=10, choices=STATUS, default='Pendiente', blank=True)
    priority = IntegerRangeField(verbose_name=_("Prioridad"), min_value=1, max_value=3, default=1, blank=True)
    container = models.ForeignKey(Container, verbose_name=_('Contenedor'), on_delete=models.CASCADE, related_name='move_task_container', blank=True)
    destination = models.ForeignKey(RoomMap, verbose_name=_('Destino'), on_delete=models.CASCADE, related_name='destination_room_map', null=True, blank=True) #, help_text='Dejar en blanco para asignar automáticamente')
    worker = models.ForeignKey(User, verbose_name=_('Trabajador'), null=True, on_delete=models.CASCADE, related_name='move_task_worker', blank=True)

    class Meta:
        verbose_name = 'Tarea de Movimiento'
        verbose_name_plural = 'Tareas de Movimiento'
        db_table = 'move_task'
        default_permissions = ()

    def __unicode__(self):

        return str(self.id) + ' | ' + str(self.container) + ' | ' + str(self.destination)

    def __str__(self):

        return str(self.id) + ' | ' + str(self.container) + ' | ' + str(self.destination)

    def custom_save(self, extra=None, *args, **kwargs):
        """
        """

        if extra is not None:
            self.status = extra['status']
            self.priority = extra['priority']
            container = get_object_or_404(Container, id=extra['container_id'])
            self.container = container
            destination = get_object_or_404(RoomMap, id=extra['destination_id'])
            self.destination = destination
            worker = get_object_or_404(User, id=extra['worker_id'])
            self.worker.id = worker.id

        self.save()

    def save(self, *args, **kwargs):
        """
        """
        #print("custom move task save function")

        room_map = None
        product = get_object_or_404(Product, id=self.container.product.id)

        RoomMap.objects.filter(id=self.container.room_map.id).update(status='Ocupado')

        # si no se ha asignado trabajador
        if self.worker is None:
            #print("worker is none")
            worker = storage_procedures.getWorker()
            #print(worker)
            self.worker_id = worker[0]

        # si el estado es pendiente
        if self.status == 'Pendiente':
            #print("status pendiente")

            # obtenemos los posibles destinos
            destinations = storage_procedures.getRoom(product.max_temperature, product.min_temperature, product.max_humidity, product.min_humidity)
            #print(destinations)

            # si no se ha asignado el destino
            if self.destination is None:
                #print("destination is none")

                # si no hay destino posibles
                if destinations is None:
                    #print("destinations is none")
                    # asignamos el destino nulo
                    self.destination = None

                # si hay destinos posibles
                else:
                    #print("destinations is not none")
                    # asignamos el destino
                    room_map_id = destinations.values('id')[0]
                    aux = get_object_or_404(RoomMap, id=room_map_id['id'])
                    self.destination = aux

                    # actualizamos el mapa de la sala
                    aux.status = 'Ocupado'
                    aux.save()

            # si se ha asignado el destino
            else:
                #print("destination is not none")
                # obtenemos los posibles destinos
                aux = []
                [aux.append(item['id']) for item in destinations.values('id')]

                # si el destino no esta dentro de los posibles
                if self.destination.id not in aux:
                    #print("destination not in destinations")
                    # asignamos el destino nulo
                    self.destination = None

                else:
                    #print("destination in destinations")
                    # asignamos el destino
                    aux = get_object_or_404(RoomMap, id=self.destination.id)

                    # actualizamos el mapa de la sala
                    aux.status = 'Ocupado'
                    aux.save()

        # si el estatus es completado
        else:
            #print("status completado")
            # si no se ha asignado el destino
            if self.destination is None:
                self.status = 'Pendiente'

            # si se ha asignado el destino
            else:
                container = get_object_or_404(Container, id=self.container.id)
                origin = get_object_or_404(RoomMap, id=container.room_map.id)

                origin.status = 'Disponible'
                origin.save()

                container.room_map = self.destination
                container.save()

        super(MoveTask, self).save(*args, **kwargs)

    @receiver(signals.post_save, sender=Container)
    def createTasks(sender, instance, created, **kwargs):
        """
        """

        print("automatically create move task ")


        if created:
            print("container created")
            print(instance)

            move_task = MoveTask.objects.create(
                container=instance,
            )

            print(move_task)


@autoconnect
class MaintenanceTask(models.Model):
    """
    """

    STATUS = (("Completada", "Completada"), ("Pendiente", "Pendiente"))
    status = models.CharField(verbose_name=_("Estado"), max_length=10, choices=STATUS, default='Pendiente', blank=True)
    priority = IntegerRangeField(verbose_name=_("Prioridad"), min_value=1, max_value=3, default=1, blank=True)
    room = models.ForeignKey(Room, verbose_name=_('Sala'), on_delete=models.CASCADE, related_name='maintenance_task_room', null=True, blank=True)
    machine = models.CharField(verbose_name=_("Máquina"), max_length=50, blank=True)

    class Meta:
        verbose_name = 'Tarea de Mantenimiento'
        verbose_name_plural = 'Tareas de Mantenimiento'
        db_table = 'maintenance_task'
        default_permissions = ()

    def __unicode__(self):
        return str(self.room) + ' | ' + self.machine

    def __str__(self):
        return str(self.room) + ' | ' + self.machine

    def custom_save(self, extra, *args, **kwargs):

        #print("custom save maintenance task function")

        self.status = extra['status']
        self.priority = extra['priority']
        self.room = extra['room_id']
        self.machine = extra['machine']

        #super(MaintenanceTask, self).save(*args, **kwargs)
        self.save()


@autoconnect
class Budget(models.Model):
    """
    """

    STATUS = (("Aprobado", "Aprobado"), ("Pendiente", "Pendiente"), ("Cancelado", "Cancelado"))
    status = models.CharField(verbose_name=_("Estado"), max_length=10, choices=STATUS, default='Pendiente')
    maintenance_task = models.ForeignKey(MaintenanceTask, verbose_name=_('Tarea'), on_delete=models.CASCADE, related_name='budget_task', blank=True)
    cantidad = models.DecimalField(verbose_name=_('Precio'), max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], blank=True)
    descripción = models.TextField(verbose_name=_('Descripción'), blank=True)

    class Meta:
        verbose_name = 'Presupuesto'
        verbose_name_plural = 'Presupuestos'
        db_table = 'budget'
        default_permissions = ()

    def __unicode__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)

    def custom_save(self, extra=None, *args, **kwargs):
        """
        """

        #print("custom save budget function")

        self.status = extra['status']
        self.maintenance_task.id = extra['maintenance_task_id']
        self.cantidad = extra['cantidad']
        self.descripcion = extra['descripción']

        # añadir coste a estadisticas

        self.save()


class Notification(models.Model):
    """
    """

    user = models.ForeignKey(User, verbose_name=_('Usuario'), on_delete=models.CASCADE, default=1)
    model = models.ForeignKey(ContentType, verbose_name=_('Modelo'), on_delete=models.CASCADE)
    object = models.PositiveIntegerField(verbose_name=_('Objeto'))
    content_object = GenericForeignKey('model', 'object')
    description = models.TextField(verbose_name=_('Descripción'))

    class Meta:
        verbose_name = _("Notificación")
        verbose_name_plural = _("Notificaciones")
        db_table = 'notification'
        default_permissions = ()

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)

    @receiver(signals.post_save, sender=MoveTask)
    def createMoveTaskNotification(sender, instance, created, **kwargs):
        """
        """

        #print("move task notification")

        content_type = get_object_or_404(ContentType, model='movetask')

        #if created:
        move_task = get_object_or_404(MoveTask, id=instance.id)

        if instance.destination is None:
            #print("destination is none")
            Notification.objects.create(
                user_id = 13,
                model = content_type,
                object = instance.id,
                description = "Ninguna sala cumple con las condiciones adecuadas para el contenedor %s" % (str(instance.container.id))
            )
        else:
            #print("destination is not none")
            if move_task.worker is not None:
                #print("worker is not none")
                if instance.status == 'Completada':
                    #print("status completada")
                    Notification.objects.create(
                        user_id = 13,
                        model = content_type,
                        object = instance.id,
                        description = "La tarea de movimiento con identificador %s se ha completado." % (str(instance.id))
                    )
                else:
                    #print("pendiente")
                    Notification.objects.create(
                        user = move_task.worker,
                        model = content_type,
                        object = instance.id,
                        description = "Se te ha asignado la tarea con identificador %s" % (str(instance.id))
                    )
            else:
                #print("worker is none")
                pass

    @receiver(signals.post_save, sender=MaintenanceTask)
    def createMaintenanceTaskNotification(sender, instance, created, **kwargs):
        """
        """
        #print("maintenace task notification")

        content_type = get_object_or_404(ContentType, model='maintenancetask')

        if instance.status == 'Completada':
            Notification.objects.create(
                user_id = 13,
                model = content_type,
                object = instance.id,
                description = "La tarea de mantenimiento con identificador %s se ha completado." % (str(instance.id))
            )

        else:
            Notification.objects.create(
                user_id = 11,
                model = content_type,
                object = instance.id,
                description = "Hay un tarea de mantenimiento pendiente con identificador %s." % (str(instance.id))
            )

    @receiver(signals.post_save, sender=Budget)
    def createBudgetNotification(sender, instance, created, **kwargs):
        """
        """
        #print("budget notification")

        content_type = get_object_or_404(ContentType, model='budget')
        estado = instance.status

        if estado != 'Pendiente':
            #print(estado)
            if estado == 'Aprobado':
                estado = 'aprobado'
            elif estado == 'Aprobado':
                estado = 'cancelado'

            Notification.objects.create(
                user_id = 11,
                model = content_type,
                object = instance.id,
                description = "El presupuesto con identificador %s se ha %s." % (str(instance.id), estado)
            )

        else:
            Notification.objects.create(
                user_id = 12,
                model = content_type,
                object = instance.id,
                description = "Se ha creado un presupuesto con identificador %s." % (str(instance.id))
            )





#
