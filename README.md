**How-to for GatherWeather API**

Follow the steps below to start receiving your weather forecast updates:

* Register
* Subscribe for weather forecast in your city. Specify preferred frequency
* Receive weather updates via email 

**1. Registration**

URL: https://gatherweather.azurewebsites.net/api/user/register/

HTTP request: POST

Parameters:
- username
- password
- password2
- email

**2. Get JWT token**
    
URL: https://gatherweather.azurewebsites.net/api/user/token/
    
HTTP request: POST
    
Parameters:
- username
- password

**3. Refresh JWT token**

URL: https://gatherweather.azurewebsites.net/api/user/token/refresh/
    
HTTP request: POST                                                                                                                                                                                
    
Parameters:
- refresh (use your refresh JWT token)
 
**4. View current subscriptions**

URL: https://gatherweather.azurewebsites.net/api/subscriptions/

HTTP request: GET

Authorization: Bearer token. Provide your JWT access token

**5. Create a new subscription**
    
URL: https://gatherweather.azurewebsites.net/api/subscriptions/
    
HTTP request: POST  

Authorization: Bearer token. Provide your JWT access token

Parameters:
- city_name
- country_code (Two-letter)
- frequency

**6. Update subscription**

URL: https://gatherweather.azurewebsites.net/api/subscriptions/<<int:pk>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            >/

HTTP request: PUT

Authorization: Bearer token. Provide your JWT access token

Parameters:
- city_name
- country_code (Two-letter)
- frequency

**7. Delete subscription**

URL: https://gatherweather.azurewebsites.net/api/subscriptions/<<int:pk>>/

HTTP request: DELETE

Authorization: Bearer token. Provide your JWT access token     

