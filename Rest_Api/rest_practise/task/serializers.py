from rest_framework import serializers
from .models import TaskList, Task, Attachment
from house.models import House


class TaskListSerializer(serializers.ModelSerializer):
    # tasks_count = serializers.SerializerMethodField(read_only=True)
    house = serializers.HyperlinkedRelatedField(queryset=House.objects.all(), many=False, view_name='house-detail')
    created_by = serializers.HyperlinkedRelatedField(read_only=True, many = False, view_name='profile-detail')
    tasks = serializers.HyperlinkedRelatedField(read_only= True, many=True, view_name='task-detail')

    class Meta:
        model = TaskList
        fields = ('id', 'name',  'house', 'created_by', 'description', 'status', 'created_on', 'completed_on', 'tasks')
        read_only_fields = ('created_on', 'completed_on')

    # def get_tasks_count(self, obj):
    #     return obj.tasks.count()

class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='profile-detail')
    completed_by = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='profile-detail')
    task_list = serializers.HyperlinkedRelatedField(queryset=TaskList.objects.all(), many=False, view_name='tasklist-detail')

    def validate_task_list(self, value):
        user_profile = self.context['request'].user.profile
        if value not in user_profile.house.lists.all():
            raise serializers.ValidationError("You are not allowed to add tasks to this task list.")
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
        task_list = TaskList.objects.get(id=task.task_list.id)
        if task_list != user_profile.house.lists.all():
            raise serializers.ValidationError("You are not allowed to add attachments to this task list.")
        

    class Meta:
        model = Attachment
        fields = ['url', 'id', 'created_on', 'data', 'task']
        read_only_fields = ('created_on',)