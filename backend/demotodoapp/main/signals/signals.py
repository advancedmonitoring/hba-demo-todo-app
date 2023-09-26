import django.dispatch

note_created = django.dispatch.Signal()
note_updated = django.dispatch.Signal()
note_deleted = django.dispatch.Signal()

todo_created = django.dispatch.Signal()
todo_updated = django.dispatch.Signal()
todo_deleted = django.dispatch.Signal()
