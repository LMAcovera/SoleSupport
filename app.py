from flask import Flask, render_template, request, jsonify, session
import random
import time
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session management

# Enhanced responses database with categories and context
responses = {
    "greeting": {
        "patterns": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "yo", "hola", "kumusta", "greetings", "mabuhay", "magandang umaga", "magandang hapon", "magandang gabi", "good day", "howdy", "what's up", "sup", "aloha", "namaste", "magandang tanghali", "magandang araw po", "kamusta po", "good evening po", "hello po", "hi po"],
        "responses": [
            "Welcome to SoleSupport! Looking for any particular type of shoes today? We have great deals starting at ₱2,499!",
            "Hi there! Ready to help you find your perfect fit. Our latest collection just arrived!",
            "Magandang araw! Whether it's running, casual, or formal shoes, I'm here to help!",
            "Magandang araw po! How can I assist you with your shoe shopping today? We have exciting deals waiting for you!",
            "Hello! Looking for the perfect pair? We've got everything from casual to athletic shoes. What's your style?",
            "Welcome! Our latest collection just arrived with prices starting at ₱2,499. What kind of shoes are you looking for today?"
        ]
    },
    "product_inquiry": {
        "patterns": ["price", "cost", "how much", "sneakers", "shoes", "available", "stock", "magkano", "presyo", "sale", "discount", "affordable", "cheap", "expensive", "budget", "high-end", "premium", "quality", "brand new", "original", "authentic", "pabili", "bili", "purchase", "buy", "order", "get", "shop", "sapatos", "tsinelas", "rubber shoes", "basketball shoes", "limited edition", "signature shoes", "branded", "original ba", "legit check", "authentic check", "genuine", "fake", "class a", "class triple a", "imitation", "copy", "replica"],
        "responses": [
            "I'd be happy to help you find the right shoes. Our prices range from ₱2,499 to ₱15,999. What style are you looking for?",
            "We have shoes for every budget! Casual shoes start at ₱2,499, while premium models go up to ₱15,999. What's your preferred style?",
            "I can help you find the perfect pair. Are you looking for athletic shoes (₱3,499+), casual (₱2,499+), or formal shoes (₱4,499+)?"
        ]
    },
    "size_guide": {
        "patterns": ["size", "fit", "measurement", "too big", "too small", "sizing", "measure", "foot size", "shoe size", "us size", "uk size", "euro size", "japanese size", "kids size", "mens size", "womens size", "unisex size", "conversion", "chart", "malaki", "maliit", "masikip", "maluwag", "tight", "loose", "half size", "size up", "size down", "true to size", "tts", "wide feet", "narrow feet", "arch support", "foot width", "size chart", "conversion table", "measure feet"],
        "responses": [
            "Here's our size guide to help you find your perfect fit. You can measure your foot length in centimeters and compare with the chart. Would you like help with the measurements?",
            "Let me show you our size guide. Remember to measure your feet in the evening when they're at their largest. Need any help with the measurements?",
            "Here's our size guide. For the best fit, measure both feet and use the larger measurement. Would you like more specific sizing advice?",
            "For wide feet, we recommend going half a size up. Would you like to see our wide-fit collection?",
            "Different brands may fit differently. Let me help you find the right size. What brand are you currently wearing?",
            "We have a comprehensive size guide with width measurements. Would you like me to show you how to measure your feet properly?"
        ]
    },
    "running_shoes": {
        "patterns": ["running", "jog", "marathon", "athletic", "sports"],
        "responses": [
            "Our running collection includes shoes for all levels. What type of running do you do?",
            "We have shoes for trail, road, and track running. Which surface do you usually run on?",
            "For running shoes, we'll need to consider your gait type. Do you know if you pronate?"
        ]
    },
    "technical_support": {
        "patterns": ["broken", "not working", "error", "problem", "issue", "help", "fix"],
        "responses": [
            "I understand you're experiencing technical difficulties. Could you describe the issue in more detail?",
            "I'm here to help resolve your technical issue. When did this problem start?",
            "Let's troubleshoot this together. Could you tell me what error messages you're seeing?"
        ]
    },
    "order_status": {
        "patterns": ["order", "tracking", "shipping", "delivery", "package", "arrive"],
        "responses": [
            "I can help you track your order. Could you provide your order number?",
            "To check your order status, I'll need your order reference number. Do you have it handy?",
            "I'll be happy to help you with your order status. Could you share your order details?"
        ]
    },
    "refund": {
        "patterns": ["refund", "return", "money back", "cancel order"],
        "responses": [
            "I can assist you with the refund process. Have you already initiated a return?",
            "I understand you're looking for a refund. Could you tell me more about your order?",
            "Let me help you with your refund request. What's the reason for the return?"
        ]
    },
    "complaint": {
        "patterns": ["complaint", "unhappy", "disappointed", "frustrated", "angry", "poor service"],
        "responses": [
            "I'm sorry to hear about your experience. Could you tell me more about what happened?",
            "I apologize for any inconvenience. Please share more details so I can better assist you.",
            "Your satisfaction is important to us. Let me help address your concerns."
        ]
    },
    "appreciation": {
        "patterns": ["thank", "thanks", "appreciate", "grateful", "good job"],
        "responses": [
            "You're welcome! Is there anything else I can help you with?",
            "Thank you for your kind words! Don't hesitate to reach out if you need further assistance.",
            "I'm glad I could help! Let me know if you have any other questions."
        ]
    },
    "goodbye": {
        "patterns": ["bye", "goodbye", "see you", "farewell"],
        "responses": [
            "Thank you for chatting with us today! Have a great day!",
            "Goodbye! Feel free to return if you need any further assistance.",
            "Thanks for reaching out! Don't hesitate to contact us again if needed."
        ]
    },
    "payment_issues": {
        "patterns": ["payment", "card declined", "transaction", "billing", "charge", "pay", "checkout", "gcash", "paymaya", "credit card", "debit card", "cash on delivery", "cod", "bank transfer", "online payment", "payment failed", "payment error", "refund", "double charge", "bayad", "payment method", "mode of payment", "installment", "credit card declined", "payment failed", "transaction failed", "payment error", "payment not going through", "payment pending", "payment verification", "payment confirmation", "payment receipt", "proof of payment", "payment screenshot"],
        "responses": [
            "I can help you with payment-related issues. What specific problem are you experiencing?",
            "Let me assist you with your payment concern. Could you provide more details about the issue?",
            "I'll help resolve your payment problem. Have you received any error messages during checkout?",
            "We offer various payment methods including installment options. Would you like to know about our 0% interest plans?",
            "For failed transactions, please wait 24 hours for automatic reversal. Would you like to try an alternative payment method?",
            "We can assist with payment verification. Could you provide your order number and payment reference?"
        ]
    },
    "account_support": {
        "patterns": ["login", "password", "account", "sign in", "register", "forgot", "reset", "email"],
        "responses": [
            "I can help you with your account. What specific issue are you experiencing?",
            "Let me assist you with your account. Could you specify if this is about login, registration, or password reset?",
            "I'll help you with your account access. What seems to be the problem?"
        ]
    },
    "warranty": {
        "patterns": ["warranty", "guarantee", "coverage", "repair", "replace", "damaged"],
        "responses": [
            "I can help you with warranty information. Could you specify which product you're inquiring about?",
            "Let me check the warranty coverage for you. Do you have your product serial number?",
            "I'll assist you with your warranty claim. When did you purchase the product?"
        ]
    },
    "shipping_info": {
        "patterns": ["shipping cost", "delivery time", "international", "shipping method", "express", "standard shipping"],
        "responses": [
            "I can provide shipping information. Which country are you shipping to?",
            "Let me help you with shipping details. Are you interested in standard or express delivery?",
            "I'll explain our shipping options. Where would you like the item shipped to?"
        ]
    },
    "promotions": {
        "patterns": ["discount", "coupon", "promo", "code", "sale", "offer", "deal"],
        "responses": [
            "I can help you with promotional offers. Are you looking for any specific product discounts?",
            "Let me check our current promotions for you. Which products are you interested in?",
            "I'll help you find the best deals. What items are you planning to purchase?"
        ]
    },
    "product_comparison": {
        "patterns": ["compare", "difference", "better", "which one", "recommend", "suggestion"],
        "responses": [
            "I can help you compare products. Which items would you like to know more about?",
            "Let me assist you in choosing the right product. What features are most important to you?",
            "I'll help you make an informed decision. What's your primary use case for the product?"
        ]
    },
    "store_location": {
        "patterns": ["store", "location", "address", "nearest", "shop", "outlet", "branch", "where", "directions", "how to get there", "landmark", "map", "saan", "lugar", "tindahan", "building", "mall", "street", "walking distance", "commute", "parking", "physical store", "branch location", "store hours", "opening hours", "closing time", "business hours", "open today", "open tomorrow", "weekend hours", "holiday hours", "parking space", "parking area", "how to commute", "directions", "sakay", "jeep route", "bus route"],
        "responses": [
            "Our store is located at P. Guevara Street, Poblacion, Santa Cruz, Laguna. We're open Monday to Sunday, 9:00 AM to 8:00 PM.",
            "You can visit us at our store in Santa Cruz, Laguna (P. Guevara Street, Poblacion). We're open daily!",
            "Come visit our store at P. Guevara Street, Poblacion, Santa Cruz, Laguna. We're here to serve you every day from 9 AM to 8 PM!",
            "Our store is open daily from 9 AM to 8 PM, including weekends and most holidays. We're located at P. Guevara Street, near the plaza. Need directions?",
            "We have free parking space for customers. Our store is easily accessible by public transport. Would you like specific commute instructions?",
            "You can find us at P. Guevara Street, Santa Cruz, Laguna. We're the building with the big shoe display. Need landmarks for easier navigation?"
        ]
    },
    "bulk_order": {
        "patterns": ["bulk", "wholesale", "business", "quantity", "corporate", "large order"],
        "responses": [
            "I can assist with bulk orders. What quantities are you looking to purchase?",
            "Let me help you with your wholesale inquiry. Are you ordering for a business?",
            "I'll provide information about bulk pricing. What products are you interested in?"
        ]
    },
    "technical_specs": {
        "patterns": ["specifications", "specs", "details", "features", "dimensions", "compatibility"],
        "responses": [
            "I can provide technical specifications. Which product would you like to know more about?",
            "Let me help you with product details. What specific information are you looking for?",
            "I'll share the technical information. Which aspects of the product interest you most?"
        ]
    },
    "feedback": {
        "patterns": ["suggest", "feedback", "improve", "review", "rating", "experience"],
        "responses": [
            "We value your feedback. What suggestions do you have for improvement?",
            "Thank you for sharing your thoughts. Could you tell us more about your experience?",
            "Your feedback helps us improve. What specific aspects would you like to comment on?"
        ]
    },
    "latest_release": {
        "patterns": ["latest release", "new arrival", "latest", "new shoe", "gt cut", "show me the latest release", "what's new", "newest", "just arrived", "fresh", "recent", "upcoming", "drop", "launch", "release date", "pre-order", "restock", "available now"],
        "responses": [
            "[SHOW_PRODUCT]Check out the new GT Cut 2: Price: ₱2,199 Sizes Available: UK 39-46 This is our latest basketball performance shoe.",
            "[SHOW_PRODUCT]The GT Cut 2 just dropped! Price: ₱2,199 Available in UK sizes 39-46",
            "[SHOW_PRODUCT]Here's our latest release - The GT Cut 2. Price: ₱2,199 Available Sizes: UK 39-46"
        ]
    },
    "rejection": {
        "patterns": ["no", "nope", "nah", "not really", "pass", "nevermind", "nothing", "wag na", "ayoko", "hindi", "no thanks", "not interested", "skip", "of course not", "definitely not"],
        "responses": [
            "Alright, no problem! Let me know if you need anything else.",
            "That's fine! Feel free to ask about something else.",
            "No worries! I'm here if you need other assistance.",
            "Okay! Is there perhaps something else you'd like to know about?",
            "Got it! Don't hesitate to ask if you have other questions."
        ]
    },
    "confirmation": {
        "patterns": ["yes", "yeah", "sure", "okay", "of course", "definitely", "absolutely", "oo", "sige", "why not", "go ahead", "proceed", "continue", "that's right", "correct", "exactly", "i do", "i am", "i would", "please"],
        "responses": [
            "Great! Let me help you with that. What specific details would you like to know?",
            "Excellent! I'll guide you through the process. What's your preference?",
            "Perfect! I'll be happy to assist you further. Could you provide more details?",
            "Wonderful! Let's proceed with your request. What would you like to know first?",
            "Alright! I'll help you with that right away. What additional information do you need?"
        ]
    },
    "what_is_your_price_range": {
        "patterns": ["What is your price range?", "what is your price range?", "Price Range?", "price range?"],
        "responses": [
            "Our shoes are available in different price ranges:\n- Casual shoes: ₱2,499 - ₱4,999\n- Athletic shoes: ₱3,499 - ₱8,999\n- Premium collection: ₱9,999 - ₱15,999\nWhat's your preferred budget?"
        ]
    },
    "show_me_latest_release": {
        "patterns": ["Show me the latest release", "show me the latest release"],
        "responses": [
            "[SHOW_PRODUCT]Check out the new GT Cut 2: Price: ₱2,199 Sizes Available: UK 39-46 This is our latest basketball performance shoe."
        ]
    },
    "where_is_store_located": {
        "patterns": [
            "Where is your store located?",
            "where is your store located?",
            "Where is your store located",
            "where is your store located",
            "store location",
            "Store location",
            "Store Location",
            "store Location"
        ],
        "responses": [
            "Our store is located at P. Guevara Street, Poblacion, Santa Cruz, Laguna. We're open Monday to Sunday, 9:00 AM to 8:00 PM.",
            "You can find us at P. Guevara Street, Santa Cruz, Laguna. We're the building with the big shoe display. Need landmarks for easier navigation?",
            "Visit us at P. Guevara Street, Poblacion, Santa Cruz, Laguna. We're open daily from 9 AM to 8 PM!"
        ]
    },
    "size_guide_button": {
        "patterns": ["Size guide", "size guide"],
        "responses": [
            "Here's our size guide to help you find your perfect fit. You can measure your foot length in centimeters and compare with the chart. Would you like help with the measurements?"
        ]
    }
}

# Add follow-up responses
follow_up_responses = {
    "product_inquiry": {
        "shoe_type": {
            "patterns": ["running", "casual", "formal", "sports", "sneakers", "basketball", "walking", "hiking", "training", "gym", "lifestyle", "limited edition", "signature", "collaboration", "custom", "personalized"],
            "responses": {
                "running": {
                    "general": "Our running shoes range from ₱3,499 to ₱8,999. Do you prefer road or trail running?",
                    "features": {
                        "cushioning": "Our max cushioning models start at ₱4,999",
                        "stability": "Stability shoes for overpronation from ₱5,499",
                        "lightweight": "Racing shoes starting at ₱6,499"
                    }
                },
                "sneakers": {
                    "general": "Our sneaker collection starts at ₱2,499. Are you looking for lifestyle or athletic sneakers?",
                    "collections": {
                        "lifestyle": "Urban collection starting at ₱2,999",
                        "limited": "Exclusive limited editions from ₱7,499",
                        "classic": "Classic styles available from ₱2,499"
                    },
                    "formal": {
                        "general": "Our formal shoes start at ₱4,499. We have both leather and synthetic options.",
                        "collections": {
                            "leather": "Genuine leather shoes from ₱5,999",
                            "synthetic": "Quality synthetic formal shoes from ₱4,499",
                            "premium": "Premium leather collection from ₱8,999"
                        }
                    }
                }
            }
        }
    },
    "technical_support": {
        "device_mentioned": {
            "patterns": ["laptop", "phone", "tablet", "watch", "headphones", "tv", "printer", "console"],
            "common_issues": {
                "laptop": {
                    "not turning on": [
                        "Let's try these steps:",
                        "1. Hold power button for 30 seconds",
                        "2. Remove battery if possible",
                        "3. Connect to power directly",
                        "Has this happened before?"
                    ],
                    "slow performance": [
                        "Common causes of slow performance:",
                        "1. Low disk space",
                        "2. Too many background programs",
                        "3. Outdated drivers",
                        "Would you like help checking these?"
                    ]
                },
                "tv": {
                    "no picture": [
                        "Let's troubleshoot:",
                        "1. Check input source",
                        "2. Verify cable connections",
                        "3. Power cycle the TV",
                        "Which step would you like to try first?"
                    ],
                    "poor quality": [
                        "For picture quality issues:",
                        "1. Check TV settings",
                        "2. Verify input signal",
                        "3. Update TV firmware",
                        "Shall we start with the settings?"
                    ]
                }
            }
        }
    },
    "shipping_info": {
        "location_mentioned": {
            "domestic": {
                "standard": "Standard shipping within Metro Manila takes 3-5 days (₱99)",
                "express": "Express shipping next-day delivery (₱199)",
                "free": "Free shipping for orders over ₱3,000",
                "provincial": "Provincial delivery 5-7 days (₱199)"
            },
            "international": {
                "standard": "International shipping takes 7-14 business days (₱1,499+)",
                "express": "International express 3-5 days (₱2,499+)",
                "restrictions": "Some locations may have additional fees"
            }
        }
    },
    "warranty": {
        "product_type": {
            "electronics": "Electronics come with a 1-year standard warranty",
            "appliances": "Appliances include a 2-year manufacturer warranty",
            "premium": "Premium products have extended 3-year warranty options"
        },
        "claim_process": [
            "To process a warranty claim:",
            "1. Provide proof of purchase",
            "2. Describe the issue",
            "3. Get return authorization",
            "Would you like to start a claim now?"
        ]
    },
    "promotions": {
        "current_deals": [
            "Buy 1 Get 1 50% OFF on selected styles",
            "₱500 OFF on orders above ₱5,000",
            "Free socks with every shoe purchase",
            "Student discount: 10% OFF with valid ID"
        ]
    },
    "size_guide": {
        "measurement_help": {
            "patterns": ["yes", "sure", "okay", "help", "how", "guide me"],
            "responses": [
                "Here's how to measure your foot:\n1. Stand on a piece of paper\n2. Mark the longest point of your foot\n3. Measure the length in centimeters\nWould you like to see our size conversion chart?",
                "To get the perfect fit:\n1. Measure in the evening (feet swell during day)\n2. Wear your usual socks\n3. Measure both feet\nShall I show you the size chart?",
                "Follow these steps:\n1. Place foot firmly on paper\n2. Mark heel and longest toe\n3. Measure length in cm\nWould you like to see our size recommendations?"
            ]
        }
    },
    "store_location": {
        "directions": {
            "patterns": ["yes", "how", "directions", "commute", "landmark"],
            "responses": [
                "From Santa Cruz proper:\n1. Head to P. Guevara Street\n2. Look for the town plaza\n3. We're beside BPI Bank\nWould you like public transportation directions?",
                "Landmarks near us:\n- Town Plaza\n- BPI Bank\n- Santa Cruz Church\nWould you like our contact number for easier navigation?",
                "We're accessible via:\n- Jeep from town proper\n- Tricycle from any point\n- Walking distance from plaza\nNeed more specific directions?"
            ]
        }
    },
    "payment_issues": {
        "payment_method": {
            "patterns": ["yes", "how", "methods", "available"],
            "responses": [
                "We accept:\n1. Cash/Card on delivery\n2. GCash\n3. PayMaya\n4. Credit/Debit Cards\nWhich payment method would you prefer?",
                "Available payment options:\n- Online banking\n- E-wallets (GCash/PayMaya)\n- Cash on delivery\n- Credit/Debit cards\nWhich would you like to use?",
                "Our payment methods include:\n- Digital wallets\n- Bank transfer\n- Cards\n- Cash on delivery\nWould you like details about a specific method?"
            ]
        }
    }
}

def get_context_aware_response(message, context=None):
    message = message.lower()
    
    if context and context.get('category') and context.get('awaiting_confirmation'):
        if any(pattern in message for pattern in responses["confirmation"]["patterns"]):
            category = context['category']
            if category in follow_up_responses:
                for sub_category in follow_up_responses[category]:
                    return random.choice(follow_up_responses[category][sub_category]["responses"])
    
    if any(pattern in message.lower() for pattern in responses["latest_release"]["patterns"]):
        if context is not None:
            context['category'] = 'latest_release'
        return random.choice(responses["latest_release"]["responses"])
    
    if context and context.get('category'):
        category = context['category']
        
        if category == 'product_inquiry':
            for product in follow_up_responses['product_inquiry']['shoe_type']['patterns']:
                if product in message:
                    return follow_up_responses['product_inquiry']['shoe_type']['responses'][product]
        
        elif category == 'technical_support':
            for device in follow_up_responses['technical_support']['device_mentioned']['patterns']:
                if device in message:
                    issues = follow_up_responses['technical_support']['device_mentioned']['common_issues'][device]
                    return f"Common {device} issues include: {', '.join(issues)}. Which issue are you experiencing?"
        
        elif category == 'order_status':
            order_match = re.search(r'\b[A-Z0-9]{6,10}\b', message.upper())
            if order_match:
                order_number = order_match.group(0)
                statuses = ['in transit', 'being processed', 'out for delivery', 'shipped']
                dates = ['tomorrow', 'next Monday', 'by end of week', 'in 2-3 business days']
                response = random.choice(follow_up_responses['order_status']['order_number']['responses'])
                return response.format(
                    order_number=order_number,
                    status=random.choice(statuses),
                    date=random.choice(dates)
                )
    
    for category, data in responses.items():
        for pattern in data["patterns"]:
            if pattern in message:
                if context is not None:
                    context['category'] = category
                return random.choice(data["responses"])
    
    if context is not None:
        context['awaiting_confirmation'] = any(
            question_marker in response.lower() 
            for response in responses[context.get('category', '')].get("responses", [])
            for question_marker in ["would you like", "need", "shall", "could you"]
        )
    
    return random.choice([
        "I understand. Could you please provide more details so I can better assist you?",
        "I want to make sure I help you correctly. Can you elaborate on that?",
        "Could you give me more specific information about your request?"
    ])

@app.route('/')
def home():
    session['context'] = {}
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data.get('message', '')
    context = session.get('context', {})
    time.sleep(0.5)
    response = get_context_aware_response(message, context)
    session['context'] = context
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True) 