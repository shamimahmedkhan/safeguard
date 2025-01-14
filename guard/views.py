from typing import Any
import folium
from django.db import models
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Therapist, Appointment, Client, SafeguardLead
from django.utils import timezone


@login_required
def index(request):
    return render(
        request=request,
        template_name="guard/index.html",
        context={'title': f'Hello {request.user}'},
    )


class TherapistListView(ListView):
    model = Therapist
    paginate_by = 100
    template_name="guard/lead_list.html"
# TODO: add map!
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         figure = folium.Figure()
#         m = folium.Map(
#             location=[45.372, -121.6972],
#             zoom_start=12,
#             tiles='openstreetmap'
#         )
#         m.add_to(figure)
#         icon = folium.features.CustomIcon("https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
#                                       icon_size=(40, 40))
#         folium.Marker(
#             location=[45.3288, -121.6625],
#             popup= """
# <a href='/therapist/1'>Test</a>
#     """,
#             icon=icon
#         ).add_to(m)

#         folium.Marker(
#             location=[45.3311, -121.7113],
#             popup='Timberline Lodge',
#             icon=folium.Icon(color='green')
#         ).add_to(m)

#         folium.Marker(
#             location=[45.3300, -121.6823],
#             popup='Some Other Location',
#             icon=folium.Icon(color='red', icon='info-sign')
#         ).add_to(m)
#         m = m._repr_html_()
#         context['map'] = m
#         return context


class TherapistDetailView(DetailView):
    model = Therapist
    template_name="guard/therapist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointments'] = context['therapist'].appointment_set.exclude(checked_out=True).order_by('start_time')
        return context


class AppointmentDetailView(DetailView):
    model = Appointment
    template_name="guard/appointment.html"


def appointment_check_in(request, pk):
    appointment = Appointment.objects.get(id=pk)
    now = timezone.now()
    if not appointment.checked_in:
        appointment.checked_in = True
        appointment.check_in_time = now
        appointment.save()
    return redirect('appointment_detail', pk=pk)


def appointment_check_out(request, pk):
    appointment = Appointment.objects.get(id=pk)
    now = timezone.now()
    if not appointment.checked_out:
        appointment.checked_out = True
        appointment.check_out_time = now
        appointment.save()
    return redirect('appointment_detail', pk=pk)


class ClientDetailView(DetailView):
    model = Client
    template_name="guard/client.html"
