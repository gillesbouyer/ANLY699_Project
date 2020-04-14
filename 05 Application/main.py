from flask import Flask, request, render_template
from py_complete import collaborative_recommender,content_tag_recommender


# create a flask object
app = Flask(__name__)

# creates an association between the / page and the entry_page function (defaults to GET)
@app.route('/')
def entry_page():
    return render_template('index.html')

# creates an association between the /complete_slogan page and the render_message function
# (includes POST requests which allow users to enter in data via form)
@app.route('/recommend_movie/', methods=['GET', 'POST'])

def render_message():

    # user-entered ingredients
    ingredients = ['movie']

    # error messages to ensure correct slogan
    messages = ["Invalid movie"]



    lesdonnees = []
    render_template('index.html', message=" ",old_input=" ")
    # code from the other app did not change
    for i, ing in enumerate(ingredients):
        user_input = request.form[ing]
        try:
            data_entered = str(user_input)
        except:
            return render_template('index.html', message=messages[i])
        lesdonnees.append(data_entered)
    content_tag_recommender(lesdonnees)
    final_message = collaborative_recommender(100,lesdonnees)
    return render_template('index.html', message=final_message.values,data=True, old_input=user_input)

if __name__ == '__main__':
    app.run(debug=True)
