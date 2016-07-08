
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib import admin
from django.core.urlresolvers import reverse
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):

    def _create_user(self, username, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        
        user = self.model(username=username,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        return self._create_user(username, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, True, True,
                                 **extra_fields)

ROLES = (
    (u'1', u'Block_Manager'),
    (u'2', u'Resident'),
)

class Block(models.Model):
	#manager=models.CharField(max_length=20, unique=True)
	block_name=models.CharField(max_length=20, unique=True)
	block_address=models.CharField(max_length=200)
	def __unicode__(self):
		return self.block_name
	def get_absolute_url(self):
		return reverse('comment_detail', args=[str(self.id)])
class Apartment(models.Model):
	apartment_no=models.CharField(max_length=6)
	block = models.ForeignKey(Block , blank=False)
	def __unicode__(self):
		return self.apartment_no
	def get_absolute_url(self):
		return reverse('comment_detail', args=[str(self.id)])

from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

ROLES = (    (u'2', u'Resident'),
    (u'1', u'Block_Manager'),)
class Account(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email and password are required. Other fields are optional.
    """
    email = models.EmailField(_('email address'), max_length=254, unique=False, blank=True)
    username = models.CharField(max_length=40, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    role=models.CharField(max_length=12, choices=ROLES, default="2")
    block=models.ForeignKey(Block , blank=False, default=0)
    apartment=models.ForeignKey(Apartment , blank=True, default=0)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name



class ChatUser(models.Model):

    name = models.CharField(max_length=20)
    session = models.CharField(max_length=20)
    room = models.ForeignKey("chat.ChatRoom", related_name="users")

    class Meta:
        ordering = ("name",)

    def __unicode__(self):
        return self.name
class ChatRoom(models.Model):

    name = models.CharField(max_length=20)
    slug = models.SlugField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Account , blank=False)
    description=models.TextField(max_length=20)
    likes = models.ManyToManyField(Account, related_name='likes')
    class Meta:
        ordering = ("name",)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("room", (self.slug,))
	@property
	def total_likes(self):
		return self.likes.count()
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(ChatRoom, self).save(*args, **kwargs)


class Message(models.Model):
    text = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Account , blank=False)
    chatroom = models.CharField(max_length=20)
admin.site.register(ChatRoom)

admin.site.register(Block)
admin.site.register(Apartment)

admin.site.register(Message)
