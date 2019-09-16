# NBA Schedule Bot (UC)
## Functions
- Ask about game schedule
    - by star
    - by team
    - by date
    - by sport center
    - by team pairs
    - by season status (pre-season, seasonal, playoff)
- Ask state
    - by star
    - by team
    - by game
    - by season
- Ask about Profile
    - by star
    - by team
- Ask about news
    ...
    
## Model Structure
- Web Crawler
    - Selenium
    ```python3
    class SeleniumRequester(BaseRequestHandler):
    @staticmethod
    def request(page, *args, **kwargs):
        # loading without pictures
        chromeOptions = webdriver.ChromeOptions()
        prefs = {'profile.managed_default_content_settings.images': 2}
        chromeOptions.add_experimental_option("prefs", prefs)
        
        driver = webdriver.Chrome(chrome_options=chromeOptions)
        driver.get(page)
        
        # DO_SOMETHING_ABOUT_THE_PAGE
        
        # SAVE PAGE AND QUIT
        html = driver.page_source
        driver.quit()
        
        return html
    ```
    - BeautifulSoup
    ```python3
    soup = BeautifulSoup(html, 'html') if html else None
    ```
- Database
    - Sqlite
    
- Bot 
    - IM: Line (pending)
    - Responses: ??


## Requirements
- Python.__version__ = 3.7
- Packages requirements
```
pip install selenium
pip install beautifulsoup4
```
- Selenium driver (have to download your suitable driver first before crawling)
    - Chrome: https://sites.google.com/a/chromium.org/chromedriver/downloads
    - Edge:	https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
    - Firefox: https://github.com/mozilla/geckodriver/releases
    - Safari: https://webkit.org/blog/6900/webdriver-support-in-safari-10/


## References
1. https://pypi.org/project/selenium/
