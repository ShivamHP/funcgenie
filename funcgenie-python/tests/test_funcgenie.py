import unittest
from funcgenie.phantom import phantom, phantom_functions

class TestFuncGenie(unittest.TestCase):
    
    @phantom
    def test_function(self, x: int, y: int):
        return x + y

    def test_decorator(self):
        self.assertIn('test_function', phantom_functions)
        self.assertEqual(phantom_functions['test_function']['function_name'], 'test_function')

if __name__ == '__main__':
    unittest.main()
