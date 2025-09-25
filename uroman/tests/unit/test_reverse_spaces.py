#!/usr/bin/env python3

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from reverse_uroman import ReverseUroman

def test_reverse_spaces():
    r = ReverseUroman()
    
    # Test Swahili
    result = r.reverse_romanize_string('habari yako', target_script='Swahili')
    print(f'Reverse uroman: "habari yako" -> "{result}"')
    print(f'Length: {len(result)}')
    print(f'Contains space: {" " in result}')
    print()
    
    # Test Arabic
    result2 = r.reverse_romanize_string('salam alaykum', target_script='Arabic')
    print(f'Reverse uroman: "salam alaykum" -> "{result2}"')
    print(f'Length: {len(result2)}')
    print(f'Contains space: {" " in result2}')

if __name__ == "__main__":
    test_reverse_spaces()
