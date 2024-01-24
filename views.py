from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import Question, SkorUser, User
from . import db
import random
import locale
import requests
from datetime import datetime

views = Blueprint('views', __name__)
locale.setlocale(locale.LC_TIME, 'id_ID.utf8')

@views.route('/')
@login_required
def home():
    current_page = request.path
    secor = SkorUser.query.filter_by(idUser = current_user.id).first()
    time = datetime.now().strftime('%A ,%d %B %Y')
    return render_template("Index.html.jinja", user=current_user, current_page=current_page, skor=secor,time=time)


# @views.route('Ramalan-Cuaca')
@views.route("Ramalan-Cuaca", methods=['GET','POST'])
@login_required
def ramalan():
    current_page = request.path
    time = datetime.now().strftime('%A ,%d %B %Y')
    if request.method == 'POST':
        try:
            city = request.form.get('city')
            print(city)

            api_key = '5769664bd50b8c7ad72d9526bdb083af'
            # city = city
            country_code = 'ID'
            units = 'metric'

            # url = f'http://api.openweathermap.org/data/2.5/find?q=q={city},{country_code}&units={units}&appid={api_key}'
            url = f'http://api.openweathermap.org/data/2.5/forecast?q={city},{country_code}&units={units}&appid={api_key}'


            response = requests.get(url)
            data = response.json()

            forecast_data = data['list'][:24]

            forecast = []
            num = 0
            for entry in forecast_data:
                timestamp = entry['dt']
                date = datetime.utcfromtimestamp(timestamp).strftime('%A, %d %B %Y %H:%M:%S')
                temperature = entry['main']['temp']
                weather_description = entry['weather'][0]['description']
                
                num += 1

                translete = {
                    'clear sky': 'langit cerah',
                    'few clouds': 'berawan tipis',
                    'scattered clouds': 'berawan sebagian',
                    'broken clouds': 'berawan pecah-pecah',
                    'overcast clouds': 'berawan mendung',
                    'light rain': 'hujan ringan',
                    'moderate rain': 'hujan sedang',
                    'heavy rain': 'hujan deras',
                    'very heavy rain': 'hujan sangat deras',
                    'rain shower': 'hujan badai',
                    'light snow': 'salju ringan',
                    'moderate snow': 'salju sedang',
                    'heavy snow': 'salju deras',
                    'sleet': 'hujan salju',
                    'shower sleet': 'badai hujan salju',
                    'light shower snow': 'hujan salju ringan',
                    'shower snow': 'badai hujan salju',
                    'mist': 'kabut',
                    'smoke': 'asap',
                    'haze': 'kabut asap',
                    'sand/ dust whirls': 'puting beliung pasir/debu',
                    'fog': 'kabut tebal',
                    'sand': 'hujan pasir',
                    'dust': 'hujan debu',
                    'volcanic ash': 'hujan abu vulkanik',
                    'squalls': 'hujan lebat',
                    'tornado': 'puting beliung'
                }

            # Jika deskripsi cuaca ada dalam terjemahan_cuaca, gunakan terjemahan tersebut; jika tidak, gunakan deskripsi asli
                deskripsi_cuaca_id = translete.get(weather_description, weather_description)

                forecast.append({
                    'no':num,
                    'date': date,
                    'temperature': temperature,
                    'weather_description': deskripsi_cuaca_id
                })

            
            return render_template("Ramalan-Cuaca.html.jinja", forecast=forecast, user=current_user, current_page=current_page, city=city, time=time)
        except:
            message = 'kota tidak ditemukan'
            return render_template("Ramalan-Cuaca.html.jinja", user=current_user, current_page=current_page, time=time, message=message)

    
    return render_template("Ramalan-Cuaca.html.jinja", user=current_user, current_page=current_page, time=time)

@views.route('Kuis', methods=['GET','POST'])
@login_required
def kuis():
    if request.method == 'POST':
        id_question = request.form.get('idQuestion')
        answer = request.form.get('gridRadios')
        print("skor bottom answer : ", answer)


        print("id Question bottom answer : ", id_question)
        question = Question.query.filter_by(id = id_question).first()

        if question and question.answer == answer:
            print("jawaban benar")
            skor = SkorUser.query.filter_by(idUser = current_user.id).first()
            skor.skor += 10
            db.session.commit()
        else:
            print("jawaban salah")



    current_page = request.path

    all_id = [record.id for record in Question.query.with_entities(Question.id).all()]
    rand_id = random.choice(all_id)
    question = Question.query.filter_by(id = rand_id).first()

    get_rank = User.query.join(SkorUser).add_columns(User.id,
                    User.nickname, SkorUser.skor).order_by(
                        SkorUser.skor.desc()
                    ).all()

    time = datetime.now().strftime('%A ,%d %B %Y')
    return render_template("Kuis.html.jinja", user=current_user, current_page=current_page, 
                           question=question,get_rank=get_rank, time=time)