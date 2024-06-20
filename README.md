# llm-agent-fitness-app

Application to help someone track their total calories and protein consumed in a day using a text based variable input which connects with an openai langchain agent equipped with a nutrionx api tool that gets nutrition information for each of the different food components. All of this is wrapped up in a simple node and react based front end.

### Usage

1. To use, download code
2. Create openai (cost) and nutritionx (free) accounts
3. Install npm
4. Create a 'secrets.json' file with the content:
   {
   "OPENAI_API_KEY": "",
   "APPLICATION_ID": "",
   "APPLICATION_KEY": ""
   }
5. cd into front_end/reactapp and run `npm start`
6. cd into back_end and run `python main.py`
