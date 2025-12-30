"""Test data factories.

This module provides factory classes for generating test data.
"""

import uuid
from datetime import datetime

import factory
from factory import fuzzy


class UserFactory(factory.Factory):
    """Factory for generating User test data."""

    class Meta:
        model = dict

    id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    email = factory.Faker("email")
    username = factory.Faker("user_name")
    full_name = factory.Faker("name")
    is_active = True
    is_superuser = False
    created_at = factory.LazyFunction(datetime.utcnow)


class DocumentFactory(factory.Factory):
    """Factory for generating Document test data."""

    class Meta:
        model = dict

    id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    name = factory.Faker("file_name", extension="docx")
    file_path = factory.LazyAttribute(lambda o: f"./uploads/{o.id}.docx")
    user_id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    current_version = 1
    metadata = factory.LazyFunction(lambda: {"author": "Test"})
    is_locked = False
    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)


class TemplateFactory(factory.Factory):
    """Factory for generating Template test data."""

    class Meta:
        model = dict

    id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    name = factory.Faker("sentence", nb_words=3)
    file_path = factory.LazyAttribute(lambda o: f"./templates/{o.id}.docx")
    description = factory.Faker("paragraph")
    category = fuzzy.FuzzyChoice(["Business", "Personal", "Academic", "General"])
    tags = factory.LazyFunction(lambda: ["template", "sample"])
    created_at = factory.LazyFunction(datetime.utcnow)


class CommentFactory(factory.Factory):
    """Factory for generating Comment test data."""

    class Meta:
        model = dict

    id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    document_id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    author = factory.Faker("name")
    text = factory.Faker("sentence")
    paragraph_index = fuzzy.FuzzyInteger(0, 10)
    is_resolved = False
    created_at = factory.LazyFunction(datetime.utcnow)
