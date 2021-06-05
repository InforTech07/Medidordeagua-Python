from flask import Flask, render_template, request,redirect, url_for, flash
import RPi.GPIO as GPIO
import time

#initializations
app = Flask(__name__)

TRIG = 23
ECHO = 24
GPIO.setmode(GPIO.BCM)

# Establecer que TRIG es un canal de salida.
GPIO.setup(TRIG, GPIO.OUT)

# Establecer que ECHO es un canal de entrada.
GPIO.setup(ECHO, GPIO.IN)





#variables globales
Tancho= 0
Tlargo = 0
Taltura = 0
Tprogreso = 0
Tminimo = 0
Tmaximo = 0
Testado = None
Tvolume = 0
Tradio = 0


#settings
app.secret_key = "mysecretkey"


def Sensor():
    global Tancho
    global Tlargo
    global Taltura
    global Tprogreso
    global Tminimo
    global Tmaximo
    global Testado
    global Tvolume
    global Tradio
    GPIO.setup(22,GPIO.OUT)

    try:
    # Ciclo infinito.
    # Para terminar el programa se debe presionar Ctrl-C.
        while True:
        # Apagar el pin activador y permitir un par de
        # segundos para que se estabilice.
            GPIO.output(TRIG, GPIO.LOW)
            print "Esperando a que el sensor se estabilice"
            time.sleep(2)
            # Prender el pin activador por 10 microsegundos
            GPIO.output(TRIG, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(TRIG, GPIO.LOW)
            # en HIGH. Se debe detectar este evento e iniciar
            print "Iniciando eco"
            while True:
                pulso_inicio = time.time()
                if GPIO.input(ECHO) == GPIO.HIGH:
                    break

            while True:
                pulso_fin = time.time()
                if GPIO.input(ECHO) == GPIO.LOW:
                    break
            duracion = pulso_fin - pulso_inicio
            distancia = (34300 * duracion) / 2
            print "Distancia: %.2f cm" % distancia
            result = int(Taltura) - int(distancia)
            Tprogreso = ((int(result) * 100)/int(Taltura))
            if int(Tradio) != 0:
                Tvolume = ((3.1416 * int(Tradio)**2)* int(result))
            else:
                Tvolume = ((int(Tancho) * int(Tlargo))* int(result))
            
            if int(Tprogreso) <= int(Tminimo):
                GPIO.output(22,GPIO.HIGH)
                Testado = "bajo"
            elif int(Tprogreso) >= int(Tmaximo):
                Testado = "lleno"
            else:
                GPIO.output(22,GPIO.LOW)
                Testado = "estable"
            print "Altura: %.2f cm " %  distancia                
            time.sleep(2)
    finally:
        GPIO.cleanup()

@app.route('/getvolumen')
def getvolumen():
    global Tprogreso
    global Testado
    global Tvolume
    data = {
            "porcentaje": Tprogreso,
            "estado": Testado,
            "volume": Tvolume
            }
    return data

@app.route('/')
def Index():
    global Testado
    print(type(Tancho))
    print(type(Tlargo))
    print(type(Taltura))
    return render_template('index.html')



@app.route('/add_settings', methods=['POST'])
def add_settings():
    if request.method == 'POST':
        global Tancho
        global Tlargo
        global Taltura
        global Tminimo
        global Tmaximo
        global Tradio
        Tancho  = request.form['ancho']
        Tlargo = request.form['largo']
        Taltura = request.form['alto']
        Tminimo = request.form['minimo']
        Tmaximo = request.form['maximo']
        Tradio = request.form['radio']
        flash('Configuracion establecida')
        flash('Inciando sensor');
        time.sleep(2)
        Sensor()
        return redirect(url_for('Index'))





if __name__ == '__main__':
    app.run(port = 3000, debug = True)
