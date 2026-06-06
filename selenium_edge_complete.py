"""
Selenium with Microsoft Edge - Complete Production Ready Example
Includes: Headless mode, Form filling, Clicks, Multiple tabs, JS execution, and more

Setup:
1. Download msedgedriver.exe from: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
2. Update DRIVER_PATH below to point to your msedgedriver.exe location
3. Run the script and uncomment the example you want to test
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import logging
import os

# Configuring logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

#  PATH to where i extracted msedgedriver.exe
DRIVER_PATH = r"C:\webdriver\msedgedriver.exe"



# EDGE BOT CLASS

class EdgeBot:
    """Reusable Edge browser automation class"""
    
    def __init__(self, headless: bool = False, maximize: bool = True):
        """Initialize Edge WebDriver with best-practice options"""
        self.driver = None
        
        edge_options = Options()
        
        if headless:
            edge_options.add_argument("--headless")
            edge_options.add_argument("--window-size=1920,1080")
        
        if maximize:
            edge_options.add_argument("--start-maximized")
        
        # Anti-detection & stability flags
        edge_options.add_argument("--disable-blink-features=AutomationControlled")
        edge_options.add_argument("--disable-extensions")
        edge_options.add_argument("--disable-notifications")
        edge_options.add_argument("--disable-gpu")
        edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        edge_options.add_experimental_option("useAutomationExtension", False)
        
        # Use manually downloaded EdgeDriver
        service = Service(executable_path=DRIVER_PATH)
        
        try:
            self.driver = webdriver.Edge(service=service, options=edge_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            logger.info(" Edge browser initialized successfully")
        except Exception as e:
            logger.error(f" Failed to initialize Edge: {e}")
            raise
    
    def navigate(self, url: str, wait_time: int = 10) -> bool:
        """Navigate to URL with explicit wait for page load"""
        try:
            logger.info(f"Navigating to: {url}")
            self.driver.get(url)
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            logger.info(f" Page loaded: {self.driver.title}")
            return True
        except TimeoutException:
            logger.error(f" Timeout loading {url}")
            return False
        except Exception as e:
            logger.error(f" Navigation error: {e}")
            return False
    
    def take_screenshot(self, filename: str = "screenshot.png") -> bool:
        """Save a screenshot of the current page"""
        try:
            self.driver.save_screenshot(filename)
            logger.info(f" Screenshot saved: {filename}")
            return True
        except Exception as e:
            logger.error(f" Screenshot failed: {e}")
            return False
    
    def find_element_safe(self, by: By, value: str, timeout: int = 10):
        """Safely find an element with explicit wait"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.presence_of_element_located((by, value)))
        except TimeoutException:
            logger.warning(f" Element not found: {by}='{value}'")
            return None
    
    def find_elements_safe(self, by: By, value: str, timeout: int = 10):
        """Safely find multiple elements"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.presence_of_all_elements_located((by, value)))
        except TimeoutException:
            logger.warning(f"Elements not found: {by}='{value}'")
            return []
    
    def click_safe(self, by: By, value: str, timeout: int = 10) -> bool:
        """Safely click an element"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.element_to_be_clickable((by, value)))
            element.click()
            logger.info(f" Clicked: {by}='{value}'")
            return True
        except TimeoutException:
            logger.warning(f" Could not click: {by}='{value}'")
            return False
        except Exception as e:
            logger.error(f" Click error: {e}")
            return False
    
    def type_text(self, by: By, value: str, text: str, timeout: int = 10) -> bool:
        """Safely type text into an input field"""
        try:
            element = self.find_element_safe(by, value, timeout)
            if element:
                element.clear()
                element.send_keys(text)
                logger.info(f" Typed text into: {by}='{value}'")
                return True
            return False
        except Exception as e:
            logger.error(f" Type error: {e}")
            return False
    
    def execute_js(self, script: str):
        """Execute JavaScript and return result"""
        return self.driver.execute_script(script)
    
    def get_page_info(self):
        """Get current page information"""
        return {
            'title': self.driver.title,
            'url': self.driver.current_url,
            'height': self.execute_js("return document.body.scrollHeight;")
        }
    
    def switch_to_tab(self, index: int):
        """Switch to a specific tab/window"""
        handles = self.driver.window_handles
        if 0 <= index < len(handles):
            self.driver.switch_to.window(handles[index])
            logger.info(f" Switched to tab {index}")
            return True
        return False
    
    def open_new_tab(self, url: str):
        """Open a new tab with URL"""
        self.driver.execute_script(f"window.open('{url}', '_blank');")
        logger.info(f" Opened new tab: {url}")
    
    def quit(self):
        """Cleanly close the browser"""
        if self.driver:
            self.driver.quit()
            logger.info(" Browser closed")



# EXAMPLE 1: Basic Navigation (DEFAULT)

def example_basic_navigation():
    """Navigate to a website and extract info"""
    print("\n" + "="*60)
    print(" EXAMPLE 1: Basic Navigation")
    print("="*60)
    
    bot = EdgeBot(headless=False)
    try:
        bot.navigate("https://www.example.com")
        
        info = bot.get_page_info()
        print(f"\n Page Title: {info['title']}")
        print(f" URL: {info['url']}")
        print(f" Page Height: {info['height']}px")
        
        heading = bot.find_element_safe(By.TAG_NAME, "h1")
        if heading:
            print(f" Heading: '{heading.text}'")
        
        bot.take_screenshot("example_basic.png")
        print("\n Basic navigation completed!")
        
    finally:
        bot.quit()



# EXAMPLE 2: Google Search (HEADLESS)

def example_google_search():
    """Search Google and print results"""
    print("\n" + "="*60)
    print(" EXAMPLE 2: Google Search (Headless)")
    print("="*60)
    
bot = EdgeBot(headless=False)  # Shows browser window
try:
        bot.navigate("https://www.google.com")
        
        # Type search query
        search_box = bot.find_element_safe(By.NAME, "q")
        if search_box:
            search_box.send_keys("Silicon Valley")
            search_box.send_keys(Keys.RETURN)
            
            # Wait for results
            time.sleep(2)
            
            # Print top 5 results
            results = bot.find_elements_safe(By.CSS_SELECTOR, "h3")
            print(f"\n Top Search Results:")
            for i, result in enumerate(results[:5], 1):
                print(f"   {i}. {result.text}")
            
            bot.take_screenshot("google_search.png")
            print("\n Google search completed!")
        
finally:
        bot.quit()



# EXAMPLE 3: Form Filling & Submission

def example_form_filling():
    """Fill and submit a test form"""
    print("\n" + "="*60)
    print(" EXAMPLE 3: Form Filling")
    print("="*60)
    
    bot = EdgeBot(headless=False)
    try:
        # Using a test form page
        bot.navigate("https://www.selenium.dev/selenium/web/web-form.html")
        
        # Fill text input
        bot.type_text(By.NAME, "my-text", "Hello Selenium!", timeout=10)
        
        # Fill password (if exists)
        bot.type_text(By.NAME, "my-password", "SecretPassword123", timeout=10)
        
        # Select textarea
        bot.type_text(By.NAME, "my-textarea", "This is a test message\nLine 2\nLine 3", timeout=10)
        
        # Click submit button
        bot.click_safe(By.CSS_SELECTOR, "button[type='submit']", timeout=10)
        
        # Wait and take screenshot
        time.sleep(2)
        bot.take_screenshot("form_submitted.png")
        
        print("\n Form filling completed!")
        
    finally:
        bot.quit()



# EXAMPLE 4: Multiple Tabs/Windows

def example_multiple_tabs():
    """Open and switch between multiple tabs"""
    print("\n" + "="*60)
    print(" EXAMPLE 4: Multiple Tabs")
    print("="*60)
    
    bot = EdgeBot(headless=False)
    try:
        # Open first page
        bot.navigate("https://www.example.com")
        print(f"\n Tab 0: {bot.driver.current_url}")
        
        # Open new tabs
        bot.open_new_tab("https://www.google.com")
        bot.open_new_tab("https://www.github.com")
        
        # Switch and print each tab
        for i in range(len(bot.driver.window_handles)):
            bot.switch_to_tab(i)
            print(f" Tab {i}: {bot.driver.current_url} - {bot.driver.title}")
        
        # Switch back to first tab
        bot.switch_to_tab(0)
        print(f"\n Back to Tab 0: {bot.driver.current_url}")
        
        bot.take_screenshot("multiple_tabs.png")
        print("\n Multiple tabs completed!")
        
    finally:
        bot.quit()



# EXAMPLE 5: JavaScript Execution

def example_javascript():
    """Execute custom JavaScript on the page"""
    print("\n" + "="*60)
    print(" EXAMPLE 5: JavaScript Execution")
    print("="*60)
    
    bot = EdgeBot(headless=False)
    try:
        bot.navigate("https://www.example.com")
        
        # Get page title via JS
        title = bot.execute_js("return document.title;")
        print(f"\n Title via JS: {title}")
        
        # Get all links
        links = bot.execute_js("return document.getElementsByTagName('a').length;")
        print(f" Number of links: {links}")
        
        # Scroll to bottom
        bot.execute_js("window.scrollTo(0, document.body.scrollHeight);")
        print(" Scrolled to bottom")
        
        # Change background color (visual demo)
        bot.execute_js("document.body.style.backgroundColor = '#ffeb3b';")
        time.sleep(2)
        
        # Get console logs (if any)
        logs = bot.driver.get_log('browser')
        if logs:
            print(f"\n Browser console logs: {len(logs)} entries")
        
        bot.take_screenshot("js_execution.png")
        print("\n JavaScript execution completed!")
        
    finally:
        bot.quit()



# EXAMPLE 6: Wait for Dynamic Content

def example_explicit_waits():
    """Demonstrate proper waiting for elements"""
    print("\n" + "="*60)
    print(" EXAMPLE 6: Explicit Waits")
    print("="*60)
    
    bot = EdgeBot(headless=False)
    try:
        bot.navigate("https://www.example.com")
        
        wait = WebDriverWait(bot.driver, 10)
        
        # Wait for element to be visible
        element = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1")))
        print(f"\n Element visible: '{element.text}'")
        
        # Wait for element to be clickable
        link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "More information...")))
        print(f"️ Element clickable: '{link.text}'")
        
        # Wait for URL to contain specific text
        print(f" Current URL contains 'example': {'example' in bot.driver.current_url}")
        
        bot.take_screenshot("explicit_waits.png")
        print("\n Explicit waits completed!")
        
    finally:
        bot.quit()



# EXAMPLE 7: Scrape Data from Page

def example_web_scraping():
    """Scrape data from a webpage"""
    print("\n" + "="*60)
    print(" EXAMPLE 7: Web Scraping")
    print("="*60)
    
    bot = EdgeBot(headless=False)
    try:
        bot.navigate("https://www.example.com")
        
        # Scrape all links
        links = bot.driver.find_elements(By.TAG_NAME, "a")
        print(f"\n Found {len(links)} link(s):")
        for i, link in enumerate(links, 1):
            href = link.get_attribute("href")
            text = link.text.strip() or "[no text]"
            print(f"   {i}. {text} → {href}")
        
        # Scrape all paragraphs
        paragraphs = bot.driver.find_elements(By.TAG_NAME, "p")
        print(f"\n Found {len(paragraphs)} paragraph(s):")
        for i, p in enumerate(paragraphs, 1):
            text = p.text.strip()[:100]  # First 100 chars
            print(f"   {i}. {text}...")
        
        # Save data to file
        with open("scraped_data.txt", "w", encoding="utf-8") as f:
            f.write(f"URL: {bot.driver.current_url}\n")
            f.write(f"Title: {bot.driver.title}\n")
            f.write(f"\nLinks ({len(links)}):\n")
            for link in links:
                f.write(f"  - {link.text.strip() or '[no text]'}: {link.get_attribute('href')}\n")
        
        print("\n Data saved to 'scraped_data.txt'")
        bot.take_screenshot("web_scraping.png")
        print("\n Web scraping completed!")
        
    finally:
        bot.quit()



# MAIN EXECUTION

if __name__ == "__main__":
    print("=" * 60)
    print(" Selenium Edge Browser - Complete Examples")
    print("=" * 60)
    print("\nSelect which example to run (uncomment in code):\n")
    print("  1. example_basic_navigation()")
    print("  2. example_google_search()")
    print("  3. example_form_filling()")
    print("  4. example_multiple_tabs()")
    print("  5. example_javascript()")
    print("  6. example_explicit_waits()")
    print("  7. example_web_scraping()")
    print("=" * 60)
    
    #  UNCOMMENT THE EXAMPLE YOU WANT TO RUN:
    
    #example_basic_navigation()     #  Default: Basic navigation
    #example_google_search()         #  Headless Google search
    example_form_filling()        # Fill and submit forms
    # example_multiple_tabs()       #  Manage multiple tabs
    # example_javascript()          #  Execute JavaScript
    # example_explicit_waits()      #  Wait for dynamic content
    # example_web_scraping()        #  Scrape data from pages
    
    print("\n" + "=" * 60)
    print(" All done!")
    print("=" * 60)