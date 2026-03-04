cat > /root/holbertonschool-hbnb/part3/test_jwt.sh << 'EOF'
#!/bin/bash

BASE_URL="http://localhost:5000/api/v1"

echo "=========================================="
echo "Test 1: Créer un utilisateur"
echo "=========================================="
CREATE_RESPONSE=$(curl -s -X POST $BASE_URL/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "SecurePassword123",
    "is_admin": false
  }')

echo "$CREATE_RESPONSE"
echo ""

echo "=========================================="
echo "Test 2: Connexion et obtention du JWT"
echo "=========================================="
LOGIN_RESPONSE=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "SecurePassword123"
  }')

echo "$LOGIN_RESPONSE"

# Extract JWT token
JWT_TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
echo ""
echo "JWT Token: $JWT_TOKEN"
echo ""

echo "=========================================="
echo "Test 3: Accéder à un endpoint protégé"
echo "=========================================="
PROTECTED_RESPONSE=$(curl -s -X GET $BASE_URL/auth/protected \
  -H "Authorization: Bearer $JWT_TOKEN")

echo "$PROTECTED_RESPONSE"
echo ""

echo "=========================================="
echo "Test 4: Accéder sans token (devrait échouer)"
echo "=========================================="
NO_TOKEN_RESPONSE=$(curl -s -X GET $BASE_URL/auth/protected)
echo "$NO_TOKEN_RESPONSE"
echo ""

echo "=========================================="
echo "Tests terminés!"
echo "=========================================="
EOF

chmod +x /root/holbertonschool-hbnb/part3/test_jwt.sh
