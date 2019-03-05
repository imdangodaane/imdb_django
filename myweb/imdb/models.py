from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, Permission

# Create your models here.
class Login(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    def __str__(self):
        return self.username


class MyUser(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    password_confirm = models.CharField(max_length=100)
    email_address = models.EmailField(max_length=254)
    def __str__(self):
        return self.username


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email_address, password=None):
        if not username:
            raise ValueError("User must have an username.")
        if not email_address:
            raise ValueError("User must have an email address.")

        user = self.model(
            username=self.get_by_natural_key(username),
            email_address=self.normalize_email(email_address),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email_address, password):
        if not username:
            raise ValueError("User must have an username.")
        if not email_address:
            raise ValueError("User must have an email address.")
        if not password:
            raise ValueError("User must have a password.")

        user = self.create_user(
            username=username,
            email_address=email_address,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)


class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    # password_confirm = models.CharField(max_length=100)
    email_address = models.EmailField(max_length=254)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group)
    user_permissions = models.ManyToManyField(Permission)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    # EMAIL_FIELD = 'email_address'
    # REQUIRED_FIELD = ['email_address']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Actor(models.Model):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    UNDEFINED = 'UNDEFINED'
    SEX_CHOICES = [
        (MALE, MALE.capitalize()),
        (FEMALE, FEMALE.capitalize()),
        (UNDEFINED, UNDEFINED.capitalize()),
    ]
    NATIONALITIES_CHOICES = (('Afghan', 'Afghan'), ('Albanian', 'Albanian'), ('Algerian', 'Algerian'), ('American', 'American'), ('Andorran', 'Andorran'), ('Angolan', 'Angolan'), ('Antiguans', 'Antiguans'), ('Argentinean', 'Argentinean'), ('Armenian', 'Armenian'), ('Australian', 'Australian'), ('Austrian', 'Austrian'), ('Azerbaijani', 'Azerbaijani'), ('Bahamian', 'Bahamian'), ('Bahraini', 'Bahraini'), ('Bangladeshi', 'Bangladeshi'), ('Barbadian', 'Barbadian'), ('Barbudans', 'Barbudans'), ('Batswana', 'Batswana'), ('Belarusian', 'Belarusian'), ('Belgian', 'Belgian'), ('Belizean', 'Belizean'), ('Beninese', 'Beninese'), ('Bhutanese', 'Bhutanese'), ('Bolivian', 'Bolivian'), ('Bosnian', 'Bosnian'), ('Brazilian', 'Brazilian'), ('British', 'British'), ('Bruneian', 'Bruneian'), ('Bulgarian', 'Bulgarian'), ('Burkinabe', 'Burkinabe'), ('Burmese', 'Burmese'), ('Burundian', 'Burundian'), ('Cambodian', 'Cambodian'), ('Cameroonian', 'Cameroonian'), ('Canadian', 'Canadian'), ('Cape Verdean', 'Cape Verdean'), ('Central African', 'Central African'), ('Chadian', 'Chadian'), ('Chilean', 'Chilean'), ('Chinese', 'Chinese'), ('Colombian', 'Colombian'), ('Comoran', 'Comoran'), ('Congolese', 'Congolese'), ('Costa Rican', 'Costa Rican'), ('Croatian', 'Croatian'), ('Cuban', 'Cuban'), ('Cypriot', 'Cypriot'), ('Czech', 'Czech'), ('Danish', 'Danish'), ('Djibouti', 'Djibouti'), ('Dominican', 'Dominican'), ('Dutch', 'Dutch'), ('Dutchman', 'Dutchman'), ('Dutchwoman', 'Dutchwoman'), ('East Timorese', 'East Timorese'), ('Ecuadorean', 'Ecuadorean'), ('Egyptian', 'Egyptian'), ('Emirian', 'Emirian'), ('Equatorial Guinean', 'Equatorial Guinean'), ('Eritrean', 'Eritrean'), ('Estonian', 'Estonian'), ('Ethiopian', 'Ethiopian'), ('Fijian', 'Fijian'), ('Filipino', 'Filipino'), ('Finnish', 'Finnish'), ('French', 'French'), ('Gabonese', 'Gabonese'), ('Gambian', 'Gambian'), ('Georgian', 'Georgian'), ('German', 'German'), ('Ghanaian', 'Ghanaian'), ('Greek', 'Greek'), ('Grenadian', 'Grenadian'), ('Guatemalan', 'Guatemalan'), ('Guinea-Bissauan', 'Guinea-Bissauan'), ('Guinean', 'Guinean'), ('Guyanese', 'Guyanese'), ('Haitian', 'Haitian'), ('Herzegovinian', 'Herzegovinian'), ('Honduran', 'Honduran'), ('Hungarian', 'Hungarian'), ('I-Kiribati', 'I-Kiribati'), ('Icelander', 'Icelander'), ('Indian', 'Indian'), ('Indonesian', 'Indonesian'), ('Iranian', 'Iranian'), ('Iraqi', 'Iraqi'), ('Irish', 'Irish'), ('Israeli', 'Israeli'), ('Italian', 'Italian'), ('Ivorian', 'Ivorian'), ('Jamaican', 'Jamaican'), ('Japanese', 'Japanese'), ('Jordanian', 'Jordanian'), ('Kazakhstani', 'Kazakhstani'), ('Kenyan', 'Kenyan'), ('Kittian and Nevisian', 'Kittian and Nevisian'), ('Kuwaiti', 'Kuwaiti'), ('Kyrgyz', 'Kyrgyz'), ('Laotian', 'Laotian'), ('Latvian', 'Latvian'), ('Lebanese', 'Lebanese'), ('Liberian', 'Liberian'), ('Libyan', 'Libyan'), ('Liechtensteiner', 'Liechtensteiner'), ('Lithuanian', 'Lithuanian'), ('Luxembourger', 'Luxembourger'), ('Macedonian', 'Macedonian'), ('Malagasy', 'Malagasy'), ('Malawian', 'Malawian'), ('Malaysian', 'Malaysian'), ('Maldivan', 'Maldivan'), ('Malian', 'Malian'), ('Maltese', 'Maltese'), ('Marshallese', 'Marshallese'), ('Mauritanian', 'Mauritanian'), ('Mauritian', 'Mauritian'), ('Mexican', 'Mexican'), ('Micronesian', 'Micronesian'), ('Moldovan', 'Moldovan'), ('Monacan', 'Monacan'), ('Mongolian', 'Mongolian'), ('Moroccan', 'Moroccan'), ('Mosotho', 'Mosotho'), ('Motswana', 'Motswana'), ('Mozambican', 'Mozambican'), ('Namibian', 'Namibian'), ('Nauruan', 'Nauruan'), ('Nepalese', 'Nepalese'), ('Netherlander', 'Netherlander'), ('New Zealander', 'New Zealander'), ('Ni-Vanuatu', 'Ni-Vanuatu'), ('Nicaraguan', 'Nicaraguan'), ('Nigerian', 'Nigerian'), ('Nigerien', 'Nigerien'), ('North Korean', 'North Korean'), ('Northern Irish', 'Northern Irish'), ('Norwegian', 'Norwegian'), ('Omani', 'Omani'), ('Pakistani', 'Pakistani'), ('Palauan', 'Palauan'), ('Panamanian', 'Panamanian'), ('Papua New Guinean', 'Papua New Guinean'), ('Paraguayan', 'Paraguayan'), ('Peruvian', 'Peruvian'), ('Polish', 'Polish'), ('Portuguese', 'Portuguese'), ('Qatari', 'Qatari'), ('Romanian', 'Romanian'), ('Russian', 'Russian'), ('Rwandan', 'Rwandan'), ('Saint Lucian', 'Saint Lucian'), ('Salvadoran', 'Salvadoran'), ('Samoan', 'Samoan'), ('San Marinese', 'San Marinese'), ('Sao Tomean', 'Sao Tomean'), ('Saudi', 'Saudi'), ('Scottish', 'Scottish'), ('Senegalese', 'Senegalese'), ('Serbian', 'Serbian'), ('Seychellois', 'Seychellois'), ('Sierra Leonean', 'Sierra Leonean'), ('Singaporean', 'Singaporean'), ('Slovakian', 'Slovakian'), ('Slovenian', 'Slovenian'), ('Solomon Islander', 'Solomon Islander'), ('Somali', 'Somali'), ('South African', 'South African'), ('South Korean', 'South Korean'), ('Spanish', 'Spanish'), ('Sri Lankan', 'Sri Lankan'), ('Sudanese', 'Sudanese'), ('Surinamer', 'Surinamer'), ('Swazi', 'Swazi'), ('Swedish', 'Swedish'), ('Swiss', 'Swiss'), ('Syrian', 'Syrian'), ('Taiwanese', 'Taiwanese'), ('Tajik', 'Tajik'), ('Tanzanian', 'Tanzanian'), ('Thai', 'Thai'), ('Togolese', 'Togolese'), ('Tongan', 'Tongan'), ('Trinidadian or Tobagonian', 'Trinidadian or Tobagonian'), ('Tunisian', 'Tunisian'), ('Turkish', 'Turkish'), ('Tuvaluan', 'Tuvaluan'), ('Ugandan', 'Ugandan'), ('Ukrainian', 'Ukrainian'), ('Uruguayan', 'Uruguayan'), ('Uzbekistani', 'Uzbekistani'), ('Venezuelan', 'Venezuelan'), ('Vietnamese', 'Vietnamese'), ('Welsh', 'Welsh'), ('Yemenite', 'Yemenite'), ('Zambian', 'Zambian'), ('Zimbabwean', 'Zimbabwean'))

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthdate = models.DateTimeField()
    sex = models.CharField(
        max_length=10,
        choices=SEX_CHOICES,
        default=UNDEFINED,
    )
    nationalities = models.CharField(
        max_length=50,
        choices=NATIONALITIES_CHOICES,
        default='Vietnamese',
    )
    alive = models.CharField(
        max_length=20,
        choices=(
            ('Alive', 'Alive'),
            ('Dead', 'Dead'),
            ('NA', 'NA'),
        ),
        default='NA',
    )

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Movie(models.Model):
    COMEDY = 'COMEDY'
    SCIFI = 'SCI-FI'
    HORROR = 'HORROR'
    ROMANCE = 'ROMANCE'
    ACTION = 'ACTION'
    THIRLLER = 'THRILLER'
    DRAMA = 'DRAMA'
    MYSTERY = 'MYSTERY'
    CRIME = 'CRIME'
    ANIMATION = 'ANIMATION'
    ADVENTURE = 'ADVENTURE'
    FANTASY = 'FANTASY'
    COMEDYROMANCE = 'COMEDY-ROMANCE'
    ACTIONCOMEDY = 'ACTION-COMEDY'
    SUPERHERO = 'SUPERHERO'

    CATEGORIES_CHOICES = [
        (COMEDY, COMEDY.capitalize()),
        (SCIFI, SCIFI.capitalize()),
        (HORROR, HORROR.capitalize()),
        (ROMANCE, ROMANCE.capitalize()),
        (ACTION, ACTION.capitalize()),
        (THIRLLER, THIRLLER.capitalize()),
        (DRAMA, DRAMA.capitalize()),
        (MYSTERY, MYSTERY.capitalize()),
        (CRIME, CRIME.capitalize()),
        (ANIMATION, ANIMATION.capitalize()),
        (ADVENTURE, ADVENTURE.capitalize()),
        (FANTASY, FANTASY.capitalize()),
        (COMEDYROMANCE, COMEDYROMANCE.capitalize()),
        (ACTIONCOMEDY, ACTIONCOMEDY.capitalize()),
        (SUPERHERO, SUPERHERO.capitalize()),
    ]

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=254)
    release_date = models.DateTimeField()
    categories = models.CharField(
        max_length=20,
        choices=CATEGORIES_CHOICES,
        default=COMEDY,
        )
    actors = models.ManyToManyField(Actor)
    logo = models.ImageField()

    def __str__(self):
        return self.title


class Award(models.Model):
    ACTOR = 'ACTOR'
    MOVIE = 'MOVIE'
    name = models.CharField(max_length=100)
    kind = models.CharField(
        max_length=50,
        choices=(
            (ACTOR, ACTOR.capitalize()),
            (MOVIE, MOVIE.capitalize()),
        )
    )

    def __str__(self):
        return self.name

