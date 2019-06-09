
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os

from django.db.models import Count, Case, When, Value, Subquery
from django.db.models import Q, F
from django.contrib.auth.models import User

from storage_go_app import models as storage_models


# Create your procedures here.
def getRoom(tempMaxDegree=None, tempMinDegree=None, humidMax=None, humidMin=None):
    """
    """

    rooms = storage_models.Room.objects \
    .filter(
        status='Abierta',
        humidity__lte=humidMax,
        humidity__gte=humidMin,
        temperature__lte=tempMaxDegree,
        temperature__gte=tempMinDegree,
    ) \
    .values('id')
    """
        .exclude(
            id=34
        ) \
    """

    #print(rooms)

    room_maps = storage_models.RoomMap.objects.filter(
        status='Disponible',
        room__id__in=rooms
    ) \
    .values('id')
    #.order_by('')

    #print(room_maps)

    if len(room_maps) < 1:
        return None
    else:
        return room_maps


def getWorker():
    """
    """

    from django.db import connection

    print("get worker procedure")

    cursor = connection.cursor()
    response = cursor.execute(' \
        SELECT au.user_id, COUNT(mt.worker_id) as num_tasks \
        FROM active_user au, auth_group ag, auth_user_groups aug \
        LEFT JOIN move_task mt \
	       ON au.user_id == mt.worker_id \
	       AND mt.status LIKE "Pendiente" \
        WHERE ag.id == 9 \
        AND aug.group_id == ag.id \
        AND au.user_id == aug.user_id \
        GROUP BY au.user_id \
        ORDER BY 2 ASC; \
    ')

    aux = response.fetchall()
    #print(aux)

    if len(aux) < 1:
        return None
    else:
        return aux[0]


def checkWithDrawal():
    """
    check if all container from a product are in 'embarque' room
    """

    pass




#
