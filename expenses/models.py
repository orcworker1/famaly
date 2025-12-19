from django.db import models
from django.utils import timezone
from django.conf import settings
import secrets


User = settings.AUTH_USER_MODEL

class Household(models.Model):
    name = models.CharField(max_length=120)
    currency = models.CharField(max_length=3, default="RUB")
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_households")
    created_at = models.DateTimeField(default=timezone.now)


class FamilyMember(models.Model):
    class Role(models.TextChoices):
        OWNER = "OWNER", "Owner"
        EDITOR = "EDITOR", "Editor"
        VIEWER = "VIEWER", "Viewer"
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='name_member')
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.VIEWER)
    joined_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = [("household", "user")]

    def __str__(self):
        return f"{self.user} in {self.household} ({self.role})"


class Invite(models.Model):
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name="invites")
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_invites")
    code = models.CharField(max_length=16, unique=True, db_index=True)
    role = models.CharField(max_length=12, choices=FamilyMember.Role.choices, default=FamilyMember.Role.EDITOR)
    expires_at = models.DateTimeField(null=True, blank=True)
    max_uses = models.PositiveIntegerField(default=1)
    uses = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    @classmethod
    def generate_code(cls) -> str:
        return secrets.token_urlsafe(9)[:12]

    def is_valid(self) -> bool:
        if self.expires_at and timezone.now() >= self.expires_at:
            return False
        return self.uses < self.max_uses
# Create your models here.
