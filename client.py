import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

player_name = input("Enter your name: ")
print("Choose one: Rock, Paper, or Scissors")
choice = input("Your choice: ").strip().lower()

response = proxy.submit_choice(player_name, choice)
print(response)
