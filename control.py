import subprocess
import time

# Run the script that gets URLs from Google
print("🔍 Running Google Search URL scraper...")
result1 = subprocess.run(["python", "automationSearch.py"])

if result1.returncode == 0:
    time.sleep(5)  # Optional: wait for a couple of seconds before running the next script
    
    print("✅ Google scraper finished successfully.\n")
    
    # Now run the email scraper
    print("📧 Running email scraper...")
    result2 = subprocess.run(["python", "emailScraper.py"])

    if result2.returncode == 0:
        print("✅ Email scraper completed successfully.")
    else:
        print("❌ Email scraper failed to run.")
else:
    print("❌ Google scraper failed. Aborting email scraping.")



