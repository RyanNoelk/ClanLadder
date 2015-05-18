from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from django.contrib.auth.views import password_change as auth_password_change
from django.contrib.auth import logout as auth_logout

from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

def Logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('Ladder:index'))

@sensitive_post_parameters()
@csrf_protect
@login_required
def PasswordChange(request):
    return auth_password_change(request,post_change_redirect='/Accounts/password/change/done', template_name='Accounts/password_change_form.html',)
    #return HttpResponseRedirect(reverse('Ladder:index'))

    
    
