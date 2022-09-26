from django.contrib import admin
from django.apps import apps

# # Register your models here.
# for model in apps.get_models():
#     try:
#         admin.site.register(model)
#     except admin.sites.AlreadyRegistered:
#         pass
    

app_config = apps.get_app_config('snippets') # Replace your_app_name it is just a placeholder
models = app_config.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass