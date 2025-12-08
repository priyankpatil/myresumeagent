# Mobile Testing Guide

This guide explains how to test the mobile experience of the resume agent dashboard locally before deploying.

## Quick Start: Chrome DevTools Mobile Emulation

The easiest way to test mobile responsiveness is using Chrome DevTools:

### Steps:

1. **Start the local server:**
   ```bash
   python main.py
   ```

2. **Open Chrome and navigate to:**
   ```
   http://localhost:8000
   ```

3. **Open DevTools:**
   - Press `F12` or `Cmd+Option+I` (Mac) / `Ctrl+Shift+I` (Windows/Linux)
   - Or right-click → "Inspect"

4. **Enable Device Toolbar:**
   - Click the device icon (📱) in the toolbar
   - Or press `Cmd+Shift+M` (Mac) / `Ctrl+Shift+M` (Windows/Linux)

5. **Select a device preset:**
   - Click the device dropdown at the top
   - Choose from presets like:
     - **iPhone 12 Pro** (390x844) - Good for modern iPhones
     - **iPhone SE** (375x667) - Good for smaller screens
     - **Samsung Galaxy S20** (360x800) - Good for Android
     - **iPad** (768x1024) - Good for tablets
     - **Custom** - Set your own dimensions

6. **Test different orientations:**
   - Click the rotate icon to switch between portrait/landscape
   - Or use the orientation dropdown

7. **Test touch interactions:**
   - Click on charts to test filtering
   - Scroll through the dashboard
   - Test the AI agent chat interface

## Advanced: Network Throttling

To simulate slower mobile connections:

1. In DevTools, go to the **Network** tab
2. Click the throttling dropdown (usually says "No throttling")
3. Select:
   - **Fast 3G** - For slower connections
   - **Slow 3G** - For very slow connections
   - **Offline** - To test error handling

## Testing on Real Devices

### Option 1: Local Network Access

1. **Find your local IP address:**
   ```bash
   # Mac/Linux
   ifconfig | grep "inet " | grep -v 127.0.0.1
   
   # Windows
   ipconfig
   ```
   Look for something like `192.168.1.x` or `10.0.0.x`

2. **Start the server bound to all interfaces:**
   ```bash
   python main.py
   ```
   Or modify `main.py` to use:
   ```python
   uvicorn.run(app, host="0.0.0.0", port=8000)
   ```

3. **On your mobile device:**
   - Connect to the same Wi-Fi network
   - Open browser and navigate to: `http://YOUR_IP:8000`
   - Example: `http://192.168.1.100:8000`

### Option 2: ngrok (Recommended for Testing)

1. **Install ngrok:**
   ```bash
   # Mac
   brew install ngrok
   
   # Or download from https://ngrok.com/
   ```

2. **Start your local server:**
   ```bash
   python main.py
   ```

3. **In another terminal, start ngrok:**
   ```bash
   ngrok http 8000
   ```

4. **Copy the HTTPS URL** (e.g., `https://abc123.ngrok.io`)

5. **Open on your mobile device:**
   - Use the ngrok URL in your mobile browser
   - Works from anywhere, not just local network

## Testing Checklist

### Visual Checks:
- [ ] Timeline chart displays correctly with proper margins
- [ ] Institution names are readable (not cut off)
- [ ] Charts fit within viewport
- [ ] Legend is visible and not overlapping
- [ ] Header information is readable
- [ ] Social links are accessible
- [ ] Filter indicator is visible when active

### Interaction Checks:
- [ ] Can tap/click on timeline chart to filter
- [ ] Can tap/click on donut chart to filter
- [ ] Can tap/click on bar chart to filter
- [ ] Clear filter button works
- [ ] AI agent chat input is accessible
- [ ] Can scroll through dashboard section
- [ ] Can scroll through chat messages

### Responsive Breakpoints:
- [ ] **Desktop (> 1024px)**: Side-by-side layout works
- [ ] **Tablet (768px - 1024px)**: Adjusted widths work
- [ ] **Mobile (480px - 768px)**: Stacked layout works
- [ ] **Small Mobile (< 480px)**: Compact layout works

### Orientation:
- [ ] Portrait mode displays correctly
- [ ] Landscape mode displays correctly
- [ ] Charts resize on orientation change

### Performance:
- [ ] Charts load within 2-3 seconds
- [ ] No lag when interacting with charts
- [ ] Smooth scrolling
- [ ] AI responses load in reasonable time

## Common Issues and Fixes

### Issue: Charts are too small on mobile
**Fix:** Check that `chart-wrapper` heights are appropriate for mobile breakpoints

### Issue: Timeline chart labels are cut off
**Fix:** Verify left margin is reduced on mobile (should be 80-100px on small screens)

### Issue: Can't interact with charts on mobile
**Fix:** Ensure `clickmode: 'event'` is set in Plotly config

### Issue: Layout breaks on orientation change
**Fix:** The resize handler should automatically reload charts - check console for errors

## Browser Testing

Test on multiple mobile browsers:
- **Safari** (iOS)
- **Chrome** (Android/iOS)
- **Firefox Mobile**
- **Samsung Internet** (Android)

## Automated Testing (Optional)

For CI/CD, you can use tools like:
- **Playwright** - Cross-browser testing
- **Puppeteer** - Chrome/Chromium automation
- **Selenium** - Browser automation

Example Playwright test:
```javascript
const { test, expect } = require('@playwright/test');

test('mobile timeline chart', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });
  await page.goto('http://localhost:8000');
  await expect(page.locator('#timeline-chart')).toBeVisible();
});
```

## Tips

1. **Use multiple devices:** Test on actual phones if possible
2. **Test in different lighting:** Check dark mode readability
3. **Test with slow network:** Use network throttling
4. **Test with different data:** Try with minimal/maximal data
5. **Test accessibility:** Use screen readers if possible

## Quick Commands

```bash
# Start server
python main.py

# Test with ngrok (in separate terminal)
ngrok http 8000

# Check local IP (Mac/Linux)
ifconfig | grep "inet " | grep -v 127.0.0.1

# Check local IP (Windows)
ipconfig
```

Happy testing! 🚀

