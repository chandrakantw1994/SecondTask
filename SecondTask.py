import requests
import hashlib
import ctypes

def get_auth_challenge(api_url):
    request_xml = """
    <iq>
        <query xmlns="admin:iq:rpc">
            <commandname>getauthchallenge</commandname>
            <commandparams>
                <authtype>1</authtype>
            </commandparams>
        </query>
    </iq>
    """

    response = requests.post(api_url, data=request_xml)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Error: Authentication challenge request failed (Status code: {response.status_code})")
        exit(1)

def create_auth_token(challenge, username, password):
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    auth_token = hashlib.md5((challenge + hashed_password).encode()).hexdigest()
    return auth_token

def get_account_list(api_url, auth_token):
    request_xml = f"""
    <iq>
        <query xmlns="admin:iq:rpc">
            <commandname>getaccountlist</commandname>
            <commandparams>
                <authtoken>{auth_token}</authtoken>
            </commandparams>
        </query>
    </iq>
    """

    response = requests.post(api_url, data=request_xml)
    if response.status_code == 200:
        # Parse the response to extract account information
        # (you may need to adapt this based on the actual API response format)
        account_list = response.content
        return account_list
    else:
        print(f"Error: Get account list request failed (Status code: {response.status_code})")
        exit(1)

def logout_user(api_url, auth_token):
    request_xml = f"""
    <iq sid="{auth_token}">
        <query xmlns="admin:iq:rpc">
            <commandname>logout</commandname>
            <commandparams/>
        </query>
    </iq>
    """

    response = requests.post(api_url, data=request_xml)
    if response.status_code == 200:
        print("User logged out successfully.")
    else:
        print(f"Error: Logout request failed (Status code: {response.status_code})")

if __name__ == "__main__":
    api_url = "http://localhost/icewarpapi/"
    auth_challenge = get_auth_challenge(api_url)
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    auth_token = create_auth_token(auth_challenge, username, password)
    print(f"Authentication token: {auth_token}")

    accounts = get_account_list(api_url, auth_token)
    account_count = len(accounts.split("\n"))  # Assuming one account per line
    print(f"Total accounts on the domain: {account_count}")

    # Log out the user
    logout_user(api_url, auth_token)
