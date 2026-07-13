import unittest

from app.services.payroll import calculate_statutory_deductions


class PayrollContributionTests(unittest.TestCase):
    def test_pagibig_uses_one_percent_at_or_below_1500(self):
        result = calculate_statutory_deductions(1500)

        self.assertEqual(result["pagibig_deduction"], 15)

    def test_pagibig_caps_employee_share_at_200(self):
        result = calculate_statutory_deductions(50000)

        self.assertEqual(result["pagibig_deduction"], 200)

    def test_philhealth_uses_minimum_salary_base(self):
        result = calculate_statutory_deductions(8000)

        self.assertEqual(result["philhealth_deduction"], 250)

    def test_philhealth_caps_at_maximum_salary_base(self):
        result = calculate_statutory_deductions(120000)

        self.assertEqual(result["philhealth_deduction"], 2500)

    def test_sss_uses_minimum_monthly_salary_credit(self):
        result = calculate_statutory_deductions(3000)

        self.assertEqual(result["sss_deduction"], 250)

    def test_sss_caps_at_maximum_monthly_salary_credit(self):
        result = calculate_statutory_deductions(50000)

        self.assertEqual(result["sss_deduction"], 1750)

    def test_sss_uses_nearest_500_peso_salary_credit(self):
        result = calculate_statutory_deductions(10240)

        self.assertEqual(result["sss_deduction"], 500)


if __name__ == "__main__":
    unittest.main()
