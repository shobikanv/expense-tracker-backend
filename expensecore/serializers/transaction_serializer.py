from rest_framework import serializers
from expensecore.models import Transaction, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Transaction
        fields = '__all__'

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', None)
        transaction = Transaction.objects.create(**validated_data)
        if tags_data:
            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(name=tag_data['name'])
                transaction.tags.add(tag)
        return transaction

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        tags = instance.tags.all()

        instance = super().update(instance, validated_data)

        if tags_data:
            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(name=tag_data['name'])
                if tag not in tags:
                    instance.tags.add(tag)
            for tag in tags:
                if tag.name not in [tag_data['name'] for tag_data in tags_data]:
                    instance.tags.remove(tag)

        return instance
