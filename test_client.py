import unittest
from unittest.mock import patch, MagicMock
import client

class TestClient(unittest.TestCase):
    @patch('builtins.input', side_effect=['Toyota'])
    def test_get_user_input_basic(self, mock_input):
        result = client.get_user_input("Qual marca?")
        self.assertEqual(result, 'Toyota')

    @patch('builtins.input', side_effect=['', 'Ford'])
    def test_get_user_input_not_empty(self, mock_input):
        result = client.get_user_input("Qual marca?", allow_empty=False)
        self.assertEqual(result, 'Ford')

    @patch('builtins.input', side_effect=['banana', 'Gasolina'])
    def test_get_user_input_options(self, mock_input):
        result = client.get_user_input("Combustível?", options=['Gasolina', 'Etanol'])
        self.assertEqual(result, 'Gasolina')

    @patch('builtins.input', side_effect=[
        'Toyota', '', '', 'Gasolina', '', 'Manual', '', '', '1.0', '2', '', 'S'
    ])
    def test_collect_filters_simple(self, mock_input):
        filters = client.collect_filters()
        self.assertIn('marca', filters)
        self.assertEqual(filters['marca'], 'Toyota')
        self.assertIn('combustível', filters)
        self.assertEqual(filters['combustível'], 'Gasolina')
        self.assertIn('transmissão', filters)
        self.assertEqual(filters['transmissão'], 'Manual')
        self.assertIn('motor', filters)
        self.assertEqual(filters['motor'], '1.0')
        self.assertIn('portas', filters)
        self.assertEqual(filters['portas'], 2)

    @patch('socket.socket')
    @patch('os.getenv', side_effect=lambda k: 'localhost' if k == 'SERVER_HOST' else '12345')
    def test_send_filters_to_server_success(self, mock_getenv, mock_socket):
        mock_sock_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_sock_instance
        mock_sock_instance.recv.return_value = b'[{"brand":"Toyota","model":"Corolla"}]'
        filters = {'marca': 'Toyota'}
        result = client.send_filters_to_server(filters)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]['brand'], 'Toyota')

    @patch('os.getenv', side_effect=lambda k: 'localhost' if k == 'SERVER_HOST' else '12345')
    def test_send_filters_to_server_env_missing(self, mock_getenv):
        filters = {'marca': 'Toyota'}
        result = client.send_filters_to_server(filters)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
