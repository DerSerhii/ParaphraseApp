from rest_framework import serializers

from nltk.tree import Tree


class ParaphraseSerializer(serializers.Serializer):
    tree = serializers.CharField(max_length=1000)
    limit = serializers.IntegerField(min_value=1, default=20)

    def validate_tree(self, data):
        """
        Check 'tree' parameter is a valid string representation of a parse tree.
        """
        try:
            Tree.fromstring(data)
        except Exception as e:
            raise serializers.ValidationError(f"Invalid parse tree: {e}")
        return data

