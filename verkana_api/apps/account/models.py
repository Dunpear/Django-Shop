from django_jalali.db import models as jmodels
import jdatetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.contrib.auth.base_user import BaseUserManager



class CustomerUserManager(BaseUserManager):
    def create_user(self, user_phone, email='', name='', family='', active_code=None, gender=None, password=None):
        if not user_phone:
            raise ValueError('شماره موبایل را وارد نکرده اید')
        user = self.model(user_phone=user_phone, email=self.normalize_email(email), name=name, family=family,
                          gender=gender, active_code=active_code)
        if len(password) < 6:
            raise ValueError('طول کلمه عبور باید بیشتر یا مساوی 6 باشد')

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_phone, email, name, family, password=None, active_code=None, gender=None):
        user = self.create_user(user_phone, email, name, family, active_code, gender, password)
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomerUser(AbstractBaseUser, PermissionsMixin):
    user_phone = models.CharField(max_length=11, unique=True, verbose_name='شماره موبایل')
    email = models.CharField(blank=True, null=True, max_length=200, verbose_name='ایمیل')
    name = models.CharField(max_length=50, verbose_name='نام')
    family = models.CharField(max_length=50, verbose_name='نام خانوادگی')
    image = models.ImageField(upload_to='users/', verbose_name='عکس پروفایل کاربری', blank=True, null=True)
    GENDER_CHOICES = (('True', 'مرد'), ('False', 'زن'))
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES, default='True', blank=True, null=True,
                              verbose_name='جنسیت')
    register_date = jmodels.jDateField(default=jdatetime.date.today(), verbose_name='تاریخ ثبت نام')
    active_code = models.CharField(max_length=10, blank=True, null=True, )
    is_active = models.BooleanField(default=False, verbose_name='وضعیت کاربر')

    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'user_phone'
    REQUIRED_FIELDS = ['name', 'family', 'email']
    objects = CustomerUserManager()

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return f'{self.name} - {self.family}'

    def has_perms(self, perm_list, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class SellerUser(CustomerUser):
    pass