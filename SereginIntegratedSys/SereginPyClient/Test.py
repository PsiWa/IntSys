import unittest
import message
from message import Message as msg

class TestMessageMethods(unittest.TestCase):

    def test_constructor_defaults(self):
        ms = msg(0, 0)
        self.assertEqual("",ms.Data)
        self.assertEqual(message.MT_DATA,ms.Header.hactioncode)

if __name__ == '__main__':
    unittest.main()