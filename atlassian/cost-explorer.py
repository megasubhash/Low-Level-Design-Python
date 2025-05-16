


import collections
import datetime


class Plan:
    def __init__(self, id, price) -> None:
        self.id = id
        self.price = price
        pass
    
    def __str__(self) -> str:
        return f"{self.id}, {self.price}"


class Subscription:
    def __init__(self, product_name, plan_id, start_date, end_date = None) -> None:
        self.product_name = product_name
        self.plan_id = plan_id
        self.start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
        pass
class CostExplorer:
    def __init__(self) -> None:
        self.subscriptions = collections.defaultdict(list)
        self.pricing_plan = {}
        pass
    
    
    def add_subscription(self, customer_id, subscription):
        self.subscriptions[customer_id].append(subscription)

    def add_pricing_plan(self,plan):
        self.pricing_plan[plan.id] = plan
    def get_monthly_cost(self, customer_id):
        subs = self.subscriptions[customer_id]
        cost = [0.0] * 12

        for sub in subs:
            plan = self.pricing_plan[sub.plan_id]
            start_date = sub.start_date
            end_date = datetime.datetime.strptime("2025-12-31", '%Y-%m-%d')
            if sub.end_date:
                end_date = min(end_date, sub.end_date)
            
            if start_date > end_date:
                continue
            
            for month in range(start_date.month, end_date.month + 1):
                cost[month - 1] += round(plan.price,2)
            # print(start_date.month)
        return cost

    def get_annual_cost(self, customer_id):
        return round(sum(self.get_monthly_cost(customer_id)), 2)
        pass




plane1 = Plan("BASIC", 9.99)
plane2 = Plan("STANDARD", 49.99)
plane3 = Plan("PREMIUM", 249.99)

cost_explorer = CostExplorer()

cost_explorer.add_pricing_plan(plane1)
cost_explorer.add_pricing_plan(plane2)
cost_explorer.add_pricing_plan(plane3)
subscription1 = Subscription("Jira", "BASIC", "2022-02-10")
subscription2 = Subscription("Trello", "PREMIUM", "2022-03-10")
cost_explorer.add_subscription("C", subscription1)
cost_explorer.add_subscription("C", subscription2)

print(cost_explorer.get_monthly_cost("C"))
print(cost_explorer.get_annual_cost("C"))


