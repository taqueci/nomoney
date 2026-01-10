# Copyright (C) Takeshi Nakamura. All rights reserved.

from rest_framework import permissions

from money.views.shared import access


class HasPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        match view.action:
            case 'create':
                return access.creatable(request.user)
            case 'update' | 'partial_update':
                return access.updatable(request.user)
            case 'destroy':
                return access.deletable(request.user)

        return access.readable(request.user)
