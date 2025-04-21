import unittest
import sys
import os
import random
from urllib.parse import quote

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# Import the pure decorator
from fp_decorators.pure import pure

# Create mock classes/objects needed for testing
class MockConfig:
    def __init__(self, user_agent='', custom_user_agent='', lang_search='', country='', lang_interface='', 
                 safe=True, block='', near=None, tor=False, tbs=''):
        self.user_agent = user_agent
        self.custom_user_agent = custom_user_agent 
        self.lang_search = lang_search
        self.country = country
        self.lang_interface = lang_interface
        self.safe = safe
        self.block = block
        self.near = near
        self.tor = tor
        self.tbs = tbs

# Define the pure function implementations to test
@pure(allow_random=True, ignore_params=['config'])
def gen_user_agent(config, is_mobile):
    """Generate a user agent based on config and device type."""
    # Define the Lynx user agent
    LYNX_UA = 'Lynx/2.9.2 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/3.4.0'

    # If using custom user agent, return the custom string
    if config.user_agent == 'custom' and config.custom_user_agent:
        return config.custom_user_agent

    # If using Lynx user agent
    if config.user_agent == 'LYNX_UA':
        return LYNX_UA

    # If no custom user agent is set, generate a random one
    firefox = random.choice(['Choir', 'Squier', 'Higher', 'Wire']) + 'fox'
    linux = random.choice(['Win', 'Sin', 'Gin', 'Fin', 'Kin']) + 'ux'

    # Mobile and desktop UA formats
    MOBILE_UA = '{}/5.0 (Android 0; Mobile; rv:54.0) Gecko/54.0 {}/59.0'
    DESKTOP_UA = '{}/5.0 (X11; {} x86_64; rv:75.0) Gecko/20100101 {}/75.0'

    if is_mobile:
        return MOBILE_UA.format("Mozilla", firefox)

    return DESKTOP_UA.format("Mozilla", linux, firefox)

@pure(ignore_params=['config'])
def gen_query(query, args, config):
    """Generate a search query string based on user inputs."""
    # Valid query params
    VALID_PARAMS = ['tbs', 'tbm', 'start', 'near', 'source', 'nfpr', 'chips']
    
    param_dict = {key: '' for key in VALID_PARAMS}

    # Use :past(hour/day/week/month/year) if available
    # example search "new restaurants :past month"
    lang = ''
    if ':past' in query and 'tbs' not in args:
        time_range = str.strip(query.split(':past', 1)[-1])
        param_dict['tbs'] = '&tbs=' + ('qdr:' + str.lower(time_range[0]))
    elif 'tbs' in args or hasattr(config, 'tbs') and getattr(config, 'tbs'):
        result_tbs = args.get('tbs', '') if 'tbs' in args else config.tbs
        param_dict['tbs'] = '&tbs=' + result_tbs

        # Handle language parameter extraction
        result_params = [_ for _ in result_tbs.split(',') if 'lr:' in _]
        if len(result_params) > 0:
            result_param = result_params[0]
            lang = result_param[result_param.find('lr:') + 3:len(result_param)]

    # Handle various query parameters
    if 'tbm' in args:
        param_dict['tbm'] = '&tbm=' + args.get('tbm')

    if 'start' in args:
        param_dict['start'] = '&start=' + args.get('start')

    if config.near:
        param_dict['near'] = '&near=' + quote(config.near)

    if 'source' in args:
        param_dict['source'] = '&source=' + args.get('source')
        param_dict['lr'] = ('&lr=' + ''.join(
            [_ for _ in lang if not _.isdigit()]
        )) if lang else ''
    else:
        param_dict['lr'] = (
            '&lr=' + config.lang_search
        ) if config.lang_search else ''

    if 'nfpr' in args:
        param_dict['nfpr'] = '&nfpr=' + args.get('nfpr')

    if 'chips' in args:
        param_dict['chips'] = '&chips=' + args.get('chips')

    param_dict['gl'] = (
        '&gl=' + config.country
    ) if config.country else ''
    param_dict['hl'] = (
        '&hl=' + config.lang_interface.replace('lang_', '')
    ) if config.lang_interface else ''
    param_dict['safe'] = '&safe=' + ('active' if config.safe else 'off')

    # Add blocking for sites
    for blocked_site in config.block.replace(' ', '').split(','):
        if not blocked_site:
            continue
        block = (' -site:' + blocked_site)
        if block not in query:
            query += block

    # Append all parameters
    for val in param_dict.values():
        if not val:
            continue
        query += val

    return query

class TestPureIntegration(unittest.TestCase):
    
    def test_gen_user_agent_purity(self):
        """Test that gen_user_agent is pure and returns expected results."""
        # Test with default config (random generation)
        config = MockConfig()
        
        # Fix the random seed for predictable results in testing
        random.seed(42)
        agent1 = gen_user_agent(config, False)
        
        # Reset seed and generate again - should be the same with same seed
        random.seed(42)
        agent2 = gen_user_agent(config, False)
        
        # Verify same inputs produce same outputs
        self.assertEqual(agent1, agent2)
        
        # Test with custom user agent
        custom_ua = "MyCustomAgent/1.0"
        config = MockConfig(user_agent='custom', custom_user_agent=custom_ua)
        self.assertEqual(gen_user_agent(config, False), custom_ua)
        
        # Test Lynx user agent
        config = MockConfig(user_agent='LYNX_UA')
        self.assertEqual(gen_user_agent(config, False), 'Lynx/2.9.2 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/3.4.0')
        
        # Test mobile vs desktop
        config = MockConfig()
        random.seed(42)
        mobile = gen_user_agent(config, True)
        random.seed(42)
        desktop = gen_user_agent(config, False)
        
        # Should be different formats
        self.assertNotEqual(mobile, desktop)
        self.assertTrue('Mobile' in mobile)
        self.assertTrue('x86_64' in desktop)
    
    def test_gen_query_purity(self):
        """Test that gen_query is pure and returns expected results."""
        # Test basic query construction
        config = MockConfig(lang_search='lang_en', country='us')
        query = "test search"
        args = {}
        
        # Generate query string
        result = gen_query(query, args, config)
        
        # Verify expected components
        self.assertTrue(result.startswith(query))
        self.assertIn("&lr=lang_en", result)
        self.assertIn("&gl=us", result)
        self.assertIn("&safe=active", result)
        
        # Test with blocked sites
        config = MockConfig(block="example.com,spam.com")
        result = gen_query("python tutorial", {}, config)
        self.assertIn("-site:example.com", result)
        self.assertIn("-site:spam.com", result)
        
        # Test parameter handling
        args = {"tbm": "isch", "start": "20", "nfpr": "1"}
        result = gen_query("image search", args, config)
        self.assertIn("&tbm=isch", result)
        self.assertIn("&start=20", result)
        self.assertIn("&nfpr=1", result)
        
        # Test time-based search
        result = gen_query("news :past day", {}, config)
        self.assertIn("&tbs=qdr:d", result)
        
        # Test near parameter
        config = MockConfig(near="New York")
        result = gen_query("restaurants", {}, config)
        self.assertIn("&near=New%20York", result)
        
        # Verify input args are not modified
        original_args = {"tbm": "isch", "start": "20"}
        args_copy = original_args.copy()
        gen_query("test", original_args, MockConfig())
        self.assertEqual(original_args, args_copy)

if __name__ == '__main__':
    unittest.main()