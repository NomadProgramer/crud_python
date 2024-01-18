task = Task.objects.create(
    title='Título de la tarea',
    description='Descripción opcional de la tarea',
    datecomplated=None,  # Deja esto como `None` si la tarea aún no se ha completado
    important=True,  # Cambia a `False` si la tarea no es importante
    user=meji,  # Asigna el usuario que creaste anteriormente
)