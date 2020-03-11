FROM debian

RUN apt update
RUN apt install python3 build-essential python-dev python3-dev chromium chromium-driver xvfb bash python3-setuptools python3-pip cron --no-install-recommends -y


RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install selenium ipython PyVirtualDisplay xlrd pystan fbprophet flask flask_sqlalchemy flask_marshmallow marshmallow-sqlalchemy flask-cors plotly


ADD . /usr/wd/urgency_predictor/.

RUN chmod 755 /usr/wd/urgency_predictor/daemon.sh /usr/wd/urgency_predictor/entry.sh
RUN crontab /usr/wd/urgency_predictor/crontab.txt
WORKDIR /usr/wd/urgency_predictor/
CMD ["bash","entry.sh"]