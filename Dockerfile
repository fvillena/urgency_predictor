FROM ubuntu

RUN apt update
RUN apt install python3 chromium-browser chromium-chromedriver xvfb bash python3-pip cron -y


RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install selenium ipython PyVirtualDisplay xlrd pystan fbprophet flask flask_sqlalchemy flask_marshmallow marshmallow-sqlalchemy plotly --no-install-recommends


ADD . /usr/wd/urgency_predictor/.

RUN chmod 755 /usr/wd/urgency_predictor/daemon.sh /usr/wd/urgency_predictor/entry.sh
RUN crontab /usr/wd/urgency_predictor/crontab.txt
RUN bash /usr/wd/urgency_predictor/entry.sh
CMD ["python3","/usr/wd/urgency_predictor/download_and_predict.py"]
CMD ["python3","/usr/wd/urgency_predictor/app.py"]