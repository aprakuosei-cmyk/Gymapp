# 🏋️‍♂️ IronSync Gym Manager

IronSync is a lightweight, cloud-synced gym management dashboard designed to run on **GitHub Pages**. It handles member registration, automated billing tracking, retail sales, and member communication.

## 🚀 Quick Start
1. **Access:** Open the GitHub Pages URL.
2. **Login:** Use your admin email and password (set up in Firebase).
3. **Add Members:** Use the "Add New Member" form. The system automatically sets a 30-day renewal date.

## 🛠 Features
* **Member CRM:** Track names, phone numbers, and membership plans.
* **Billing Alerts:** Members turn **RED** automatically when their 30 days are up.
* **One-Tap Renewal:** Clicking "Renew" adds another 30 days to the member's profile.
* **Retail Shop:** A built-in POS (Point of Sale) to track supplement and water sales.
* **Live Analytics:** * **Monthly Revenue:** Calculated based on active membership plans.
    * **Daily Sales:** Tracks cash/retail sales made today.
* **Messaging:** Integrated WhatsApp and SMS triggers for overdue reminders.
* **Security:** Protected by Firebase Authentication and Firestore Security Rules.

## 📂 Project Structure
* `index.html`: The structure and UI of the dashboard.
* `style.css`: Custom "IronSync" Dark/Light theme variables.
* `script.js`: The "Brain" – handles Firebase syncing, sales logic, and search.

## ⚙️ Maintenance & Updates
### Adding Products to the Shop
1. Scroll to the **Supplement & Gear Shop**.
2. Expand the **+ Add New Product** section.
3. Enter name, price, and initial stock.

### Exporting Data
Click the **Export CSV** button next to the search bar to download your entire member list into Excel for tax reporting or backups.

## 🔒 Security Note
This app uses Firebase Security Rules. Ensure your Firestore rules are set to:
`allow read, write: if request.auth != null;`
This prevents unauthorized access to your member data.
