# !WIP: NBA Schedule Bot
## Bot的功能
- Ask about game schedule 問行程
    - by star
    - by team
    - by date
    - by sport center
    - by team pairs
    - by season status (pre-season, seasonal, playoff)
- Ask state 問
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
### 1. Web Crawler
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
### 2. Database
    - Sqlite
    
### 3. Bot (WIP) 
    - IM: Line
    - Server: Heroku + Flask API
    - Responses: ??

## Heroku 架設 （WIP）
(參考[XiaoSean](https://xiaosean.github.io/server/2018-04-11-Flask_Heroku/))
- Register a Heroku account
- Download a Heroku CLI(Command Line Interface)
    ```
    $ heroku login
    ```
   之後可以使用cmd呼叫heroku指令
- create heroku virtual machine
    ```
    $ heroku create
    ```
- push your code to heroku git
    ```
    $ git push heroku master
    ```
    *這裡不要搞混，這邊只有把程式碼推到heroku，若project原來已連結github，並不會上傳到git上。
    
    上傳code至heroku方法跟git使用方式差不多，每次修改都需要重新commit上傳
    
- Test
    ```
    $ heroku open
    ```
- Log status
    ```
    heroku logs -tail
    ```
    或在官方heroku網頁中找出專案的dashboard

- Procfile - 設定/切換python的專案 （待補充）


## Requirements
- Python.__version__ = 3.7
- Packages requirements
    - Web Crawler
    ```
    $ pip install selenium
    $ pip install beautifulsoup4
    ```
    - LineBot
   
    ```
    $ pip install flask
    $ pip install line-bot-sdk
    ```
   
- Selenium driver (have to download your suitable driver first before crawling)
    - Chrome: https://sites.google.com/a/chromium.org/chromedriver/downloads
    - Edge:	https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
    - Firefox: https://github.com/mozilla/geckodriver/releases
    - Safari: https://webkit.org/blog/6900/webdriver-support-in-safari-10/


## References
1. https://pypi.org/project/selenium/
