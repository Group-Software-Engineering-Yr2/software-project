# Create account endpoint

curl -X POST http://127.0.0.1:8000/accounts/register/ \
 -H "Content-Type: application/json" \
 -d '{
"username": "john_doe",
"email": "john@example.com",
"password": "securepassword",
"team_name": "recycle"
}'

# Login endpoint

curl -X POST http://127.0.0.1:8000/accounts/login/ \
 -H "Content-Type: application/json" \
 -d '{
"username": "john_doe",
"password": "securepassword"
}'

# Update profile

Ensure auth token matches the user

curl -X PUT http://127.0.0.1:8000/accounts/profile/update/ \
 -H "Content-Type: application/json" \
 -H "Authorization: Token 417548f7d6e4e6ce12590f20e309ce50ab472a29" \
 -d '{
"wrapper_count": 10,
"pack_count": 5,
}'

# Get profile

curl -X GET http://127.0.0.1:8000/accounts/profile/ \
 -H "Authorization: Token 417548f7d6e4e6ce12590f20e309ce50ab472a29"
