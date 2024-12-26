import json
import os
import time
import requests
from typing import List, Dict
import sys
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.config import Config
from src.vectorstore.vector_store import VectorStore

HELP_CENTER_BASE_URL = "https://help.deriv.com/payments"

def generate_payment_docs() -> List[Dict]:
    """Generate payment documentation with help center links."""
    payment_docs = [
        {
            "title": "Card Payment Declined",
            "content": f"""Common reasons for card payment failures:
            1. Insufficient funds in the account
            2. Card expired or approaching expiration date
            3. Incorrect card details (number, CVV, expiration)
            4. Bank security measures or fraud prevention
            5. Geographic restrictions or international payment blocks
            6. Daily/monthly spending limits reached
            7. Unusual transaction patterns flagged

            Troubleshooting steps:
            1. Verify all card details are entered correctly
            2. Check available balance and spending limits
            3. Contact card issuer to verify transaction blocks
            4. Try alternative payment method if issues persist
            5. Ensure transaction amount is within daily limits
            6. Check if international transactions are enabled

            For detailed instructions, visit: {HELP_CENTER_BASE_URL}/card-payments

            Need immediate assistance? Contact your card issuer or visit our help center: {HELP_CENTER_BASE_URL}/support""",
            "category": "card_payments",
            "help_url": f"{HELP_CENTER_BASE_URL}/card-payments"
        },
        {
            "title": "Bank Transfer Issues",
            "content": f"""Common bank transfer problems:
            1. Incorrect bank details (IBAN, SWIFT code)
            2. Processing delays due to verification
            3. International transfer restrictions
            4. Bank maintenance periods
            5. Regulatory compliance holds

            Resolution steps:
            1. Double-check all bank details
            2. Verify transfer limits and fees
            3. Check compliance requirements
            4. Contact bank support with reference number

            For more details about bank transfers, visit: {HELP_CENTER_BASE_URL}/bank-transfers

            Track your transfer status here: {HELP_CENTER_BASE_URL}/track-transfer""",
            "category": "bank_transfers",
            "help_url": f"{HELP_CENTER_BASE_URL}/bank-transfers"
        },
        {
            "title": "E-Wallet Processing Times",
            "content": f"""E-wallet transfer timeframes:
            1. Internal transfers: Instant
            2. Bank to e-wallet: 1-3 business days
            3. E-wallet to bank: 1-5 business days

            Common delays:
            1. First-time transfers require verification
            2. Large transfers may need additional security checks
            3. Bank processing times vary by country

            Check current processing times: {HELP_CENTER_BASE_URL}/processing-times

            View supported e-wallets: {HELP_CENTER_BASE_URL}/payment-methods""",
            "category": "processing_times",
            "help_url": f"{HELP_CENTER_BASE_URL}/processing-times"
        }
    ]
    return payment_docs

def generate_sample_queries() -> List[Dict]:
    """Generate sample queries and their expected responses."""
    return [
        {
            "query": "Why was my card payment declined?",
            "expected_response": """Your card payment might have been declined for several common reasons:
            1. Insufficient funds
            2. Incorrect card details
            3. Card expiration
            4. Security measures

            Please verify:
            - Your card has sufficient funds
            - All card details are entered correctly
            - Your card hasn't expired

            For more help, visit: {}/card-payments""".format(HELP_CENTER_BASE_URL)
        },
        {
            "query": "How long do bank transfers take?",
            "expected_response": """Bank transfer processing times vary:
            - Domestic transfers: 1-3 business days
            - International transfers: 3-7 business days

            Factors that affect processing time:
            - Bank working hours
            - International holidays
            - Verification requirements

            Track your transfer: {}/track-transfer""".format(HELP_CENTER_BASE_URL)
        },
        {
            "query": "What should I do if my e-wallet transfer is delayed?",
            "expected_response": """If your e-wallet transfer is delayed:
            1. Check your email for verification requests
            2. Verify the transfer amount is within limits
            3. Ensure your account is fully verified

            Normal processing times:
            - Internal transfers: Instant
            - To/From bank: 1-5 business days

            View current status: {}/processing-times""".format(HELP_CENTER_BASE_URL)
        }
    ]

def wait_for_qdrant(timeout: int = 60):
    """Wait for Qdrant to become available."""
    print(f"{Fore.CYAN}Waiting for Qdrant to be ready...{Style.RESET_ALL}")
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            response = requests.get("http://qdrant:6333/collections")
            if response.status_code == 200:
                print(f"{Fore.GREEN}Qdrant is ready!{Style.RESET_ALL}")
                return True
        except requests.exceptions.RequestException:
            pass
        print(".", end="", flush=True)
        time.sleep(2)

    print(f"\n{Fore.RED}Qdrant did not become ready within {timeout} seconds{Style.RESET_ALL}")
    return False

def main():
    """Populate the vector database with payment documentation."""
    try:
        print(f"{Fore.CYAN}Starting data population process...{Style.RESET_ALL}")

        # Wait for Qdrant to be ready
        if not wait_for_qdrant():
            sys.exit(1)

        # Generate documentation
        print(f"{Fore.CYAN}Generating documentation...{Style.RESET_ALL}")
        docs = generate_payment_docs()

        # Save raw docs for reference
        print(f"{Fore.CYAN}Saving documentation files...{Style.RESET_ALL}")
        data_dir = os.path.join('/app', 'data')
        os.makedirs(data_dir, exist_ok=True)

        with open(os.path.join(data_dir, 'payment_docs.json'), 'w') as f:
            json.dump(docs, f, indent=2)

        # Save sample queries
        queries = generate_sample_queries()
        with open(os.path.join(data_dir, 'sample_queries.json'), 'w') as f:
            json.dump(queries, f, indent=2)

        # Initialize vector store and verify connection
        print(f"{Fore.CYAN}Initializing vector store...{Style.RESET_ALL}")
        config = Config()
        vector_store = VectorStore(config)

        # Add documents
        print(f"{Fore.CYAN}Adding documents to vector store...{Style.RESET_ALL}")
        vector_store.add_documents(docs)

        print("Successfully populated vector database with payment documentation")
        print(f"Added {len(docs)} documents")
        print(f"Generated {len(queries)} sample queries")
        print("\nTest the system with these sample queries using:")
        print('curl -X POST http://localhost:8000/query \\')
        print('  -H "Content-Type: application/json" \\')
        print('  -d \'{"query": "Why was my card payment declined?"}\'')

    except Exception as e:
        print(f"Error populating database: {str(e)}")
        raise

if __name__ == "__main__":
    main()
