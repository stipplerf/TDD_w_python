from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):
    
    def test_cannot_add_emtpy_list_items(self):
        self.fail('write me!')