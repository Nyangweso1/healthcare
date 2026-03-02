# CSS Organization Guide

## 📁 CSS File Structure

All CSS files are now organized in `/static/css/` folder:

### **1. style.css** (Main/Global Styles)
- Global variables and resets
- Navigation bar styles
- Footer styles
- Base typography
- Background gradients
- **Use:** Loaded on all pages via base.html

### **2. home.css** (Homepage Specific)
- Hero section styles
- Feature cards grid
- Trust section
- Risk info section
- Call-to-action buttons
- **Use:** Load only on index.html

### **3. admin.css** (Admin Dashboard)
- Admin header styles
- Statistics cards
- Admin tables
- User management interface
- Badge styles (admin/user/risk levels)
- **Use:** Load on admin pages only

### **4. forms.css** (All Forms)
- Authentication forms (login/register)
- Assessment form styles
- Form validation styles
- Input fields, selects, textareas
- Submit buttons
- Form sections and grouping
- **Use:** Load on pages with forms

### **5. messages.css** (Messaging System)
- Message inbox/sent boxes
- Message items and cards
- Unread message indicators
- Message headers
- Scrollable message lists
- **Use:** Load on contact/messages page

### **6. alerts.css** (Notifications)
- Success/error/warning/info alerts
- Toast notifications
- Flash messages
- Loading spinners
- Dismissible alerts
- **Use:** Loaded globally via base.html

### **7. components.css** (Reusable Components)
- Cards (info cards, stat cards)
- Progress bars
- Badges
- Statistics grids
- General component styles
- **Use:** Loaded globally via base.html

---

## 🎯 How to Use CSS Files

### **In base.html (Global CSS):**
```html
<!-- Always loaded -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
<link rel="stylesheet" href="{{ url_for('static', filename='css/components.css') }}">
<link rel="stylesheet" href="{{ url_for('static', filename='css/alerts.css') }}">
<link rel="stylesheet" href="{{ url_for('static', filename='css/forms.css') }}">
```

### **In Specific Templates (Page-specific CSS):**
```html
{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/home.css') }}">
{% endblock %}
```

---

## 📋 Template CSS Loading

| Template | CSS Files Loaded |
|----------|------------------|
| **base.html** | style.css, components.css, alerts.css, forms.css |
| **index.html** | + home.css |
| **admin_dashboard.html** | + admin.css |
| **admin_user_view.html** | + admin.css |
| **contact.html** | + messages.css |
| **login.html** | Already has forms.css from base |
| **register.html** | Already has forms.css from base |
| **assess.html** | Already has forms.css from base |

---

## ✅ Benefits of This Organization

1. **No Inline Styles**: All CSS moved to external files
2. **Modular**: Easy to maintain specific sections
3. **Reusable**: Components CSS can be used anywhere
4. **Performance**: Browser caching of CSS files
5. **Clean HTML**: Templates are cleaner without `<style>` tags
6. **Easy Updates**: Change one file, affects all relevant pages

---

## 🎨 Adding New Styles

### **For a new page:**
1. Create new CSS file (e.g., `blog.css`)
2. Add styles specific to that page
3. Load it in template:
```html
{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/blog.css') }}">
{% endblock %}
```

### **For global styles:**
Add to `style.css` or `components.css`

### **For form styles:**
Add to `forms.css`

---

## 🔍 Quick Reference

**Need button styles?** → components.css  
**Need form styles?** → forms.css  
**Need alert styles?** → alerts.css  
**Need admin styles?** → admin.css  
**Need message styles?** → messages.css  
**Need homepage styles?** → home.css  
**Need global styles?** → style.css

---

## 📝 Example: Adding a New Feature

**Scenario:** Add a new "Reports" page

1. Create `static/css/reports.css`:
```css
.report-container {
    padding: 30px;
}

.report-chart {
    background: white;
    border-radius: 15px;
    padding: 20px;
}
```

2. In `templates/reports.html`:
```html
{% extends "base.html" %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/reports.css') }}">
{% endblock %}

{% block content %}
<div class="report-container">
    <div class="report-chart">
        <!-- Chart content -->
    </div>
</div>
{% endblock %}
```

Done! Clean, organized, and maintainable. ✨
