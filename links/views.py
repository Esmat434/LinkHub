from django.shortcuts import render
from django.views import View

from accounts.mixins import (
    LoginRequiredMixin
)

from .models import (
    Link
)

