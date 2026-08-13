from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from apps.accounts.models import Client
from apps.cases.models import Case, Document, InternalNote, ClientCommunication, AuditLog


class ClientRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Client
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'phone_number', 'country', 'telegram_handle',
            'password', 'confirm_password'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        # Use email as username if username not provided
        if not validated_data.get('username'):
            validated_data['username'] = validated_data['email']
        
        user = Client.objects.create_user(**validated_data)
        return user


class ClientLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = Client.objects.get(email=email)
        except Client.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")

        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        attrs['user'] = user
        return attrs


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'country', 'telegram_handle']


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = [
            'id', 'case_number', 'client', 'status', 'scam_category',
            'loss_amount', 'currency', 'recovery_amount', 'fee_amount',
            'transaction_method', 'transaction_data',
            'first_transaction_date', 'last_transaction_date',
            'narrative', 'submitted_at', 'updated_at', 'recovery_completed_at'
        ]
        read_only_fields = ['id', 'case_number', 'client', 'status', 'submitted_at', 'updated_at', 'fee_amount']

    def create(self, validated_data):
        validated_data['client'] = self.context['request'].user
        return super().create(validated_data)


class CaseDetailSerializer(CaseSerializer):
    client = ClientSerializer(read_only=True)


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'case', 'document_type', 'file_name', 'file_url', 'file_size', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class InternalNoteSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = InternalNote
        fields = ['id', 'case', 'author', 'author_name', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def get_author_name(self, obj):
        return obj.author.get_full_name()

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)