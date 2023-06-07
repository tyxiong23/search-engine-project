from rest_framework import serializers
from .models import Case

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['id', 'qw_value', 'ws_value', 'jbfy_value', 'xzqh_p_value', 'xzqh_c_value', 'land_value']

