from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
import pandas as pd

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

df = pd.read_csv("assignment_raw_rate.csv")

@app.route('/')
def index():
    return render_template('frontend.html')

@app.route('/calculate_premium', methods=['POST'])
def calculate_premium():
    data = request.get_json()
    ages = data['ages']
    sum_insured = data.get('sumInsured')
    sum_insured = float(sum_insured)
    city_tier = int(data['cityTier'])
    tenure = int(data['tenure'])
    
    # Perform premium calculation logic here using the provided data
    premium = calculate_premium_logic(ages, sum_insured, city_tier, tenure)
    
    # Store the calculated premium in MongoDB
    mongo.db.premiums.insert_one({'ages': ages, 'sum_insured': sum_insured, 'city_tier': city_tier, 'tenure': tenure, 'premium': premium})
    
    # Return the premium as a response
    response = {'premium': premium}
    return jsonify(response)

def calculate_premium_logic(ages, sum_insured, city_tier, tenure):
    # Implement your premium calculation logic here based on the rate card logic provided
    premium = 0

    try:
        if len(ages) == 1:
            age = int(ages[0])
            premium = df.loc[(df['Age'] == age) & (df['TierID'] == city_tier) & (df['Tenure'] == tenure) & (df['SumInsured'] == sum_insured), 'Rate'].values[0] * 1.00000
        elif len(ages) == 2:
            age1 = int(ages[0])
            age2 = int(ages[1])
            premium = (
                df.loc[(df['Age'] == age1) & (df['TierID'] == city_tier) & (df['Tenure'] == tenure) & (df['SumInsured'] == sum_insured), 'Rate'].values[0] +
                df.loc[(df['Age'] == age2) & (df['TierID'] == city_tier) & (df['Tenure'] == tenure) & (df['SumInsured'] == sum_insured), 'Rate'].values[0] * 0.5
            ) * 1.0000
            
            
        elif len(ages) == 3:
            age1 = int(ages[0])
            age2 = int(ages[1])
            age3 = int(ages[2])
            premium = (
                df.loc[(df['Age'] == age1) & (df['TierID'] == city_tier) & (df['Tenure'] == tenure) & (df['SumInsured'] == sum_insured), 'Rate'].values[0] +
                df.loc[(df['Age'] == age2) & (df['TierID'] == city_tier) & (df['Tenure'] == tenure) & (df['SumInsured'] == sum_insured), 'Rate'].values[0] * 0.5 +
                df.loc[(df['Age'] == age3) & (df['TierID'] == city_tier) & (df['Tenure'] == tenure) & (df['SumInsured'] == sum_insured), 'Rate'].values[0] * 0.5
            ) * 1.00000
        # Add more conditions for other combinations based on the rate card logic
    except KeyError:
        # Handle the missing column error
        premium = None  # or any default value or error handling code

    return premium

if __name__ == '__main__':
    app.run(debug=True)
