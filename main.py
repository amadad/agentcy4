import datetime
import time
from textwrap import dedent

from crewai import Crew
from dotenv import load_dotenv
from tiktoken import Tokenizer
from tiktoken.models import Model

from trip_agents import TripAgents
from trip_tasks import TripTasks

load_dotenv()

class TripCrew:

  def __init__(self, origin, cities, date_range, interests):
    self.cities = cities
    self.origin = origin
    self.interests = interests
    self.date_range = date_range

  def run(self):
    agents = TripAgents()
    tasks = TripTasks()

    city_selector_agent = agents.city_selection_agent()
    local_expert_agent = agents.local_expert()
    travel_concierge_agent = agents.travel_concierge()

    identify_task = tasks.identify_task(
      city_selector_agent,
      self.origin,
      self.cities,
      self.interests,
      self.date_range
    )
    gather_task = tasks.gather_task(
      local_expert_agent,
      self.origin,
      self.interests,
      self.date_range
    )
    plan_task = tasks.plan_task(
      travel_concierge_agent, 
      self.origin,
      self.interests,
      self.date_range
    )

    crew = Crew(
      agents=[
        city_selector_agent, local_expert_agent, travel_concierge_agent
      ],
      tasks=[identify_task, gather_task, plan_task],
      verbose=True
    )

    result = crew.kickoff()
    return result

if __name__ == "__main__":
  print("## Welcome to Trip Planner Crew")
  print('-------------------------------')
  location = input(
    dedent("""
      From where will you be travelling from?
    """))
  cities = input(
    dedent("""
      What are the cities options you are intereseted in visiting?
    """))
  date_range = input(
    dedent("""
      What is the date range you are intereseted in traveling?
    """))
  interests = input(
    dedent("""
      What are some of your high level interests and hobbies?
    """))

def count_tokens(text):
    tokenizer = Tokenizer()
    model = Model()
    tokens = list(tokenizer.tokenize(text))
    token_count = model.count_tokens(tokens)
    return token_count

def calculate_cost(token_count):
    cost_per_token = 20.00 / 1000  # $20 per 1000 tokens
    cost = token_count * cost_per_token
    return cost

def save_to_markdown(result, location, date_range, duration, token, cost):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"/output/TripPlan_{location}_{date_range.replace(' ', '_')}_{date}.md"
    
    with open(filename, 'w') as f:
        f.write("########################\n")
        f.write("## Here is your Trip Plan\n")
        f.write("########################\n\n")
        f.write(result)
        f.write("\n\n## Additional Information\n")
        f.write(f"Duration: {duration} seconds\n")
        f.write(f"Token: {token}\n")
        f.write(f"Cost: {cost}\n")

start_time = time.time()
trip_crew = TripCrew(location, cities, date_range, interests)
result = trip_crew.run()
end_time = time.time()
duration = end_time - start_time

# Replace with the actual count of tokens in `result`
token = count_tokens(result)  # You need to define the count_tokens function

# Replace with the actual cost of the tokens
cost = calculate_cost(token)  # You need to define the calculate_cost function

save_to_markdown(result, location, date_range, duration, token, cost)