import random


def welcome_message():
    print("\n" + "=" * 50)
    print("WELCOME TO PASSWORD GENERATOR")
    print("=" * 50 + "\n")


def validate_include(input):
    lis = input.split()
    if len(lis) < 2:
        return False
    if len(lis) > 4:
        return False
    for i in lis:
        if (not i.isdigit()) or int(i) < 0 or int(i) > 5:
            return False
    return True


def password_generator(pass_length, included_types):
    included_types = included_types.split()
    pass_length = int(pass_length)
    included_types = list(set(included_types))
    pass_list = []
    uppercase_letters = [x for x in range(65,91)]
    lowercase_letters = [x for x in range(97,123)]
    numbers = [x for x in range(48, 58)]
    symbols = [x for x in range(33, 127)]
    symbols = list(set(symbols) - (set(uppercase_letters + lowercase_letters + numbers)))
    final_pass = ""
    for i in included_types:
        if i == "1":
            pass_list += uppercase_letters
        elif i == "2":
            pass_list += lowercase_letters
        elif i == "3":
            pass_list += numbers
        else:
            pass_list += symbols
    for _ in range(pass_length):
        temp = random.choice(pass_list)
        final_pass += chr(int(temp))
    return final_pass



def main():
    length = input("Enter the length of the password?(Minimum length must be 8): ")
    if length.isdigit() and int(length) >= 8:
        print("\n")
        print("="*50)
        print("Password generator is valid!")
        print("="*50 + "\n")
        print("What type of character you want to include. \nYou must at least select two from the following.")
        print("1. Include uppercase letters\n2. Include lowercase letters\n3. Include numbers\n4. Include symbols")
        print("Enter the numbers corresponding to your desired character types (e.g., enter 1 3 4 for uppercase, numbers, and symbols).")
        while True:
            include = input("Enter your choice: ").strip()
            valid = validate_include(include)
            if valid:
                break
            print("Enter valid input as shown in the example above.")
        print("\n\nYour newly generated password is: " + password_generator(length, include))
    else:
        print("Please enter a valid input.")
        main()


welcome_message()
main()
