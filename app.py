from flask import Flask, render_template, request
import hashlib
import time

app = Flask(__name__)

# Common weak passwords (simulated attacker wordlist)
common_passwords = [
    "123456", "password", "12345678", "qwerty",
    "admin", "welcome", "letmein", "abc123",
    "iloveyou", "123123", "password123"
]

def check_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1
    if any(char.isupper() for char in password):
        score += 1
    if any(char.islower() for char in password):
        score += 1
    if any(char.isdigit() for char in password):
        score += 1
    if any(char in "!@#$%^&*()" for char in password):
        score += 1

    if score <= 2:
        return "Weak ❌"
    elif score <= 4:
        return "Medium ⚠️"
    else:
        return "Strong ✅"

def generate_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Dictionary attack simulation
def dictionary_attack(password):
    start_time = time.time()

    for guess in common_passwords:
        if guess == password:
            end_time = time.time()
            return True, round(end_time - start_time, 5)

    end_time = time.time()
    return False, round(end_time - start_time, 5)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = ""
    hash_value = ""
    attack_result = ""

    if request.method == 'POST':
        password = request.form['password']

        result = check_strength(password)
        hash_value = generate_hash(password)

        cracked, time_taken = dictionary_attack(password)

        if cracked:
            attack_result = f"❌ Password cracked in {time_taken} seconds (Dictionary Attack Successful)"
        else:
            attack_result = f"✅ Password resisted dictionary attack ({time_taken} seconds)"

    return render_template(
        'index.html',
        result=result,
        hash_value=hash_value,
        attack_result=attack_result
    )

if __name__ == '__main__':
    app.run(debug=True)
