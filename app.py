from flask import Flask, render_template

app = Flask(__name__)
# from forms import Origin_Destination


@app.route('/')
def hello_world():
    # form = Origin_Destination
    return render_template('home.html')

if __name__ == '__main__':
    app.run()
