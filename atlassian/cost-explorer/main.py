import collections
import datetime
from enum import Enum


class PlanType(Enum):
    BASIC = "BASIC"
    STANDARD = "STANDARD"
    PREMIUM = "PREMIUM"


class Subscription:
    def __init__(self, name, plan, start_date, end_date = None) -> None:
        self.name = name
        self.start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
        self.plan = plan
        pass


class CostManager:
    def __init__(self) -> None:
        self.plan = {}
        self.subscriptions = collections.defaultdict(list)
        pass

    def add_plan(self, plan_type: PlanType, cost: float):
        self.plan[plan_type] = cost
    
    def add_subscription(self, customer, subscription):
        self.subscriptions[customer].append(subscription)
        pass
    
    def monthly_cost_list(self, customer):
        costs = [0] * 12
        for subscription in self.subscriptions[customer]:
            start_month = subscription.start_date.month
            end_month = 12
            if subscription.end_date:
                end_month = subscription.end_date.month 
            for month in range(start_month - 1, end_month):
                costs[month] +=  self.plan[subscription.plan]
        return [round(c, 2) for c in costs]
        pass

    def annual_cost(self, customer):
        return round(sum(self.monthly_cost_list(customer)), 2)
        pass

cost_manager = CostManager()

cost_manager.add_plan(PlanType.BASIC, 9.99)
cost_manager.add_plan(PlanType.STANDARD, 49.99)
cost_manager.add_plan(PlanType.PREMIUM, 249.99)


subscription = Subscription("Jira", PlanType.BASIC, "2025-05-17")
subscription1 = Subscription("Trello", PlanType.STANDARD, "2025-05-17")

customer = "Subhash"

cost_manager.add_subscription(customer, subscription)
cost_manager.add_subscription(customer, subscription1)

print(cost_manager.monthly_cost_list(customer))
print(cost_manager.annual_cost(customer))