import unittest
import threading
import time
import client
import server

class TestIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start the server in a background thread
        cls.server_thread = threading.Thread(target=server.start_server, daemon=True)
        cls.server_thread.start()
        time.sleep(1)  # Give server time to start

    def test_client_server_interaction(self):
        filters = {'marca': 'Toyota'}
        result = client.send_filters_to_server(filters)
        self.assertIsInstance(result, list)

    def test_client_server_full_filters(self):
        filters = {
            'quilometragem': 10000
        }
        result = client.send_filters_to_server(filters)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

if __name__ == '__main__':
    unittest.main()