import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import spacy
import json
import random
from datetime import datetime
from typing import List, Dict
import os

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    messagebox.showerror("Error", "spaCy model 'en_core_web_sm' not found. Please install it:\npython -m spacy download en_core_web_sm")
    exit()

# Load product database
def load_products():
    try:
        with open('products.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", "products.json file not found!")
        return {}

# Extract nouns from user input using NLP
def extract_items(text: str) -> List[str]:
    doc = nlp(text.lower())
    items = []
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop and not token.is_space:
            items.append(token.lemma_)  # Use lemma for better matching
    return list(set(items))

# Improved item matching function
def find_item_in_database(item: str, products_db: Dict) -> Dict:
    """Find item in database with better matching logic"""
    item = item.lower().strip()
    
    # Direct exact match
    for category, data in products_db.items():
        if item in data["items"]:
            return {
                "shelf": data["shelf"],
                "category": category
            }
    
    # Partial matching and common variations
    for category, data in products_db.items():
        for db_item in data["items"]:
            # Check if item is contained in database item or vice versa
            if item in db_item or db_item in item:
                return {
                    "shelf": data["shelf"],
                    "category": category
                }
            
            # Handle common plural/singular variations
            if item + 's' == db_item or item == db_item + 's':
                return {
                    "shelf": data["shelf"],
                    "category": category
                }
    
    return {
        "shelf": "Not found in store",
        "category": "unknown"
    }

# Find shelf locations with improved matching
def find_shelves(items: List[str], products_db: Dict) -> Dict[str, Dict]:
    result = {}
    for item in items:
        result[item] = find_item_in_database(item, products_db)
    return result

class SupermarketChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🛒 Smart Supermarket Assistant")
        self.root.geometry("900x750")
        self.root.minsize(700, 600)
        
        # Enhanced styling
        self.root.configure(bg="#f0f0f0")
        
        self.products_db = load_products()
        self.shopping_list = {}  # Store current shopping list
        self.conversation = []   # Store conversation history
        
        # Create GUI elements
        self.create_widgets()
        
        # Initial greeting
        self.initial_greeting()

    def create_widgets(self):
        # Main container with gradient background
        main_container = tk.Frame(self.root, bg="#f0f0f0")
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Enhanced Header with gradient effect
        header_frame = tk.Frame(main_container, height=80, bg="#2E7D32")
        header_frame.pack(fill=tk.X, pady=(0, 15))
        header_frame.pack_propagate(False)
        
        # Title with store icon
        title_container = tk.Frame(header_frame, bg="#2E7D32")
        title_container.pack(expand=True, fill=tk.BOTH)
        
        store_icon = tk.Label(title_container, text="🏪", font=("Arial", 24), bg="#2E7D32", fg="white")
        store_icon.pack(side=tk.LEFT, padx=(20, 10), pady=15)
        
        title_label = tk.Label(title_container, text="Smart Supermarket Assistant", 
                              font=("Arial", 20, "bold"), bg="#2E7D32", fg="white")
        title_label.pack(side=tk.LEFT, pady=15)
        
        subtitle_label = tk.Label(title_container, text="🤖 Powered by AI • Find anything instantly!", 
                                 font=("Arial", 11), bg="#2E7D32", fg="#E8F5E8")
        subtitle_label.place(relx=0.15, rely=0.65)
        
        # Enhanced Control Panel
        control_panel = tk.Frame(main_container, bg="#ffffff", relief="raised", bd=2)
        control_panel.pack(fill=tk.X, pady=(0, 15), ipady=10)
        
        # Control buttons with better styling
        button_frame = tk.Frame(control_panel, bg="#ffffff")
        button_frame.pack(pady=10)
        
        self.show_list_btn = tk.Button(button_frame, text="📋 My Shopping List", 
                                      command=self.show_shopping_list, 
                                      bg="#FF6B35", fg="white", font=("Arial", 11, "bold"),
                                      relief="flat", padx=20, pady=8, cursor="hand2")
        self.show_list_btn.pack(side=tk.LEFT, padx=10)
        
        self.print_list_btn = tk.Button(button_frame, text="🖨️ Export List", 
                                       command=self.print_shopping_list, 
                                       bg="#1976D2", fg="white", font=("Arial", 11, "bold"),
                                       relief="flat", padx=20, pady=8, cursor="hand2")
        self.print_list_btn.pack(side=tk.LEFT, padx=10)
        
        self.clear_btn = tk.Button(button_frame, text="🗑️ New Session", 
                                  command=self.clear_chat, 
                                  bg="#D32F2F", fg="white", font=("Arial", 11, "bold"),
                                  relief="flat", padx=20, pady=8, cursor="hand2")
        self.clear_btn.pack(side=tk.LEFT, padx=10)
        
        # Shopping stats
        stats_frame = tk.Frame(control_panel, bg="#ffffff")
        stats_frame.pack(pady=(0, 10))
        
        self.stats_label = tk.Label(stats_frame, text="Items in list: 0 | Categories: 0", 
                                   font=("Arial", 10), bg="#ffffff", fg="#666666")
        self.stats_label.pack()
        
        # Enhanced Chat container with shadow effect
        chat_outer = tk.Frame(main_container, bg="#dddddd", relief="solid", bd=1)
        chat_outer.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        chat_container = tk.Frame(chat_outer, bg="#ffffff")
        chat_container.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        
        # Chat display area with modern styling
        self.chat_frame = tk.Frame(chat_container)
        self.chat_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas and scrollbar for chat
        self.chat_canvas = tk.Canvas(self.chat_frame, bg="#F5F5F5", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.chat_frame, orient="vertical", command=self.chat_canvas.yview)
        self.scrollable_frame = tk.Frame(self.chat_canvas, bg="#F5F5F5")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.chat_canvas.configure(
                scrollregion=self.chat_canvas.bbox("all")
            )
        )
        
        self.chat_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.chat_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.chat_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Enhanced Input section
        input_container = tk.Frame(main_container, bg="#ffffff", relief="solid", bd=1)
        input_container.pack(fill=tk.X, ipady=10)
        
        input_frame = tk.Frame(input_container, bg="#ffffff")
        input_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # Input label
        input_label = tk.Label(input_frame, text="💬 What are you looking for today?", 
                              font=("Arial", 10), bg="#ffffff", fg="#666666")
        input_label.pack(anchor="w", pady=(0, 5))
        
        # Input field with better styling
        input_field_frame = tk.Frame(input_frame, bg="#ffffff")
        input_field_frame.pack(fill=tk.X)
        
        self.user_input = tk.Entry(input_field_frame, font=("Arial", 12), relief="solid", bd=1,
                                  bg="#f9f9f9", fg="#333333", insertbackground="#333333")
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=8)
        self.user_input.bind("<Return>", self.process_input)
        self.user_input.bind("<FocusIn>", self.on_entry_focus_in)
        self.user_input.bind("<FocusOut>", self.on_entry_focus_out)
        
        # Enhanced Send button
        send_btn = tk.Button(input_field_frame, text="Send 📤", command=self.process_input, 
                            bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
                            relief="flat", padx=25, pady=8, cursor="hand2")
        send_btn.pack(side=tk.RIGHT)
        
        # Bind mousewheel to scroll
        self.chat_canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", self._on_mousewheel)
        
        # Focus on input field
        self.user_input.focus_set()

    def on_entry_focus_in(self, event):
        if self.user_input.get() == "Type your message here...":
            self.user_input.delete(0, tk.END)
            self.user_input.config(fg="#333333")

    def on_entry_focus_out(self, event):
        if not self.user_input.get():
            self.user_input.insert(0, "Type your message here...")
            self.user_input.config(fg="#999999")

    def _on_mousewheel(self, event):
        self.chat_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def update_stats(self):
        """Update the statistics display"""
        total_items = len(self.shopping_list)
        categories = len(set(info["category"] for info in self.shopping_list.values() 
                           if info["category"] != "unknown"))
        self.stats_label.config(text=f"Items in list: {total_items} | Categories: {categories}")

    def initial_greeting(self):
        greeting = random.choice([
            "Hello! 👋 Welcome to our Smart Supermarket!\n\nI'm your AI shopping assistant, ready to help you find anything you need. Just tell me what items you're looking for, and I'll guide you to the right shelves instantly! 🛒✨",
            "Hi there! 😊 I'm your intelligent shopping companion!\n\nWhether you need a single item or planning a full grocery trip, just describe what you're looking for and I'll show you exactly where to find it. Let's make your shopping super efficient! 🎯",
            "Greetings! 🤖 Welcome to the future of shopping assistance!\n\nI can help you locate any item in our store using natural language. Try saying something like 'I need ingredients for pasta' or 'Where can I find cleaning supplies?' Let's get started! 🚀"
        ])
        self.add_message("assistant", greeting)

    def add_message(self, sender, message):
        # Create message bubble with enhanced styling
        bubble_container = tk.Frame(self.scrollable_frame, bg="#F5F5F5")
        bubble_container.pack(fill=tk.X, padx=15, pady=8)
        
        timestamp = datetime.now().strftime("%H:%M")

        if sender == "user":
    # User message row (use grid for full width control)
            bubble_frame = tk.Frame(bubble_container, bg="#F5F5F5")
            bubble_frame.pack(fill=tk.X, expand=True, pady=5)

            bubble_frame.grid_columnconfigure(0, weight=1)  # left space expands
            bubble_frame.grid_columnconfigure(1, weight=0)  # content fixed to right

            # Right container (bubble + avatar)
            right_container = tk.Frame(bubble_frame, bg="#F5F5F5")
            right_container.grid(row=0, column=1, sticky="e", padx=10)

            # User avatar (far right)
            avatar = tk.Label(right_container, text="👤", font=("Arial", 16), bg="#F5F5F5")
            avatar.pack(side=tk.RIGHT, padx=(6, 0))

            # Bubble (just left of avatar)
            bubble = tk.Frame(right_container, bg="#1976D2", relief="solid", bd=0)
            bubble.pack(side=tk.RIGHT, padx=(0, 6))

       
            
            # Message content
            message_label = tk.Label(bubble, text=message, bg="#1976D2", fg="white", 
                                   font=("Arial", 11), wraplength=300, justify=tk.RIGHT)
            message_label.pack(padx=15, pady=(10, 5))
            
            # Time label
            time_label = tk.Label(bubble, text=timestamp, bg="#1976D2", fg="#E3F2FD", 
                                font=("Arial", 8))
            time_label.pack(anchor="e", padx=15, pady=(0, 8))
            
        else:
            # Assistant message (left-aligned, clean white with accent)
            bubble_frame = tk.Frame(bubble_container, bg="#F5F5F5")
            bubble_frame.pack(anchor="w")
            
            # Bot avatar (on the left side)
            avatar = tk.Label(bubble_frame, text="🤖", font=("Arial", 16), bg="#F5F5F5")
            avatar.pack(side=tk.LEFT, padx=(0, 8), pady=5)
            
            bubble = tk.Frame(bubble_frame, bg="white", relief="solid", bd=1)
            bubble.pack(anchor="w", side=tk.LEFT)
            
            # Message content with better formatting
            message_label = tk.Label(bubble, text=message, bg="white", fg="#333333", 
                                   font=("Arial", 11), wraplength=400, justify=tk.LEFT)
            message_label.pack(padx=15, pady=(10, 5))
            
            # Time label
            time_label = tk.Label(bubble, text=timestamp, bg="white", fg="#888888", 
                                font=("Arial", 8))
            time_label.pack(anchor="w", padx=15, pady=(0, 8))
        
        # Update scroll region and scroll to bottom
        self.scrollable_frame.update_idletasks()
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        self.chat_canvas.yview_moveto(1)

    def process_input(self, event=None):
        user_text = self.user_input.get().strip()
        if not user_text or user_text == "Type your message here...":
            return
            
        # Add user message
        self.add_message("user", user_text)
        self.user_input.delete(0, tk.END)
        
        # Handle thank you messages
        if self.is_thank_you(user_text):
            thank_you_responses = [
                "You're very welcome! 😊 I'm always happy to help you find what you need. Have a wonderful shopping experience! 🛒✨",
                "My pleasure! 🌟 Thank you for using our smart shopping assistant. Hope you found everything you needed! Come back anytime! 👋",
                "You're most welcome! 🤗 It was great helping you today. Enjoy your shopping and have a fantastic day! 🎉",
                "Glad I could help! 😄 Thanks for choosing our AI assistant. Wishing you a pleasant shopping trip! 🛍️"
            ]
            response = random.choice(thank_you_responses)
            self.add_message("assistant", response)
            return
        
        # Handle greetings
        if self.is_greeting(user_text):
            response = random.choice([
                "Hello there! 😊 How can I help you with your shopping today? Just tell me what you're looking for! 🛒",
                "Hi! Nice to meet you! 👋 What items can I help you locate in our store today?",
                "Greetings! 🌟 I'm ready to help you find anything in our store! What do you need?"
            ])
            self.add_message("assistant", response)
            return
        
        # Extract items using NLP
        items = extract_items(user_text)
        if not items:
            helpful_responses = [
                "I couldn't identify any specific items from your message. 🤔\n\nCould you please mention what you're looking for? For example:\n• 'I need apples and milk'\n• 'Where can I find bread?'\n• 'Looking for cleaning supplies'",
                "I'm not sure what items you're looking for. 😅\n\nTry being more specific about the products you need. I can help you find anything from fruits to cleaning supplies!",
                "Hmm, I didn't catch any product names there. 🧐\n\nJust tell me what items you want to buy, and I'll show you exactly where to find them!"
            ]
            self.add_message("assistant", random.choice(helpful_responses))
            return
        
        # Acknowledge the request
        acknowledgment = random.choice([
            "Perfect! Let me help you find those items right away! 🔍",
            "Great choice! I'll locate those items for you instantly! ⚡",
            "Excellent! Let me check our store layout for you! 📍",
            "Sure thing! Finding the best locations for your items! 🎯"
        ])
        self.add_message("assistant", acknowledgment)
        
        # Find shelves
        results = find_shelves(items, self.products_db)
        
        # Update shopping list
        self.shopping_list.update(results)
        self.update_stats()
        
        # Display results
        self.display_results(results)
        
        # Ask for more items after showing results
        followup_questions = [
            "Anything else you'd like to add to your shopping list? 🛍️",
            "Is there anything else you're looking for today? 😊",
            "Would you like me to help you find any other items? 🤔",
            "Any other products you need help locating? 📦",
            "What else can I help you find in our store? 🛒"
        ]
        
        # Small delay effect for better user experience
        self.root.after(1000, lambda: self.add_message("assistant", random.choice(followup_questions)))

    def is_greeting(self, text):
        greetings_list = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening", "howdy"]
        text_lower = text.lower()
        return any(greeting in text_lower for greeting in greetings_list)

    def is_thank_you(self, text):
        thank_you_phrases = ["thank you", "thanks", "thank u", "thx", "appreciate", "grateful", "bye", "goodbye"]
        text_lower = text.lower()
        return any(phrase in text_lower for phrase in thank_you_phrases)

    def display_results(self, results: Dict[str, Dict]):
        # Create results message with enhanced formatting
        result_lines = ["🔍 **Shelf Locations Found:**"]
        result_lines.append("═" * 40)
        
        categories_found = {}
        not_found = []
        
        for item, info in results.items():
            if info["category"] != "unknown":
                if info["category"] not in categories_found:
                    categories_found[info["category"]] = []
                categories_found[info["category"]].append((item, info["shelf"]))
            else:
                not_found.append(item)
        
        # Display items by category with better icons
        category_icons = {
            "fruits": "🍎", "dairy": "🥛", "bakery": "🍞", "stationary": "📝", 
            "cleaning": "🧽", "beverages": "☕", "snacks": "🍿", 
            "frozen": "🧊", "vegetables": "🥬", "spices": "🧂"
        }
        
        for category, items in categories_found.items():
            category_name = category.replace('_', ' ').title()
            icon = category_icons.get(category, "📁")
            result_lines.append(f"\n{icon} **{category_name} Section:**")
            for item, shelf in items:
                result_lines.append(f"   ✓ {item.capitalize()} → {shelf}")
        
        # Display not found items
        if not_found:
            result_lines.append(f"\n❌ **Items Not Available:**")
            for item in not_found:
                result_lines.append(f"   • {item.capitalize()} → Sorry, not in our current inventory")
        
        # Add helpful tip
        if categories_found:
            result_lines.append(f"\n💡 **Shopping Tip:** Visit sections in order for efficient shopping!")
        
        # Add results message
        self.add_message("assistant", "\n".join(result_lines))

    def show_shopping_list(self):
        if not self.shopping_list:
            messagebox.showinfo("Shopping List", "🛒 Your shopping list is empty!\n\nStart adding items by telling me what you need!")
            return
        
        # Create enhanced shopping list window
        list_window = tk.Toplevel(self.root)
        list_window.title("📋 My Smart Shopping List")
        list_window.geometry("600x500")
        list_window.minsize(500, 400)
        list_window.configure(bg="#f0f0f0")
        
        # Header
        header = tk.Frame(list_window, bg="#1976D2", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title_label = tk.Label(header, text="📋 My Shopping List", font=("Arial", 16, "bold"), 
                              bg="#1976D2", fg="white")
        title_label.pack(expand=True)
        
        # List display with modern styling
        list_frame = tk.Frame(list_window, bg="#ffffff", relief="solid", bd=1)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Scrollable text area with better formatting
        list_text = scrolledtext.ScrolledText(list_frame, wrap=tk.WORD, font=("Courier New", 11),
                                             bg="#fafafa", fg="#333333", relief="flat",
                                             padx=15, pady=15)
        list_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Format shopping list with better organization
        categories = {}
        not_found = []
        
        for item, info in self.shopping_list.items():
            if info["category"] != "unknown":
                if info["category"] not in categories:
                    categories[info["category"]] = []
                categories[info["category"]].append((item, info["shelf"]))
            else:
                not_found.append(item)
        
        # Create organized list content
        list_content = []
        list_content.append("🛒 SMART SHOPPING LIST")
        list_content.append("=" * 50)
        list_content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d at %H:%M')}")
        list_content.append(f"Total Items: {len(self.shopping_list)}")
        list_content.append("=" * 50)
        list_content.append("")
        
        category_icons = {
            "fruits": "🍎", "dairy": "🥛", "bakery": "🍞", "eggs": "🥚", 
            "cleaning": "🧽", "beverages": "☕", "snacks": "🍿", 
            "frozen": "🧊", "canned": "🥫", "spices": "🧂"
        }
        
        for category, items in sorted(categories.items()):
            category_name = category.replace('_', ' ').title()
            icon = category_icons.get(category, "📁")
            list_content.append(f"{icon} {category_name.upper()} SECTION:")
            list_content.append("-" * 30)
            for item, shelf in sorted(items):
                list_content.append(f"  ✓ {item.capitalize():<20} → {shelf}")
            list_content.append("")
        
        if not_found:
            list_content.append("❌ ITEMS NOT AVAILABLE:")
            list_content.append("-" * 30)
            for item in not_found:
                list_content.append(f"  • {item.capitalize()}")
            list_content.append("")
        
        list_content.append("💡 Happy Shopping! 🛍️")
        
        list_text.insert(tk.END, "\n".join(list_content))
        list_text.config(state=tk.DISABLED)

    def print_shopping_list(self):
        if not self.shopping_list:
            messagebox.showinfo("Export Shopping List", "🛒 Your shopping list is empty!\n\nAdd some items before exporting!")
            return
        
        try:
            # Create downloads directory if it doesn't exist
            if not os.path.exists("shopping_lists"):
                os.makedirs("shopping_lists")
            
            filename = f"shopping_lists/SmartList_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("🛒 SMART SUPERMARKET SHOPPING LIST\n")
                f.write("═" * 60 + "\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}\n")
                f.write(f"Total Items: {len(self.shopping_list)}\n")
                f.write("═" * 60 + "\n\n")
                
                categories = {}
                not_found = []
                
                for item, info in self.shopping_list.items():
                    if info["category"] != "unknown":
                        if info["category"] not in categories:
                            categories[info["category"]] = []
                        categories[info["category"]].append((item, info["shelf"]))
                    else:
                        not_found.append(item)
                
                category_icons = {
                    "fruits": "🍎", "dairy": "🥛", "bakery": "🍞", "eggs": "🥚", 
                    "cleaning": "🧽", "beverages": "☕", "snacks": "🍿", 
                    "frozen": "🧊", "canned": "🥫", "spices": "🧂"
                }
                
                for category, items in sorted(categories.items()):
                    category_name = category.replace('_', ' ').title()
                    icon = category_icons.get(category, "📁")
                    f.write(f"{icon} {category_name.upper()} SECTION:\n")
                    f.write("-" * 40 + "\n")
                    for item, shelf in sorted(items):
                        f.write(f"  ✓ {item.capitalize():<25} → {shelf}\n")
                    f.write("\n")
                
                if not_found:
                    f.write("❌ ITEMS NOT AVAILABLE:\n")
                    f.write("-" * 40 + "\n")
                    for item in not_found:
                        f.write(f"  • {item.capitalize()}\n")
                    f.write("\n")
                
                f.write("═" * 60 + "\n")
                f.write("💡 Tip: Follow the shelf order for efficient shopping!\n")
                f.write("🛍️ Happy Shopping!\n")
            
            success_message = f"🎉 Success!\n\nYour shopping list has been exported to:\n{filename}\n\nThe file is ready to print or share!"
            messagebox.showinfo("Export Complete", success_message)
            
        except Exception as e:
            error_message = f"❌ Export Failed\n\nSorry, I couldn't save your shopping list.\nError: {str(e)}\n\nPlease try again or contact support."
            messagebox.showerror("Export Error", error_message)

    def clear_chat(self):
        # Show confirmation dialog
        result = messagebox.askyesno("New Session", 
                                   "🗑️ Start a new session?\n\nThis will:\n• Clear all chat messages\n• Empty your shopping list\n• Reset the conversation\n\nAre you sure?")
        
        if not result:
            return
        
        # Clear chat display
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Clear shopping list
        self.shopping_list.clear()
        self.update_stats()
        
        # Reset scroll
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        
        # Show initial greeting
        self.initial_greeting()
        
        # Focus back to input
        self.user_input.focus_set()

if __name__ == "__main__":
    root = tk.Tk()
    app = SupermarketChatbotGUI(root)
    root.mainloop()