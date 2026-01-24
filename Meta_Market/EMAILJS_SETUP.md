# EmailJS Setup Instructions for Meta Market

## Quick Setup (5 minutes)

### Step 1: Create EmailJS Account

1. Go to [https://emailjs.com](https://emailjs.com)
2. Click "Sign Up" (it's FREE!)
3. Verify your email address

### Step 2: Add Email Service

1. In EmailJS dashboard, click "Add New Service"
2. Choose "Gmail" (since you're using gmail.com)
3. Click "Connect Account" and authorize with **rhithvik.ashok@gmail.com**
4. Copy your **Service ID** (looks like: service_xxxxxxx)

### Step 3: Create Email Template

1. Click "Email Templates" in sidebar
2. Click "Create New Template"
3. Use this template content:

**Subject:**

```
{{subject}}
```

**Body:**

```
{{message}}
```

4. Save the template
5. Copy your **Template ID** (looks like: template_xxxxxxx)

### Step 4: Get Public Key

1. Go to "Account" → "General"
2. Find your **Public Key** (looks like: xxxxxxxxxxxx)

### Step 5: Update Your Code

1. Open `index.html`
2. Find line ~677 (search for "YOUR_SERVICE_ID")
3. Replace the three placeholders:

```javascript
const serviceID = "service_xxxxxxx"; // Your Service ID
const templateID = "template_xxxxxxx"; // Your Template ID
const publicKey = "xxxxxxxxxxxx"; // Your Public Key
```

### Step 6: Test It!

1. Open `index.html` in your browser
2. Add some items to cart
3. Fill in delivery address
4. Check the Terms & Conditions box
5. Click "Place Order"
6. Check your email at rhithvik.ashok@gmail.com!

## ✅ That's It!

Once configured, every order will automatically send you an email with:

- Full delivery address
- All ordered items with prices
- Total amount to collect (COD)
- Delivery notes
- Timestamp

## Troubleshooting

**Error: "Please setup EmailJS"**

- Make sure you replaced ALL three placeholders
- Check that IDs don't have quotes or spaces
- Verify your EmailJS account is active

**Email not received?**

- Check spam folder
- Verify Gmail connection in EmailJS dashboard
- Check EmailJS usage limits (free tier: 200 emails/month)

**Need Help?**

- EmailJS Docs: https://www.emailjs.com/docs/
- Check browser console for errors (F12)

---

**File to Edit:** `c:\Rhithvik\Code\RhithuBeast\RhithuBeast\Meta_Market\index.html` (line 677)
