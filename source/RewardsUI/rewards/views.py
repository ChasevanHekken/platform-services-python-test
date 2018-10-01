import logging
import requests

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django.shortcuts import render
from .forms import UserForm

class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__)):
        self.logger = logger

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        self.refresh(context)
        user_form = UserForm()
        context['user_form'] = user_form

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        form = UserForm(request.POST)
        form.is_valid()

        request_body = {
            "emailAddress": form.cleaned_data["email"],
            "orderTotal": form.cleaned_data["order"]
        }
        requests.post("http://rewardsservice:7050/create", data = request_body)
        self.refresh(context)

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def refresh(self, context):
        response = requests.get("http://rewardsservice:7050/rewards")
        context['rewards_data'] = response.json()

        usersResponse = requests.get("http://rewardsservice:7050/users")
        context['users_data'] = usersResponse.json()

        user_form = UserForm()
        context['user_form'] = user_form