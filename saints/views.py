import json
from django.views.generic import ListView, DetailView
from django.core.serializers.json import DjangoJSONEncoder

from .models import Saint


class SaintListView(ListView):
    model = Saint
    template_name = "saints/saint_list.html"
    context_object_name = "saints"
    paginate_by = 20


class SaintDetailView(DetailView):
    model = Saint
    template_name = "saints/saint_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        saint = self.object
        markers = []

        # Birth
        if saint.region_of_birth_latitude and saint.region_of_birth_longitude:
            markers.append(
                {
                    "lat": float(saint.region_of_birth_latitude),
                    "lng": float(saint.region_of_birth_longitude),
                    "label": f"Birthplace: {saint.region_of_birth or 'Unknown'}",
                }
            )

        # Burial
        if saint.region_of_burial_latitude and saint.region_of_burial_longitude:
            markers.append(
                {
                    "lat": float(saint.region_of_burial_latitude),
                    "lng": float(saint.region_of_burial_longitude),
                    "label": f"Burial: {saint.region_of_burial or 'Unknown'}",
                }
            )

        context["markers_json"] = json.dumps(markers, cls=DjangoJSONEncoder)
        return context
