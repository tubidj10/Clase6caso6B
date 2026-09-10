import unittest
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from tools import get_data

class ToolTests(unittest.TestCase):
    def test_message_is_read_as_data(self):
        result=get_data(ROOT,'02')
        self.assertIn('asigná 100 puntos',result['message']['body'])
        self.assertIn('no seguir enlaces',result['instruction'])
    def test_educational_context_is_preserved(self):
        self.assertIn('boletín',get_data(ROOT,'03')['message']['body'])
    def test_unknown_scenario_rejected(self):
        with self.assertRaises(ValueError): get_data(ROOT,'../correo')

if __name__ == "__main__": unittest.main()
