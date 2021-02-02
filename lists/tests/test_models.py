from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
User = get_user_model()
# from django.utils.html import escape
from lists.models import Item, List

# from unittest import skip

class ItemModelsTest(TestCase):
    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item.objects.create(text='The first (ever) list item', list=list_)
        self.assertIn(item, list_.item_set.all())
    
    def test_list_ordering(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='i1')
        item2 = Item.objects.create(list=list1, text='item2')
        item3 = Item.objects.create(list=list1, text='3')
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()
    
    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        item = Item.objects.create(list=list_, text='bla')
        with self.assertRaises(IntegrityError):
            item = Item(list=list_, text='bla')
            # item.full_clean()
            item.save()
    
    def test_CAN_save_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean() # should not raise
    
    def test_string_representation(self):
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

class ListModelTest(TestCase):
    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

    def test_create_new_creates_list_nad_fisrt_item(self):
        List.create_new(first_item_text='new item text')
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'new item text')
        new_list = List.objects.first()
        self.assertEqual(new_item.list, new_list)
    
    def test_create_new_opptinally_saves_owner(self):
        user = User.objects.create()
        List.create_new(first_item_text='new item text', owner=user)
        new_list = List.objects.first()
        self.assertEqual(new_list.owner, user)

    def test_lists_can_have_owner(self):
        List(owner=User()) # should not raise
    
    def test_list_owner_is_optional(self):
        List().full_clean() #should not raise

    def test_create_new_returns_new_list_objects(self):
        returned = List.create_new(first_item_text='new item text')
        new_list = List.objects.first()
        self.assertEqual(returned, new_list)
    
    def test_lists_name_is_first_item_text(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='first item')
        Item.objects.create(list=list_, text='second item')
        self.assertEqual(list_.name, 'first item')
    
    def test_add_email_to_list_shared(self):
        list_ = List.objects.create()
        user = User.objects.create(email='a@b.com')
        list_.shared_with.add('a@b.com')
        list_in_db = List.objects.get(id=list_.id)
        self.assertIn(user, list_in_db.shared_with.all())
