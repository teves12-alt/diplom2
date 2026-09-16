# Статус-коды
STATUS_OK = 200
STATUS_CREATED = 200
STATUS_BAD_REQUEST = 400
STATUS_UNAUTHORIZED = 401
STATUS_FORBIDDEN = 403
STATUS_INTERNAL_ERROR = 500
MAX_LOG_LENGTH = 250

# Тексты ответов
TEXT_USER_EXISTS = "User already exists"
TEXT_MISSING_FIELDS = "Email, password and name are required fields"
TEXT_INVALID_CREDENTIALS = "email or password are incorrect"
TEXT_NO_INGREDIENTS = "Ingredient ids must be provided"
TEXT_INVALID_HASH = "One or more ids provided are not valid ingredient ids"

# Хеши ингредиентов
INGREDIENT_BUN = "61c0c5a71d1f82001bdaaa6d"
INGREDIENT_FILLING = "61c0c5a71d1f82001bdaaa6f"
INGREDIENT_SAUCE = "61c0c5a71d1f82001bdaaa72"
INGREDIENT_INVALID = "invalid_hash_12345"
