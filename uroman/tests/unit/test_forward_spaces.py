#!/usr/bin/env python3

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from uroman import Uroman

def test_forward_spaces():
    u = Uroman()
    
    # Test Swahili
    result = u.romanize_string('habari yako', lcode='swa')
    print(f'Forward uroman: "habari yako" -> "{result}"')
    print(f'Length: {len(result)}')
    print(f'Contains space: {" " in result}')
    print()
    
    # Test Arabic
    result2 = u.romanize_string('salam alaykum', lcode='ara')
    print(f'Forward uroman: "salam alaykum" -> "{result2}"')
    print(f'Length: {len(result2)}')
    print(f'Contains space: {" " in result2}')
    print()
    
    # Test with different scripts
    result3 = u.romanize_string('hello world', lcode='eng')
    print(f'Forward uroman: "hello world" -> "{result3}"')
    print(f'Length: {len(result3)}')
    print(f'Contains space: {" " in result3}')

if __name__ == "__main__":
    test_forward_spaces()
