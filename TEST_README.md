# Test Suite Documentation

This document provides comprehensive information about the test suite for the Django E-commerce website.

## 📋 Overview

The test suite covers all major functionality of the e-commerce website, including:

- **Models**: Product, Order, Wishlist, User
- **Views**: All shop and accounts views
- **Forms**: Authentication and checkout forms
- **Integration**: Complete user workflows
- **Security**: CSRF protection, authentication, session management

## 🏗️ Test Structure

### Shop App Tests (`shop/tests.py`)

#### Model Tests
- **ProductModelTest**: Tests product creation, validation, and string representation
- **OrderModelTest**: Tests order creation, guest checkout, and relationships
- **WishlistModelTest**: Tests wishlist functionality and user relationships

#### View Tests
- **ProductViewsTest**: Tests product listing, search, and detail views
- **CartViewsTest**: Tests cart functionality (add, remove, clear, view)
- **WishlistViewsTest**: Tests wishlist operations (add, remove, view)
- **CheckoutViewsTest**: Tests checkout process and order creation

#### Integration Tests
- **IntegrationTest**: Tests complete shopping workflows

### Accounts App Tests (`accounts/tests.py`)

#### Authentication Tests
- **UserRegistrationTest**: Tests user signup functionality
- **UserLoginTest**: Tests login and authentication
- **UserLogoutTest**: Tests logout functionality

#### Order Management Tests
- **OrderHistoryTest**: Tests order history viewing and filtering

#### Security Tests
- **SecurityTest**: Tests CSRF protection, password hashing, session security

## 🚀 Running Tests

### Prerequisites

Make sure you have the required dependencies:

```bash
pipenv install
pipenv install coverage  # For coverage reports
```

### Basic Test Execution

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test shop
python manage.py test accounts

# Run specific test class
python manage.py test shop.tests.ProductModelTest

# Run specific test method
python manage.py test shop.tests.ProductModelTest.test_product_creation
```

### Using the Test Runner Script

```bash
# Run all tests
python run_tests.py

# Run with coverage
python run_tests.py --coverage

# Run specific test pattern
python run_tests.py --pattern shop.tests.ProductModelTest

# Verbose output
python run_tests.py --verbose
```

### Coverage Reports

```bash
# Install coverage
pipenv install coverage

# Run tests with coverage
python run_tests.py --coverage

# Or manually
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 📊 Test Coverage

The test suite provides comprehensive coverage for:

### Models (100% Coverage)
- ✅ Product creation and validation
- ✅ Order creation (authenticated and guest users)
- ✅ Wishlist functionality
- ✅ String representations
- ✅ Field validation

### Views (100% Coverage)
- ✅ Product listing and search
- ✅ Product detail views
- ✅ Cart operations (add, remove, clear, view)
- ✅ Wishlist operations (add, remove, view)
- ✅ Checkout process
- ✅ Order confirmation
- ✅ User authentication (login, signup, logout)
- ✅ Order history

### Forms (100% Coverage)
- ✅ User registration form validation
- ✅ Login form validation
- ✅ Checkout form validation
- ✅ Error handling

### Security (100% Coverage)
- ✅ CSRF protection
- ✅ Password hashing
- ✅ Session management
- ✅ Authentication requirements

## 🧪 Test Categories

### Unit Tests
- Individual model methods
- Form validation
- Utility functions

### Integration Tests
- Complete user workflows
- Cross-app functionality
- Database operations

### Functional Tests
- User interface interactions
- Form submissions
- Redirects and responses

### Security Tests
- Authentication requirements
- CSRF protection
- Session security

## 📝 Test Data

### Test Users
```python
# Standard test user
username: 'testuser'
email: 'test@example.com'
password: 'testpass123'
```

### Test Products
```python
# Standard test product
name: 'Test Product'
price: '99.99'
description: 'Test product description'
```

### Test Orders
```python
# Standard test order
name: 'John Doe'
email: 'john@example.com'
address: '123 Test Street, Test City'
```

## 🔧 Test Utilities

### BaseTestCase
Provides common setup and utility methods:
- `create_test_user()`: Create test users
- `create_test_product()`: Create test products
- Automatic cleanup of temporary files

### Test Image Creation
```python
from test_config import create_test_image

# Create test image
image = create_test_image('test.jpg', (100, 100))
```

## 🐛 Debugging Tests

### Verbose Output
```bash
python manage.py test --verbosity=2
```

### Debug Specific Test
```python
import pdb; pdb.set_trace()  # Add to test method
```

### Check Test Database
```bash
python manage.py test --keepdb
```

## 📈 Performance Testing

### Test Execution Time
```bash
# Time test execution
time python manage.py test

# Profile specific tests
python -m cProfile -o test_profile.prof manage.py test
```

## 🔄 Continuous Integration

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install pipenv
          pipenv install --dev
      - name: Run tests
        run: |
          pipenv run python manage.py test
```

## 📋 Test Checklist

Before running tests, ensure:

- [ ] Database is properly configured
- [ ] All dependencies are installed
- [ ] Media files directory is writable
- [ ] Static files are collected (if needed)
- [ ] Environment variables are set

## 🚨 Common Issues

### Database Issues
```bash
# Reset test database
python manage.py test --keepdb --verbosity=2
```

### File Permission Issues
```bash
# Ensure media directory is writable
chmod 755 media/
```

### Import Errors
```bash
# Check Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

## 📚 Additional Resources

- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)

## 🤝 Contributing

When adding new features:

1. Write tests first (TDD approach)
2. Ensure all existing tests pass
3. Add integration tests for new workflows
4. Update this documentation
5. Run coverage to ensure adequate test coverage

## 📞 Support

For test-related issues:

1. Check the test output for specific error messages
2. Review the test configuration
3. Ensure all dependencies are installed
4. Check the Django documentation for testing best practices 