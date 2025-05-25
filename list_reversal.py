# Finance calculations list reversal example
all_calculations = ['[24/05/2025] Loan: Amount: $50,000.00, Rate: 5.5%, Term: 10 years → Monthly: $542.43',
                   '[23/05/2025] Mortgage: Home: $750,000.00, Down: $150,000.00, Rate: 6.2% → Monthly: $4,234.56, LVR: 80.0%',
                   '[22/05/2025] Investment: Initial: $10,000.00, Annual: $5,000.00, Return: 7%, Period: 20 years → Final: $245,678.90',
                   '[21/05/2025] Retirement: Age: 30→65, Balance: $25,000.00, Salary: $70,000.00 → Retirement Balance: $892,345.67',
                   '[20/05/2025] Loan: Amount: $25,000.00, Rate: 4.8%, Term: 5 years → Monthly: $469.12',
                   '[19/05/2025] Investment: Initial: $5,000.00, Annual: $2,000.00, Return: 8%, Period: 15 years → Final: $89,456.78']

newest_first = list(reversed(all_calculations))

print("==== Oldest to Newest for File ====")
for item in all_calculations:
    print(item)

print()

print("==== Most Recent First ====")
for item in newest_first:
    print(item)