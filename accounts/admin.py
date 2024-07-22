from django.contrib import admin
from .models import User, Ranking, Code, UserHistory, Waste
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.admin import ModelAdmin
import csv
from django.http import HttpResponse
from io import StringIO


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        (
            'Campos adicionales',
            {
                'fields': (
                    'profile_picture',
                    'experience_points',
                ),
            },
        ),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'profile_picture':
            formfield.label = 'Imagen de perfil'
        elif db_field.name == 'experience_points':
            formfield.label = 'Puntos de experiencia'
        return formfield


@admin.register(Ranking)
class RankingAdmin(ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'name':
            formfield.label = 'Nombre'
        elif db_field.name == 'level':
            formfield.label = 'Nivel'
        elif db_field.name == 'from_points':
            formfield.label = 'Puntos iniciales'
        elif db_field.name == 'to_points':
            formfield.label = 'Puntos finales'
        elif db_field.name == 'image':
            formfield.label = 'Imagen'
        return formfield


@admin.register(Code)
class CodeAdmin(ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'created_at':
            formfield.label = 'Fecha de creación'
        elif db_field.name == 'random_code':
            formfield.label = 'Código aleatorio (8 dígitos - mayúsculas)'
        elif db_field.name == 'used_by_user':
            formfield.label = 'Utilizado por usuario'
        elif db_field.name == 'redemption_date':
            formfield.label = 'Fecha de redención'
        elif db_field.name == 'user':
            formfield.label = 'Usuario'
        return formfield

    def get_actions(self, request):
        actions = super(CodeAdmin, self).get_actions(request)
        actions['download_csv'] = (CodeAdmin.custom_download_csv, 'download_csv', 'Download CSV')
        return actions

    def custom_download_csv(modeladmin, request, queryset):
        fields = ['random_code']

        f = StringIO()
        writer = csv.writer(f)
        writer.writerow(fields)

        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in fields])

        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="codes.csv"'
        return response


@admin.register(UserHistory)
class UserHistoryAdmin(ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'user':
            formfield.label = 'Usuario'
        elif db_field.name == 'type_of_activity':
            formfield.label = 'Tipo de actividad'
        elif db_field.name == 'accumulated_points':
            formfield.label = 'Puntos acumulados'
        elif db_field.name == 'created_at':
            formfield.label = 'Fecha de creación'
        return formfield


@admin.register(Waste)
class WasteAdmin(ModelAdmin):
    change_list_template = 'accounts/admin/waste_list.html'

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'iteration':
            formfield.label = 'Iteración'
        elif db_field.name == 'date':
            formfield.label = 'Fecha'
        elif db_field.name == 'name_ima_before':
            formfield.label = 'Nombre imagen antes'
        elif db_field.name == 'name_ima_after':
            formfield.label = 'Nombre imagen después'
        elif db_field.name == 'mode':
            formfield.label = 'Modo'
        elif db_field.name == 'folder':
            formfield.label = 'Carpeta'
        elif db_field.name == 'res':
            formfield.label = 'Res'
        elif db_field.name == 'rec':
            formfield.label = 'Rec'
        elif db_field.name == 'ecological_point':
            formfield.label = 'Punto ecologico'
        elif db_field.name == 'model_version':
            formfield.label = 'Versión del modelo'
        elif db_field.name == 'success':
            formfield.label = 'Éxito'
        return formfield
