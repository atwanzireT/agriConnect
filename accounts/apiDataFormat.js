// POST /api/auth/register/farmer/
const farmer = {
    "email": "farmer@example.com",
    "password": "farmersecure123",
    "password2": "farmersecure123",
    "role": "farmer",
    "phone_number": "+255123456789",
    "location": "Arusha",
    "preferred_language": "sw",
    "farmer_profile": {
        "farm_size": 5.5,
        "farm_size_unit": "acres",
        "expected_harvest_date": "2023-12-15",
        "id_card_number": "12345678",
        "certification": "Organic Certified",
        "years_of_experience": 10
    }
}

// POST /api/auth/register/buyer/
const buyer = {
    "email": "buyer@example.com",
    "password": "buyersecure123",
    "password2": "buyersecure123",
    "role": "buyer",
    "phone_number": "+255123456789",
    "location": "Nairobi",
    "preferred_language": "en",
    "buyer_profile": {
        "business_name": "Fresh Foods Ltd",
        "registration_number": "REG12345",
        "company_type": "supermarket",
        "preferred_products": ["maize", "beans", "potatoes"],
        "delivery_address": "123 Main Street, Nairobi",
        "additional_addresses": ["456 Second Street, Nairobi"],
        "contact_person": "John Doe",
        "contact_phone": "+254712345678",
        "tax_identification": "TAX12345",
        "preferred_communication": "whatsapp"
    }
}

// POST /api/auth/register/
const guest = {
    "email": "user@example.com",
    "password": "securepassword123",
    "password2": "securepassword123",
    "role": "guest",
    "phone_number": "+255123456789",
    "location": "Dar es Salaam",
    "preferred_language": "sw"
}