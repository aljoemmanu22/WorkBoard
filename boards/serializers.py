from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password', 'is_admin']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_admin=validated_data.get('is_admin', False)
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        print("Login data received:", data)  # New debug statement
        print(f"Attempting login with Username: {username}, Password: {password}")
        
        if username and password:
            user = authenticate(username=username, password=password)
            print("User:", user)  # New debug statement
            if user:
                if user.is_active:
                    return {
                        'user': user,
                        'is_admin': user.is_admin  # Return is_admin field as well
                    }
                else:
                    raise serializers.ValidationError("User is deactivated.")
            else:
                raise serializers.ValidationError("Invalid credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")


from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import WorkBoard, Task, WorkBoardUserRole

User = get_user_model()

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model to handle task creation and updates.
    """
    assigned_user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',  # Assign task by username
        required=False,         # Make this field optional
        allow_null=True
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'assigned_user', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        """
        Custom create method to handle task creation.
        """
        return Task.objects.create(**validated_data)


class WorkBoardSerializer(serializers.ModelSerializer):
    """
    Serializer for the WorkBoard model to handle the creation, listing, and details of task boards.
    """
    tasks = TaskSerializer(many=True, read_only=True)  # Nested tasks for listing and board details
    created_by = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = WorkBoard
        fields = ['id', 'title', 'description', 'created_by', 'tasks', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']


class WorkBoardCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a Work Board without associated tasks.
    """
    class Meta:
        model = WorkBoard
        fields = ['title', 'description']  # Only title and description

    def create(self, validated_data):
        """
        Custom create method to handle the creation of a Work Board.
        """
        return WorkBoard.objects.create(**validated_data)



class WorkBoardUserRoleSerializer(serializers.ModelSerializer):
    """
    Serializer for assigning user roles on a Work Board.
    """
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'  # Role assignment by username
    )

    class Meta:
        model = WorkBoardUserRole
        fields = ['id', 'user', 'role']
        read_only_fields = ['id']

