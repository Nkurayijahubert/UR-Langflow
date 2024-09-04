import unittest
from unittest.mock import patch, MagicMock
from app.langflow_integration.langflow_config import run_flow

class TestRunFlow(unittest.TestCase):
    @patch('app.langflow_integration.langflow_config.run_flow_from_json')
    def test_run_flow_valid_input(self, mock_run_flow_from_json):
        # Setup
        mock_run_flow_from_json.return_value = "Flow result"
        input_data = "Hello, world!"

        # Call function
        result = run_flow(input_data)

        # Assert
        self.assertEqual(result, "Flow result")
        mock_run_flow_from_json.assert_called_once()
        call_args = mock_run_flow_from_json.call_args[1]  # Get keyword arguments
        self.assertEqual(call_args['input_value'], input_data)
        self.assertEqual(call_args['flow'], 'test_rag.json')
        self.assertTrue(call_args['fallback_to_env_vars'])

    @patch('app.langflow_integration.langflow_config.run_flow_from_json')
    def test_run_flow_invalid_input(self, mock_run_flow_from_json):
        # Setup
        mock_run_flow_from_json.side_effect = Exception("Invalid input")
        input_data = None

        # Call function
        result = run_flow(input_data)

        # Assert
        self.assertIn("Error running flow", result)
        self.assertIn("Invalid input", result)
        mock_run_flow_from_json.assert_called_once()
        call_args = mock_run_flow_from_json.call_args[1]  # Get keyword arguments
        self.assertEqual(call_args['input_value'], 'None')  # Note: None is converted to string
        self.assertEqual(call_args['flow'], 'test_rag.json')
        self.assertTrue(call_args['fallback_to_env_vars'])

if __name__ == '__main__':
    unittest.main()