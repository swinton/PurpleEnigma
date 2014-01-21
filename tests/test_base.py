import mock

import unittest

from PurpleEnigma import PurpleEnigma


class TestPurpleEnigma(unittest.TestCase):
    def setUp(self):
        self.enigma_key = "foo" * 8
        self.enigma = PurpleEnigma(key=self.enigma_key)

        self.imposter_key = "bar" * 8
        self.imposter = PurpleEnigma(key=self.imposter_key)

    def test_init(self):
        """
        PurpleEnigma instances are instantiated correctly
        """
        self.assertEqual(self.enigma_key, self.enigma.key)

    def test_encryption1(self):
        """
        Encrypted 'x' does not equal 'x'
        """
        self.assertNotEqual("x", self.enigma.encrypt("x"))

    def test_encryption2(self):
        """
        Encrypted 'x' can be decrypted
        """
        self.assertEqual("x", self.enigma.decrypt(self.enigma.encrypt("x")))

    def test_encryption3(self):
        """
        Encrypted 'x' is different each time
        """
        self.assertNotEqual(self.enigma.encrypt("x"), self.enigma.encrypt("x"))

    def test_encryption4(self):
        """
        An imposter cannot decrypt 'x' without our key
        """
        self.assertNotEqual("x", self.imposter.decrypt(self.enigma.encrypt("x")))

    @mock.patch("PurpleEnigma.base.base64.b64encode")
    @mock.patch("PurpleEnigma.base.Random")
    @mock.patch("PurpleEnigma.base.AES")
    @mock.patch("PurpleEnigma.base.pad")
    def test_encryption5(self, pad, AES, Random, b64encode):
        """
        Test all the things are called as expected when encrypting.
        """
        pad.return_value = "x"
        Random.new.return_value.read.return_value = "y"
        AES.new.return_value.encrypt.return_value = "z"
        AES.block_size = "b"
        AES.MODE_CBC = "m"

        self.enigma.encrypt("x")

        self.assertListEqual(pad.mock_calls, [
            mock.call("x")
        ])
        self.assertListEqual(Random.mock_calls, [
            mock.call.new(),
            mock.call.new().read("b")
        ])
        self.assertListEqual(AES.mock_calls, [
            mock.call.new(self.enigma_key, "m", "y"),
            mock.call.new().encrypt("x")
        ])
        self.assertListEqual(b64encode.mock_calls, [
            mock.call("yz")
        ])

    @mock.patch("PurpleEnigma.base.base64.b64decode")
    @mock.patch("PurpleEnigma.base.AES")
    @mock.patch("PurpleEnigma.base.unpad")
    def test_encryption6(self, unpad, AES, b64decode):
        """
        Test all the things are called as expected when decrypting.
        """
        b64decode.return_value = "x" * 16 + "x"
        AES.new.return_value.decrypt.return_value = "y"
        AES.MODE_CBC = "m"
        unpad.return_value = "z"

        self.enigma.decrypt("x")

        self.assertListEqual(b64decode.mock_calls, [
            mock.call("x")
        ])
        self.assertListEqual(AES.mock_calls, [
            mock.call.new(self.enigma_key, "m", "x" * 16),
            mock.call.new().decrypt("x")
        ])
        self.assertListEqual(unpad.mock_calls, [
            mock.call("y")
        ])
