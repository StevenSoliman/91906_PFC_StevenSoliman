"""
Personal Finance Calculation Module - New Zealand Edition
Contains all calculation functions for the Personal Finance Calculator
Includes NZ-specific features like GST, KiwiSaver, and local formatting
"""

# New Zealand specific constants
NZ_GST_RATE = 0.15  # 15% GST in New Zealand
KIWISAVER_MINIMUM_RATE = 0.03  # 3% minimum employee contribution
KIWISAVER_EMPLOYER_RATE = 0.03  # 3% employer contribution
KIWISAVER_GOVERNMENT_CONTRIBUTION = 521.43  # Annual government contribution (2024)


def format_nz_currency(amount):
    """
    Format amount as New Zealand currency

    Args:
        amount: Amount to format

    Returns:
        str: Formatted currency string (e.g., "$1,234.56 NZD")
    """
    return f"${amount:,.2f} NZD"


def calculate_gst_inclusive(amount):
    """
    Calculate GST-inclusive price from GST-exclusive amount

    Args:
        amount: GST-exclusive amount

    Returns:
        tuple: (gst_inclusive_amount, gst_amount)
    """
    gst_amount = amount * NZ_GST_RATE
    gst_inclusive_amount = amount + gst_amount
    return gst_inclusive_amount, gst_amount


def calculate_gst_exclusive(gst_inclusive_amount):
    """
    Calculate GST-exclusive amount from GST-inclusive price

    Args:
        gst_inclusive_amount: GST-inclusive amount

    Returns:
        tuple: (gst_exclusive_amount, gst_amount)
    """
    gst_exclusive_amount = gst_inclusive_amount / (1 + NZ_GST_RATE)
    gst_amount = gst_inclusive_amount - gst_exclusive_amount
    return gst_exclusive_amount, gst_amount


def calculate_kiwisaver_contributions(annual_salary, employee_rate=None, include_employer=True,
                                      include_government=True):
    """
    Calculate KiwiSaver contributions

    Args:
        annual_salary: Annual salary before tax
        employee_rate: Employee contribution rate (3%, 4%, 6%, 8%, or 10%)
        include_employer: Whether to include 3% employer contribution
        include_government: Whether to include government contribution

    Returns:
        dict: Dictionary with contribution breakdown
    """
    if employee_rate is None:
        employee_rate = KIWISAVER_MINIMUM_RATE

    # Convert percentage to decimal if needed
    if employee_rate > 1:
        employee_rate = employee_rate / 100

    employee_contribution = annual_salary * employee_rate
    employer_contribution = annual_salary * KIWISAVER_EMPLOYER_RATE if include_employer else 0
    government_contribution = KIWISAVER_GOVERNMENT_CONTRIBUTION if include_government else 0

    total_annual_contribution = employee_contribution + employer_contribution + government_contribution

    return {
        'employee_contribution': employee_contribution,
        'employer_contribution': employer_contribution,
        'government_contribution': government_contribution,
        'total_annual_contribution': total_annual_contribution,
        'employee_rate': employee_rate * 100
    }


def calculate_loan_payment(principal, annual_rate, years):
    """
    Calculate monthly loan payment and total interest (NZ Edition)

    Args:
        principal: Loan amount in NZD
        annual_rate: Annual interest rate as percentage
        years: Loan term in years

    Returns:
        tuple: (monthly_payment, total_interest, total_amount)
    """
    monthly_rate = annual_rate / 100 / 12
    months = years * 12

    if monthly_rate == 0:  # Handle 0% interest rate
        monthly_payment = principal / months
        total_interest = 0
    else:
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
        total_interest = monthly_payment * months - principal

    total_amount = principal + total_interest

    return monthly_payment, total_interest, total_amount


def calculate_nz_mortgage_payment(home_price, down_payment, annual_rate, years, include_insurance=True):
    """
    Calculate monthly mortgage payment and total cost (NZ specific)

    Args:
        home_price: Total price of the home in NZD
        down_payment: Down payment amount in NZD
        annual_rate: Annual interest rate as percentage
        years: Loan term in years
        include_insurance: Whether to include mortgage protection insurance estimate

    Returns:
        dict: Dictionary with mortgage details
    """
    loan_amount = home_price - down_payment
    monthly_rate = annual_rate / 100 / 12
    months = years * 12

    if monthly_rate == 0:  # Handle 0% interest rate
        monthly_payment = loan_amount / months
        total_cost = loan_amount
    else:
        monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** months) / (
                    (1 + monthly_rate) ** months - 1)
        total_cost = monthly_payment * months

    # Calculate LVR (Loan to Value Ratio) - important for NZ mortgages
    lvr = (loan_amount / home_price) * 100

    # Estimate mortgage protection insurance (roughly 0.5-1% of loan amount annually)
    insurance_annual = loan_amount * 0.007 if include_insurance else 0  # 0.7% estimate
    insurance_monthly = insurance_annual / 12

    total_monthly_payment = monthly_payment + insurance_monthly

    return {
        'loan_amount': loan_amount,
        'monthly_payment': monthly_payment,
        'total_cost': total_cost,
        'total_interest': total_cost - loan_amount,
        'lvr': lvr,
        'insurance_monthly': insurance_monthly,
        'total_monthly_payment': total_monthly_payment,
        'requires_lmi': lvr > 80  # LMI typically required if LVR > 80% in NZ
    }


def calculate_investment_growth_nz(initial_investment, annual_contribution, annual_return_rate, years,
                                   include_tax=True):
    """
    Calculate investment growth over time with NZ tax considerations

    Args:
        initial_investment: Starting investment amount in NZD
        annual_contribution: Amount added each year in NZD
        annual_return_rate: Expected annual return as percentage
        years: Investment period in years
        include_tax: Whether to include PIE tax estimates (28% for high earners)

    Returns:
        dict: Investment projection details
    """
    rate = annual_return_rate / 100

    # Adjust for PIE tax if applicable (assuming 28% PIE rate for conservative estimate)
    if include_tax:
        effective_rate = rate * (1 - 0.28)  # 28% PIE tax rate
    else:
        effective_rate = rate

    # Start with initial investment growing
    final_value = initial_investment * (1 + effective_rate) ** years

    # Add contributions with compound growth
    for year in range(int(years)):
        final_value += annual_contribution * (1 + effective_rate) ** (years - year - 1)

    total_contributions = initial_investment + (annual_contribution * years)
    total_growth = final_value - total_contributions

    # Calculate pre-tax equivalent if tax was considered
    if include_tax:
        pre_tax_equivalent = total_growth / (1 - 0.28)
        tax_paid_estimate = pre_tax_equivalent - total_growth
    else:
        pre_tax_equivalent = total_growth
        tax_paid_estimate = 0

    return {
        'final_value': final_value,
        'total_contributions': total_contributions,
        'total_growth': total_growth,
        'effective_annual_return': effective_rate * 100,
        'tax_paid_estimate': tax_paid_estimate,
        'pre_tax_growth': pre_tax_equivalent
    }


def calculate_kiwisaver_retirement(current_age, retirement_age, current_balance, annual_salary,
                                   employee_rate=3, expected_return=5, salary_growth=2):
    """
    Calculate KiwiSaver retirement projection

    Args:
        current_age: Current age
        retirement_age: Planned retirement age (minimum 65 for NZ Super)
        current_balance: Current KiwiSaver balance
        annual_salary: Current annual salary
        employee_rate: Employee contribution rate (3, 4, 6, 8, or 10)
        expected_return: Expected annual return percentage
        salary_growth: Annual salary growth percentage

    Returns:
        dict: KiwiSaver retirement projection
    """
    years_to_retirement = retirement_age - current_age
    return_rate = expected_return / 100
    growth_rate = salary_growth / 100

    # Calculate KiwiSaver balance at retirement
    balance = current_balance
    current_salary = annual_salary

    for year in range(years_to_retirement):
        # Calculate contributions for this year
        kiwisaver_contrib = calculate_kiwisaver_contributions(current_salary, employee_rate / 100)
        annual_contribution = kiwisaver_contrib['total_annual_contribution']

        # Grow existing balance and add contributions
        balance = balance * (1 + return_rate) + annual_contribution

        # Grow salary for next year
        current_salary *= (1 + growth_rate)

    # NZ Super estimate (April 2024 rates - married couple)
    nz_super_annual = 26364  # Approximate annual NZ Super for married couple after tax

    # 4% withdrawal rule for retirement savings to last ~30 years
    sustainable_withdrawal = balance * 0.04

    return {
        'projected_balance': balance,
        'annual_nz_super': nz_super_annual,
        'sustainable_annual_withdrawal': sustainable_withdrawal,
        'years_to_retirement': years_to_retirement
    }
