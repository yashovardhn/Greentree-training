from rest_framework import serializers
from .models import House

class HouseSerializer(serializers.ModelSerializer):
    members_counts = serializers.SerializerMethodField(read_only=True)
    members = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='profile-detail')
    manager = serializers.HyperlinkedRelatedField(read_only=True,many=False, view_name='profile-detail')

    class Meta:
        model = House
        fields = (
            'url', 'id', 'name', 'created_on', 
            'description', 'manager', 'points', 
            'completed_task_count', 'not_completed_task_count','members','members_counts','image' # Added 'number_counts' to the fields tuple
        )
        read_only_fields = ('points', 'completed_task_count', 'not_completed_task_count')


    def get_members_counts(self, obj):
        """
        Calculates the count for members related to the House instance.
        """
        # Replace this with your actual logic to count members. 
        # Example if 'members' is a related manager on the House model:
        # return obj.members.count()
        return 0
    
    
    # def create(self, validated_data):
    #     house = House.objects.create(**validated_data)
    #     return house

    # def update(self, instance, validated_data):
    #     instance.address = validated_data.get('address', instance.address)
    #     instance.image = validated_data.get('image', instance.image)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.save()
    #     return instance
