# Rising Stars Academy Website

Modern, responsive website prototype for Rising Stars Academy — a K-12 educational institution in Johannesburg.

## 📋 Contents

- **index.html** — Main website file (single-page app with Tailwind CSS)
- **staff-data.json** — Staff information template (for future CMS integration)
- **HANDOFF.md** — Setup & deployment instructions for in-laws
- **Assets/** — (Linked from main project folder)

## ✨ Features

- ✅ Home page with hero, values, stats
- ✅ About page (history, vision, mission)
- ✅ Why Rising Stars (differentiators & testimonials)
- ✅ Three school pages (Educare, Primary, High)
- ✅ Staff directory (by school) — **READY FOR STAFF INFO**
- ✅ Enrollments & Fees page
- ✅ Photo gallery
- ✅ Contact form
- ✅ Fully responsive (mobile, tablet, desktop)
- ✅ Smooth page transitions & animations

## 🎨 Design

- **Brand Colors:** Navy (#1B3A5C), Light Blue (#13a4ec), plus school-specific colors
- **Font:** Work Sans (Google Fonts)
- **Icons:** Material Symbols (Google)
- **CSS Framework:** Tailwind CSS v3

## 🚀 How to Use

### Local Testing
1. Open `index.html` in any browser
2. Click through pages using the navigation menu
3. Test mobile responsiveness (use DevTools)

### Deploy to Netlify (Recommended)
1. Push to GitHub (done ✓)
2. Go to [Netlify.com](https://netlify.com)
3. Connect your GitHub repo: `dexterdeaguiar/rising-stars-academy`
4. Deploy with one click
5. Connect custom domain: `risingstarsacademy.co.za`

### Deploy to GitHub Pages
1. In repo settings → Pages → Select `main` branch + `/ (root)`
2. Site deploys automatically at `https://dexterdeaguiar.github.io/rising-stars-academy`
3. Can still use custom domain

## 📝 Next Steps for In-Laws

See **HANDOFF.md** for complete instructions, including:
- How to add staff photos + info
- How to fill in contact details
- How to update fee structure
- How to add testimonials
- How to link enrollment forms

## 📄 File Structure

```
/
├── index.html          # Main website file
├── staff-data.json     # Staff info template (future use)
├── README.md          # This file
├── HANDOFF.md         # In-laws setup guide
└── Assets/            # (Stored in main project folder)
    ├── Photos/
    ├── Logos/
    └── Documents/
```

## 🔧 Customization Tips

### Change Colors
Edit the Tailwind config in `<script>` tag (line ~13):
```javascript
colors: {
  brand: "#1B3A5C",      // Main navy
  primary: "#13a4ec",    // Light blue
  educare: "#E67E22",    // Orange
  prim: "#27AE60",       // Green
  high: "#8E44AD",       // Purple
}
```

### Update Contact Info
Search for:
- `+27 (0) 11 555 1234` → replace with actual numbers
- `info@risingstarsacademy.co.za` → actual email

### Add Real Photos
Replace placeholder image URLs:
- `Assets/4P2A6116copy.jpg` → point to your actual photos
- Use full paths or relative paths

### Add Staff Members
Edit the Staff page section (line ~1100) with real names, photos, and bios.

## 📱 Responsive Design

- **Mobile-first:** Designed for phones first, scales up to desktop
- **Breakpoints:** sm (640px), md (768px), lg (1024px)
- **Mobile menu:** Hamburger nav on small screens
- **Touch-friendly:** Buttons and links are easy to tap

## 🎯 SEO Notes

- **Title & Meta:** Update `<title>` and meta description in `<head>`
- **Headings:** Proper H1-H3 hierarchy for search engines
- **Images:** Add `alt` text to all images
- **Links:** Use descriptive anchor text

## 🔗 Links to Update

When deploying to risingstarsacademy.co.za:
1. Update all internal links (currently use onclick events)
2. Link to actual enrollment forms (Wix, Google Forms, etc.)
3. Link to actual downloadable documents (PDFs)
4. Embed Google Maps for location
5. Add social media links (Facebook, Instagram, LinkedIn)

## ❓ Common Questions

**Q: Can I edit this without coding?**  
A: Not easily. The HTML/Tailwind needs to be edited by someone with web dev skills. Consider hiring a developer or using Wix/Squarespace if you need a no-code builder.

**Q: How do I change the layout?**  
A: Edit the HTML directly. For major changes, consider rebuilding with a website builder (Wix, Webflow, Squarespace).

**Q: Can I use this with a CMS (WordPress, etc.)?**  
A: This is a static HTML file. For a CMS, you'd need to convert to WordPress or similar. Talk to Dex about this.

**Q: How do I add a blog?**  
A: This template doesn't include a blog. Would need a CMS like WordPress or a static site generator.

## 📞 Support

Questions about the website? Contact **Dexter** at dexterdeaguiar.com

---

**Version:** 1.0  
**Last Updated:** April 2026  
**Status:** Ready for in-law review & feedback
