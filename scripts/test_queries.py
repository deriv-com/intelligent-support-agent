import json
import requests
import sys
import os
import time
from typing import Dict, List
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

def load_sample_queries() -> List[Dict]:
    """Load sample queries from the data file."""
    try:
        with open('data/sample_queries.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{Fore.RED}Error: sample_queries.json not found. Run populate_data.py first.{Style.RESET_ALL}")
        sys.exit(1)

def test_query(query: str, api_url: str = "http://app:8000/query") -> Dict:
    """Send a test query to the API and return the response."""
    try:
        response = requests.post(
            api_url,
            json={"query": query},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error making request: {str(e)}{Style.RESET_ALL}")
        return None

def run_tests():
    """Run test queries and display results."""
    print(f"{Fore.CYAN}Loading sample queries...{Style.RESET_ALL}")
    queries = load_sample_queries()

    print(f"{Fore.CYAN}Testing API responses...{Style.RESET_ALL}\n")

    for i, query_data in enumerate(queries, 1):
        query = query_data["query"]
        expected = query_data["expected_response"]

        print(f"{Fore.YELLOW}Test {i}: {query}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Expected to contain:{Style.RESET_ALL}")
        print(expected.split('\n')[0])  # Print first line of expected response

        response = test_query(query)
        if response:
            print(f"{Fore.GREEN}Actual response:{Style.RESET_ALL}")
            print(response["response"])

            # Check if help center links are included
            if "help.deriv.com/payments" in response["response"].lower():
                print(f"{Fore.GREEN}✓ Contains help center link{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}⚠ No help center link found{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Expected URL format: https://help.deriv.com/payments/...\n{Style.RESET_ALL}")

        print("\n" + "-"*80 + "\n")

def wait_for_api(timeout: int = 60):
    """Wait for the API to become available."""
    print(f"{Fore.CYAN}Waiting for API to be ready...{Style.RESET_ALL}")
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            response = requests.get("http://app:8000/health")
            if response.status_code == 200:
                print(f"{Fore.GREEN}API is ready!{Style.RESET_ALL}")
                return True
        except requests.exceptions.RequestException:
            pass
        print(".", end="", flush=True)
        time.sleep(2)

    print(f"\n{Fore.RED}API did not become ready within {timeout} seconds{Style.RESET_ALL}")
    return False

def main():
    """Main test execution function."""
    print(f"{Fore.CYAN}Payment Support System - Query Tests{Style.RESET_ALL}")
    print("="*50 + "\n")

    try:
        if not wait_for_api():
            sys.exit(1)

        run_tests()
        print(f"{Fore.GREEN}Tests completed successfully!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error during testing: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
