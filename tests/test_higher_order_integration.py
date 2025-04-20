import unittest
import sys
import os
import random

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# Import higher-order functions
from fp_decorators.higher_order import (
    higher_order, memoize, is_higher_order
)

# Create mock objects needed for testing
class MockConfig:
    def __init__(self):
        self.user_agent = ''
        self.custom_user_agent = ''


class TestHigherOrderIntegration(unittest.TestCase):
    
    def test_higher_order_decorator(self):
        """Test applying the higher_order decorator to a simple function."""
        
        # Define a simple function with higher_order decorator
        @higher_order(enhanced=True)
        def generate_greeting(name, formal=False):
            """Generate a greeting message."""
            if formal:
                return f"Good day, {name}."
            return f"Hello, {name}!"
        
        # Verify the function is marked as higher-order
        self.assertTrue(is_higher_order(generate_greeting))
        
        # Test the basic function still works
        result = generate_greeting("Alice")
        self.assertEqual(result, "Hello, Alice!")
        
        # Test with formal parameter
        result = generate_greeting("Mr. Smith", formal=True)
        self.assertEqual(result, "Good day, Mr. Smith.")
        
        # Verify the function has enhanced methods
        self.assertTrue(hasattr(generate_greeting, 'partial'))
        self.assertTrue(hasattr(generate_greeting, 'curry'))
        self.assertTrue(hasattr(generate_greeting, 'compose'))
        self.assertTrue(hasattr(generate_greeting, 'pipe'))
        
        # Test the partial method
        formal_greeting = generate_greeting.partial(formal=True)
        result = formal_greeting("Dr. Johnson")
        self.assertEqual(result, "Good day, Dr. Johnson.")
    
    def test_memoization(self):
        """Test applying memoization to a function with repeated calls."""
        
        # Track call count
        call_count = 0
        
        # Define a function with memoization
        @memoize
        def compute_expensive_value(n):
            """Simulate an expensive computation."""
            nonlocal call_count
            call_count += 1
            # Just a simple calculation for testing
            return n * n
        
        # First call should execute the function
        result1 = compute_expensive_value(5)
        self.assertEqual(result1, 25)
        self.assertEqual(call_count, 1)
        
        # Second call with same value should use cache
        result2 = compute_expensive_value(5)
        self.assertEqual(result2, 25)
        self.assertEqual(call_count, 1)  # Still 1, used cache
        
        # Call with different value should execute function again
        result3 = compute_expensive_value(10)
        self.assertEqual(result3, 100)
        self.assertEqual(call_count, 2)  # Incremented for new input


if __name__ == '__main__':
    unittest.main()