from socketio import socketio_manage

from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, render, redirect

from chat.models import *
from chat.sockets import ChatNamespace
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
def login_chat(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/')

    return render(request, 'registration/login.html')
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django import forms

class AccountDetail(DetailView):
    model = Account
class AccountForm(forms.ModelForm):

	class Meta(object):
		model = Account
		fields =  ['username', 'password', 'apartment']
	def __init__(self, *args, **kwargs):
		blocks = kwargs.pop('blocks')
        # now kwargs doesn't contain 'place_user', so we can safely pass it to the base class method
		super(AccountForm, self).__init__(*args, **kwargs)
		self.fields['apartment'].queryset = Apartment.objects.filter(block=blocks)
class AccountUpdateForm(forms.ModelForm):

	class Meta(object):
		model = Account
		fields =  ['username', 'apartment']
		success_url = reverse_lazy('rooms')
	def __init__(self, *args, **kwargs):
		blocks = kwargs.pop('blocks')
        # now kwargs doesn't contain 'place_user', so we can safely pass it to the base class method
		super(AccountUpdateForm, self).__init__(*args, **kwargs)
		self.fields['apartment'].queryset = Apartment.objects.filter(block=blocks)
class AccountCreate(CreateView):
    model = Account
    #form_class = AccountForm
    fields = ['username', 'password', 'apartment']
    success_url = reverse_lazy('rooms')
    form_class = AccountForm
   
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AccountCreate, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(AccountCreate, self).get_form_kwargs()
        kwargs.update({'blocks': self.request.user.block})
        return kwargs
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_password(form.cleaned_data['password'])
        self.object.block=self.request.user.block
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
class ApartmentForm(forms.ModelForm):

	class Meta(object):
		model = Apartment
		fields =  ['apartment_no','block']
	def __init__(self, *args, **kwargs):
		blocks = kwargs.pop('blocks')
		print blocks
        # now kwargs doesn't contain 'place_user', so we can safely pass it to the base class method
		super(ApartmentForm, self).__init__(*args, **kwargs)
		self.fields['block'].queryset = Block.objects.filter(block_name=blocks)
        
class ApartmentCreate(CreateView):
    model = Apartment
    form_class= ApartmentForm
    #fields = ['apartment_no']
    success_url = reverse_lazy('account_create')
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ApartmentCreate, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ApartmentCreate, self).get_form_kwargs()
        kwargs.update({'blocks': self.request.user.block})
        return kwargs
    def form_valid(self, form):
		
        #self.success_url=self.request.GET.get('next', None)
        self.object = form.save(commit=False)
        self.object.block=self.request.user.block
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
from django.contrib.auth.views import password_reset
class AccountUpdate(UpdateView):
    model = Account
    form_class = AccountUpdateForm
    fields =  ['username', 'apartment']
    success_url = reverse_lazy('rooms')
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AccountUpdate, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(AccountUpdate, self).get_form_kwargs()
        kwargs.update({'blocks': self.request.user.block})
        return kwargs
	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.set_password(form.cleaned_data['password'])
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())
class AccountDelete(DeleteView):
    model = Account
    success_url = reverse_lazy('rooms')
@login_required
def rooms(request, template="rooms.html"):
    """
    Homepage - lists all rooms.
    """
    print request.user.role
    if request.user.role=="1":
		context = {"rooms": ChatRoom.objects.filter(created_by__apartment__block__block_name=request.user.block), "residents":Account.objects.filter(block=request.user.block)}
    elif request.user.role=="2":
		context = {"rooms": ChatRoom.objects.filter(created_by__apartment__block__block_name=request.user.block)}
    return render(request, template, context)


def room(request, slug, template="room.html"):
    """
    Show a room.
    """
    room=get_object_or_404(ChatRoom, slug=slug)

    his=Message.objects.filter(chatroom=room.id)

    context = {"room": room,"user":request.user, 'history':his, 'slug':slug}
    return render(request, template, context)


def create(request):
    """
    Handles post from the "Add room" form on the homepage, and
    redirects to the new room.
    """
    name = request.POST.get("name")
    description=request.POST.get("description")
    if name:
        room, created = ChatRoom.objects.get_or_create(name=name, created_by=Account.objects.get(username=request.user), description=description)
        return redirect(room)
    return redirect(rooms)

from django.http import HttpResponse
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


@login_required
@require_POST
def like(request):
    if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug', None)
        print slug
        need = get_object_or_404(ChatRoom, slug=slug)
   
        if need.likes.filter(id=user.id).exists():
            # user has already liked this company
            # remove like/user
            need.likes.remove(user)
            message = 'You removed your order'
        else:
            # add a new like for a company
            need.likes.add(user)
            message = 'You placed an order'

    ctx = {'likes_count': need.likes.count(), 'message': message, 'need':need.name}
    # use mimetype instead of content_type if django < 5
    return HttpResponse(json.dumps(ctx), content_type='application/json')
