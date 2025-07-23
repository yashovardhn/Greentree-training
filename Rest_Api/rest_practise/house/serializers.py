from rest_framework import serializers
from .models import House
from users.models import Profile

class HouseSerializer(serializers.ModelSerializer):
    members_counts = serializers.SerializerMethodField(read_only=True)
    members = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), many=True, required=False)
    manager = serializers.HyperlinkedRelatedField(read_only=True,many=False, view_name='profile-detail')
    taskLists = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='tasklist-detail', source='tasks')

    class Meta:
        model = House
        fields = (
            'name', 'url', 'id', 'created_on', 
            'description', 'manager', 'points', 
            'completed_task_count', 'not_completed_task_count','members','members_counts','image' , 'taskLists',# Added 'number_counts' to the fields tuple
        )
        read_only_fields = ('points', 'completed_task_count', 'not_completed_task_count')


    # def get_members_counts(self, obj):
    #     """
    #     Calculates the count for members related to the House instance.
    #     """
    #     # Replace this with your actual logic to count members. 
    #     # Example if 'members' is a related manager on the House model:
    #     return obj.members.count()

    
    
    # def create(self, validated_data):
    #     # Custom logic before creation, e.g. assign a manager automatically if needed
    #     house = House.objects.create(**validated_data)
    #     # For example, assign manager from serializer context (if passed)
    #     request = self.context.get('request')
    #     if request and hasattr(request.user, 'profile'):
    #         house.manager = request.user.profile
    #         house.save()
    #     return house
