"""
Desktop automation module using pyppeteer.
"""
import asyncio
from pyppeteer import launch
from typing import Optional, Dict, Any

class DesktopAutomation:
    def __init__(self):
        self.browser = None
        self.page = None
        
    async def initialize(self):
        """Initialize the browser and create a new page."""
        if not self.browser:
            self.browser = await launch(
                headless=False,  # Set to True for headless mode
                args=['--start-maximized']
            )
            self.page = await self.browser.newPage()
            await self.page.setViewport({'width': 1920, 'height': 1080})
            
    async def navigate(self, url: str):
        """Navigate to a specific URL."""
        if not self.page:
            await self.initialize()
        await self.page.goto(url)
        
    async def click(self, selector: str):
        """Click an element on the page."""
        if not self.page:
            raise RuntimeError("Browser not initialized")
        await self.page.click(selector)
        
    async def type_text(self, selector: str, text: str):
        """Type text into an input field."""
        if not self.page:
            raise RuntimeError("Browser not initialized")
        await self.page.type(selector, text)
        
    async def get_text(self, selector: str) -> str:
        """Get text content from an element."""
        if not self.page:
            raise RuntimeError("Browser not initialized")
        element = await self.page.querySelector(selector)
        if element:
            return await self.page.evaluate('(element) => element.textContent', element)
        return ""
        
    async def screenshot(self, path: str):
        """Take a screenshot of the current page."""
        if not self.page:
            raise RuntimeError("Browser not initialized")
        await self.page.screenshot({'path': path})
        
    async def close(self):
        """Close the browser."""
        if self.browser:
            await self.browser.close()
            self.browser = None
            self.page = None

# Helper function to run async code
def run_async(coro):
    """Run an async coroutine in a synchronous context."""
    return asyncio.get_event_loop().run_until_complete(coro) 