"""REST API viewsets for nautobot_bgp_models."""

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from nautobot.extras.api.views import CustomFieldModelViewSet, StatusViewSetMixin
from nautobot.utilities.utils import dynamic_import

import nautobot_bgp_models.filters as filters
import nautobot_bgp_models.models as models
from . import serializers


class PluginModelViewSet(CustomFieldModelViewSet):
    """Base class for all REST API viewsets in this plugin."""

    def get_serializer_class(self):
        """Override the default ModelViewSet implementation as it doesn't handle plugins correctly."""
        app_label, model_name = self.queryset.model._meta.label.split(".")
        if self.brief:
            try:
                return dynamic_import(f"{app_label}.api.serializers.Nested{model_name}Serializer")
            except AttributeError:
                pass

        return self.serializer_class


class AutonomousSystemViewSet(PluginModelViewSet, StatusViewSetMixin):
    """REST API viewset for AutonomousSystem records."""

    queryset = models.AutonomousSystem.objects.all()
    serializer_class = serializers.AutonomousSystemSerializer
    filterset_class = filters.AutonomousSystemFilterSet


class PeeringRoleViewSet(PluginModelViewSet):
    """REST API viewset for PeeringRole records."""

    queryset = models.PeeringRole.objects.all()
    serializer_class = serializers.PeeringRoleSerializer
    filterset_class = filters.PeeringRoleFilterSet


include_inherited = openapi.Parameter(
    "include_inherited",
    openapi.IN_QUERY,
    description="Include inherited configuration values",
    type=openapi.TYPE_BOOLEAN,
)


class InheritableFieldsViewSetMixin:
    """Common mixin for ViewSets that support an additional `include_inherited` query parameter."""

    @swagger_auto_schema(manual_parameters=[include_inherited])
    def list(self, request):
        """List all objects of this type."""
        return super().list(request)

    @swagger_auto_schema(manual_parameters=[include_inherited])
    def retrieve(self, request, pk=None):
        """Retrieve a specific object instance."""
        return super().retrieve(request, pk=pk)


class PeerGroupViewSet(InheritableFieldsViewSetMixin, PluginModelViewSet):
    """REST API viewset for PeerGroup records."""

    queryset = models.PeerGroup.objects.all()
    serializer_class = serializers.PeerGroupSerializer
    filterset_class = filters.PeerGroupFilterSet


class PeerEndpointViewSet(InheritableFieldsViewSetMixin, PluginModelViewSet):
    """REST API viewset for PeerEndpoint records."""

    queryset = models.PeerEndpoint.objects.all()
    serializer_class = serializers.PeerEndpointSerializer
    filterset_class = filters.PeerEndpointFilterSet


class PeerSessionViewSet(PluginModelViewSet, StatusViewSetMixin):
    """REST API viewset for PeerSession records."""

    queryset = models.PeerSession.objects.all()
    serializer_class = serializers.PeerSessionSerializer
    filterset_class = filters.PeerSessionFilterSet


class AddressFamilyViewSet(InheritableFieldsViewSetMixin, PluginModelViewSet):
    """REST API viewset for AddressFamily records."""

    queryset = models.AddressFamily.objects.all()
    serializer_class = serializers.AddressFamilySerializer
    filterset_class = filters.AddressFamilyFilterSet
