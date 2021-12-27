# Found Bugs

## API Tests

### 1. It's possible to delete non existent cat

- Send DELETE request to /api/kitties/Christmas with header = "Authorization": "Bearer adminToken",
where "Christmas" is non-existent cat's name.

    **Actual result:** Status code is 200.

    **Expected result:** Status code is 400. Error is "Unknown kitty requested to be deleted".


### 2. It's possible to delete cat by user

- Send DELETE request to /api/kitties/Harri with header = "Authorization": "Bearer userToken",
where "Harri" is existent cat's name.

    **Actual result:** Status code is 200.

    **Expected result:** Status code is 401.

    *Information from functional requirements:*
> 5.Only admin users are able to delete cats from the list. 


## Manual Tests

### 1. There is no error about invalid credentials in login page

- Fill in username: "Frog" and password "Green". 
Where username and password of non-existent user.
- Click on Log in button.

    **Actual result:** There is no error about invalid credentials.

    **Expected result:** User should know when credentials not right.

### 2. It's possible to rename cat to existent name via copy and past this name

- Login to the site with valid credentials.
- Copy "Sergey" name and past its to "Peter".
- Save changes.

    **Actual result:** Changes successfully saved. There are two cats with "Sergey" name.

    **Expected result:** Save (diskette icon) button should be not allowed.


```
Please note that the name copied as a web element. 
We can see it on the Network tab in Chrome DevTools:
PUT request with newName = "<span style="font-size: 26.6667px;">Sergey</span>"
```
