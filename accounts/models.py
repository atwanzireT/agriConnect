from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.auth.base_user import BaseUserManager
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        extra_fields.setdefault('role', 'guest')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


# ==============================
# Custom User Model
# ==============================

class User(AbstractUser):
    username = None  # Remove username, use email instead
    email = models.EmailField(_('email address'), unique=True)

    ROLE_CHOICES = [
        ('admin', _('System Administrator')),
        ('farmer', _('Farmer')),
        ('buyer', _('Buyer')),
        ('logistics', _('Logistics Partner')),
        ('finance', _('Financial Institution')),
        ('guest', _('Guest User')),
    ]

    LANGUAGE_CHOICES = [
        ('en', _('English')),
        ('sw', _('Swahili')),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='guest')
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
        blank=True,
        null=True
    )
    location = models.CharField(max_length=100, blank=True, null=True)
    verified = models.BooleanField(default=False)
    preferred_language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='en')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']
    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        permissions = [
            ('can_manage_users', 'Can manage all users'),
            ('can_verify_users', 'Can verify user accounts'),
        ]

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    def save(self, *args, **kwargs):
        if self.role == 'admin':
            self.is_staff = True
            self.is_superuser = True
        elif self.role == 'guest':
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)


# ==============================
# Farmer Profile Model (Updated)
# ==============================

class FarmerProfile(models.Model):
    FARM_UNITS = [
        ('acres', 'Acres'),
        ('hectares', 'Hectares'),
        ('sqm', 'Square Meters'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmer_profile')
    is_group = models.BooleanField(default=False, verbose_name=_("Farmer Group/Cooperative"))
    
    # Fields for individual farmers
    farm_size = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        blank=True,
        null=True
    )
    farm_size_unit = models.CharField(
        max_length=10, 
        choices=FARM_UNITS, 
        default='acres',
        blank=True
    )
    years_of_experience = models.PositiveIntegerField(blank=True, null=True)
    
    # Fields for farmer groups
    group_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name=_("Group/Cooperative Name")
    )
    group_registration_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Registration Number")
    )
    group_members_count = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_("Number of Members")
    )
    group_formation_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Formation Date")
    )
    
    # Common fields for both
    crop_types = models.ManyToManyField('produce.Crop')
    expected_harvest_date = models.DateField(blank=True, null=True)
    id_card_number = models.CharField(max_length=50, blank=True)
    certification = models.CharField(max_length=100, blank=True)
    contact_person = models.CharField(max_length=100, blank=True)
    contact_phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
        blank=True
    )

    class Meta:
        verbose_name = _('farmer profile')
        verbose_name_plural = _('farmer profiles')

    def __str__(self):
        if self.is_group:
            return f"{self.group_name} (Group)"
        return f"{self.user.email}'s farm"

    def clean(self):
        if self.is_group:
            if not self.group_name:
                raise ValidationError(_("Group name is required for farmer groups"))
        else:
            if not self.farm_size:
                raise ValidationError(_("Farm size is required for individual farmers"))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

        
# ==============================
# Buyer Profile Model
# ==============================

class BuyerProfile(models.Model):
    COMPANY_TYPES = [
        ('factory', _('Factory')),
        ('wholesaler', _('Wholesaler')),
        ('supermarket', _('Supermarket')),
        ('processor', _('Food Processor')),
        ('individual', _('Individual')),
        ('exporter', _('Exporter')),
        ('restaurant', _('Restaurant/Hotel')),
    ]

    COMMUNICATION_CHOICES = [
        ('email', _('Email')),
        ('phone', _('Phone')),
        ('whatsapp', _('WhatsApp')),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_profile')
    business_name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=100, blank=True)
    company_type = models.CharField(max_length=50, choices=COMPANY_TYPES)
    preferred_products = models.ManyToManyField('produce.Crop')
    delivery_address = models.TextField()
    additional_addresses = models.JSONField(default=list, blank=True)
    contact_person = models.CharField(max_length=100)
    contact_phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')]
    )
    tax_identification = models.CharField(max_length=50, blank=True)
    preferred_communication = models.CharField(max_length=20, choices=COMMUNICATION_CHOICES, default='email')

    class Meta:
        verbose_name = _('buyer profile')
        verbose_name_plural = _('buyer profiles')

    def __str__(self):
        return f"{self.business_name} ({self.get_company_type_display()})"