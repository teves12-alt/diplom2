# Статус-коды
STATUS_OK = 200
STATUS_CREATED = 200          # API возвращает 200, а не 201
STATUS_BAD_REQUEST = 400
STATUS_UNAUTHORIZED = 401
STATUS_FORBIDDEN = 403
STATUS_INTERNAL_ERROR = 500

# Тексты ответов
TEXT_USER_EXISTS = "User already exists"
TEXT_MISSING_FIELDS = "Email, password and name are required fields"
TEXT_INVALID_CREDENTIALS = "email or password are incorrect"
TEXT_NO_INGREDIENTS = "Ingredient ids must be provided"
TEXT_INVALID_HASH = "One or more ids provided are not valid ingredient ids"

# Хеши ингредиентов (из ответа GET /api/ingredients)
INGREDIENT_BUN = "61c0c5a71d1f82001bdaaa6d"    # Флюоресцентная булка R2-D3
INGREDIENT_FILLING = "61c0c5a71d1f82001bdaaa6f"  # Биокотлета из марси
INGREDIENT_SAUCE = "61c0c5a71d1f82001bdaaa72"    # Соус традиционный галактический
INGREDIENT_INVALID = "invalid_hash_12345"
