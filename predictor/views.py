from django.shortcuts import render
import pickle
import pandas as pd
with open("car_evaluation_model.pkl", "rb") as file:
    model = pickle.load(file)


def home(request):

    result = None

    if request.method == "POST":

        buying = request.POST["buying"]
        maint = request.POST["maint"]
        doors = request.POST["doors"]
        persons = request.POST["persons"]
        lug_boot = request.POST["lug_boot"]
        safety = request.POST["safety"]

        input_data = pd.DataFrame([{
            "buying": buying,
            "maint": maint,
            "doors": doors,
            "persons": persons,
            "lug_boot": lug_boot,
            "safety": safety
        }])

        input_data = pd.get_dummies(input_data)

        expected_columns = [
            "buying_high",
            "buying_low",
            "buying_med",
            "buying_vhigh",
            "maint_high",
            "maint_low",
            "maint_med",
            "maint_vhigh",
            "doors_2",
            "doors_3",
            "doors_4",
            "doors_5more",
            "persons_2",
            "persons_4",
            "persons_more",
            "lug_boot_big",
            "lug_boot_med",
            "lug_boot_small",
            "safety_high",
            "safety_low",
            "safety_med"
        ]

        input_data = input_data.reindex(
            columns=expected_columns,
            fill_value=0
        )

        prediction = model.predict(input_data)[0]

        class_names = {
            0: "acceptable",
            1: "good",
            2: "unacceptable",
            3: "vgood"
        }

        result = class_names[prediction]

    return render(
        request,
        "predictor/home.html",
        {"result": result}
    )
