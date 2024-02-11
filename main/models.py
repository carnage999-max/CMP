import uuid
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "Superuser must have is_staff=True "
            )
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must have is_superuser=True"
            )

        return self._create_user(email, password, **extra_fields)


LEVEL = (
    ('100', '100'),
    ('200', '200'),
    ('300', '300'),
    ('400', '400'),
    ('500', '500'),
    ('600', '600'),
    ('700', '700'),
    ('800', '800'),
    ('900', '900'),
)

class UserProfile(AbstractUser):
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    student_tag = models.CharField(max_length=64, unique=True, null=False)
    middle_name = models.CharField(_("Middle name"), blank=True, max_length=150)
    matric_number = models.CharField(_("Number"), max_length=20)
    department = models.CharField(_("Department"), max_length=200)
    level = models.CharField(_("Level"), max_length=200, choices=LEVEL)
    no_of_friends = models.IntegerField(_("No of Friends"), blank=True, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email
    
    def get_full_name(self):
        return f"{(self.last_name).upper()} {self.first_name} {self.middle_name}"


GROUP_TYPE = (
    ('virtual', 'Virtual'),
    ('physical', 'Physical'),
)

class StudyGroup(models.Model):
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='users')
    members = models.ManyToManyField(UserProfile)
    title = models.CharField(_("Title"), max_length=1024)
    descripton = models.CharField(_("Descripton"), max_length=2048)
    group_type = models.CharField(_("Group Type"), max_length=200, choices=GROUP_TYPE)
    number_of_participants = models.IntegerField(_("Number of participants"), default=0)
    
    def __str__(self):
        return f"{self.title} created by {self.creator}"
    
    def get_group_creator(self):
        return self.creator
    
    
class Resources(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    description = models.CharField(_("Description"), max_length=1024, null=True, default="Well, this might be useful")
    resource = models.FileField(_("Resource"), upload_to='files/')
    uploaded_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = _("Resource")
        verbose_name_plural = _("Resources")
    
    def __str__(self):
        return f"{self.title} uploaded by {self.uploaded_by}"
    
    
class QuizQuestion(models.Model):
    course_code = models.CharField(_("Course Code"), max_length=10)
    course_title = models.CharField(_("Course Title"), max_length=200)
    question = models.TextField(_("Question"))
    optionA = models.CharField(_("Option A"), max_length=200)
    optionB = models.CharField(_("Option B"), max_length=200)
    optionC = models.CharField(_("Option C"), max_length=200)
    optionD = models.CharField(_("Option D"), max_length=200)
    answer = models.CharField(_("Answer"), max_length=1024)
    
    class Meta:
        verbose_name = _("Quiz Question")
        verbose_name_plural = _("Quiz Questions")
        
    def __str__(self):
        return self.course_code
    
        
class Quiz(models.Model):
    quiz_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    user_taking = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    final_score = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")