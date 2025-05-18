import unittest

from main import Subscription, CostManager, PlanType

class Test(unittest.TestCase):

    def setUp(self):

        self.cost_manager = CostManager()

        self.cost_manager.add_plan(PlanType.BASIC, 9.99)
        self.cost_manager.add_plan(PlanType.STANDARD, 49.99)
        self.cost_manager.add_plan(PlanType.PREMIUM, 249.99)
        subscription = Subscription("Jira", PlanType.BASIC, "2025-05-17")

        self.customer = "Subhash"

        self.cost_manager.add_subscription(self.customer, subscription)
    def test_monthly_cost(self):

        self.assertEqual(len(self.cost_manager.monthly_cost_list(self.customer)),12)
    
    def test_annual_cost(self):
        self.assertEqual(self.cost_manager.annual_cost(self.customer),79.92)

if __name__ == "__main__":
    unittest.main()
