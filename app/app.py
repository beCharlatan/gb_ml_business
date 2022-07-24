from flask import Flask, render_template, request, url_for, redirect
import dill
import pandas as pd

app = Flask(__name__)

pd.set_option('display.max_columns', None)

with open('models/pipeline.dill', 'rb') as pipeline_file:
    model = dill.load(pipeline_file)


@app.route('/')
def root():
    predicted_price = request.args.get('predicted_price')
    predicted_df = request.args.get('predicted_df')
    print(predicted_price, 'price')
    return render_template('index.html', predicted_price=predicted_price, predicted_df=predicted_df)


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        manufacturer = request.form.get('Manufacturer')
        car_model = request.form.get('Model')
        prod_year = request.form.get('Prodyear')
        category = request.form.get('Category')
        airbags = request.form.get('Airbags')
        fuel_type = request.form.get('Fueltype')
        gear_box_type = request.form.get('Gearboxtype')
        drive_wheels = request.form.get('Drivewheels')
        color = request.form.get('Color')
        leather_interior = request.form.get('Leatherinterior')
        wheel = request.form.get('Wheel')
        levy = request.form.get('Levy')
        mileage = request.form.get('Mileage')
        engine_volume = request.form.get('Enginevolume')
        doors = request.form.get('Doors')

        predicted_df = pd.DataFrame({
            'Manufacturer': [manufacturer],
            'Model': [car_model],
            'Prod. year': [prod_year],
            'Category': [category],
            'Airbags': [airbags],
            'Fuel type': [fuel_type],
            'Gear box type': [gear_box_type],
            'Drive wheels': [drive_wheels],
            'Color': color,
            'Leather interior': [leather_interior],
            'Wheel': [wheel],
            'Levy': [levy],
            'Mileage': [mileage],
            'Engine volume': [engine_volume],
            'Doors': [doors]
        })

        preds = model.predict(predicted_df)

        return redirect(url_for('root', predicted_price=preds[0], predicted_df=predicted_df.to_html(index=False)))


if __name__ == '__main__':
    app.run(debug=True, port=8081, host='0.0.0.0')
