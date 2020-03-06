from src.predictor import Predictor
import os
wd = os.getcwd() + "/"
p = Predictor(wd+"../urgency_predictor_data/data.sqlite")
p.fit()
p.predict(60)
p.write()
print("foo")