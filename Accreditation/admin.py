from django.contrib import admin

from .models import *

# Individual registrations
admin.site.register(accredbodies)
admin.site.register(accredlevel)
admin.site.register(instrument)
admin.site.register(instrument_level)
admin.site.register(instrument_level_folder)
admin.site.register(files)
admin.site.register(program_accreditation)
admin.site.register(result_remarks)
admin.site.register(accreditation_certificates)
admin.site.register(user_assigned_to_folder)

