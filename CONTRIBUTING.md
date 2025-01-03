# Contributing Guide

This document outlines the best practices and guidelines for contributing to the project.

## Code Modification Best Practices

### General Principles
1. Follow Test-Driven Development (TDD)
2. Make targeted, minimal changes
3. Preserve existing code structure
4. Maintain consistent code style

### Code Modification Process

1. **Targeted Updates First**
   - Always attempt targeted updates for small changes
   - Use minimal unique pattern matching
   - Modify only specific functions/sections that need changes
   - Preserve all other code exactly as is

2. **Update Strategy**
   ```
   For single-line changes:
   1. Try with minimal context
   2. If fails, try once more with expanded context
   
   For function changes:
   1. Try with minimal pattern matching
   2. If fails, try using function boundaries
   ```

3. **When to Use Complete Rewrites**
   - Only after both targeted update attempts fail
   - For complex changes affecting multiple locations
   - When explicitly informing about the rewrite approach

### Test-Driven Development (TDD)

1. **Write Test First**
   ```python
   # Example: Adding new payment validation
   def test_validate_payment_amount():
       payment = PaymentRequest(amount=-100)
       with pytest.raises(ValidationError):
           validate_payment_amount(payment)
   ```

2. **Run Test (Should Fail)**
   ```bash
   docker compose --profile test run test pytest -k test_validate_payment_amount
   ```

3. **Implement Feature**
   ```python
   def validate_payment_amount(payment: PaymentRequest) -> None:
       if payment.amount <= 0:
           raise ValidationError("Payment amount must be positive")
   ```

4. **Run Test Again (Should Pass)**
   ```bash
   docker compose --profile test run test pytest -k test_validate_payment_amount
   ```

### Testing Guidelines

1. **Test Organization**
   ```
   tests/
   ├── unit/              # Unit tests
   │   ├── test_chain.py
   │   └── test_vector_store.py
   ├── integration/       # Integration tests
   │   └── test_api.py
   └── conftest.py       # Shared fixtures
   ```

2. **Test Categories**
   - Unit Tests: Test individual components
   - Integration Tests: Test component interactions
   - End-to-End Tests: Test complete workflows

3. **Test Naming Convention**
   ```python
   # Format: test_<component>_<scenario>_<expected_result>
   def test_payment_validation_negative_amount_raises_error():
       pass

   def test_vector_search_empty_query_returns_empty_list():
       pass
   ```

4. **Test Coverage Requirements**
   - Minimum 80% code coverage
   - 100% coverage for critical paths
   - All edge cases must be tested

### Code Style

1. **Python Style**
   - Follow PEP 8
   - Use type hints
   - Maximum line length: 88 characters (black default)
   - Use docstrings for all public functions

2. **Example**
   ```python
   from typing import List, Optional

   def process_payment(
       amount: float,
       currency: str,
       description: Optional[str] = None
   ) -> List[dict]:
       """
       Process a payment transaction.

       Args:
           amount: Payment amount
           currency: Three-letter currency code
           description: Optional payment description

       Returns:
           List of processed transaction details

       Raises:
           ValidationError: If amount is invalid
           CurrencyError: If currency is not supported
       """
       pass
   ```

### Commit Guidelines

1. **Commit Message Format**
   ```
   <type>(<scope>): <subject>

   <body>

   <footer>
   ```

2. **Types**
   - feat: New feature
   - fix: Bug fix
   - refactor: Code change that neither fixes a bug nor adds a feature
   - test: Adding missing tests
   - docs: Documentation only changes

3. **Example**
   ```
   feat(payment): add validation for negative amounts

   - Add PaymentValidator class
   - Implement amount validation
   - Add unit tests

   Closes #123
   ```

### Pull Request Process

1. **Before Submitting**
   - Write/update tests
   - Run full test suite
   - Update documentation
   - Follow code modification guidelines

2. **PR Template**
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Test Coverage
   - [ ] Unit tests added/updated
   - [ ] Integration tests added/updated
   - [ ] All tests passing

   ## Documentation
   - [ ] README updated
   - [ ] Docstrings updated
   - [ ] Comments added for complex logic
   ```

### Development Setup

1. **Local Environment**
   ```bash
   # Clone repository
   git clone <repo-url>
   cd intelligent-support-agent

   # Set up environment files
   cp .env.app.example .env.app
   cp .env.postgres.example .env.postgres
   cp .env.redis.example .env.redis
   cp .env.qdrant.example .env.qdrant

   # Start services
   docker compose up -d

   # Run tests
   docker compose --profile test up test
   ```

2. **Pre-commit Checks**
   ```bash
   # Run formatter
   docker compose exec app black .

   # Run linter
   docker compose exec app flake8

   # Run type checker
   docker compose exec app mypy .

   # Run tests
   docker compose --profile test up test
   ```

### Documentation Requirements

1. **Code Documentation**
   - All public functions must have docstrings
   - Complex logic must have inline comments
   - Update README for new features
   - Keep architecture diagrams current

2. **Example Documentation**
   ```python
   class PaymentProcessor:
       """
       Handles payment processing and validation.

       Attributes:
           supported_currencies: List of supported currency codes
           max_amount: Maximum allowed payment amount

       Example:
           >>> processor = PaymentProcessor()
           >>> result = processor.process_payment(100, "USD")
       """

       def validate_amount(self, amount: float) -> None:
           """
           Validate payment amount.

           Args:
               amount: Payment amount to validate

           Raises:
               ValidationError: If amount is negative or exceeds maximum
           """
           # Implementation
   ```

Remember:
- Speed and efficiency are priorities
- Preserve existing code structure
- Pattern matching must be precise and unique
- Respect existing code style
- Always follow TDD approach
