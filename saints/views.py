from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import (
    Saint, HagiographyOrWrittenSource, AspectsOfCult,
    ArchaeologicalAndArchitecturalEvidence, Image, Bibliography
)
from django.shortcuts import render
import json


# --- Saint Views ---
class SaintListView(ListView):
    model = Saint
    template_name = 'saints/saint_list.html'
    context_object_name = 'saints'
    paginate_by = 20


class SaintDetailView(DetailView):
    model = Saint
    template_name = 'saints/saint_detail.html'
    context_object_name = 'saint'


class SaintCreateView(CreateView):
    model = Saint
    template_name = 'saints/saint_form.html'
    fields = '__all__'
    success_url = reverse_lazy('saint-list')


class SaintUpdateView(UpdateView):
    model = Saint
    template_name = 'saints/saint_form.html'
    fields = '__all__'
    success_url = reverse_lazy('saint-list')


class SaintDeleteView(DeleteView):
    model = Saint
    template_name = 'saints/saint_confirm_delete.html'
    success_url = reverse_lazy('saint-list')


# --- Example for Hagiography ---
class HagiographyListView(ListView):
    model = HagiographyOrWrittenSource
    template_name = 'saints/hagiography_list.html'
    context_object_name = 'hagiographies'


class HagiographyDetailView(DetailView):
    model = HagiographyOrWrittenSource
    template_name = 'saints/hagiography_detail.html'


class HagiographyCreateView(CreateView):
    model = HagiographyOrWrittenSource
    fields = '__all__'
    template_name = 'saints/hagiography_form.html'
    success_url = reverse_lazy('hagiography-list')


class HagiographyUpdateView(UpdateView):
    model = HagiographyOrWrittenSource
    fields = '__all__'
    template_name = 'saints/hagiography_form.html'
    success_url = reverse_lazy('hagiography-list')


class HagiographyDeleteView(DeleteView):
    model = HagiographyOrWrittenSource
    template_name = 'saints/hagiography_confirm_delete.html'
    success_url = reverse_lazy('hagiography-list')



