from rest_framework import serializers
from .models import TaskList, Task, Attachment
from house.models import House


class TaskListSerializer(serializers.ModelSerializer):
    tasks_count = serializers.SerializerMethodField(read_only=True) # Assuming this is uncommented now
    house = serializers.HyperlinkedRelatedField(queryset=House.objects.all(), many=False, view_name='house-detail')
    created_by = serializers.HyperlinkedRelatedField(read_only=True, many = False, view_name='profile-detail')
    tasks = serializers.HyperlinkedRelatedField(read_only= True, many=True, view_name='task-detail')

    class Meta:
        model = TaskList
        fields = ('id', 'name',  'house', 'created_by', 'description', 'status', 'created_on', 'completed_on', 'tasks', 'tasks_count')
        read_only_fields = ('created_on', 'completed_on')

    def get_tasks_count(self, obj):
        return obj.tasks.count()

class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='profile-detail')
    completed_by = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='profile-detail')
    task_list = serializers.HyperlinkedRelatedField(queryset=TaskList.objects.all(), many=False, view_name='tasklist-detail')

    def validate_task_list(self, value):
        user_profile = self.context['request'].user.profile
        
        # --- FIX STARTS HERE ---
        # Check if the user_profile is associated with a house
        if user_profile.house is None:
            raise serializers.ValidationError("You must be a member of a house to create tasks.")
            
        # Now it's safe to access user_profile.house.lists
        if value not in user_profile.house.lists.all():
            raise serializers.ValidationError("You are not allowed to add tasks to this task list (it does not belong to your house).")
        # --- FIX ENDS HERE ---
        
        return value
    
    def create(self, validated_data):
        user_profile = self.context['request'].user.profile
        task = Task.objects.create(
            **validated_data
        )
        task.created_by = user_profile
        task.save()
        return task

    class Meta:
        model = Task
        fields = [
            'url', 'id', 'name', 'description', 'status', 'created_on',
            'completed_on', 'created_by', 'completed_by', 'task_list','attachments'
        ]
        read_only_fields = (
            'created_on', 'completed_on', 'created_by', 'completed_by'
        )


class AttachmentSerializer(serializers.ModelSerializer):
    task = serializers.HyperlinkedRelatedField(queryset=Task.objects.all(), many=False, view_name='task-detail')

    def validate(self, attrs):
        user_profile = self.context['request'].user.profile
        task = attrs['task']
        
        # --- ALSO ADD CHECKS HERE FOR ROBUSTNESS ---
        if user_profile.house is None:
            raise serializers.ValidationError({"task": "You must be a member of a house to add attachments."})
        
        if not task.task_list: # Ensure the task itself has a task_list
            raise serializers.ValidationError({"task": "The selected task is not associated with a task list."})

        # Check if the task's task_list belongs to the user's house
        if task.task_list not in user_profile.house.lists.all():
            raise serializers.ValidationError({"task": "You are not allowed to add attachments to this task (it's not in your house's task lists)."})
        # --- END CHECKS ---
        
        return attrs
        

    class Meta:
        model = Attachment
        fields = ['url', 'id', 'created_on', 'data', 'task']
        read_only_fields = ('created_on',)