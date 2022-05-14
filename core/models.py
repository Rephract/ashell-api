# from django.db import models


# class BaseCoreModel(models.Model):
#     """Base model structure
#     """
#     user = models.OneToOneField('account.User', related_name='profile', on_delete=models.CASCADE)
#     organization = models.ForeignKey('account.Organization', on_delete=models.CASCADE, null=True, blank=True)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
