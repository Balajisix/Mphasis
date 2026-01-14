from guardrails import Guard, OnFailAction

rail = """ - name: phone type: string pattern: "^\\(?\\d{3}\\)?-?\\s*\\d{3}-?\\s*\\d{4}$" on_fail: exception """

guard = Guard(rails=rail)

try:
    guard.validate({"phone":"123-456-7890"})
    guard.validate({"phone":"invalid-number"})
except Exception as e:
    print("Error:\n", e)