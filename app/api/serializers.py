# Copyright (C) Takeshi Nakamura. All rights reserved.

from django.contrib.auth import get_user_model
from rest_framework import serializers

from doc.models import Page
from money.models import Account, Attachment, Journal, Tag

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'full_name']


class AttachmentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'file', 'base_name', 'digest']


class AttachmentSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    author = UserSerializer()

    class Meta:
        model = Attachment
        fields = '__all__'

    def get_file(self, obj):
        return obj.file.url


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class AccountDetailSerializer(AccountSerializer):
    entry = serializers.SerializerMethodField()

    def get_entry(self, obj):
        return {'value': obj.entry, 'label': obj.get_entry_display()}


class AccountSummarySerializer(AccountSerializer):
    class Meta:
        model = Account
        fields = ['name', 'entry']


class AccountListSerializer(AccountSerializer):
    class Meta:
        model = Account
        exclude = ['description']


class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = '__all__'
        read_only_fields = ['author']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class JournalDetailSerializer(JournalSerializer):
    debit = AccountDetailSerializer()
    credit = AccountDetailSerializer()
    author = UserSerializer()
    attachments = AttachmentSerializer(many=True)
    tags = TagSerializer(many=True)


class JournalListSerializer(JournalSerializer):
    debit = AccountSummarySerializer()
    credit = AccountSummarySerializer()

    class Meta:
        model = Journal
        fields = [
            'id', 'debit', 'credit', 'date', 'amount', 'summary',
            'fy', 'enabled', 'author', 'created', 'updated',
        ]


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'
        read_only_fields = ['author', 'digest']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PageDetailSerializer(PageSerializer):
    author = UserSerializer()


class PageListSerializer(PageSerializer):
    author = UserSerializer()

    class Meta:
        model = Page
        exclude = ['content']
