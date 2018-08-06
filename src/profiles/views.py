from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, View

from menus.models import Item
from restaurants.models import RestaurantLocation
from .models import Profile

User = get_user_model()

class ProfileFollowToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username_to_toggle = request.POST.get("username")
        is_following = False
        profile, is_following = Profile.objects.toggle_follow(request.user, username_to_toggle)
        return redirect(f"/u/{profile.user.username}")

class ProfileDetailview(DetailView):
    template_name = 'profiles/user.html'

    def get_object(self):
        username = self.kwargs.get("username")
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username, is_active=True)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailview, self).get_context_data(*args, **kwargs)
        user = context['user']
        is_following = False
        if user.profile in self.request.user.is_following.all():
            is_following = True
        context['is_following'] = is_following
        query = self.request.GET.get('query')
        item_exists = Item.objects.filter(user=user).exists()
        qs = RestaurantLocation.objects.filter(owner=user).search(query)
        if item_exists and qs.exists:
            context['locations'] = qs
        return context