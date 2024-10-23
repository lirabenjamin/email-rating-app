1. Get the documents you want to rate. save them in a parquet file with the columns 'text_id' and 'text'
Save this in 'instance/texts_to_rate.parquet'
Use the pandas_to_json.py file to save the emails2.json file, which is going to be rated.

2. Edit the instance/users.json file to choose the actual users to be created

3. Edit the instance/questions.json file to choose the prompts to be rated

4. Make sure you have the right number of questions in  the app/routes.py file, within the rate_email function

5. Go to mongodb and delete any extisitng data to start fresh. Don't delete the database, just the contents.

I think that repsonses.rxt and read_data.py are not needed.

redeploy the app to heroku