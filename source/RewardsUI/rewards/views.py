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

        search = request.GET.get('search', None)
        if search != None:
            single_user = requests.get("http://rewardsservice:7050/find?emailAddress=" + search)
            if single_user.json():
                context['users_data'] = [single_user.json()]
            else:
                self.refresh_users(context)
        else:
            self.refresh_users(context)

        self.refresh_rewards(context)
        self.refresh_create_form(context)
        
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
        self.refresh_rewards(context)
        self.refresh_users(context)
        self.refresh_create_form(context)

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def refresh_rewards(self, context):
        rewards = requests.get("http://rewardsservice:7050/rewards")
        context['rewards_data'] = rewards.json()

    def refresh_users(self, context):
        all_users = requests.get("http://rewardsservice:7050/users")
        context['users_data'] = all_users.json()

    def refresh_create_form(self, context):
        user_form = UserForm()
        context['user_form'] = user_form