class StoreSystem:
    def __init__(self):
        # యూజర్ క్రెడెన్షియల్స్ మరియు పాస్‌వర్డ్స్
        self.users = {
            "admin": {"password": "manikanta123", "role": "owner"},
            "manikanta": {"password": "samsri2528", "role": "staff"},
        }
        self.owner_password = "samsri25285"  # ఖర్చులు మరియు స్టాక్ అప్రూవల్ కోసం ఓనర్ పాస్‌వర్డ్
        
        # సాంపుల్ ఇన్వెంటరీ (స్టాక్ మరియు ధరలు)
        self.inventory = {
            "Rice Bag": {"price": 1200, "stock": 50},
            "Sugar": {"price": 45, "stock": 100}
        }
        
        self.pending_expenses = []

    def login(self):
        print("--- లాగిన్ అవ్వండి ---")
        username = input("యూజర్‌నేమ్ ఎంటర్ చేయండి: ")
        password = input("పాస్‌వర్డ్ ఎంటర్ చేయండి: ")
        
        if username in self.users and self.users[username]["password"] == password:
            print(f"లాగిన్ విజయవంతమైంది! ({self.users[username]['role'].upper()})")
            return username, self.users[username]["role"]
        else:
            print("తప్పు యూజర్‌నేమ్ లేదా పాస్‌వర్డ్!")
            return None, None

    def add_or_update_stock(self, role):
        # 1. Manage Inventory లో స్టాక్ యాడ్ చేయడానికి పాస్‌వర్డ్ అడగాలి
        print("\n--- స్టాక్ మేనేజ్‌మెంట్ ---")
        entered_pass = input("స్టాక్ మార్చడానికి ఓనర్ పాస్‌వర్డ్ (samsri25285) ఎంటర్ చేయండి: ")
        
        if entered_pass != self.owner_password:
            print("అనుమతి లేదు! తప్పు పాస్‌వర్డ్.")
            return

        item = input("ఐటమ్ పేరు ఎంటర్ చేయండి: ")
        price = float(input("ధర ఎంటర్ చేయండి: "))
        qty = int(input("స్టాక్ క్వాంటిటీ ఎంటర్ చేయండి: "))
        
        self.inventory[item] = {"price": price, "stock": qty}
        print(f"'{item}' విజయవంతంగా అప్‌డేట్ చేయబడింది!")

    def billing_section(self):
        # 2. బిల్లింగ్ చేసేటప్పుడు ప్రైస్ మార్చే ఆప్షన్ ఉండకూడదు
        print("\n--- బిల్లింగ్ కౌంటర్ ---")
        item = input("కొనుగోలు చేస్తున్న ఐటమ్ పేరు: ")
        
        if item not in self.inventory:
            print("ఈ ఐటమ్ ఇన్వెంటరీలో లేదు!")
            return
            
        fixed_price = self.inventory[item]["price"]
        qty = int(input(f"క్వాంటిటీ ఎంటర్ చేయండి (ఫిక్స్డ్ ధర: {fixed_price}): "))
        
        total_amount = fixed_price * qty
        print(f"మొత్తం బిల్లు: {total_amount} (ధర మార్చడానికి అనుమతి లేదు)")

    def petty_cash_expense(self):
        # 3. ఖర్చులు & డిస్కౌంట్లు ఓనర్ అథరైజేషన్ ఉండాలి
        print("\n--- పెట్టీ క్యాష్ / ఖర్చులు / డిస్కౌంట్లు ---")
        reason = input("ఖర్చు లేదా డిస్కౌంట్ ఎందుకు ఇస్తున్నారు?: ")
        amount = float(input("మొత్తం (Amount): "))
        
        entered_pass = input("దీనిని అప్రూవ్ చేయడానికి ఓనర్ పాస్‌వర్డ్ ఎంటర్ చేయండి: ")
        
        if entered_pass == self.owner_password:
            print(f"ఖర్చు '{reason}' ({amount}) ఓనర్ చేత అథరైజ్ చేయబడింది మరియు సేవ్ అయింది!")
            self.pending_expenses.append({"reason": reason, "amount": amount, "status": "Approved"})
        else:
            print("ఓనర్ పాస్‌వర్డ్ తప్పు! ఈ ఖర్చు పెండింగ్‌లో ఉంది లేదా రద్దు చేయబడింది.")

# రన్ చేసే విధానం
app = StoreSystem()
while True:
    user, role = app.login()
    if user:
        while True:
            print("\n1. స్టాక్ యాడ్/ఎడిట్ చేయి (Inventory)\n2. బిల్లింగ్ చేయి (Billing)\n3. ఖర్చు లేదా డిస్కౌంట్ ఎంటర్ చేయి (Petty Cash)\n4. లాగౌట్")
            choice = input("మీ ఆప్షన్ ఎంచుకోండి (1-4): ")
            
            if choice == "1":
                app.add_or_update_stock(role)
            elif choice == "2":
                app.billing_section()
            elif choice == "3":
                app.petty_cash_expense()
            elif choice == "4":
                print("లాగౌట్ అయ్యారు.\n")
                break
            else:
                print("తప్పు ఆప్షన్ ఎంచుకున్నారు.")
